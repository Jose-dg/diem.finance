from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from apps.fintech.utils import recalculate_credit
from .models import Transaction, AccountMethodAmount, Credit
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

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

@receiver(post_save, sender=AccountMethodAmount)
def update_credit_on_account_method_change(sender, instance, **kwargs):
    """
    Solo actualizamos el crédito si la transacción es de tipo 'income'
    """
    if instance.transaction.transaction_type == 'income':
        instance.credit.update_total_abonos(instance.amount_paid)

@receiver(post_delete, sender=AccountMethodAmount)
def adjust_credit_on_delete(sender, instance, **kwargs):
    """
    Ajusta el total de abonos cuando se elimina un AccountMethodAmount.
    """
    if instance.credit:
        instance.credit.update_total_abonos(-instance.amount_paid)

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
            transaction=transaction  
        )

@receiver(post_save, sender=Transaction)
def handle_transaction_save(sender, instance, **kwargs):
    """
    Recalcula el crédito completo al guardar una transacción confirmada de ingreso.
    """
    if instance.transaction_type != 'income' or instance.status != 'confirmed':
        return

    if instance.credit:
        recalculate_credit(instance.credit.uid)
        
@receiver(post_delete, sender=Transaction)
def handle_transaction_delete(sender, instance, **kwargs):
    """
    Recalcula el crédito completo si se elimina una transacción que afecta el saldo.
    """
    if instance.credit:
        recalculate_credit(instance.credit.uid)