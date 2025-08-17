from django.db.models import Q, Count, Sum, Avg, Max, Min, F
from django.db.models.functions import TruncDate, TruncMonth, Extract
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal
from django.core.paginator import Paginator
from apps.fintech.models import Credit, Transaction, User, Installment
from apps.insights.models import FinancialControlMetrics, FinancialAlert, DefaultersReport
import logging

logger = logging.getLogger(__name__)

class FinancialControlService:
    """Servicio para control financiero y seguimiento de morosidad"""
    
    @staticmethod
    def calculate_user_financial_metrics(user):
        """Calcula las métricas financieras de un usuario"""
        try:
            # Obtener créditos del usuario
            user_credits = Credit.objects.filter(user=user)
            overdue_credits = user_credits.filter(is_in_default=True)
            
            # Calcular métricas básicas
            total_overdue_amount = overdue_credits.aggregate(
                total=Sum('pending_amount')
            )['total'] or Decimal('0.00')
            
            overdue_credits_count = overdue_credits.count()
            
            # Calcular días en mora
            days_in_default = 0
            max_days_overdue = 0
            
            if overdue_credits.exists():
                for credit in overdue_credits:
                    if credit.first_date_payment:
                        days_overdue = (timezone.now().date() - credit.first_date_payment).days
                        days_in_default = max(days_in_default, days_overdue)
                        max_days_overdue = max(max_days_overdue, days_overdue)
            
            # Calcular puntuación de riesgo
            risk_score = FinancialControlService._calculate_risk_score(
                total_overdue_amount, overdue_credits_count, days_in_default
            )
            
            # Determinar nivel de riesgo
            risk_level = FinancialControlService._determine_risk_level(risk_score)
            
            # Calcular métricas de comportamiento
            payment_frequency, avg_payment_delay = FinancialControlService._calculate_payment_behavior(user)
            
            # Crear o actualizar métricas
            metrics, created = FinancialControlMetrics.objects.get_or_create(
                user=user,
                defaults={
                    'total_overdue_amount': total_overdue_amount,
                    'overdue_credits_count': overdue_credits_count,
                    'days_in_default': days_in_default,
                    'max_days_overdue': max_days_overdue,
                    'risk_score': risk_score,
                    'risk_level': risk_level,
                    'payment_frequency': payment_frequency,
                    'avg_payment_delay': avg_payment_delay,
                    'default_history': FinancialControlService._get_default_history(user)
                }
            )
            
            if not created:
                # Actualizar métricas existentes
                metrics.total_overdue_amount = total_overdue_amount
                metrics.overdue_credits_count = overdue_credits_count
                metrics.days_in_default = days_in_default
                metrics.max_days_overdue = max_days_overdue
                metrics.risk_score = risk_score
                metrics.risk_level = risk_level
                metrics.payment_frequency = payment_frequency
                metrics.avg_payment_delay = avg_payment_delay
                metrics.default_history = FinancialControlService._get_default_history(user)
                metrics.save()
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating financial metrics for user {user.id}: {e}")
            return None
    
    @staticmethod
    def _calculate_risk_score(overdue_amount, overdue_count, days_in_default):
        """Calcula la puntuación de riesgo (0-100)"""
        try:
            # Factores de riesgo
            amount_factor = min(overdue_amount / 1000, 1.0) * 40  # Máximo 40 puntos por monto
            count_factor = min(overdue_count / 5, 1.0) * 30      # Máximo 30 puntos por cantidad
            days_factor = min(days_in_default / 90, 1.0) * 30    # Máximo 30 puntos por días
            
            risk_score = amount_factor + count_factor + days_factor
            return min(risk_score, 100)
        except Exception:
            return 0
    
    @staticmethod
    def _determine_risk_level(risk_score):
        """Determina el nivel de riesgo basado en la puntuación"""
        if risk_score >= 80:
            return 'critical'
        elif risk_score >= 60:
            return 'high'
        elif risk_score >= 30:
            return 'medium'
        else:
            return 'low'
    
    @staticmethod
    def _calculate_payment_behavior(user):
        """Calcula métricas de comportamiento de pagos"""
        try:
            # Obtener pagos del usuario
            payments = Transaction.objects.filter(
                user=user,
                transaction_type='income',
                status='confirmed'
            ).order_by('date')
            
            if not payments.exists():
                return Decimal('0.00'), Decimal('0.00')
            
            # Calcular frecuencia de pagos (por mes)
            first_payment = payments.first().date
            last_payment = payments.last().date
            months_diff = (last_payment.year - first_payment.year) * 12 + (last_payment.month - first_payment.month)
            months_diff = max(months_diff, 1)
            
            payment_frequency = payments.count() / months_diff
            
            # Calcular retraso promedio (simplificado)
            avg_payment_delay = Decimal('0.00')  # Implementar lógica más compleja si es necesario
            
            return Decimal(str(payment_frequency)), avg_payment_delay
            
        except Exception:
            return Decimal('0.00'), Decimal('0.00')
    
    @staticmethod
    def _get_default_history(user):
        """Obtiene el historial de morosidad del usuario"""
        try:
            history = []
            credits = Credit.objects.filter(user=user).order_by('-created_at')
            
            for credit in credits:
                if credit.is_in_default:
                    history.append({
                        'credit_id': str(credit.uid),
                        'amount': float(credit.pending_amount or 0),
                        'days_overdue': (timezone.now().date() - credit.first_date_payment).days if credit.first_date_payment else 0,
                        'default_date': credit.first_date_payment.isoformat() if credit.first_date_payment else None,
                        'morosidad_level': credit.morosidad_level
                    })
            
            return history
        except Exception:
            return []
    
    @staticmethod
    def get_defaulters_list(page=1, page_size=20, filters=None):
        """Obtiene lista paginada de clientes morosos"""
        try:
            # Aplicar filtros
            queryset = FinancialControlMetrics.objects.filter(
                overdue_credits_count__gt=0
            ).select_related('user').order_by('-risk_score', '-total_overdue_amount')
            
            if filters:
                if filters.get('risk_level'):
                    queryset = queryset.filter(risk_level=filters['risk_level'])
                
                if filters.get('min_overdue_amount'):
                    queryset = queryset.filter(
                        total_overdue_amount__gte=Decimal(filters['min_overdue_amount'])
                    )
                
                if filters.get('max_overdue_amount'):
                    queryset = queryset.filter(
                        total_overdue_amount__lte=Decimal(filters['max_overdue_amount'])
                    )
                
                if filters.get('min_days_overdue'):
                    queryset = queryset.filter(days_in_default__gte=int(filters['min_days_overdue']))
            
            # Paginación
            paginator = Paginator(queryset, page_size)
            page_obj = paginator.get_page(page)
            
            return {
                'results': list(page_obj),
                'pagination': {
                    'count': paginator.count,
                    'num_pages': paginator.num_pages,
                    'current_page': page_obj.number,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
                    'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting defaulters list: {e}")
            return {'results': [], 'pagination': {}}
    
    @staticmethod
    def create_financial_alert(user, alert_type, title, description, priority='medium', alert_data=None):
        """Crea una nueva alerta financiera"""
        try:
            alert = FinancialAlert.objects.create(
                user=user,
                alert_type=alert_type,
                title=title,
                description=description,
                priority=priority,
                alert_data=alert_data or {},
                expires_at=timezone.now() + timedelta(days=30)  # Expira en 30 días
            )
            
            logger.info(f"Financial alert created: {alert.id} for user {user.id}")
            return alert
            
        except Exception as e:
            logger.error(f"Error creating financial alert: {e}")
            return None
    
    @staticmethod
    def generate_defaulters_report(report_type='daily', generated_by=None):
        """Genera un reporte de clientes morosos"""
        try:
            # Calcular métricas del reporte
            metrics = FinancialControlMetrics.objects.filter(overdue_credits_count__gt=0)
            
            total_defaulters = metrics.count()
            total_overdue_amount = metrics.aggregate(
                total=Sum('total_overdue_amount')
            )['total'] or Decimal('0.00')
            
            avg_days_overdue = metrics.aggregate(
                avg=Avg('days_in_default')
            )['avg'] or Decimal('0.00')
            
            # Distribución por niveles de riesgo
            risk_distribution = metrics.values('risk_level').annotate(
                count=Count('id')
            )
            
            low_risk_count = next((item['count'] for item in risk_distribution if item['risk_level'] == 'low'), 0)
            medium_risk_count = next((item['count'] for item in risk_distribution if item['risk_level'] == 'medium'), 0)
            high_risk_count = next((item['count'] for item in risk_distribution if item['risk_level'] == 'high'), 0)
            critical_risk_count = next((item['count'] for item in risk_distribution if item['risk_level'] == 'critical'), 0)
            
            # Datos detallados de morosos
            defaulters_data = []
            for metric in metrics.select_related('user')[:100]:  # Limitar a 100 para el reporte
                defaulters_data.append({
                    'user_id': metric.user.id,
                    'username': metric.user.username,
                    'email': metric.user.email,
                    'total_overdue_amount': float(metric.total_overdue_amount),
                    'overdue_credits_count': metric.overdue_credits_count,
                    'days_in_default': metric.days_in_default,
                    'risk_level': metric.risk_level,
                    'risk_score': float(metric.risk_score)
                })
            
            # Crear reporte
            report = DefaultersReport.objects.create(
                report_type=report_type,
                total_defaulters=total_defaulters,
                total_overdue_amount=total_overdue_amount,
                avg_days_overdue=avg_days_overdue,
                low_risk_count=low_risk_count,
                medium_risk_count=medium_risk_count,
                high_risk_count=high_risk_count,
                critical_risk_count=critical_risk_count,
                defaulters_data=defaulters_data,
                risk_distribution=list(risk_distribution),
                recovery_potential=FinancialControlService._calculate_recovery_potential(metrics),
                generated_by=generated_by
            )
            
            logger.info(f"Defaulters report generated: {report.id}")
            return report
            
        except Exception as e:
            logger.error(f"Error generating defaulters report: {e}")
            return None
    
    @staticmethod
    def _calculate_recovery_potential(metrics_queryset):
        """Calcula el potencial de recuperación"""
        try:
            # Análisis de potencial de recuperación
            high_recovery_potential = metrics_queryset.filter(
                risk_level__in=['low', 'medium'],
                days_in_default__lte=30
            ).count()
            
            medium_recovery_potential = metrics_queryset.filter(
                risk_level='high',
                days_in_default__lte=60
            ).count()
            
            low_recovery_potential = metrics_queryset.filter(
                risk_level='critical',
                days_in_default__gt=90
            ).count()
            
            return {
                'high_potential': high_recovery_potential,
                'medium_potential': medium_recovery_potential,
                'low_potential': low_recovery_potential,
                'total_recoverable': high_recovery_potential + medium_recovery_potential
            }
            
        except Exception:
            return {}
    
    @staticmethod
    def get_financial_control_dashboard():
        """Obtiene datos para el dashboard de control financiero"""
        try:
            # Métricas generales
            total_metrics = FinancialControlMetrics.objects.count()
            active_defaulters = FinancialControlMetrics.objects.filter(
                overdue_credits_count__gt=0
            ).count()
            
            total_overdue_amount = FinancialControlMetrics.objects.aggregate(
                total=Sum('total_overdue_amount')
            )['total'] or Decimal('0.00')
            
            # Distribución por riesgo
            risk_distribution = FinancialControlMetrics.objects.values('risk_level').annotate(
                count=Count('id'),
                total_amount=Sum('total_overdue_amount')
            )
            
            # Alertas activas
            active_alerts = FinancialAlert.objects.filter(
                status='active'
            ).count()
            
            # Tendencias (últimos 30 días)
            thirty_days_ago = timezone.now() - timedelta(days=30)
            new_defaulters = FinancialControlMetrics.objects.filter(
                last_calculation__gte=thirty_days_ago,
                overdue_credits_count__gt=0
            ).count()
            
            return {
                'total_metrics': total_metrics,
                'active_defaulters': active_defaulters,
                'total_overdue_amount': total_overdue_amount,
                'risk_distribution': list(risk_distribution),
                'active_alerts': active_alerts,
                'new_defaulters_30_days': new_defaulters,
                'default_rate': (active_defaulters / total_metrics * 100) if total_metrics > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting financial control dashboard: {e}")
            return {}
