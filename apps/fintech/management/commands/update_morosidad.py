from django.core.management.base import BaseCommand
from apps.fintech.models import Credit
from apps.fintech.utils import recalculate_credit 


class Command(BaseCommand):
    help = "Actualiza la morosidad de los créditos"

    def handle(self, *args, **kwargs):
        total = Credit.objects.count()
        self.stdout.write(f"Procesando {total} créditos...")

        for credit in Credit.objects.iterator(chunk_size=100):
            try:
                recalculate_credit(credit)
            except Exception as e:
                self.stderr.write(f"Error en crédito {credit.id}: {str(e)}")

        self.stdout.write(self.style.SUCCESS("Actualización finalizada con éxito."))

# class Command(BaseCommand):
#     help = 'Recalcula abonos, pendientes y morosidad para todos los créditos'

#     def handle(self, *args, **kwargs):
#         credits = Credit.objects.filter(state__in=['pending', 'completed'])
#         total_updated = 0

#         for credit in credits:
#             recalculate_credit(credit)
#             total_updated += 1

#             self.stdout.write(self.style.SUCCESS(
#                 f'✅ Crédito {credit.uid} recalculado.'
#             ))

#         self.stdout.write(self.style.SUCCESS(
#             f'\n🎯 Créditos actualizados: {total_updated} / {credits.count()}'
#         ))


# # 
# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from django.db.models import Sum

# from apps.fintech.models import Credit, Transaction


# class Command(BaseCommand):
#     help = 'Recalcula abonos, pendientes y morosidad para todos los créditos'

#     def handle(self, *args, **kwargs):
#         today = timezone.now().date()
#         credits = Credit.objects.filter(state__in=['pending', 'completed'])
#         total_updated = 0

#         for credit in credits:
#             total_abonos = Transaction.objects.filter(
#                 account_method_amounts__credit=credit,
#                 transaction_type='income',
#                 status='confirmed'
#             ).aggregate(total=Sum('account_method_amounts__amount_paid'))['total'] or 0

#             pending = credit.price - total_abonos

#             last_payment = Transaction.objects.filter(
#                 account_method_amounts__credit=credit,
#                 transaction_type='income',
#                 status='confirmed'
#             ).order_by('-date').first()

#             last_payment_date = last_payment.date.date() if last_payment else credit.first_date_payment

#             updated = False

#             # Calcular morosidad solo si hay saldo pendiente
#             if pending <= 0.01:
#                 morosidad = 'on_time'
#                 state = 'completed'
#                 is_in_default = False
#                 pending = 0  # Normalizar si hay redondeo
#             else:
#                 period_days = credit.periodicity.days if credit.periodicity and credit.periodicity.days else 30
#                 days_since_last_payment = (today - last_payment_date).days
#                 delay_ratio = days_since_last_payment / period_days

#                 if delay_ratio < 1:
#                     morosidad = 'on_time'
#                 elif delay_ratio < 2:
#                     morosidad = 'mild_default'
#                 elif delay_ratio < 3:
#                     morosidad = 'moderate_default'
#                 elif delay_ratio < 4:
#                     morosidad = 'severe_default'
#                 elif delay_ratio < 5:
#                     morosidad = 'recurrent_default'
#                 else:
#                     morosidad = 'critical_default'

#                 state = credit.state
#                 is_in_default = morosidad != 'on_time'

#             # Aplicar actualizaciones si algo cambió
#             if credit.total_abonos != total_abonos:
#                 credit.total_abonos = total_abonos
#                 updated = True

#             if credit.pending_amount != pending:
#                 credit.pending_amount = pending
#                 updated = True

#             if credit.morosidad_level != morosidad:
#                 credit.morosidad_level = morosidad
#                 updated = True

#             if credit.is_in_default != is_in_default:
#                 credit.is_in_default = is_in_default
#                 updated = True

#             if credit.state != state:
#                 credit.state = state
#                 updated = True

#             if updated:
#                 credit.save()
#                 total_updated += 1
#                 self.stdout.write(self.style.SUCCESS(
#                     f'✅ Crédito {credit.uid} actualizado → Abonos: {total_abonos}, Pendiente: {pending}, Morosidad: {morosidad}, Estado: {state}'
#                 ))

#         self.stdout.write(self.style.SUCCESS(
#             f'\n🎯 Créditos actualizados: {total_updated} / {credits.count()}'
#         ))
