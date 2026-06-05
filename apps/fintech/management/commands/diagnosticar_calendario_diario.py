from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Count, Q, Sum
from django.utils import timezone

from apps.fintech.models import Credit, Installment, Seller


ELIGIBLE_STATUSES = ['pending', 'partial', 'overdue']


class Command(BaseCommand):
    help = 'Diagnostica creditos diarios y cuotas que deberian aparecer en el calendario de cobranza'

    def add_arguments(self, parser):
        parser.add_argument(
            '--seller-id',
            type=int,
            help='Filtra el diagnostico por Seller.id',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Horizonte futuro del calendario en dias. Default: 30',
        )
        parser.add_argument(
            '--sample',
            type=int,
            default=20,
            help='Cantidad maxima de ejemplos a mostrar. Default: 20',
        )

    def handle(self, *args, **options):
        seller_id = options.get('seller_id')
        days = options['days']
        sample = options['sample']

        today = timezone.now().date()
        horizon = today + timedelta(days=days)

        self.stdout.write('DIAGNOSTICO CALENDARIO - CREDITOS DIARIOS')
        self.stdout.write('=' * 70)
        self.stdout.write(f'Fecha actual: {today}')
        self.stdout.write(f'Horizonte calendario: {horizon} ({days} dias)')
        self.stdout.write(f'Status elegibles: {", ".join(ELIGIBLE_STATUSES)}')
        self.stdout.write('')

        seller = None
        if seller_id:
            try:
                seller = Seller.objects.select_related('user').get(id=seller_id)
                seller_name = f'{seller.user.first_name} {seller.user.last_name}'.strip() or seller.user.username
                self.stdout.write(f'Filtro seller: {seller.id} - {seller_name}')
                self.stdout.write('')
            except Seller.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'No existe Seller.id={seller_id}'))
                return

        credit_filter = Q(periodicity__days=1)
        installment_filter = Q(credit__periodicity__days=1)

        if seller:
            credit_filter &= Q(seller=seller)
            installment_filter &= Q(credit__seller=seller)

        self._print_periodicity_overview(seller)
        self._print_daily_credit_overview(credit_filter)
        self._print_installment_overview(installment_filter, today, horizon)
        self._print_sunday_overview(installment_filter, horizon)
        self._print_calendar_equivalent_query(installment_filter, horizon)
        self._print_by_seller(installment_filter, horizon)
        self._print_sample(installment_filter, horizon, sample)

        self.stdout.write('')
        self.stdout.write('COMO INTERPRETAR')
        self.stdout.write('-' * 70)
        self.stdout.write(
            'Si "Cuotas diarias elegibles para calendario" es mayor a 0, '
            'backend deberia entregarlas en /fintech/collector/my-portfolio/.'
        )
        self.stdout.write(
            'Si summary.installments_by_periodicity trae periodicity_days=1, '
            'frontend esta recibiendo cuotas diarias.'
        )
        self.stdout.write(
            'Si hay creditos diarios pero 0 cuotas elegibles, revisar si no tienen cuotas, '
            'si todas estan paid/cancelled, si no tienen seller o si las fechas estan fuera del horizonte.'
        )

    def _print_periodicity_overview(self, seller):
        self.stdout.write('PERIODICIDADES EN CREDITOS')
        self.stdout.write('-' * 70)

        qs = Credit.objects.all()
        if seller:
            qs = qs.filter(seller=seller)

        rows = list(
            qs.values('periodicity__id', 'periodicity__name', 'periodicity__days')
            .annotate(credits=Count('id'))
            .order_by('periodicity__days', 'periodicity__name')
        )

        if not rows:
            self.stdout.write('No hay creditos para este filtro.')
        for row in rows:
            self.stdout.write(
                f"days={row['periodicity__days']} "
                f"name={row['periodicity__name']} "
                f"credits={row['credits']}"
            )
        self.stdout.write('')

    def _print_daily_credit_overview(self, credit_filter):
        self.stdout.write('CREDITOS DIARIOS')
        self.stdout.write('-' * 70)

        daily_credits = Credit.objects.filter(credit_filter)
        total = daily_credits.count()
        with_seller = daily_credits.filter(seller__isnull=False).count()
        without_seller = daily_credits.filter(seller__isnull=True).count()
        with_installments = daily_credits.filter(installments__isnull=False).distinct().count()
        without_installments = daily_credits.filter(installments__isnull=True).count()

        self.stdout.write(f'Total creditos periodicity.days=1: {total}')
        self.stdout.write(f'Con seller: {with_seller}')
        self.stdout.write(f'Sin seller: {without_seller}')
        self.stdout.write(f'Con cuotas: {with_installments}')
        self.stdout.write(f'Sin cuotas: {without_installments}')
        self.stdout.write('')

    def _print_installment_overview(self, installment_filter, today, horizon):
        self.stdout.write('CUOTAS DE CREDITOS DIARIOS')
        self.stdout.write('-' * 70)

        qs = Installment.objects.filter(installment_filter)
        total = qs.count()
        eligible = qs.filter(status__in=ELIGIBLE_STATUSES, due_date__lte=horizon).count()
        overdue_or_today = qs.filter(status__in=ELIGIBLE_STATUSES, due_date__lte=today).count()
        next_window = qs.filter(status__in=ELIGIBLE_STATUSES, due_date__gt=today, due_date__lte=horizon).count()
        no_due_date = qs.filter(due_date__isnull=True).count()

        self.stdout.write(f'Total cuotas de creditos diarios: {total}')
        self.stdout.write(f'Cuotas diarias elegibles para calendario: {eligible}')
        self.stdout.write(f'Vencidas o de hoy: {overdue_or_today}')
        self.stdout.write(f'Futuras hasta horizonte: {next_window}')
        self.stdout.write(f'Sin due_date: {no_due_date}')
        self.stdout.write('')

        by_status = list(qs.values('status').annotate(count=Count('id')).order_by('status'))
        self.stdout.write('Por status:')
        for row in by_status:
            self.stdout.write(f"  {row['status']}: {row['count']}")
        self.stdout.write('')

    def _print_sunday_overview(self, installment_filter, horizon):
        self.stdout.write('CUOTAS DIARIAS EN DOMINGO')
        self.stdout.write('-' * 70)

        qs = Installment.objects.filter(installment_filter, due_date__week_day=1)
        total_sunday = qs.count()
        eligible_sunday = qs.filter(
            credit__seller__isnull=False,
            status__in=ELIGIBLE_STATUSES,
            due_date__lte=horizon,
        ).exclude(status='cancelled').count()

        self.stdout.write(f'Total cuotas daily con due_date domingo: {total_sunday}')
        self.stdout.write(f'Cuotas daily domingo elegibles para calendario: {eligible_sunday}')

        sample = list(
            qs.filter(
                credit__seller__isnull=False,
                status__in=ELIGIBLE_STATUSES,
                due_date__lte=horizon,
            )
            .select_related('credit', 'credit__seller__user')
            .order_by('due_date', 'id')[:10]
        )

        if sample:
            self.stdout.write('Muestra domingos:')
            for inst in sample:
                seller_username = inst.credit.seller.user.username if inst.credit.seller else None
                self.stdout.write(
                    f"  installment_id={inst.id} due_date={inst.due_date} "
                    f"status={inst.status} credit_uid={inst.credit.uid} "
                    f"seller_id={inst.credit.seller_id} seller={seller_username} "
                    f"remaining={inst.remaining_amount}"
                )
        self.stdout.write('')

    def _print_calendar_equivalent_query(self, installment_filter, horizon):
        self.stdout.write('QUERY EQUIVALENTE AL CALENDARIO')
        self.stdout.write('-' * 70)

        qs = (
            Installment.objects
            .filter(installment_filter)
            .filter(
                credit__seller__isnull=False,
                status__in=ELIGIBLE_STATUSES,
                due_date__lte=horizon,
            )
            .exclude(status='cancelled')
        )

        aggregate = qs.aggregate(
            count=Count('id'),
            total_remaining=Sum('remaining_amount'),
            total_amount=Sum('amount'),
        )

        self.stdout.write(f"Cuotas que cumplen el query del calendario: {aggregate['count'] or 0}")
        self.stdout.write(f"Total remaining_amount: {aggregate['total_remaining'] or 0}")
        self.stdout.write(f"Total amount: {aggregate['total_amount'] or 0}")
        self.stdout.write('')

    def _print_by_seller(self, installment_filter, horizon):
        self.stdout.write('CUOTAS DIARIAS ELEGIBLES POR SELLER')
        self.stdout.write('-' * 70)

        rows = list(
            Installment.objects
            .filter(installment_filter)
            .filter(
                credit__seller__isnull=False,
                status__in=ELIGIBLE_STATUSES,
                due_date__lte=horizon,
            )
            .values('credit__seller_id', 'credit__seller__user__username')
            .annotate(
                installments=Count('id'),
                credits=Count('credit_id', distinct=True),
                total_remaining=Sum('remaining_amount'),
            )
            .order_by('-installments')[:30]
        )

        if not rows:
            self.stdout.write('No hay cuotas diarias elegibles por seller.')
        for row in rows:
            self.stdout.write(
                f"seller_id={row['credit__seller_id']} "
                f"username={row['credit__seller__user__username']} "
                f"credits={row['credits']} "
                f"installments={row['installments']} "
                f"remaining={row['total_remaining'] or 0}"
            )
        self.stdout.write('')

    def _print_sample(self, installment_filter, horizon, sample):
        self.stdout.write('MUESTRA DE CUOTAS DIARIAS ELEGIBLES')
        self.stdout.write('-' * 70)

        rows = list(
            Installment.objects
            .filter(installment_filter)
            .filter(
                credit__seller__isnull=False,
                status__in=ELIGIBLE_STATUSES,
                due_date__lte=horizon,
            )
            .select_related('credit', 'credit__seller__user', 'credit__user', 'credit__periodicity')
            .order_by('due_date', 'id')[:sample]
        )

        if not rows:
            self.stdout.write('No hay muestra para este filtro.')
        for inst in rows:
            client_name = f'{inst.credit.user.first_name} {inst.credit.user.last_name}'.strip() or inst.credit.user.username
            seller_username = inst.credit.seller.user.username if inst.credit.seller else None
            self.stdout.write(
                f"installment_id={inst.id} "
                f"due_date={inst.due_date} "
                f"status={inst.status} "
                f"credit_uid={inst.credit.uid} "
                f"seller_id={inst.credit.seller_id} "
                f"seller={seller_username} "
                f"client={client_name} "
                f"amount={inst.amount} "
                f"remaining={inst.remaining_amount}"
            )
