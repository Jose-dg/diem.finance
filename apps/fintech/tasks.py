import math
from celery import shared_task, group
from celery.utils.log import get_task_logger
from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from apps.fintech.models import Credit, Installment
from apps.fintech.utils import recalculate_credit
from apps.fintech.services.installment_service import InstallmentService
from apps.fintech.services.installment_calculator import InstallmentCalculator

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


@shared_task
def calculate_installment_fields_batch():
    """Calcula campos para cuotas que necesitan actualización"""
    print("🔄 Iniciando cálculo masivo de campos de cuotas...")
    
    today = timezone.now().date()
    
    # Cuotas que vencen hoy
    due_today = Installment.objects.filter(
        due_date=today,
        status='pending'
    )
    
    # Cuotas con más de 30 días de mora
    overdue_30 = Installment.objects.filter(
        due_date__lt=today - timedelta(days=30),
        status__in=['pending', 'partial']
    )
    
    # Cuotas con pagos parciales recientes
    recent_partials = Installment.objects.filter(
        status='partial',
        updated_at__gte=timezone.now() - timedelta(hours=24)
    )
    
    # Cuotas que necesitan recálculo según periodicidad
    needs_recalc = Installment.objects.filter(
        status='pending',
        updated_at__lt=timezone.now() - timedelta(hours=6)
    )
    
    # Combinar todas las cuotas que necesitan cálculo
    all_installments = (due_today | overdue_30 | recent_partials | needs_recalc).distinct()
    
    processed_count = 0
    for installment in all_installments:
        try:
            # Limpiar cache anterior
            InstallmentCalculator.clear_cache(installment.id)
            
            # Calcular campos (esto actualiza el cache)
            InstallmentCalculator.get_remaining_amount(installment)
            InstallmentCalculator.get_days_overdue(installment)
            InstallmentCalculator.get_late_fee(installment)
            
            processed_count += 1
            
        except Exception as e:
            print(f"❌ Error procesando cuota {installment.id}: {e}")
    
    print(f"✅ Procesadas {processed_count} cuotas")
    return processed_count


@shared_task
def calculate_overdue_installments():
    """Calcula campos para cuotas vencidas"""
    print("🔄 Calculando cuotas vencidas...")
    
    today = timezone.now().date()
    
    # Cuotas vencidas que necesitan actualización
    overdue_installments = Installment.objects.filter(
        due_date__lt=today,
        status__in=['pending', 'partial']
    )
    
    processed_count = 0
    for installment in overdue_installments:
        try:
            # Actualizar estado si es necesario
            days_overdue = InstallmentCalculator.get_days_overdue(installment)
            if days_overdue > 0 and installment.status == 'pending':
                installment.status = 'overdue'
                installment.save(update_fields=['status'])
            
            # Calcular campos
            InstallmentCalculator.get_late_fee(installment)
            InstallmentCalculator.get_total_amount_due(installment)
            
            processed_count += 1
            
        except Exception as e:
            print(f"❌ Error procesando cuota vencida {installment.id}: {e}")
    
    print(f"✅ Procesadas {processed_count} cuotas vencidas")
    return processed_count


@shared_task
def update_credit_statuses():
    """Actualiza el estado de todos los créditos"""
    print("🔄 Actualizando estados de créditos...")
    
    # Créditos con cuotas que necesitan actualización
    credits_to_update = Credit.objects.filter(
        installments__status__in=['pending', 'overdue', 'partial']
    ).distinct()
    
    processed_count = 0
    for credit in credits_to_update:
        try:
            InstallmentCalculator.update_credit_status(credit)
            processed_count += 1
            
        except Exception as e:
            print(f"❌ Error actualizando crédito {credit.id}: {e}")
    
    print(f"✅ Actualizados {processed_count} créditos")
    return processed_count


@shared_task
def calculate_periodic_installments():
    """Calcula campos según periodicidad del crédito"""
    print("🔄 Calculando cuotas por periodicidad...")
    
    today = timezone.now().date()
    
    # Cuotas diarias (periodicidad <= 7 días)
    daily_installments = Installment.objects.filter(
        credit__periodicity__days__lte=7,
        status='pending',
        due_date__lte=today + timedelta(days=7)
    )
    
    # Cuotas semanales (periodicidad 14-15 días)
    weekly_installments = Installment.objects.filter(
        credit__periodicity__days__in=[14, 15],
        status='pending',
        due_date__lte=today + timedelta(days=14)
    )
    
    # Cuotas mensuales (periodicidad >= 28 días)
    monthly_installments = Installment.objects.filter(
        credit__periodicity__days__gte=28,
        status='pending',
        due_date__lte=today + timedelta(days=30)
    )
    
    all_installments = (daily_installments | weekly_installments | monthly_installments).distinct()
    
    processed_count = 0
    for installment in all_installments:
        try:
            # Limpiar cache y recalcular
            InstallmentCalculator.clear_cache(installment.id)
            InstallmentCalculator.get_remaining_amount(installment)
            InstallmentCalculator.get_days_overdue(installment)
            InstallmentCalculator.get_late_fee(installment)
            
            processed_count += 1
            
        except Exception as e:
            print(f"❌ Error procesando cuota periódica {installment.id}: {e}")
    
    print(f"✅ Procesadas {processed_count} cuotas por periodicidad")
    return processed_count


@shared_task
def clear_old_cache():
    """Limpia cache antiguo"""
    print("🧹 Limpiando cache antiguo...")
    
    # Esta tarea se ejecuta para limpiar cache que ya no se necesita
    # Django cache tiene expiración automática, pero podemos forzar limpieza
    
    from django.core.cache import cache
    cache.clear()
    
    print("✅ Cache limpiado")
    return True
