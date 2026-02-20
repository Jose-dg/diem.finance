from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction as db_transaction
import logging

from apps.fintech.models import Credit, Transaction
from .services import ActivityService
from .tasks import recalculate_user_metrics_task

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
            
            # Recalcular métricas del usuario en segundo plano
            if instance.user:
                db_transaction.on_commit(
                    lambda: recalculate_user_metrics_task.delay(instance.user.id)
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
            
            # Recalcular métricas del usuario en segundo plano
            if instance.user:
                db_transaction.on_commit(
                    lambda: recalculate_user_metrics_task.delay(instance.user.id)
                )
    except Exception as e:
        logger.error(f"Error logging credit activity: {e}")
 