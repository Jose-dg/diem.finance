from datetime import timedelta, date
from django.utils import timezone
from django.db.models import Sum

def calculate_credit_morosity(credit):
    """
    Calcula y actualiza el estado de morosidad de un crédito.
    Esta función puede ser llamada desde signals, vistas, o tareas en Celery.
    """

    if not credit.periodicity or not credit.periodicity.days or not credit.installment_value:
        return

    today = timezone.now().date()
    
    # Calcular la fecha esperada del próximo pago
    expected_next_payment = credit.first_date_payment + timedelta(days=(credit.periodicity.days))

    # Determinar días de atraso
    days_late = max(0, (today - expected_next_payment).days)

    # Determinar nivel de morosidad
    if credit.total_abonos >= credit.price:
        credit.morosidad_level = "on_time"
    elif days_late <= 15:
        credit.morosidad_level = "mild_default"
    elif days_late <= 30:
        credit.morosidad_level = "moderate_default"
    elif days_late <= 60:
        credit.morosidad_level = "severe_default"
    elif days_late <= 90:
        credit.morosidad_level = "recurrent_default"
    else:
        credit.morosidad_level = "critical_default"

    # Indicar si el crédito está en mora
    credit.is_in_default = days_late > 0

    # Guardar cambios en el modelo
    credit.save(update_fields=['morosidad_level', 'is_in_default'])

def recalculate_credit_pending_amount(credit):
    """
    Recalcula el total de abonos y el saldo pendiente de un crédito.
    """
    total_abonos = credit.transaction_set.aggregate(total_abonos=Sum('amount'))['total_abonos'] or 0
    pending_amount = max(credit.price - total_abonos, 0)

    credit.total_abonos = total_abonos
    credit.pending_amount = pending_amount
    credit.save(update_fields=['total_abonos', 'pending_amount'])

    return credit


