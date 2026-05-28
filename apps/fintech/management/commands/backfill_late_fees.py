from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.fintech.models import Installment


class Command(BaseCommand):
    help = "Recalcula days_overdue y late_fee para todas las cuotas vencidas no pagadas."

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Muestra qué haría sin escribir nada en la base de datos.",
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help="Procesar solo N cuotas (útil para staging).",
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        limit = options['limit']
        today = date.today()

        if dry_run:
            self.stdout.write(self.style.WARNING("Modo --dry-run activo: no se escribirá nada."))

        qs = (
            Installment.objects
            .filter(due_date__lt=today)
            .exclude(status__in=['paid', 'cancelled'])
            .select_related('credit')
            .order_by('due_date')
        )
        if limit:
            qs = qs[:limit]

        total = 0
        with_fee = 0
        promoted = 0
        fee_total = Decimal('0.00')
        errors = 0

        to_update = []

        for installment in qs:
            try:
                new_days = (today - installment.due_date).days
                new_fee = installment.calculate_late_fee()
                new_status = installment.status

                if new_days > 3 and installment.status == 'pending':
                    new_status = 'overdue'
                    promoted += 1

                total += 1
                if new_fee > 0:
                    with_fee += 1
                fee_total += new_fee

                if not dry_run:
                    installment.days_overdue = new_days
                    installment.late_fee = new_fee
                    installment.status = new_status
                    to_update.append(installment)
                else:
                    self.stdout.write(
                        f"  Cuota #{installment.id} due={installment.due_date} "
                        f"days={new_days} fee={new_fee} status={new_status}"
                    )

            except Exception as e:
                errors += 1
                self.stderr.write(f"  Error en cuota {installment.id}: {e}")

        if not dry_run and to_update:
            Installment.objects.bulk_update(to_update, ['days_overdue', 'late_fee', 'status'])

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=== Resumen ==="))
        self.stdout.write(f"  Total procesadas       : {total}")
        self.stdout.write(f"  Con late_fee > 0       : {with_fee}")
        self.stdout.write(f"  Pending → overdue      : {promoted}")
        self.stdout.write(f"  Suma total late_fee    : {fee_total}")
        self.stdout.write(f"  Errores                : {errors}")
        if dry_run:
            self.stdout.write(self.style.WARNING("  (dry-run: ningún cambio fue escrito)"))
