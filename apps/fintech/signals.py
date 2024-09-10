from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Transaction, AccountMethodAmount

@receiver(pre_save, sender=AccountMethodAmount)
def adjust_credit_on_update(sender, instance, **kwargs):
    if instance.pk:  # Actualización de una transacción existente
        previous = AccountMethodAmount.objects.get(pk=instance.pk)
        if previous.amount_paid != instance.amount_paid:
            difference = instance.amount_paid - previous.amount_paid
            instance.credit.update_total_abonos(difference)

@receiver(post_save, sender=AccountMethodAmount)
def update_credit_pending_amount_on_create(sender, instance, created, **kwargs):
    if created:  # Nueva transacción
        instance.credit.update_total_abonos(instance.amount_paid)
    instance.credit.save()

@receiver(post_delete, sender=AccountMethodAmount)
def adjust_credit_on_delete(sender, instance, **kwargs):
    if instance.credit:
        instance.credit.update_total_abonos(-instance.amount_paid)
        instance.credit.save()

@receiver(post_save, sender=AccountMethodAmount)
def update_account_balance_on_create(sender, instance, created, **kwargs):
    if created:  # Nueva transacción
        instance.payment_method.balance += instance.amount_paid
        instance.payment_method.save()

@receiver(pre_save, sender=AccountMethodAmount)
def adjust_account_balance_on_update(sender, instance, **kwargs):
    if instance.pk:  # Actualización de una transacción existente
        previous = AccountMethodAmount.objects.get(pk=instance.pk)
        if previous.amount_paid != instance.amount_paid:
            difference = instance.amount_paid - previous.amount_paid
            instance.payment_method.balance += difference
            instance.payment_method.save()

@receiver(post_delete, sender=AccountMethodAmount)
def adjust_account_balance_on_delete(sender, instance, **kwargs):
    if instance.payment_method:
        instance.payment_method.balance -= instance.amount_paid
        instance.payment_method.save()

@receiver(post_save, sender=Transaction)
def calculate_morosidad(sender, instance, **kwargs):
    """
    Calcula la morosidad del crédito cada vez que se guarda una transacción (abono).
    """
    # Obtiene el crédito asociado a la transacción
    credit = instance.credit

    # Si existe un crédito asociado a la transacción, actualiza la morosidad
    if credit:
        credit.check_if_payment_is_due()