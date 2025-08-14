from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
import logging

from apps.fintech.models import Credit, Transaction, AccountMethodAmount
from .models import CreditEarnings, EarningsAdjustment
from .services.earnings_service import EarningsService

logger = logging.getLogger(__name__)

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
        # Si el crédito se actualizó, actualizar ganancias de forma síncrona
        if hasattr(instance, 'earnings_detail'):
            try:
                # Actualizar ganancias directamente
                earnings = CreditEarnings.objects.filter(credit=instance).first()
                if earnings:
                    earnings.theoretical_earnings = EarningsService.calculate_theoretical_earnings(instance)
                    earnings.save()
            except Exception as e:
                logger.error(f"Error actualizando ganancias para crédito {instance.id}: {e}")

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
        
        # Actualizar ganancias de forma síncrona
        for credit_id in credit_ids:
            try:
                # Actualizar ganancias directamente
                earnings = CreditEarnings.objects.filter(credit_id=credit_id).first()
                if earnings:
                    # Recalcular ganancias realizadas basadas en transacciones confirmadas
                    from django.db.models import Sum
                    total_income = Transaction.objects.filter(
                        account_method_amounts__credit_id=credit_id,
                        transaction_type='income',
                        status='confirmed'
                    ).aggregate(total=Sum('account_method_amounts__amount_paid'))['total'] or Decimal('0.00')
                    
                    earnings.realized_earnings = total_income
                    if earnings.theoretical_earnings > 0:
                        earnings.earnings_rate = (total_income / earnings.theoretical_earnings).quantize(Decimal('0.0001'))
                    earnings.save()
            except Exception as e:
                logger.error(f"Error actualizando ganancias para crédito {credit_id}: {e}")

@receiver(post_save, sender=EarningsAdjustment)
def update_earnings_on_adjustment(sender, instance, created, **kwargs):
    """
    Actualiza CreditEarnings cuando se crea un ajuste.
    """
    if created:
        try:
            # Actualizar ganancias directamente
            earnings = CreditEarnings.objects.filter(credit=instance.credit_earnings.credit).first()
            if earnings:
                # Recalcular ganancias realizadas
                from django.db.models import Sum
                total_income = Transaction.objects.filter(
                    account_method_amounts__credit=instance.credit_earnings.credit,
                    transaction_type='income',
                    status='confirmed'
                ).aggregate(total=Sum('account_method_amounts__amount_paid'))['total'] or Decimal('0.00')
                
                earnings.realized_earnings = total_income
                if earnings.theoretical_earnings > 0:
                    earnings.earnings_rate = (total_income / earnings.theoretical_earnings).quantize(Decimal('0.0001'))
                earnings.save()
        except Exception as e:
            logger.error(f"Error actualizando ganancias por ajuste: {e}")

# Comentamos esta señal ya que los snapshots no son críticos para transacciones puntuales
# @receiver([post_save, post_delete], sender=CreditEarnings)
# def create_earnings_snapshot(sender, instance, **kwargs):
#     """
#     Genera un snapshot cuando cambian las ganancias.
#     """
#     # Los snapshots se pueden generar de forma periódica con Celery
#     pass 