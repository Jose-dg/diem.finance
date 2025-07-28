import math
from celery import shared_task, group
from celery.utils.log import get_task_logger
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from django.db.models import F

from apps.fintech.models import Credit, Installment
from apps.fintech.utils import recalculate_credit
from apps.fintech.services.installment_service import InstallmentService
from apps.fintech.services.installment_calculator import InstallmentCalculator
from apps.fintech.services.credit_adjustment_service import CreditAdjustmentService

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
        # Buscar créditos sin cuotas
        credits_without_installments = Credit.objects.filter(
            installments__isnull=True
        ).exclude(
            state__in=['cancelled', 'to_solve']
        )
        
        count = 0
        for credit in credits_without_installments:
            try:
                InstallmentService.generate_installments_for_credit(credit)
                count += 1
                logger.info(f"Cuotas generadas para crédito {credit.uid}")
            except Exception as e:
                logger.error(f"Error generando cuotas para crédito {credit.uid}: {str(e)}")
        
        logger.info(f"Se generaron cuotas para {count} créditos")
        return count
        
    except Exception as e:
        logger.error(f"Error en generación de cuotas: {str(e)}")
        return 0

@shared_task(
    bind=True,
    name="fintech.installment_daily_maintenance",
)
def installment_daily_maintenance(self):
    """
    Mantenimiento diario de cuotas - TAREA PRINCIPAL
    """
    try:
        logger.info("Iniciando mantenimiento diario de cuotas...")
        
        # 1. Actualizar estados de cuotas
        success, message = InstallmentService.update_all_installment_statuses()
        logger.info(f"Estados actualizados: {message}")
        
        # 2. Enviar recordatorios
        success, message = InstallmentService.schedule_payment_reminders()
        logger.info(f"Recordatorios enviados: {message}")
        
        # 3. Notificaciones de mora
        success, message = InstallmentService.send_overdue_notifications()
        logger.info(f"Notificaciones enviadas: {message}")
        
        # 4. Generar cuotas para créditos nuevos
        count = generate_installments_for_new_credits.delay()
        logger.info(f"Cuotas generadas: {count}")
        
        logger.info("Mantenimiento diario completado exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"Error en mantenimiento diario: {str(e)}")
        return False

@shared_task
def check_additional_interest_daily():
    """
    Verifica diariamente créditos que necesitan interés adicional
    """
    try:
        from apps.fintech.services.credit_adjustment_service import CreditAdjustmentService
        
        # Créditos con pagos parciales que no han recibido interés adicional
        credits_with_partial_payments = Credit.objects.filter(
            total_abonos__lt=F('price'),
            state__in=['pending', 'completed']
        ).exclude(
            adjustments__type__code='C0001'  # Excluir los que ya tienen interés adicional
        )
        
        applied_count = 0
        for credit in credits_with_partial_payments:
            try:
                if CreditAdjustmentService.should_apply_additional_interest(credit):
                    amount = CreditAdjustmentService.apply_additional_interest(
                        credit,
                        reason=f"Verificación diaria: Total pagado {credit.total_abonos} < Total pactado {credit.price}"
                    )
                    if amount > 0:
                        applied_count += 1
                        logger.info(f"Interés adicional aplicado a crédito {credit.uid}: ${amount}")
                        
            except Exception as e:
                logger.error(f"Error aplicando interés adicional a crédito {credit.uid}: {str(e)}")
        
        logger.info(f"Verificación diaria completada. Interés aplicado a {applied_count} créditos")
        return applied_count
        
    except Exception as e:
        logger.error(f"Error en verificación diaria de interés adicional: {str(e)}")
        return 0

@shared_task
def calculate_installment_fields_batch():
    """Calcula campos para cuotas que necesitan actualización"""
    from django.conf import settings
    
    # Identificar cuotas que necesitan recálculo
    all_installments = []
    
    # 1. Cuotas que vencen hoy
    today = timezone.now().date()
    due_today = Installment.objects.filter(
        due_date=today,
        status='pending'
    )
    all_installments.extend(due_today)
    
    # 2. Cuotas con mora alta (30+ días)
    overdue_30_plus = Installment.objects.filter(
        status__in=['pending', 'partial'],
        due_date__lt=today - timedelta(days=30)
    )
    all_installments.extend(overdue_30_plus)
    
    # 3. Cuotas con pagos parciales recientes
    recent_partial = Installment.objects.filter(
        status='partial',
        updated_at__gte=timezone.now() - timedelta(hours=24)
    )
    all_installments.extend(recent_partial)
    
    # 4. Cuotas que necesitan recálculo general
    for installment in Installment.objects.filter(status__in=['pending', 'partial']):
        if InstallmentCalculator.should_recalculate(installment):
            all_installments.append(installment)
    
    # Eliminar duplicados
    unique_installments = list(set(all_installments))
    
    # Procesar en lotes
    processed_count = 0
    for installment in unique_installments:
        try:
            # Limpiar cache
            InstallmentCalculator.clear_cache(installment.id)
            
            # Recalcular campos
            InstallmentCalculator.get_remaining_amount(installment)
            InstallmentCalculator.get_days_overdue(installment)
            InstallmentCalculator.get_late_fee(installment)
            
            processed_count += 1
            
        except Exception as e:
            logger.error(f"Error procesando cuota {installment.id}: {str(e)}")
    
    logger.info(f"Procesadas {processed_count} cuotas de {len(unique_installments)} identificadas")
    return processed_count

@shared_task
def calculate_overdue_installments():
    """Actualiza cuotas vencidas y calcula mora"""
    today = timezone.now().date()
    
    # Cuotas vencidas que no están marcadas como overdue
    overdue_installments = Installment.objects.filter(
        due_date__lt=today,
        status__in=['pending', 'partial']
    )
    
    updated_count = 0
    for installment in overdue_installments:
        try:
            # Actualizar estado
            if installment.status == 'pending':
                installment.status = 'overdue'
            
            # Recalcular mora
            InstallmentCalculator.clear_cache(installment.id)
            late_fee = InstallmentCalculator.get_late_fee(installment)
            days_overdue = InstallmentCalculator.get_days_overdue(installment)
            
            installment.late_fee = late_fee
            installment.days_overdue = days_overdue
            installment.save(update_fields=['status', 'late_fee', 'days_overdue'])
            
            updated_count += 1
            
        except Exception as e:
            logger.error(f"Error actualizando cuota vencida {installment.id}: {str(e)}")
    
    logger.info(f"Actualizadas {updated_count} cuotas vencidas")
    return updated_count

@shared_task
def update_credit_statuses():
    """Actualiza estados de créditos basado en sus cuotas"""
    credits_with_installments = Credit.objects.filter(
        installments__isnull=False
    ).distinct()
    
    updated_count = 0
    for credit in credits_with_installments:
        try:
            InstallmentCalculator.update_credit_status(credit)
            updated_count += 1
            
        except Exception as e:
            logger.error(f"Error actualizando estado de crédito {credit.uid}: {str(e)}")
    
    logger.info(f"Estados actualizados para {updated_count} créditos")
    return updated_count

@shared_task
def calculate_periodic_installments():
    """Calcula campos basado en periodicidad del crédito"""
    from apps.fintech.models import Periodicity
    
    # Obtener periodicidades
    periodicities = Periodicity.objects.all()
    
    total_processed = 0
    for periodicity in periodicities:
        # Calcular cuotas que necesitan actualización según periodicidad
        if periodicity.days == 1:  # Diario
            days_back = 1
        elif periodicity.days == 7:  # Semanal
            days_back = 7
        elif periodicity.days == 30:  # Mensual
            days_back = 30
        else:
            days_back = periodicity.days
        
        # Cuotas de créditos con esta periodicidad que vencen en el rango
        installments = Installment.objects.filter(
            credit__periodicity=periodicity,
            due_date__gte=timezone.now().date() - timedelta(days=days_back),
            due_date__lte=timezone.now().date() + timedelta(days=days_back),
            status__in=['pending', 'partial']
        )
        
        processed_count = 0
        for installment in installments:
            try:
                InstallmentCalculator.clear_cache(installment.id)
                InstallmentCalculator.get_remaining_amount(installment)
                InstallmentCalculator.get_days_overdue(installment)
                InstallmentCalculator.get_late_fee(installment)
                processed_count += 1
                
            except Exception as e:
                logger.error(f"Error procesando cuota periódica {installment.id}: {str(e)}")
        
        total_processed += processed_count
        logger.info(f"Procesadas {processed_count} cuotas para periodicidad {periodicity.name}")
    
    logger.info(f"Total procesadas: {total_processed} cuotas por periodicidad")
    return total_processed

@shared_task
def clear_old_cache():
    """Limpia el cache completo de Django"""
    from django.core.cache import cache
    
    try:
        cache.clear()
        logger.info("Cache limpiado exitosamente")
        return True
    except Exception as e:
        logger.error(f"Error limpiando cache: {str(e)}")
        return False
