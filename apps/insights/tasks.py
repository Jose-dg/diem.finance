from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging

from apps.insights.services.financial_control_service import FinancialControlService
from apps.fintech.models import User

logger = logging.getLogger(__name__)

@shared_task
def calculate_all_financial_metrics():
    """Calcula métricas financieras para todos los usuarios"""
    try:
        users = User.objects.all()
        processed_count = 0
        error_count = 0
        
        for user in users:
            try:
                FinancialControlService.calculate_user_financial_metrics(user)
                processed_count += 1
            except Exception as e:
                logger.error(f"Error calculating metrics for user {user.id}: {e}")
                error_count += 1
        
        logger.info(f"Financial metrics calculation completed. Processed: {processed_count}, Errors: {error_count}")
        return {
            'processed': processed_count,
            'errors': error_count,
            'total': users.count()
        }
    except Exception as e:
        logger.error(f"Error in calculate_all_financial_metrics: {e}")
        return {'error': str(e)}

@shared_task
def generate_daily_defaulters_report():
    """Genera reporte diario de morosos"""
    try:
        report = FinancialControlService.generate_defaulters_report(
            report_type='daily',
            generated_by=None  # Sistema automático
        )
        
        if report:
            logger.info(f"Daily defaulters report generated: {report.id}")
            return {'report_id': report.id, 'status': 'success'}
        else:
            logger.error("Failed to generate daily defaulters report")
            return {'status': 'error', 'message': 'Failed to generate report'}
            
    except Exception as e:
        logger.error(f"Error generating daily defaulters report: {e}")
        return {'status': 'error', 'message': str(e)}

@shared_task
def generate_weekly_defaulters_report():
    """Genera reporte semanal de morosos"""
    try:
        report = FinancialControlService.generate_defaulters_report(
            report_type='weekly',
            generated_by=None  # Sistema automático
        )
        
        if report:
            logger.info(f"Weekly defaulters report generated: {report.id}")
            return {'report_id': report.id, 'status': 'success'}
        else:
            logger.error("Failed to generate weekly defaulters report")
            return {'status': 'error', 'message': 'Failed to generate report'}
            
    except Exception as e:
        logger.error(f"Error generating weekly defaulters report: {e}")
        return {'status': 'error', 'message': str(e)}

@shared_task
def generate_monthly_defaulters_report():
    """Genera reporte mensual de morosos"""
    try:
        report = FinancialControlService.generate_defaulters_report(
            report_type='monthly',
            generated_by=None  # Sistema automático
        )
        
        if report:
            logger.info(f"Monthly defaulters report generated: {report.id}")
            return {'report_id': report.id, 'status': 'success'}
        else:
            logger.error("Failed to generate monthly defaulters report")
            return {'status': 'error', 'message': 'Failed to generate report'}
            
    except Exception as e:
        logger.error(f"Error generating monthly defaulters report: {e}")
        return {'status': 'error', 'message': str(e)}

@shared_task
def cleanup_expired_alerts():
    """Limpia alertas expiradas"""
    try:
        from apps.insights.models import FinancialAlert
        
        # Marcar alertas expiradas como expiradas
        expired_alerts = FinancialAlert.objects.filter(
            status='active',
            expires_at__lt=timezone.now()
        )
        
        expired_count = expired_alerts.count()
        expired_alerts.update(status='expired')
        
        logger.info(f"Cleaned up {expired_count} expired alerts")
        return {'expired_count': expired_count, 'status': 'success'}
        
    except Exception as e:
        logger.error(f"Error cleaning up expired alerts: {e}")
        return {'status': 'error', 'message': str(e)}

@shared_task
def create_high_risk_alerts():
    """Crea alertas automáticas para usuarios de alto riesgo"""
    try:
        from apps.insights.models import FinancialControlMetrics, FinancialAlert
        
        # Buscar usuarios de alto riesgo sin alertas activas recientes
        high_risk_users = FinancialControlMetrics.objects.filter(
            risk_level__in=['high', 'critical'],
            total_overdue_amount__gt=0
        ).select_related('user')
        
        created_count = 0
        
        for metrics in high_risk_users:
            # Verificar si ya existe una alerta activa reciente
            recent_alert = FinancialAlert.objects.filter(
                user=metrics.user,
                alert_type='risk_increase',
                status='active',
                created_at__gte=timezone.now() - timedelta(days=7)
            ).exists()
            
            if not recent_alert:
                # Crear alerta
                alert = FinancialControlService.create_financial_alert(
                    user=metrics.user,
                    alert_type='risk_increase',
                    title=f"Usuario de alto riesgo: {metrics.user.username}",
                    description=f"El usuario tiene un nivel de riesgo {metrics.risk_level} con ${metrics.total_overdue_amount} en mora",
                    priority='high' if metrics.risk_level == 'high' else 'urgent',
                    alert_data={
                        'risk_score': float(metrics.risk_score),
                        'overdue_amount': float(metrics.total_overdue_amount),
                        'days_in_default': metrics.days_in_default
                    }
                )
                
                if alert:
                    created_count += 1
        
        logger.info(f"Created {created_count} high-risk alerts")
        return {'created_count': created_count, 'status': 'success'}
        
    except Exception as e:
        logger.error(f"Error creating high-risk alerts: {e}")
        return {'status': 'error', 'message': str(e)}

@shared_task
def update_financial_control_dashboard():
    """Actualiza el dashboard de control financiero"""
    try:
        # Esta tarea puede ser usada para actualizar métricas en tiempo real
        # o para generar cache del dashboard
        
        dashboard_data = FinancialControlService.get_financial_control_dashboard()
        
        logger.info("Financial control dashboard updated")
        return {'status': 'success', 'data': dashboard_data}
        
    except Exception as e:
        logger.error(f"Error updating financial control dashboard: {e}")
        return {'status': 'error', 'message': str(e)} 