from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Count, Q, Sum
from django.utils import timezone

from apps.fintech.models import AccountMethodAmount, Credit, User


ELIGIBLE_STATUSES = ['pending', 'partial', 'overdue']


class Command(BaseCommand):
    help = 'Diagnostica creditos y cuotas de un cliente para el calendario de cobranza'

    def add_arguments(self, parser):
        parser.add_argument('query', type=str, help='Username, parte del username o nombre del cliente')
        parser.add_argument('--days', type=int, default=30, help='Horizonte futuro del calendario. Default: 30')
        parser.add_argument('--sample', type=int, default=30, help='Cantidad de cuotas a mostrar por credito. Default: 30')

    def handle(self, *args, **options):
        query = options['query']
        days = options['days']
        sample = options['sample']

        today = timezone.now().date()
        horizon = today + timedelta(days=days)

        users = (
            User.objects
            .filter(
                Q(username__iexact=query) |
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
            .distinct()
            .order_by('id')
        )

        self.stdout.write('DIAGNOSTICO CLIENTE - CALENDARIO')
        self.stdout.write('=' * 70)
        self.stdout.write(f'Busqueda: {query}')
        self.stdout.write(f'Fecha actual: {today}')
        self.stdout.write(f'Horizonte calendario: {horizon} ({days} dias)')
        self.stdout.write('')

        if not users.exists():
            self.stdout.write(self.style.WARNING('No se encontraron clientes.'))
            return

        self.stdout.write('CLIENTES ENCONTRADOS')
        self.stdout.write('-' * 70)
        for user in users:
            self.stdout.write(
                f'id={user.id} username={user.username} '
                f'name={user.first_name} {user.last_name}'.strip()
            )
        self.stdout.write('')

        for user in users:
            self._print_user_detail(user, horizon, sample)

    def _print_user_detail(self, user, horizon, sample):
        self.stdout.write(f'CLIENTE {user.id} - {user.username}')
        self.stdout.write('-' * 70)

        credits = (
            Credit.objects
            .filter(user=user)
            .select_related('periodicity', 'seller__user')
            .order_by('-created_at')
        )

        self.stdout.write(f'Creditos: {credits.count()}')
        if not credits.exists():
            self.stdout.write('')
            return

        for credit in credits:
            self._print_credit_detail(credit, horizon, sample)

    def _print_credit_detail(self, credit, horizon, sample):
        installments = credit.installments.all().order_by('due_date', 'number', 'id')
        payments = (
            AccountMethodAmount.objects
            .filter(
                credit=credit,
                transaction__transaction_type='income',
                transaction__status='confirmed',
            )
            .select_related('transaction')
            .order_by('transaction__date', 'id')
        )

        total_payments = payments.aggregate(total=Sum('amount_paid'))['total'] or 0
        eligible = installments.filter(
            status__in=ELIGIBLE_STATUSES,
            due_date__lte=horizon,
        ).count()
        sunday_count = installments.filter(due_date__week_day=1).count()

        self.stdout.write('')
        self.stdout.write(f'CREDITO {credit.uid}')
        self.stdout.write(
            f'  state={credit.state} seller_id={credit.seller_id} '
            f'seller={credit.seller.user.username if credit.seller else None}'
        )
        self.stdout.write(
            f'  periodicity={credit.periodicity.name if credit.periodicity else None} '
            f'days={credit.periodicity.days if credit.periodicity else None}'
        )
        self.stdout.write(
            f'  price={credit.price} pending_amount={credit.pending_amount} '
            f'total_abonos={credit.total_abonos} confirmed_payments={total_payments}'
        )
        self.stdout.write(
            f'  first_date_payment={credit.first_date_payment} '
            f'second_date_payment={credit.second_date_payment} credit_days={credit.credit_days}'
        )
        self.stdout.write(
            f'  installment_number={credit.installment_number} '
            f'installment_value={credit.installment_value}'
        )
        self.stdout.write(
            f'  installments={installments.count()} eligible_calendar={eligible} '
            f'sunday_installments={sunday_count}'
        )

        status_rows = list(
            installments.values('status')
            .annotate(
                count=Count('id'),
                amount=Sum('amount'),
                paid=Sum('amount_paid'),
                remaining=Sum('remaining_amount'),
            )
            .order_by('status')
        )
        self.stdout.write(f'  status_counts={status_rows}')

        if not installments.exists():
            self.stdout.write(self.style.WARNING(
                '  SIN CUOTAS: este credito no puede aparecer en el calendario.'
            ))
            return

        zero_pending = installments.filter(status__in=ELIGIBLE_STATUSES, remaining_amount__lte=0).count()
        if zero_pending:
            self.stdout.write(self.style.WARNING(
                f'  INCONSISTENCIA: {zero_pending} cuotas elegibles tienen remaining_amount <= 0.'
            ))

        self.stdout.write(f'  primeras {sample} cuotas:')
        for inst in installments[:sample]:
            self.stdout.write(
                f'    id={inst.id} number={inst.number} due_date={inst.due_date} '
                f'status={inst.status} amount={inst.amount} amount_paid={inst.amount_paid} '
                f'remaining={inst.remaining_amount} paid={inst.paid} paid_on={inst.paid_on} '
                f'days_overdue={inst.days_overdue}'
            )
