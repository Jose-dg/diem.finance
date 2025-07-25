from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from django.db import transaction
from decimal import Decimal
from django.db import transaction
from apps.fintech.models import Installment, Transaction
from decimal import Decimal, ROUND_HALF_UP
from django.utils.timezone import now
import math

from django.db import transaction
from django.utils import timezone

from datetime import date, timedelta
import calendar
from django.utils import timezone
from dateutil.relativedelta import relativedelta


from decimal import Decimal
from datetime import date
import calendar
from django.utils import timezone
from django.db.models import Sum

from apps.fintech.models import Installment, Transaction, Credit, Adjustment  

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

def credit_has_overdue_installments(credit):
    today = now().date()
    return Installment.objects.filter(
        credit=credit,
        paid=False,
        due_date__lt=today
    ).exists()


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

def update_credit_payment_dates(credit):
    installments = credit.installments.all()

    # Última cuota pagada
    last_paid = installments.filter(paid=True).order_by('-paid_on').first()
    credit.first_date_payment = last_paid.paid_on if last_paid else None

    # Próxima cuota pendiente
    today = timezone.now().date()
    next_due = installments.filter(paid=False, due_date__gte=today).order_by('due_date').first()
    credit.second_date_payment = next_due.due_date if next_due else None

    credit.save(update_fields=['first_date_payment', 'second_date_payment'])
# apps/fintech/utils.py

@transaction.atomic
def recalculate_credit(credit: Credit):
    """
    1) Vuelve a sumar abonos confirmados y ajustes
    2) Recalcula earnings, interés, pending_amount, installment_number, installment_value
    3) Genera la lista de fechas esperadas (hasta 'hoy') con generate_payment_dates()
       (respetando si first_date_payment y second_date_payment ya estaban definidas)
    4) Compara esas fechas con los pagos realizados (los Transactions confirmados),
       para determinar si hay cuotas vencidas (morosidad).
    5) Ajusta credit.morosidad_level, credit.is_in_default, credit.state.
    6) Guarda el crédito.
    """

    today = timezone.now().date()

    # 1) Sumar abonos de transacciones confirmadas para este crédito
    total_abonos = Transaction.objects.filter(
        account_method_amounts__credit=credit,
        transaction_type='income',
        status='confirmed'
    ).aggregate(total=Sum('account_method_amounts__amount_paid'))['total'] or Decimal('0.00')

    # 2) Sumar ajustes de intereses adicionales (si usas un modelo Adjustment)
    total_adjustments = credit.adjustments.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')

    # 3) Recalcular earnings e interés
    cost = Decimal(credit.cost)
    price = Decimal(credit.price)
    credit_days = Decimal(credit.credit_days)
    periodicity_days = Decimal(credit.periodicity.days) if credit.periodicity and credit.periodicity.days else Decimal(1)

    credit.earnings = price - cost
    if cost and price and credit_days:
        # Fórmula de interés que ya tenías
        credit.interest = (Decimal(1) / (credit_days / Decimal(30))) * ((price - cost) / cost)

    # 4) Recalcular número y valor de cuotas
    if periodicity_days and credit_days:
        installment_number = math.ceil(credit_days / periodicity_days)
        credit.installment_number = installment_number
        if installment_number > 0:
            credit.installment_value = (price / Decimal(installment_number)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        else:
            credit.installment_value = price

    # 5) Recalcular pending_amount
    pending = (price + total_adjustments) - total_abonos
    credit.total_abonos = total_abonos
    credit.pending_amount = pending

    # 6) Generar la lista de fechas esperadas de pago
    first_date = credit.first_date_payment
    second_date = credit.second_date_payment
    # Pasamos periodicity_days como entero a la función
    payment_dates = generate_payment_dates(first_date, second_date, int(periodicity_days), today)

    # 7) Obtener todas las fechas en las que ya hubo un pago confirmado
    payments_made = Transaction.objects.filter(
        account_method_amounts__credit=credit,
        transaction_type='income',
        status='confirmed'
    ).values_list('date', flat=True).distinct()

    # 8) De todas las fechas esperadas, las que ya pasaron (<= hoy) pero no están en payments_made,
    #    son "fechas vencidas sin pago": morosidad
    missed_dates = [
        d for d in payment_dates
        if d <= today and d not in payments_made
    ]

    # 9) Determinar nivel de morosidad
    if not missed_dates:
        credit.morosidad_level = 'on_time'
        credit.is_in_default = False
        credit.state = 'completed' if pending <= Decimal('0.01') else 'pending'
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
        credit.state = 'pending' if pending > Decimal('0.00') else 'completed'

    credit.updated_at = timezone.now()
    credit.save()

    return credit


def next_quincena(from_date: date) -> date:
    """
    (Misma lógica que antes) para calcular la próxima quincena
    respetando la regla "< 5 días → saltar".
    """
    dia = from_date.day
    mes = from_date.month
    año = from_date.year

    if dia < 15:
        candidato = date(año, mes, 15)
    else:
        ultimo = calendar.monthrange(año, mes)[1]
        candidato = date(año, mes, ultimo)

    if (candidato - from_date).days < 5:
        if dia < 15:
            ultimo = calendar.monthrange(año, mes)[1]
            nuevo = date(año, mes, ultimo)
            if (nuevo - from_date).days < 5:
                if mes == 12:
                    candidato = date(año + 1, 1, 15)
                else:
                    candidato = date(año, mes + 1, 15)
            else:
                candidato = nuevo
        else:
            if mes == 12:
                candidato = date(año + 1, 1, 15)
            else:
                candidato = date(año, mes + 1, 15)

    return candidato


def generate_payment_dates(first_date, second_date, periodicity_days, today=None):
    """
    Genera la secuencia de fechas de pago esperadas según:
    - Si el crédito ya trae first_date_payment y second_date_payment, inferimos periodicidad.
    - Caso contrario, periódicamente cada N días, o "quincenal" con la regla < 5 días, o "mensual exacto".
    Devuelve todas las fechas <= hoy.
    """
    if today is None:
        today = timezone.now().date()

    dates = []

    # 1) Inferir periodicidad real
    if first_date and second_date:
        infer_days = (second_date - first_date).days
    else:
        infer_days = periodicity_days or 1

    current_date = first_date

    # 2) Iterar hasta 'today'
    while current_date and current_date <= today:
        dates.append(current_date)

        if infer_days == 1:
            # Diario
            current_date = current_date + timedelta(days=1)

        elif infer_days == 15:
            # Quincenal con regla
            next_date = next_quincena(current_date)
            if next_date <= current_date:
                break
            current_date = next_date

        elif 28 <= infer_days <= 31:
            # Mensual exacto
            try:
                current_date = current_date + relativedelta(months=1)
            except ValueError:
                # Ajustar al último día del mes
                temp = current_date + relativedelta(months=1)
                ultimo = calendar.monthrange(temp.year, temp.month)[1]
                current_date = temp.replace(day=ultimo)

        else:
            # Cada N días
            current_date = current_date + timedelta(days=infer_days)

    return dates
