from django.utils import timezone
from apps.fintech.models import Credit
from apps.fintech.utils import calculate_credit_morosity

def run_daily_morosity_check():
    today = timezone.now().date()
    credits = Credit.objects.filter(state="pending")

    for credit in credits:
        calculate_credit_morosity(credit)
