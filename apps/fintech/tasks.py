import math
from celery import shared_task, group
from celery.utils.log import get_task_logger
from django.db import transaction
from apps.fintech.models import Credit
from apps.fintech.utils import recalculate_credit

logger = get_task_logger(__name__)

@shared_task(
    bind=True,
    name="fintech.batch_recalculate_credits",
)
def batch_recalculate_credits(self, chunk_size=100):
    """
    Actualiza la morosidad de todos los créditos de manera secuencial,
    idéntico al management command original.
    """
    total = Credit.objects.count()
    logger.info(f"Procesando {total} créditos...")

    # Iteración secuencial en chunks
    for credit in Credit.objects.iterator(chunk_size=chunk_size):
        recalculate_credit(credit)
    
    print("Actualización finalizada con éxito.")
    return total
