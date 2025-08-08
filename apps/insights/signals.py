from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

from apps.fintech.models import Credit, Transaction
from .services import ActivityService

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Transaction)
def transaction_activity(sender, instance, created, **kwargs):
    try:
        if created and instance.transaction_type == 'income' and instance.status == 'confirmed':
            credit_ids = instance.accountmethodamount_set.values_list('credit_id', flat=True)
            for cid in credit_ids:
                credit = Credit.objects.filter(id=cid).first()
                if credit:
                    ActivityService.log(
                        user=credit.user,
                        activity_type='payment_made',
                        description='Pago confirmado',
                        credit=credit,
                        transaction=instance,
                        amount=float(getattr(instance, 'amount', 0)) or None,
                        metadata={'transaction_id': instance.id}
                    )
    except Exception as e:
        logger.error(f"Error logging transaction activity: {e}")

@receiver(post_save, sender=Credit)
def credit_state_activity(sender, instance, created, **kwargs):
    try:
        if created:
            ActivityService.log(
                user=instance.user,
                activity_type='credit_approved' if getattr(instance, 'status', '') == 'approved' else 'credit_request',
                description='Nuevo crédito creado',
                credit=instance,
                metadata={'credit_uid': str(instance.uid)}
            )
    except Exception as e:
        logger.error(f"Error logging credit activity: {e}") 