from datetime import timedelta, date
import math
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from apps.fintech.models import Credit, Transaction
from decimal import Decimal
from django.db import transaction
from decimal import Decimal
from django.db import transaction

from apps.fintech.models import Transaction  # Asegúrate de importar correctamente

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
    Recalcula el total de abonos y el saldo pendiente de un crédito,
    sumando todas las transacciones de tipo "income".
    """
    total_abonos = credit.transaction_set.filter(transaction_type="income").aggregate(total_abonos=Sum('amount'))['total_abonos'] or 0
    pending_amount = max(credit.price - total_abonos, 0)

    credit.total_abonos = total_abonos
    credit.pending_amount = pending_amount
    credit.save(update_fields=['total_abonos', 'pending_amount'])

    return credit

def evaluate_morosidad(credit):
    """
    Determina si el crédito está en mora y su nivel.
    """
    # Esto se puede hacer más complejo luego según reglas de negocio
    overdue_days = (timezone.now().date() - credit.second_date_payment).days
    is_in_default = overdue_days > 0

    if overdue_days <= 0:
        level = 'on_time'
    elif overdue_days <= 5:
        level = 'mild_default'
    elif overdue_days <= 15:
        level = 'moderate_default'
    elif overdue_days <= 30:
        level = 'severe_default'
    elif overdue_days <= 60:
        level = 'recurrent_default'
    else:
        level = 'critical_default'

    return is_in_default, level

@transaction.atomic
def recalculate_credit(credit):
    today = timezone.now().date()

    # 1. Sumar abonos de transacciones confirmadas
    total_abonos = Transaction.objects.filter(
        account_method_amounts__credit=credit,
        transaction_type='income',
        status='confirmed'
    ).aggregate(total=Sum('account_method_amounts__amount_paid'))['total'] or Decimal('0.00')

    # 2. Sumar o restar ajustes de intereses adicionales
    total_adjustments = credit.adjustments.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')

    # 3. Recalcular earnings e interés
    cost = Decimal(credit.cost)
    price = Decimal(credit.price)
    credit_days = Decimal(credit.credit_days)
    periodicity_days = Decimal(credit.periodicity.days) if credit.periodicity and credit.periodicity.days else Decimal(1)

    credit.earnings = price - cost
    if cost and price and credit_days:
        credit.interest = (Decimal(1) / (credit_days / Decimal(30))) * ((price - cost) / cost)

    # 4. Cuotas
    if periodicity_days and credit_days:
        installment_number = math.ceil(credit_days / periodicity_days)
        credit.installment_number = installment_number

        if installment_number > 0:
            credit.installment_value = (price / Decimal(installment_number)).quantize(Decimal('.01'))
        else:
            credit.installment_value = price

    # 5. Calculamos el pending amount ajustado
    pending = (price + total_adjustments) - total_abonos
    credit.total_abonos = total_abonos
    credit.pending_amount = pending

    # 6. Morosidad y estado
    last_payment = Transaction.objects.filter(
        account_method_amounts__credit=credit,
        transaction_type='income',
        status='confirmed'
    ).order_by('-date').first()

    last_payment_date = last_payment.date.date() if last_payment else credit.first_date_payment

    if pending <= 0.01:
        credit.morosidad_level = 'on_time'
        credit.is_in_default = False
        credit.state = 'completed'
        credit.pending_amount = 0  # Normalizamos
    else:
        days_since_last_payment = (today - last_payment_date).days
        delay_ratio = days_since_last_payment / periodicity_days

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

        credit.morosidad_level = morosidad
        credit.is_in_default = morosidad != 'on_time'

    credit.updated_at = timezone.now()
    credit.save()

    return credit
