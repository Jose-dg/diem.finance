import math
from celery import shared_task, group
from celery.utils.log import get_task_logger
from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from apps.fintech.models import Credit, Installment
from apps.fintech.utils import recalculate_credit
from apps.fintech.services.installment_service import InstallmentService

logger = get_task_logger(__name__)

@shared_task(
    bind=True,
    name="fintech.batch_recalculate_credits",
)
def batch_recalculate_credits(self, chunk_size=100):
    """
    Actualiza la morosidad de todos los créditos de manera secuencial,
    optimizado para incluir funcionalidades de cuotas.
    """
    total = Credit.objects.count()
    logger.info(f"Procesando {total} créditos...")

    # Actualizar estados de cuotas primero
    success, message = InstallmentService.update_all_installment_statuses()
    logger.info(f"Actualización de cuotas: {message}")

    # Iteración secuencial en chunks
    for credit in Credit.objects.iterator(chunk_size=chunk_size):
        recalculate_credit(credit)
        
        # Calcular morosidad basada en cuotas
        morosidad_rate = InstallmentService.calculate_credit_morosidad(credit)
        if morosidad_rate > 0:
            credit.is_in_default = True
            credit.save()
    
    logger.info("Actualización finalizada con éxito.")
    return total

@shared_task(
    bind=True,
    name="fintech.update_installment_statuses",
)
def update_installment_statuses(self):
    """
    Actualiza el estado de todas las cuotas pendientes
    """
    try:
        success, message = InstallmentService.update_all_installment_statuses()
        logger.info(f"Actualización de estados de cuotas: {message}")
        return success
    except Exception as e:
        logger.error(f"Error actualizando estados de cuotas: {str(e)}")
        return False

@shared_task(
    bind=True,
    name="fintech.send_payment_reminders",
)
def send_payment_reminders(self):
    """
    Envía recordatorios de pago para cuotas que vencen pronto - OPTIMIZADO
    """
    try:
        # Usar el servicio optimizado
        success, message = InstallmentService.schedule_payment_reminders()
        logger.info(f"Recordatorios de pago: {message}")
        return success
    except Exception as e:
        logger.error(f"Error enviando recordatorios: {str(e)}")
        return False

@shared_task(
    bind=True,
    name="fintech.send_overdue_notifications",
)
def send_overdue_notifications(self):
    """
    Envía notificaciones de cuotas vencidas
    """
    try:
        success, message = InstallmentService.send_overdue_notifications()
        logger.info(f"Notificaciones de cuotas vencidas: {message}")
        return success
    except Exception as e:
        logger.error(f"Error enviando notificaciones de mora: {str(e)}")
        return False

@shared_task(
    bind=True,
    name="fintech.generate_installments_for_new_credits",
)
def generate_installments_for_new_credits(self):
    """
    Genera cuotas para créditos nuevos que no las tienen
    """
    try:
        # Obtener créditos sin cuotas
        credits_without_installments = Credit.objects.filter(
            installments__isnull=True
        ).exclude(
            state__in=['completed', 'cancelled']
        )
        
        generated_count = 0
        for credit in credits_without_installments:
            success, message = InstallmentService.generate_installments_for_credit(credit)
            if success:
                generated_count += 1
        
        logger.info(f"Se generaron cuotas para {generated_count} créditos")
        return generated_count
    except Exception as e:
        logger.error(f"Error generando cuotas: {str(e)}")
        return 0

@shared_task(
    bind=True,
    name="fintech.installment_daily_maintenance",
)
def installment_daily_maintenance(self):
    """
    Mantenimiento diario de cuotas - OPTIMIZADO
    """
    try:
        logger.info("Iniciando mantenimiento diario de cuotas...")
        
        # 1. Actualizar estados y montos en batch
        success, message = InstallmentService.update_all_installment_statuses()
        logger.info(f"Actualización de estados: {message}")
        
        # 2. Actualizar montos restantes
        success, message = InstallmentService.bulk_update_remaining_amounts()
        logger.info(f"Actualización de montos: {message}")
        
        # 3. Programar recordatorios
        success, message = InstallmentService.schedule_payment_reminders()
        logger.info(f"Programación de recordatorios: {message}")
        
        # 4. Enviar notificaciones de mora
        success, message = InstallmentService.send_overdue_notifications()
        logger.info(f"Notificaciones de mora: {message}")
        
        # 5. Generar cuotas para créditos nuevos
        generate_installments_for_new_credits.delay()
        
        logger.info("Mantenimiento diario de cuotas completado")
        return True
    except Exception as e:
        logger.error(f"Error en mantenimiento diario: {str(e)}")
        return False
