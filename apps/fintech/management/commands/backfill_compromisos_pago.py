from datetime import timedelta
from decimal import Decimal
from math import ceil

from django.core.management.base import CommandError
from django.utils import timezone
from django.utils.dateparse import parse_date

from apps.fintech.management.commands.backfill_cuotas_diarias import (
    Command as DailyBackfillCommand,
    SUNDAY,
)
from apps.fintech.models import Credit


class Command(DailyBackfillCommand):
    help = (
        'Crea cuotas/compromisos faltantes para creditos recientes de cualquier '
        'periodicidad y repara estados/saldos de cuotas existentes'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--from-date',
            type=str,
            help='Procesa creditos creados desde esta fecha, formato YYYY-MM-DD.',
        )
        parser.add_argument(
            '--seller-id',
            type=int,
            help='Procesa solo creditos de un Seller.id.',
        )
        parser.add_argument(
            '--credit-uid',
            type=str,
            help='Procesa solo un credito por UID.',
        )
        parser.add_argument(
            '--apply',
            action='store_true',
            help='Aplica cambios. Sin este flag solo muestra diagnostico.',
        )
        parser.add_argument(
            '--create-missing',
            action='store_true',
            help='Crea cuotas para creditos que no tienen ninguna cuota.',
        )
        parser.add_argument(
            '--repair-existing',
            action='store_true',
            help='Recalcula amount_paid, remaining_amount, paid/status de cuotas existentes segun pagos confirmados.',
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Limita la cantidad de creditos procesados.',
        )
        parser.add_argument(
            '--show-dates',
            action='store_true',
            help='Muestra primeras y ultimas fechas generadas para creditos sin cuotas.',
        )

    def handle(self, *args, **options):
        today = timezone.now().date()
        from_date = self._parse_from_date(options.get('from_date'), today)
        apply_changes = options['apply']
        create_missing = options['create_missing']
        repair_existing = options['repair_existing']

        if not create_missing and not repair_existing:
            self.stdout.write(self.style.WARNING(
                'No se indico accion. Usa --create-missing y/o --repair-existing. '
                'Sin --apply se ejecuta en modo diagnostico.'
            ))

        qs = (
            Credit.objects
            .filter(created_at__date__gte=from_date)
            .select_related('user', 'seller__user', 'periodicity')
            .order_by('id')
        )

        if options.get('seller_id'):
            qs = qs.filter(seller_id=options['seller_id'])
        if options.get('credit_uid'):
            qs = qs.filter(uid=options['credit_uid'])
        if options.get('limit'):
            qs = qs[:options['limit']]

        mode = 'APPLY' if apply_changes else 'DRY-RUN'

        self.stdout.write('BACKFILL COMPROMISOS DE PAGO')
        self.stdout.write('=' * 70)
        self.stdout.write(f'Modo: {mode}')
        self.stdout.write(f'Fecha actual: {today}')
        self.stdout.write(f'Creditos creados desde: {from_date}')
        self.stdout.write(f'Crear faltantes: {create_missing}')
        self.stdout.write(f'Reparar existentes: {repair_existing}')
        self.stdout.write('')

        stats = {
            'credits_seen': 0,
            'credits_without_installments': 0,
            'credits_with_installments': 0,
            'credits_skipped': 0,
            'installments_to_create': 0,
            'installments_created': 0,
            'installments_to_repair': 0,
            'installments_repaired': 0,
        }

        for credit in qs:
            stats['credits_seen'] += 1
            installment_count = credit.installments.count()

            if installment_count == 0:
                stats['credits_without_installments'] += 1
                if create_missing:
                    created = self._handle_missing_installments(
                        credit,
                        apply_changes,
                        options['show_dates'],
                    )
                    stats['installments_to_create'] += created['to_create']
                    stats['installments_created'] += created['created']
                else:
                    stats['credits_skipped'] += 1
            else:
                stats['credits_with_installments'] += 1
                if repair_existing:
                    repaired = self._handle_existing_installments(credit, apply_changes)
                    stats['installments_to_repair'] += repaired['to_repair']
                    stats['installments_repaired'] += repaired['repaired']

        self.stdout.write('')
        self.stdout.write('RESUMEN')
        self.stdout.write('-' * 70)
        for key, value in stats.items():
            self.stdout.write(f'{key}: {value}')

        if not apply_changes:
            self.stdout.write('')
            self.stdout.write(self.style.WARNING(
                'No se aplicaron cambios. Repite con --apply para escribir en BD.'
            ))

    def _parse_from_date(self, value, today):
        if not value:
            return today.replace(month=5, day=1)

        parsed = parse_date(value)
        if not parsed:
            raise CommandError('--from-date debe tener formato YYYY-MM-DD.')

        return parsed

    def _expected_dates(self, credit):
        start = credit.first_date_payment
        if not start:
            return []

        installment_count = int(credit.installment_number or 0)
        if installment_count <= 0:
            installment_count = self._effective_installment_count(credit)

        if installment_count <= 0:
            return []

        dates = []
        current = start
        periodicity_days = self._periodicity_days(credit)

        while len(dates) < installment_count:
            if self._is_valid_due_date_for_credit(credit, current):
                dates.append(current)
            current += timedelta(days=periodicity_days)

        return dates

    def _effective_installment_count(self, credit):
        days = int(credit.credit_days or 0)
        periodicity_days = self._periodicity_days(credit)

        if days > 0:
            if self._should_exclude_sundays_for_credit(credit):
                return days
            return max(1, ceil(days / periodicity_days))

        if credit.first_date_payment and credit.second_date_payment:
            count = 0
            current = credit.first_date_payment
            while current <= credit.second_date_payment:
                if self._is_valid_due_date_for_credit(credit, current):
                    count += 1
                current += timedelta(days=periodicity_days)
            return count

        return 0

    def _periodicity_days(self, credit):
        days = credit.periodicity.days if credit.periodicity else 1
        return max(1, int(days or 1))

    def _should_exclude_sundays_for_credit(self, credit):
        return self._periodicity_days(credit) == 1

    def _is_valid_due_date_for_credit(self, credit, due_date):
        if not due_date:
            return False
        if self._should_exclude_sundays_for_credit(credit) and due_date.weekday() == SUNDAY:
            return False
        return True
