from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Sum

from apps.fintech.models import Credit, Transaction

class Command(BaseCommand):
    help = 'Recalcula abonos, pendientes y morosidad para todos los créditos'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        credits = Credit.objects.filter(state='pending')
        total_updated = 0

        for credit in credits:
            # 1. Sumar abonos a través de AccountMethodAmount
            total_abonos = Transaction.objects.filter(
                account_method_amounts__credit=credit,
                transaction_type='income',
                status='confirmed'
            ).aggregate(total=Sum('account_method_amounts__amount_paid'))['total'] or 0

            # 2. Calcular monto pendiente
            pending = credit.price - total_abonos

            # 3. Último pago
            last_payment = Transaction.objects.filter(
                account_method_amounts__credit=credit,
                transaction_type='income',
                status='confirmed'
            ).order_by('-date').first()

            if last_payment:
                last_payment_date = last_payment.date.date()
            else:
                last_payment_date = credit.first_date_payment

            # 4. Calcular morosidad
            days_since_last_payment = (today - last_payment_date).days
            period_days = credit.periodicity.days if credit.periodicity else 30
            delay_ratio = days_since_last_payment / period_days

            if delay_ratio < 1:
                morosidad = 'on_time'
            elif delay_ratio < 2:
                morosidad = 'mild_default'
            elif delay_ratio < 3:
                morosidad = 'moderate_default'
            elif delay_ratio < 4:
                morosidad = 'severe_default'
            elif delay_ratio < 5:
                morosidad = 'recurrent_default'
            else:
                morosidad = 'critical_default'

            # 5. Verificar si algo cambió
            updated = False
            if credit.total_abonos != total_abonos:
                credit.total_abonos = total_abonos
                updated = True
            if credit.pending_amount != pending:
                credit.pending_amount = pending
                updated = True
            if credit.morosidad_level != morosidad:
                credit.morosidad_level = morosidad
                credit.is_in_default = morosidad != 'on_time'
                updated = True

            if updated:
                credit.save()
                total_updated += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Actualizado crédito {credit.uid} → Abonos: {total_abonos}, Pendiente: {pending}, Morosidad: {morosidad}'
                ))

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Créditos actualizados: {total_updated} / {credits.count()}'
        ))
