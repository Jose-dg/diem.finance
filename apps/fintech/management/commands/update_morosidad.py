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