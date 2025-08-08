from celery import shared_task
from django.utils import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal
import logging
from datetime import timedelta, date

from apps.fintech.models import Credit
from .services import PredictionService, SeasonalService, RiskService
from .models import CreditPrediction, SeasonalPattern, RiskAssessment

logger = logging.getLogger(__name__)

@shared_task(bind=True, retry_backoff=True, acks_late=True)
def generate_credit_predictions(self, credit_id: str = None):
    """
    Genera predicciones para créditos.
    """
    try:
        if credit_id:
            # Predicción para un crédito específico
            credit = Credit.objects.get(uid=credit_id)
            credits = [credit]
        else:
            # Predicciones para todos los créditos activos
            credits = Credit.objects.filter(pending_amount__gt=0)
        
        predictions_created = 0
        
        for credit in credits:
            try:
                # Crear predicciones para diferentes tipos
                prediction_types = ['payment_date', 'completion_date', 'default_risk', 'payment_amount']
                
                for pred_type in prediction_types:
                    # Verificar si ya existe una predicción reciente
                    existing_prediction = CreditPrediction.objects.filter(
                        credit=credit,
                        prediction_type=pred_type,
                        expires_at__gt=timezone.now()
                    ).first()
                    
                    if not existing_prediction:
                        PredictionService.create_credit_prediction(
                            credit=credit,
                            prediction_type=pred_type
                        )
                        predictions_created += 1
                
            except Exception as e:
                logger.error(f"Error generating predictions for credit {credit.uid}: {e}")
                continue
        
        logger.info(f"Predicciones generadas: {predictions_created}")
        return predictions_created
        
    except Exception as e:
        logger.error(f"Error in generate_credit_predictions task: {e}")
        raise self.retry(exc=e, countdown=60)

@shared_task(bind=True, retry_backoff=True, acks_late=True)
def identify_seasonal_patterns(self, pattern_type: str = None, months_back: int = 12):
    """
    Identifica patrones estacionales en los datos.
    """
    try:
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=months_back * 30)
        
        if pattern_type:
            pattern_types = [pattern_type]
        else:
            pattern_types = ['monthly', 'quarterly', 'weekly']
        
        patterns_created = 0
        
        for pattern_type in pattern_types:
            try:
                if pattern_type == 'monthly':
                    SeasonalService.identify_monthly_patterns(start_date, end_date, 'payments')
                    SeasonalService.identify_monthly_patterns(start_date, end_date, 'credits')
                elif pattern_type == 'quarterly':
                    SeasonalService.identify_quarterly_patterns(start_date, end_date, 'payments')
                    SeasonalService.identify_quarterly_patterns(start_date, end_date, 'credits')
                elif pattern_type == 'weekly':
                    SeasonalService.identify_weekly_patterns(start_date, end_date, 'payments')
                    SeasonalService.identify_weekly_patterns(start_date, end_date, 'credits')
                
                patterns_created += 2  # 2 por tipo (payments y credits)
                
            except ValidationError as e:
                logger.warning(f"No se pudo identificar patrón {pattern_type}: {e}")
                continue
            except Exception as e:
                logger.error(f"Error identifying pattern {pattern_type}: {e}")
                continue
        
        logger.info(f"Patrones estacionales identificados: {patterns_created}")
        return patterns_created
        
    except Exception as e:
        logger.error(f"Error in identify_seasonal_patterns task: {e}")
        raise self.retry(exc=e, countdown=180)

@shared_task(bind=True, retry_backoff=True, acks_late=True)
def assess_risks(self, risk_type: str = None):
    """
    Evalúa riesgos en la cartera.
    """
    try:
        if risk_type:
            risk_types = [risk_type]
        else:
            risk_types = ['credit_default', 'portfolio_concentration', 'liquidity_risk']
        
        assessments_created = 0
        
        for risk_type in risk_types:
            try:
                if risk_type == 'credit_default':
                    # Evaluar riesgos de créditos individuales
                    credits = Credit.objects.filter(pending_amount__gt=0)
                    for credit in credits[:100]:  # Limitar a 100 para evitar sobrecarga
                        RiskService.assess_credit_default_risk(credit)
                        assessments_created += 1
                
                elif risk_type == 'portfolio_concentration':
                    RiskService.assess_portfolio_concentration_risk()
                    assessments_created += 1
                
                elif risk_type == 'liquidity_risk':
                    RiskService.assess_liquidity_risk()
                    assessments_created += 1
                
            except Exception as e:
                logger.error(f"Error assessing risk {risk_type}: {e}")
                continue
        
        logger.info(f"Evaluaciones de riesgo creadas: {assessments_created}")
        return assessments_created
        
    except Exception as e:
        logger.error(f"Error in assess_risks task: {e}")
        raise self.retry(exc=e, countdown=300)

@shared_task(bind=True, retry_backoff=True, acks_late=True)
def cleanup_forecasting_data(self):
    """
    Limpia datos antiguos de forecasting.
    """
    try:
        # Limpiar predicciones expiradas
        expired_predictions = PredictionService.cleanup_expired_predictions()
        
        # Limpiar patrones antiguos
        old_patterns = SeasonalService.cleanup_old_patterns()
        
        # Limpiar evaluaciones expiradas
        expired_assessments = RiskService.cleanup_expired_assessments()
        
        total_cleaned = expired_predictions + old_patterns + expired_assessments
        
        logger.info(f"Datos de forecasting limpiados: {total_cleaned}")
        return {
            'expired_predictions': expired_predictions,
            'old_patterns': old_patterns,
            'expired_assessments': expired_assessments,
            'total': total_cleaned
        }
        
    except Exception as e:
        logger.error(f"Error in cleanup_forecasting_data task: {e}")
        raise self.retry(exc=e, countdown=600)

@shared_task(bind=True, retry_backoff=True, acks_late=True)
def generate_forecasting_report(self, report_type: str = 'comprehensive'):
    """
    Genera reportes de forecasting.
    """
    try:
        report_data = {
            'generated_at': timezone.now().isoformat(),
            'report_type': report_type
        }
        
        if report_type in ['comprehensive', 'predictions']:
            # Reporte de predicciones
            active_predictions = PredictionService.get_active_predictions()
            report_data['predictions'] = {
                'total_active': len(active_predictions),
                'by_type': {}
            }
            
            for pred in active_predictions:
                pred_type = pred.prediction_type
                if pred_type not in report_data['predictions']['by_type']:
                    report_data['predictions']['by_type'][pred_type] = 0
                report_data['predictions']['by_type'][pred_type] += 1
        
        if report_type in ['comprehensive', 'patterns']:
            # Reporte de patrones
            active_patterns = SeasonalService.get_active_patterns()
            report_data['patterns'] = {
                'total_active': len(active_patterns),
                'by_type': {}
            }
            
            for pattern in active_patterns:
                pattern_type = pattern.pattern_type
                if pattern_type not in report_data['patterns']['by_type']:
                    report_data['patterns']['by_type'][pattern_type] = 0
                report_data['patterns']['by_type'][pattern_type] += 1
        
        if report_type in ['comprehensive', 'risks']:
            # Reporte de riesgos
            active_risks = RiskService.get_active_assessments()
            report_data['risks'] = {
                'total_active': len(active_risks),
                'by_level': {}
            }
            
            for risk in active_risks:
                level = risk.risk_level
                if level not in report_data['risks']['by_level']:
                    report_data['risks']['by_level'][level] = 0
                report_data['risks']['by_level'][level] += 1
        
        logger.info(f"Reporte de forecasting generado: {report_type}")
        return report_data
        
    except Exception as e:
        logger.error(f"Error in generate_forecasting_report task: {e}")
        raise self.retry(exc=e, countdown=120) 