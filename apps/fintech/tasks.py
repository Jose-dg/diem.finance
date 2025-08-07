import math
from celery import shared_task, group
from celery.utils.log import get_task_logger
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from django.db.models import F, Q
from decimal import Decimal

from apps.fintech.models import Credit, Installment, Transaction, AccountMethodAmount
from apps.fintech.utils.root import recalculate_credit
from apps.fintech.services.installment_service import InstallmentService
from apps.fintech.services.credit_service import CreditService
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

    processed_count = 0
    error_count = 0

    # Actualizar estados de cuotas primero
    try:
        success, message = InstallmentService.update_all_installment_statuses()
        logger.info(f"Actualización de cuotas: {message}")
    except Exception as e:
        logger.error(f"Error actualizando estados de cuotas: {str(e)}")

    # Iteración secuencial en chunks con manejo de errores
    for credit in Credit.objects.iterator(chunk_size=chunk_size):
        try:
            with transaction.atomic():
                # Recalcular crédito usando el servicio robusto
                success, result = CreditService.update_credit_status(credit)
                
                if success:
                    processed_count += 1
                    logger.info(f"Crédito {credit.uid} actualizado exitosamente")
                else:
                    error_count += 1
                    logger.error(f"Error actualizando crédito {credit.uid}: {result}")
                    
        except Exception as e:
            error_count += 1
            logger.error(f"Error procesando crédito {credit.uid}: {str(e)}")
    
    logger.info(f"Procesamiento completado. Exitosos: {processed_count}, Errores: {error_count}")
    return {
        'total': total,
        'processed': processed_count,
        'errors': error_count
    }

@shared_task(
    bind=True,
    name="fintech.update_installment_statuses",
)
def update_installment_statuses(self):
    """
    Actualiza el estado de todas las cuotas pendientes usando el servicio robusto
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
    Envía notificaciones de cuotas vencidas usando el sistema de notificaciones
    """
    try:
        # Obtener cuotas vencidas
        overdue_installments = Installment.objects.filter(
            status='overdue',
            notification_sent=False
        ).select_related('credit', 'credit__user')
        
        notification_count = 0
        
        for installment in overdue_installments:
            try:
                # Crear notificación usando el sistema robusto
                from apps.notifications.services import NotificationService
                
                success = NotificationService.create_notification(
                    installment.credit.user,
                    'overdue_installment',
                    {
                        'installment_number': installment.number,
                        'amount': float(installment.amount),
                        'days_overdue': installment.days_overdue,
                        'credit_id': str(installment.credit.uid),
                        'due_date': installment.due_date.strftime('%Y-%m-%d') if installment.due_date else None
                    },
                    priority='high',
                    channels='email,web'
                )
                
                if success:
                    installment.notification_sent = True
                    installment.save(update_fields=['notification_sent'])
                    notification_count += 1
                    
            except Exception as e:
                logger.error(f"Error enviando notificación para cuota {installment.id}: {str(e)}")
        
        logger.info(f"Notificaciones de mora enviadas: {notification_count}")
        return notification_count
        
    except Exception as e:
        logger.error(f"Error enviando notificaciones de mora: {str(e)}")
        return 0

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
                success, message = InstallmentService.generate_installments_for_credit(credit)
                if success:
                    count += 1
                    logger.info(f"Cuotas generadas para crédito {credit.uid}: {message}")
                else:
                    logger.error(f"Error generando cuotas para crédito {credit.uid}: {message}")
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
    Mantenimiento diario de cuotas - TAREA PRINCIPAL OPTIMIZADA
    """
    try:
        logger.info("Iniciando mantenimiento diario de cuotas...")
        
        results = {}
        
        # 1. Actualizar estados de cuotas
        try:
            success, message = InstallmentService.update_all_installment_statuses()
            results['installment_statuses'] = {'success': success, 'message': message}
            logger.info(f"Estados actualizados: {message}")
        except Exception as e:
            results['installment_statuses'] = {'success': False, 'error': str(e)}
            logger.error(f"Error actualizando estados: {str(e)}")
        
        # 2. Enviar recordatorios
        try:
            success, message = InstallmentService.schedule_payment_reminders()
            results['payment_reminders'] = {'success': success, 'message': message}
            logger.info(f"Recordatorios enviados: {message}")
        except Exception as e:
            results['payment_reminders'] = {'success': False, 'error': str(e)}
            logger.error(f"Error enviando recordatorios: {str(e)}")
        
        # 3. Notificaciones de mora
        try:
            count = send_overdue_notifications.delay()
            results['overdue_notifications'] = {'count': count}
            logger.info(f"Notificaciones enviadas: {count}")
        except Exception as e:
            results['overdue_notifications'] = {'error': str(e)}
            logger.error(f"Error enviando notificaciones: {str(e)}")
        
        # 4. Generar cuotas para créditos nuevos
        try:
            count = generate_installments_for_new_credits.delay()
            results['new_installments'] = {'count': count}
            logger.info(f"Cuotas generadas: {count}")
        except Exception as e:
            results['new_installments'] = {'error': str(e)}
            logger.error(f"Error generando cuotas: {str(e)}")
        
        logger.info("Mantenimiento diario completado exitosamente")
        return results
        
    except Exception as e:
        logger.error(f"Error en mantenimiento diario: {str(e)}")
        return {'error': str(e)}

@shared_task
def check_additional_interest_daily():
    """
    Verifica diariamente créditos que necesitan interés adicional - OPTIMIZADO
    """
    try:
        # Créditos activos con pagos parciales que no han recibido interés adicional
        credits_with_partial_payments = Credit.objects.filter(
            total_abonos__lt=F('price'),
            state__in=['pending', 'completed'],
            is_in_default=False  # Solo créditos no en mora
        ).exclude(
            adjustments__type__code='C0001'  # Excluir los que ya tienen interés adicional
        ).select_related('user')
        
        applied_count = 0
        for credit in credits_with_partial_payments:
            try:
                # Verificar si debe aplicar interés adicional usando el servicio
                if CreditAdjustmentService.should_apply_additional_interest(credit):
                    amount = CreditAdjustmentService.apply_additional_interest(
                        credit,
                        reason=f"Verificación diaria: Total pagado {credit.total_abonos} < Total pactado {credit.price}"
                    )
                    if amount > 0:
                        applied_count += 1
                        logger.info(f"Interés adicional aplicado a crédito {credit.uid}: ${amount}")
                        
                        # Crear notificación para el administrador
                        try:
                            from apps.notifications.services import NotificationService
                            from apps.fintech.models import User
                            
                            admin_users = User.objects.filter(is_staff=True)
                            NotificationService.send_bulk_notifications(
                                admin_users,
                                'additional_interest',
                                {
                                    'credit_id': str(credit.uid),
                                    'user_name': credit.user.get_full_name(),
                                    'amount': float(amount),
                                    'reason': f"Verificación diaria: Total pagado {credit.total_abonos} < Total pactado {credit.price}"
                                },
                                priority='high'
                            )
                        except Exception as e:
                            logger.error(f"Error enviando notificación de interés adicional: {str(e)}")
                        
            except Exception as e:
                logger.error(f"Error aplicando interés adicional a crédito {credit.uid}: {str(e)}")
        
        logger.info(f"Verificación diaria completada. Interés aplicado a {applied_count} créditos")
        return applied_count
        
    except Exception as e:
        logger.error(f"Error en verificación diaria de interés adicional: {str(e)}")
        return 0

@shared_task
def calculate_installment_fields_batch():
    """Calcula campos para cuotas que necesitan actualización - OPTIMIZADO"""
    from django.conf import settings
    
    # Identificar cuotas que necesitan recálculo
    today = timezone.now().date()
    
    # 1. Cuotas que vencen hoy y están pendientes
    due_today = Installment.objects.filter(
        due_date=today,
        status='pending'
    )
    
    # 2. Cuotas con mora alta (30+ días)
    overdue_30_plus = Installment.objects.filter(
        status__in=['pending', 'partial'],
        due_date__lt=today - timedelta(days=30)
    )
    
    # 3. Cuotas con pagos parciales recientes
    recent_partial = Installment.objects.filter(
        status='partial',
        updated_at__gte=timezone.now() - timedelta(hours=24)
    )
    
    # 4. Cuotas que necesitan recálculo general
    pending_installments = Installment.objects.filter(
        status__in=['pending', 'partial']
    )
    
    # Combinar todas las cuotas únicas
    all_installments = list(set(list(due_today) + list(overdue_30_plus) + list(recent_partial) + list(pending_installments)))
    
    # Procesar en lotes
    processed_count = 0
    for installment in all_installments:
        try:
            with transaction.atomic():
                # Recalcular campos usando el servicio
                success, message = InstallmentService.update_installment_calculations(installment)
                
                if success:
                    processed_count += 1
                else:
                    logger.error(f"Error procesando cuota {installment.id}: {message}")
                    
        except Exception as e:
            logger.error(f"Error procesando cuota {installment.id}: {str(e)}")
    
    logger.info(f"Procesadas {processed_count} cuotas de {len(all_installments)} identificadas")
    return processed_count

@shared_task
def calculate_overdue_installments():
    """Actualiza cuotas vencidas y calcula mora - OPTIMIZADO"""
    today = timezone.now().date()
    
    # Cuotas vencidas que no están marcadas como overdue
    overdue_installments = Installment.objects.filter(
        due_date__lt=today,
        status__in=['pending', 'partial']
    ).select_related('credit')
    
    updated_count = 0
    for installment in overdue_installments:
        try:
            with transaction.atomic():
                # Actualizar estado usando el servicio
                success, message = InstallmentService.mark_installment_overdue(installment)
                
                if success:
                    updated_count += 1
                    logger.info(f"Cuota {installment.id} marcada como vencida")
                else:
                    logger.error(f"Error actualizando cuota {installment.id}: {message}")
                    
        except Exception as e:
            logger.error(f"Error actualizando cuota vencida {installment.id}: {str(e)}")
    
    logger.info(f"Actualizadas {updated_count} cuotas vencidas")
    return updated_count

@shared_task
def update_credit_statuses():
    """Actualiza estados de créditos basado en sus cuotas - OPTIMIZADO"""
    credits_with_installments = Credit.objects.filter(
        installments__isnull=False
    ).distinct()
    
    updated_count = 0
    for credit in credits_with_installments:
        try:
            with transaction.atomic():
                # Usar el servicio robusto para actualizar estado
                success, message = CreditService.update_credit_status(credit)
                
                if success:
                    updated_count += 1
                    logger.info(f"Estado actualizado para crédito {credit.uid}")
                else:
                    logger.error(f"Error actualizando crédito {credit.uid}: {message}")
                    
        except Exception as e:
            logger.error(f"Error actualizando estado de crédito {credit.uid}: {str(e)}")
    
    logger.info(f"Estados actualizados para {updated_count} créditos")
    return updated_count

@shared_task
def calculate_periodic_installments():
    """Calcula campos basado en periodicidad del crédito - OPTIMIZADO"""
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
                with transaction.atomic():
                    # Usar el servicio para recalcular
                    success, message = InstallmentService.update_installment_calculations(installment)
                    
                    if success:
                        processed_count += 1
                    else:
                        logger.error(f"Error procesando cuota periódica {installment.id}: {message}")
                        
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

@shared_task
def reconcile_payments():
    """
    Tarea para conciliar pagos y verificar inconsistencias
    """
    try:
        # Buscar transacciones de pago que no tienen AccountMethodAmount
        orphan_transactions = Transaction.objects.filter(
            transaction_type='income',
            status='confirmed'
        ).exclude(
            account_method_amounts__isnull=False
        )
        
        reconciled_count = 0
        for transaction in orphan_transactions:
            try:
                with transaction.atomic():
                    # Intentar reconciliar la transacción
                    success, message = CreditService.reconcile_transaction(transaction)
                    
                    if success:
                        reconciled_count += 1
                        logger.info(f"Transacción {transaction.uid} reconciliada")
                    else:
                        logger.error(f"Error reconciliando transacción {transaction.uid}: {message}")
                        
            except Exception as e:
                logger.error(f"Error reconciliando transacción {transaction.uid}: {str(e)}")
        
        logger.info(f"Reconciliación completada. {reconciled_count} transacciones reconciliadas")
        return reconciled_count
        
    except Exception as e:
        logger.error(f"Error en reconciliación de pagos: {str(e)}")
        return 0
