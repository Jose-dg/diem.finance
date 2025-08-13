from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.utils import timezone
from decimal import Decimal

from apps.fintech.models import Credit, Transaction, AccountMethodAmount
from .models import CreditEarnings, EarningsAdjustment
from .services.earnings_service import EarningsService
from .tasks import update_credit_earnings, generate_earnings_snapshots

@receiver(post_save, sender=Credit)
def create_credit_earnings(sender, instance, created, **kwargs):
    """
    Crea o actualiza CreditEarnings cuando se crea o modifica un crédito.
    """
    if created:
        theoretical = EarningsService.calculate_theoretical_earnings(instance)
        CreditEarnings.objects.create(
            credit=instance,
            theoretical_earnings=theoretical,
            realized_earnings=Decimal('0.00'),
            earnings_rate=Decimal('0.0000')
        )
    else:
        # Si el crédito se actualizó, programar recálculo de ganancias
        if hasattr(instance, 'earnings_detail'):
            transaction.on_commit(lambda: update_credit_earnings.delay(instance.id))

@receiver(post_save, sender=Transaction)
def update_earnings_on_transaction(sender, instance, created, **kwargs):
    """
    Actualiza CreditEarnings cuando hay una nueva transacción confirmada.
    """
    if instance.status == 'confirmed' and instance.transaction_type == 'income':
        # Obtener créditos afectados por la transacción
        credit_ids = AccountMethodAmount.objects.filter(
            transaction=instance
        ).values_list('credit_id', flat=True).distinct()
        
        # Programar actualización para cada crédito
        for credit_id in credit_ids:
            transaction.on_commit(
                lambda cid=credit_id: update_credit_earnings.delay(cid)
            )

@receiver(post_save, sender=EarningsAdjustment)
def update_earnings_on_adjustment(sender, instance, created, **kwargs):
    """
    Actualiza CreditEarnings cuando se crea un ajuste.
    """
    if created:
        transaction.on_commit(
            lambda: update_credit_earnings.delay(instance.credit_earnings.credit_id)
        )

@receiver([post_save, post_delete], sender=CreditEarnings)
def create_earnings_snapshot(sender, instance, **kwargs):
    """
    Genera un snapshot cuando cambian las ganancias.
    """
    transaction.on_commit(
        lambda: generate_earnings_snapshots.delay(batch_size=1)
    ) 