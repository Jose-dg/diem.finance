from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from apps.fintech.models import AccountMethodAmount, Credit, Installment


CENT = Decimal('0.01')
SUNDAY = 6


class Command(BaseCommand):
    help = 'Crea cuotas faltantes para creditos diarios y repara estados/saldos de cuotas existentes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--seller-id',
            type=int,
            help='Procesa solo creditos de un Seller.id',
        )
        parser.add_argument(
            '--credit-uid',
            type=str,
            help='Procesa solo un credito por UID',
        )
        parser.add_argument(
            '--apply',
            action='store_true',
            help='Aplica cambios. Sin este flag solo muestra diagnostico.',
        )
        parser.add_argument(
            '--create-missing',
            action='store_true',
            help='Crea cuotas para creditos diarios que no tienen ninguna cuota.',
        )
        parser.add_argument(
            '--repair-existing',
            action='store_true',
            help='Recalcula amount_paid, remaining_amount, paid/status de cuotas existentes segun pagos confirmados.',
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Limita la cantidad de creditos diarios procesados.',
        )
        parser.add_argument(
            '--show-dates',
            action='store_true',
            help='Muestra primeras y ultimas fechas generadas para creditos sin cuotas.',
        )

    def handle(self, *args, **options):
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
            .filter(periodicity__days=1)
            .select_related('user', 'seller__user', 'periodicity')
            .order_by('id')
        )

        if options.get('seller_id'):
            qs = qs.filter(seller_id=options['seller_id'])
        if options.get('credit_uid'):
            qs = qs.filter(uid=options['credit_uid'])
        if options.get('limit'):
            qs = qs[:options['limit']]

        today = timezone.now().date()
        mode = 'APPLY' if apply_changes else 'DRY-RUN'

        self.stdout.write('BACKFILL CUOTAS DIARIAS')
        self.stdout.write('=' * 70)
        self.stdout.write(f'Modo: {mode}')
        self.stdout.write(f'Fecha actual: {today}')
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
                    created = self._handle_missing_installments(credit, apply_changes, options['show_dates'])
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

    def _handle_missing_installments(self, credit, apply_changes, show_dates=False):
        dates = self._expected_dates(credit)
        if not dates:
            self.stdout.write(self.style.WARNING(
                f'SKIP credit={credit.uid}: no se pudieron calcular fechas esperadas.'
            ))
            return {'to_create': 0, 'created': 0}

        amounts = self._installment_amounts(credit.price, len(dates))
        payments = self._confirmed_payments(credit)
        installments = self._build_installments(credit, dates, amounts)
        self._apply_payments_to_installments(installments, payments)

        seller_id = credit.seller_id
        client = credit.user.username if credit.user else None
        sunday_count = sum(1 for due_date in dates if due_date.weekday() == SUNDAY)
        self.stdout.write(
            f"MISSING credit={credit.uid} seller_id={seller_id} client={client} "
            f"dates={len(dates)} sundays={sunday_count} price={credit.price} "
            f"paid={sum(p['amount'] for p in payments)} "
            f"credit_days={credit.credit_days} installment_number={credit.installment_number}"
        )
        if show_dates:
            self.stdout.write(f"  first_dates={dates[:10]}")
            self.stdout.write(f"  last_dates={dates[-10:]}")

        if not apply_changes:
            return {'to_create': len(installments), 'created': 0}

        with transaction.atomic():
            Installment.objects.bulk_create(installments)
            self._sync_credit_installment_fields(credit)

        return {'to_create': len(installments), 'created': len(installments)}

    def _handle_existing_installments(self, credit, apply_changes):
        payments = self._confirmed_payments(credit)
        installments = list(credit.installments.all().order_by('due_date', 'number', 'id'))

        snapshot = {
            inst.id: (
                inst.amount_paid,
                inst.remaining_amount,
                inst.status,
                inst.paid,
                inst.paid_on,
                inst.days_overdue,
            )
            for inst in installments
        }

        self._reset_installments_for_distribution(installments)
        self._apply_payments_to_installments(installments, payments)
        self._refresh_overdue_fields(installments)

        changed = [
            inst for inst in installments
            if snapshot[inst.id] != (
                inst.amount_paid,
                inst.remaining_amount,
                inst.status,
                inst.paid,
                inst.paid_on,
                inst.days_overdue,
            )
        ]

        if changed:
            self.stdout.write(
                f"REPAIR credit={credit.uid} installments_changed={len(changed)} "
                f"total_installments={len(installments)}"
            )

        if not apply_changes or not changed:
            return {'to_repair': len(changed), 'repaired': 0}

        with transaction.atomic():
            Installment.objects.bulk_update(
                changed,
                ['amount_paid', 'remaining_amount', 'status', 'paid', 'paid_on', 'days_overdue'],
            )
            self._sync_credit_installment_fields(credit)

        return {'to_repair': len(changed), 'repaired': len(changed)}

    def _expected_dates(self, credit):
        start = credit.first_date_payment
        if not start:
            return []

        installment_count = credit.installment_number or 0
        if installment_count <= 0:
            installment_count = self._effective_installment_count(credit)

        if installment_count <= 0:
            return []

        dates = []
        current = start
        while len(dates) < installment_count:
            if self._is_valid_due_date_for_credit(credit, current):
                dates.append(current)
            current += timedelta(days=credit.periodicity.days or 1)

        return dates

    def _effective_installment_count(self, credit):
        if self._should_exclude_sundays_for_credit(credit):
            return self._count_effective_daily_dates_from_credit_days(credit)

        if credit.second_date_payment and credit.first_date_payment:
            current = credit.first_date_payment
            count = 0
            while current <= credit.second_date_payment:
                if self._is_valid_due_date_for_credit(credit, current):
                    count += 1
                current += timedelta(days=1)
            if count > 0:
                return count

        days = int(credit.credit_days or 0)
        if days <= 0:
            return 0

        current = credit.first_date_payment
        count = 0
        for _ in range(days):
            if self._is_valid_due_date_for_credit(credit, current):
                count += 1
            current += timedelta(days=1)
        return count

    def _count_effective_daily_dates_from_credit_days(self, credit):
        """
        Para creditos diarios, credit_days representa dias cobrables/cuotas,
        no dias calendario. Si credit_days=24, deben generarse 24 cuotas
        saltando domingos hasta completar esa cantidad.
        """
        days = int(credit.credit_days or 0)
        if days <= 0 or not credit.first_date_payment:
            return 0
        return days

    def _is_valid_due_date_for_credit(self, credit, due_date):
        if not due_date:
            return False
        if self._should_exclude_sundays_for_credit(credit) and due_date.weekday() == SUNDAY:
            return False
        return True

    def _should_exclude_sundays_for_credit(self, credit):
        """
        Regla explicita del backfill: solo los creditos diarios excluyen domingos.

        No usamos should_exclude_sundays() porque en el codigo historico esa funcion
        interpreta "periodicity < 30" como excluible, lo cual tambien afectaria
        semanales/quincenales. Para este backfill solo procesamos Daily.
        """
        return bool(credit.periodicity and credit.periodicity.days == 1)

    def _installment_amounts(self, price, count):
        if count <= 0:
            return []

        price = Decimal(str(price or 0)).quantize(CENT)
        base = (price / Decimal(count)).quantize(CENT, rounding=ROUND_HALF_UP)
        amounts = [base for _ in range(count)]
        difference = price - sum(amounts)
        amounts[-1] = (amounts[-1] + difference).quantize(CENT)
        return amounts

    def _confirmed_payments(self, credit):
        qs = (
            AccountMethodAmount.objects
            .filter(
                credit=credit,
                transaction__transaction_type='income',
                transaction__status='confirmed',
            )
            .select_related('transaction')
            .order_by('transaction__date', 'id')
        )

        return [
            {
                'amount': ama.amount_paid or Decimal('0'),
                'date': ama.transaction.date.date() if ama.transaction and ama.transaction.date else None,
            }
            for ama in qs
            if (ama.amount_paid or Decimal('0')) > 0
        ]

    def _build_installments(self, credit, dates, amounts):
        installments = []
        for index, (due_date, amount) in enumerate(zip(dates, amounts), start=1):
            installments.append(Installment(
                credit=credit,
                number=index,
                due_date=due_date,
                amount=amount,
                amount_paid=Decimal('0.00'),
                remaining_amount=amount,
                principal_amount=amount,
                interest_amount=Decimal('0.00'),
                status='pending',
                paid=False,
                days_overdue=0,
            ))
        return installments

    def _reset_installments_for_distribution(self, installments):
        for inst in installments:
            amount = (inst.amount or Decimal('0')).quantize(CENT)
            inst.amount_paid = Decimal('0.00')
            inst.remaining_amount = amount
            inst.status = 'pending'
            inst.paid = False
            inst.paid_on = None
            inst.days_overdue = 0

    def _apply_payments_to_installments(self, installments, payments):
        for payment in payments:
            remaining_payment = payment['amount']
            payment_date = payment['date']

            for inst in installments:
                if remaining_payment <= Decimal('0'):
                    break

                inst_remaining = inst.remaining_amount or Decimal('0')
                if inst_remaining <= Decimal('0'):
                    continue

                applied = min(remaining_payment, inst_remaining)
                inst.amount_paid = (inst.amount_paid or Decimal('0')) + applied
                inst.remaining_amount = (inst.amount or Decimal('0')) - inst.amount_paid

                if inst.remaining_amount <= Decimal('0.00'):
                    inst.remaining_amount = Decimal('0.00')
                    inst.status = 'paid'
                    inst.paid = True
                    inst.paid_on = payment_date
                else:
                    inst.status = 'partial'
                    inst.paid = False

                remaining_payment -= applied

        self._refresh_overdue_fields(installments)

    def _refresh_overdue_fields(self, installments):
        today = timezone.now().date()
        for inst in installments:
            if inst.status == 'paid':
                inst.days_overdue = 0
                continue

            inst.days_overdue = (
                (today - inst.due_date).days
                if inst.due_date and inst.due_date < today
                else 0
            )

            if inst.amount_paid and inst.amount_paid > Decimal('0'):
                inst.status = 'partial'
            elif inst.days_overdue > 3:
                inst.status = 'overdue'
            else:
                inst.status = 'pending'

    def _sync_credit_installment_fields(self, credit):
        installments = credit.installments.all()
        count = installments.count()
        average = (
            installments.aggregate(total=Sum('amount'))['total'] / Decimal(count)
            if count
            else Decimal('0.00')
        )
        credit.installment_number = count
        credit.installment_value = average.quantize(CENT) if count else Decimal('0.00')
        credit.save(update_fields=['installment_number', 'installment_value'])
