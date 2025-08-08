from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
import logging

from apps.fintech.models import Credit, Transaction, AccountMethodAmount
from apps.revenue.models import CreditEarnings
from .models import CreditPrediction, SeasonalPattern, RiskAssessment
from .services import PredictionService, RiskService

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Credit)
def credit_saved_handler(sender, instance, created, **kwargs):
    """
    Maneja cambios en créditos para actualizar predicciones y evaluaciones de riesgo.
    """
    try:
        if created:
            # Nuevo crédito - crear predicciones iniciales
            logger.info(f"Nuevo crédito creado: {instance.uid}")
            # Las predicciones se crearán de forma asíncrona
            
        else:
            # Crédito actualizado - invalidar predicciones existentes
            CreditPrediction.objects.filter(
                credit=instance,
                expires_at__gt=timezone.now()
            ).update(expires_at=timezone.now())
            
            logger.info(f"Predicciones invalidadas para crédito: {instance.uid}")
            
    except Exception as e:
        logger.error(f"Error en credit_saved_handler: {e}")

@receiver(post_save, sender=Transaction)
def transaction_saved_handler(sender, instance, created, **kwargs):
    """
    Maneja cambios en transacciones para actualizar predicciones relacionadas.
    """
    try:
        if created and instance.transaction_type == 'income' and instance.status == 'confirmed':
            # Nueva transacción de ingreso confirmada
            related_credits = AccountMethodAmount.objects.filter(
                transaction=instance
            ).values_list('credit_id', flat=True)
            
            for credit_id in related_credits:
                # Invalidar predicciones de fecha de pago y monto
                CreditPrediction.objects.filter(
                    credit_id=credit_id,
                    prediction_type__in=['payment_date', 'payment_amount'],
                    expires_at__gt=timezone.now()
                ).update(expires_at=timezone.now())
                
            logger.info(f"Predicciones actualizadas por nueva transacción: {instance.id}")
            
    except Exception as e:
        logger.error(f"Error en transaction_saved_handler: {e}")

@receiver(post_save, sender=AccountMethodAmount)
def account_method_amount_saved_handler(sender, instance, created, **kwargs):
    """
    Maneja cambios en montos de métodos de cuenta para actualizar predicciones.
    """
    try:
        if created:
            # Nuevo pago registrado
            credit = instance.credit
            if credit:
                # Invalidar predicciones de pago relacionadas
                CreditPrediction.objects.filter(
                    credit=credit,
                    prediction_type__in=['payment_date', 'payment_amount', 'completion_date'],
                    expires_at__gt=timezone.now()
                ).update(expires_at=timezone.now())
                
                logger.info(f"Predicciones actualizadas por nuevo pago: {credit.uid}")
                
    except Exception as e:
        logger.error(f"Error en account_method_amount_saved_handler: {e}")

@receiver(post_save, sender=CreditEarnings)
def credit_earnings_saved_handler(sender, instance, created, **kwargs):
    """
    Maneja cambios en ganancias de créditos para actualizar análisis de tendencias.
    """
    try:
        if created or instance.updated_at:
            # Ganancias actualizadas - podría afectar análisis de tendencias
            logger.info(f"Ganancias actualizadas para crédito: {instance.credit.uid}")
            # Los análisis de tendencias se actualizarán de forma asíncrona
            
    except Exception as e:
        logger.error(f"Error en credit_earnings_saved_handler: {e}")

@receiver(post_delete, sender=CreditPrediction)
def prediction_deleted_handler(sender, instance, **kwargs):
    """
    Maneja eliminación de predicciones.
    """
    try:
        logger.info(f"Predicción eliminada: {instance.id} para crédito {instance.credit.uid}")
        
    except Exception as e:
        logger.error(f"Error en prediction_deleted_handler: {e}")

@receiver(post_delete, sender=SeasonalPattern)
def seasonal_pattern_deleted_handler(sender, instance, **kwargs):
    """
    Maneja eliminación de patrones estacionales.
    """
    try:
        logger.info(f"Patrón estacional eliminado: {instance.id}")
        
    except Exception as e:
        logger.error(f"Error en seasonal_pattern_deleted_handler: {e}")

@receiver(post_delete, sender=RiskAssessment)
def risk_assessment_deleted_handler(sender, instance, **kwargs):
    """
    Maneja eliminación de evaluaciones de riesgo.
    """
    try:
        logger.info(f"Evaluación de riesgo eliminada: {instance.id}")
        
    except Exception as e:
        logger.error(f"Error en risk_assessment_deleted_handler: {e}") 