# apps/fintech/management/commands/recalculate_installment_dates.py

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.fintech.models import Credit
from apps.fintech.utils import generar_cuotas

class Command(BaseCommand):
    help = "Reconstruye únicamente las fechas (Installments) de todos los créditos que ya tienen cuotas."

    def handle(self, *args, **options):
        total = Credit.objects.count()
        self.stdout.write(f"Procesando {total} créditos en total...")

        # Iteramos por todos los créditos, sin cargar demasiados en memoria.
        for credit in Credit.objects.iterator(chunk_size=100):
            # Solo actuamos si ya existe al menos 1 Installment
            if not credit.installments.exists():
                continue

            try:
                with transaction.atomic():
                    # 1) Borrar las cuotas antiguas (solo las fechas erróneas)
                    credit.installments.all().delete()

                    # 2) Reconstruirlas con las fechas correctas
                    generar_cuotas(credit)

                    # Nota: generar_cuotas ya asigna credit.first_date_payment y credit.second_date_payment
                    #       y hace el save() correspondiente.
                    #       Si quieres forzar un save explícito aquí, podrías llamar:
                    # credit.save(update_fields=['first_date_payment', 'second_date_payment'])
            except Exception as e:
                self.stderr.write(f"Error procesando crédito {credit.id}: {str(e)}")

        self.stdout.write(self.style.SUCCESS("Reconstrucción de fechas de cuotas finalizada con éxito."))
