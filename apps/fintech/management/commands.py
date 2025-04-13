from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.fintech.models import Credit
from apps.fintech.utils import calculate_credit_morosity

class Command(BaseCommand):
    help = "Actualiza la morosidad de todos los créditos pendientes."

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        self.stdout.write(f"Iniciando actualización de morosidad - {today}")

        credits = Credit.objects.filter(state="pending")

        count = 0
        for credit in credits:
            calculate_credit_morosity(credit)
            count += 1

        self.stdout.write(self.style.SUCCESS(f"{count} créditos actualizados correctamente."))
