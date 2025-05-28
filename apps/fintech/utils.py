from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from django.db import transaction
from decimal import Decimal
from django.db import transaction
from apps.fintech.models import Installment, Transaction
from decimal import Decimal, ROUND_HALF_UP

import math

from django.db import transaction
from django.utils import timezone

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

    # 6. Generar fechas esperadas de pago según periodicidad
    first_date_payment = credit.first_date_payment
    second_date_payment = credit.second_date_payment

    payment_dates = generate_payment_dates(first_date_payment, second_date_payment, periodicity_days, today)

    # 7. Verificar pagos realizados en las fechas esperadas
    payments_made = Transaction.objects.filter(
        account_method_amounts__credit=credit,
        transaction_type='income',
        status='confirmed'
    ).values_list('date', flat=True).distinct()

    missed_dates = [date for date in payment_dates if date <= today and date not in payments_made]

    # 8. Determinar morosidad basado en fechas perdidas
    if not missed_dates:
        credit.morosidad_level = 'on_time'
        credit.is_in_default = False
        credit.state = 'completed' if pending <= 0.01 else 'pending'
    else:
        missed_count = len(missed_dates)
        if missed_count == 1:
            morosidad = 'mild_default'
        elif missed_count == 2:
            morosidad = 'moderate_default'
        elif missed_count == 3:
            morosidad = 'severe_default'
        elif missed_count == 4:
            morosidad = 'recurrent_default'
        else:
            morosidad = 'critical_default'

        credit.morosidad_level = morosidad
        credit.is_in_default = True

        # Si hay saldo pendiente, el estado será siempre "pending"
        credit.state = 'pending' if pending > 0 else 'completed'

    credit.updated_at = timezone.now()
    credit.save()
    return credit

def generate_payment_dates(first_date, second_date, periodicity_days, today):
    dates = []
    current_date = first_date
    periodicity_days = int(periodicity_days)  # Convertimos a entero directamente

    while current_date <= today:
        dates.append(current_date)
        if periodicity_days == 7:
            current_date += timezone.timedelta(days=7)
        elif periodicity_days == 15:
            next_day = second_date if current_date == first_date else first_date + timezone.timedelta(days=15)
            if next_day > today:
                break
            dates.append(next_day)
            current_date += timezone.timedelta(days=15)
        elif periodicity_days == 30:
            current_date += timezone.timedelta(days=30)
        else:
            current_date += timezone.timedelta(days=periodicity_days)

    return dates


def generar_cuotas(credit):
    if not credit.periodicity or not credit.installment_number or not credit.installment_value:
        return

    cuotas = []
    fecha_inicial = credit.created_at.date()
    dias_periodicidad = credit.periodicity.days

    for i in range(credit.installment_number):
        fecha_vencimiento = fecha_inicial + timedelta(days=(i + 1) * dias_periodicidad)
        cuota = Installment(
            credit=credit,
            number=i + 1,
            due_date=fecha_vencimiento,
            amount=credit.installment_value,
            principal_amount=credit.installment_value,  # Puedes refinar esto si separas interés
            interest_amount=Decimal('0.00')
        )
        cuotas.append(cuota)

    Installment.objects.bulk_create(cuotas)

    # Actualizar las fechas de primer y último pago
    if cuotas:
        credit.first_date_payment = cuotas[0].due_date
        credit.second_date_payment = cuotas[-1].due_date
        credit.save(update_fields=['first_date_payment', 'second_date_payment'])


def distribuir_pago_a_cuotas(credit, monto_pagado, fecha_pago=None):
    monto_restante = monto_pagado

    cuotas_pendientes = Installment.objects.filter(
        credit=credit,
        paid=False
    ).order_by('due_date', 'number')

    for cuota in cuotas_pendientes:
        if monto_restante <= Decimal('0.00'):
            break

        monto_cuota = cuota.amount or Decimal('0.00')

        if monto_restante >= monto_cuota:
            cuota.principal_amount = monto_cuota
            cuota.paid = True
            cuota.paid_on = fecha_pago
            cuota.save()
            monto_restante -= monto_cuota
        else:
            cuota.principal_amount = (cuota.principal_amount or Decimal('0.00')) + monto_restante
            cuota.save()
            monto_restante = Decimal('0.00')
            break