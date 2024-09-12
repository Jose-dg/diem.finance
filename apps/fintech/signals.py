from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Expense, Transaction, AccountMethodAmount, Credit
from datetime import date, timedelta, datetime

@receiver(pre_save, sender=AccountMethodAmount)
def adjust_credit_on_update(sender, instance, **kwargs):
    """
    Ajusta el total de abonos cuando se actualiza un AccountMethodAmount.
    """
    if instance.pk:
        previous = AccountMethodAmount.objects.get(pk=instance.pk)
        if previous.amount_paid != instance.amount_paid:
            difference = instance.amount_paid - previous.amount_paid
            instance.credit.update_total_abonos(difference)

# @receiver(post_save, sender=AccountMethodAmount)
# def update_credit_on_create(sender, instance, created, **kwargs):
#     """
#     Actualiza el total de abonos y el saldo pendiente cuando se crea un nuevo AccountMethodAmount.
#     """
#     if created:
#         instance.credit.update_total_abonos(instance.amount_paid)

@receiver(post_save, sender=AccountMethodAmount)
def update_credit_on_account_method_change(sender, instance, **kwargs):
    # Solo actualizamos el crédito si la transacción es de tipo 'income'
    if instance.transaction.transaction_type == 'income':
        instance.credit.update_total_abonos(instance.amount_paid)


@receiver(post_delete, sender=AccountMethodAmount)
def adjust_credit_on_delete(sender, instance, **kwargs):
    """
    Ajusta el total de abonos cuando se elimina un AccountMethodAmount.
    """
    if instance.credit:
        instance.credit.update_total_abonos(-instance.amount_paid)

# @receiver(post_save, sender=Credit)
# def create_transaction_on_credit_creation(sender, instance, created, **kwargs):
#     """
#     Crea una transacción de tipo 'expense' cuando se crea un nuevo crédito.
#     """
#     if created:
#         Transaction.objects.create(
#             transaction_type='expense',
#             user=instance.user,
#             category=instance.subcategory,
#             date=instance.created_at,
#             description=f"Crédito creado por valor de ${instance.price}.00",
#         )
#             # Crear AccountMethodAmount asociado a la transacción del crédito
#         AccountMethodAmount.objects.create(
#             payment_method=instance.payment,  # Método de pago relacionado al crédito
#             payment_code=f"{transaction.uid}-credit",  # Código único
#             amount=instance.price,  # Monto total del crédito (lo que se entrega)
#             amount_paid=instance.price,  # El monto entregado al cliente es igual al amount
#             currency=instance.currency,
#             credit=instance,
#             transaction=transaction
#         )

@receiver(post_save, sender=Credit)
def create_transaction_and_account_method(sender, instance, created, **kwargs):
    """
    Crea una transacción de tipo 'expense' cuando se crea un nuevo crédito y un registro asociado en AccountMethodAmount.
    """
    if created:
        # Crear la transacción de crédito
        transaction = Transaction.objects.create(
            transaction_type='expense',
            user=instance.user,
            category=instance.subcategory,
            date=instance.created_at,
            description=f"Crédito de ${instance.price}.00 registrado.",
        )

        # Formatear la fecha y hora para el payment_code
        current_datetime = datetime.now()
        payment_code = current_datetime.strftime("%d%m%Y%H%M")  # Formato DDMMYYYYHHMM

        # Crear AccountMethodAmount asociado a la transacción
        AccountMethodAmount.objects.create(
            payment_method=instance.payment,  # Método de pago relacionado al crédito
            payment_code=f"CP{payment_code}",  # Código único
            amount=instance.price,  # Monto total del crédito (lo que se entrega)
            amount_paid=instance.price,  # El monto entregado al cliente es igual al amount
            currency=instance.currency,
            credit=instance,
            transaction=transaction  # Asignar la transacción creada
        )

@receiver(post_save, sender=AccountMethodAmount)
def check_if_payment_is_due(sender, instance, **kwargs):
    """
    Verifica si el cliente ha incumplido pagos y ajusta el nivel de morosidad.
    """
    credit = instance.credit
    today = date.today()

    # Calcular los días desde el primer pago
    days_since_first_payment = (today - credit.first_date_payment).days

    # Calcular cuántos pagos deberían haberse realizado hasta hoy
    payments_due = days_since_first_payment // credit.periodicity.days if credit.periodicity else 0

    # Total que debería haberse pagado hasta hoy
    total_expected_payment = payments_due * credit.installment_value if credit.installment_value else 0

    # Evaluar el estado de morosidad
    if credit.total_abonos < total_expected_payment:
        if credit.total_abonos > 0:
            credit.morosidad_level = 'mild_default'
            missed_periods = (total_expected_payment - credit.total_abonos) // credit.installment_value
            if missed_periods >= 2:
                credit.morosidad_level = 'recurrent_default'
        else:
            if days_since_first_payment > 2 * credit.periodicity.days:
                credit.morosidad_level = 'critical_default'
            else:
                credit.morosidad_level = 'severe_default'
        credit.is_in_default = True
    else:
        expected_payment_date = credit.first_date_payment + timedelta(days=payments_due * credit.periodicity.days)
        if payments_due > 0 and today > expected_payment_date:
            credit.morosidad_level = 'moderate_default'
        else:
            credit.morosidad_level = 'on_time'
            credit.is_in_default = False

    credit.save()

@receiver(post_save, sender=Expense)
def create_transaction_and_update_account(sender, instance, created, **kwargs):
    if created:
        # Crear la transacción del gasto
        transaction = Transaction.objects.create(
            transaction_type='expense',
            user=instance.registered_by,  # Quién hizo el gasto
            category=instance.subcategory,
            date=instance.date,
            description=f"Gasto registrado por ${instance.amount}.00",
        )
        # Actualizar AccountMethodAmount con el gasto
        AccountMethodAmount.objects.create(
            payment_method=instance.account,  # Cuenta desde donde se pagó
            payment_code=f"{transaction.uid}-expense",  # Código único
            amount=instance.amount,
            amount_paid=instance.amount,  # El monto total se refleja en el gasto
            currency=instance.account.currency,
            transaction=transaction
        )
