from django.db.models import Q, Count, Sum, Avg, Max, Min
from django.db.models.functions import TruncDate, TruncMonth, TruncYear, Extract
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal
from apps.fintech.models import Credit, Transaction, User, Installment, Expense, Seller
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Servicio de analytics avanzado para insights - Independiente de modelos de insights"""
    
    @staticmethod
    def get_portfolio_overview():
        """Vista general del portafolio de créditos"""
        try:
            total_credits = Credit.objects.count()
            active_credits = Credit.objects.filter(state='completed').count()
            pending_credits = Credit.objects.filter(state='pending').count()
            
            total_portfolio_value = Credit.objects.filter(
                state='completed'
            ).aggregate(
                total=Sum('price')
            )['total'] or Decimal('0.00')
            
            total_pending_amount = Credit.objects.filter(
                state='completed'
            ).aggregate(
                total=Sum('pending_amount')
            )['total'] or Decimal('0.00')
            
            avg_credit_amount = Credit.objects.filter(
                state='completed'
            ).aggregate(
                avg=Avg('price')
            )['avg'] or Decimal('0.00')
            
            return {
                'total_credits': total_credits,
                'active_credits': active_credits,
                'pending_credits': pending_credits,
                'total_portfolio_value': total_portfolio_value,
                'total_pending_amount': total_pending_amount,
                'avg_credit_amount': avg_credit_amount,
                'collection_rate': ((total_portfolio_value - total_pending_amount) / total_portfolio_value * 100) if total_portfolio_value > 0 else 0
            }
        except Exception as e:
            logger.error(f"Error getting portfolio overview: {e}")
            return {}
    
    @staticmethod
    def get_credit_performance_metrics(days=30):
        """Métricas de rendimiento de créditos"""
        try:
            start_date = timezone.now() - timedelta(days=days)
            
            # Créditos por estado
            credits_by_status = Credit.objects.filter(
                created_at__gte=start_date
            ).values('state').annotate(
                count=Count('id'),
                total_amount=Sum('price')
            )
            
            # Créditos por categoría
            credits_by_category = Credit.objects.filter(
                created_at__gte=start_date
            ).values(
                'subcategory__name'
            ).annotate(
                count=Count('id'),
                total_amount=Sum('price'),
                avg_amount=Avg('price')
            ).order_by('-total_amount')
            
            # Tendencias temporales
            daily_credits = Credit.objects.filter(
                created_at__gte=start_date
            ).annotate(
                date=TruncDate('created_at')
            ).values('date').annotate(
                count=Count('id'),
                total_amount=Sum('price')
            ).order_by('date')
            
            return {
                'credits_by_status': list(credits_by_status),
                'credits_by_category': list(credits_by_category),
                'daily_trends': list(daily_credits),
                'period_days': days
            }
        except Exception as e:
            logger.error(f"Error getting credit performance metrics: {e}")
            return {}
    
    @staticmethod
    def get_user_behavior_analytics():
        """Analytics de comportamiento de usuarios"""
        try:
            # Usuarios más activos
            active_users = User.objects.annotate(
                credit_count=Count('credits'),
                transaction_count=Count('transactions'),
                total_credit_amount=Sum('credits__price'),
                last_activity=Max('credits__created_at')
            ).filter(
                credit_count__gt=0
            ).order_by('-total_credit_amount')[:10]
            
            # Segmentación por valor
            user_segments = User.objects.annotate(
                total_credit_amount=Sum('credits__price')
            ).filter(
                total_credit_amount__isnull=False
            ).aggregate(
                high_value=Count('id', filter=Q(total_credit_amount__gte=10000)),
                medium_value=Count('id', filter=Q(total_credit_amount__gte=5000, total_credit_amount__lt=10000)),
                low_value=Count('id', filter=Q(total_credit_amount__lt=5000))
            )
            
            return {
                'active_users': list(active_users.values(
                    'id_user', 'username', 'credit_count', 'transaction_count', 
                    'total_credit_amount', 'last_activity'
                )),
                'user_segments': user_segments
            }
        except Exception as e:
            logger.error(f"Error getting user behavior analytics: {e}")
            return {}
    
    @staticmethod
    def get_risk_analytics():
        """Analytics de riesgo crediticio"""
        try:
            # Créditos en mora
            overdue_credits = Credit.objects.filter(
                state='completed',
                pending_amount__gt=0
            ).count()
            
            # Cuotas vencidas
            overdue_installments = Installment.objects.filter(
                status='overdue'
            ).count()
            
            # Distribución de morosidad
            default_distribution = Credit.objects.filter(
                state='completed'
            ).values('morosidad_level').annotate(
                count=Count('id'),
                total_amount=Sum('pending_amount')
            )
            
            # Riesgo por categoría
            risk_by_category = Credit.objects.filter(
                state='completed',
                pending_amount__gt=0
            ).values(
                'subcategory__name'
            ).annotate(
                count=Count('id'),
                total_pending=Sum('pending_amount'),
                avg_pending=Avg('pending_amount')
            ).order_by('-total_pending')
            
            return {
                'overdue_credits': overdue_credits,
                'overdue_installments': overdue_installments,
                'default_distribution': list(default_distribution),
                'risk_by_category': list(risk_by_category)
            }
        except Exception as e:
            logger.error(f"Error getting risk analytics: {e}")
            return {}
    
    @staticmethod
    def get_revenue_analytics():
        """Analytics de ingresos y rentabilidad"""
        try:
            # Ingresos por período
            monthly_revenue = Credit.objects.filter(
                state='completed',
                created_at__gte=timezone.now() - timedelta(days=365)
            ).annotate(
                month=TruncMonth('created_at')
            ).values('month').annotate(
                total_revenue=Sum('earnings'),
                total_credits=Count('id'),
                avg_earnings=Avg('earnings')
            ).order_by('month')
            
            # Rentabilidad por categoría
            profitability_by_category = Credit.objects.filter(
                state='completed'
            ).values(
                'subcategory__name'
            ).annotate(
                total_revenue=Sum('earnings'),
                total_cost=Sum('cost'),
                total_price=Sum('price'),
                credit_count=Count('id')
            ).annotate(
                profit_margin=(Sum('earnings') / Sum('price') * 100)
            ).order_by('-total_revenue')
            
            # Tendencias de ganancias
            earnings_trend = Credit.objects.filter(
                state='completed',
                created_at__gte=timezone.now() - timedelta(days=90)
            ).annotate(
                date=TruncDate('created_at')
            ).values('date').annotate(
                daily_earnings=Sum('earnings'),
                credit_count=Count('id')
            ).order_by('date')
            
            return {
                'monthly_revenue': list(monthly_revenue),
                'profitability_by_category': list(profitability_by_category),
                'earnings_trend': list(earnings_trend)
            }
        except Exception as e:
            logger.error(f"Error getting revenue analytics: {e}")
            return {}
    
    @staticmethod
    def get_operational_metrics():
        """Métricas operacionales"""
        try:
            # Eficiencia de procesamiento
            processing_times = Credit.objects.filter(
                state__in=['completed', 'to_solve'],
                created_at__gte=timezone.now() - timedelta(days=30)
            ).aggregate(
                total_credits=Count('id'),
                completed_credits=Count('id', filter=Q(state='completed')),
                pending_credits=Count('id', filter=Q(state='pending')),
                rejected_credits=Count('id', filter=Q(state='to_solve'))
            )
            
            if processing_times['total_credits'] > 0:
                processing_times['completion_rate'] = (
                    processing_times['completed_credits'] * 100.0 / processing_times['total_credits']
                )
            else:
                processing_times['completion_rate'] = 0
            
            # Distribución de trabajo por vendedor
            seller_performance = Credit.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=30)
            ).values(
                'seller__user__username'
            ).annotate(
                credits_created=Count('id'),
                total_amount=Sum('price'),
                avg_amount=Avg('price'),
                completed_credits=Count('id', filter=Q(state='completed'))
            ).annotate(
                completion_rate=(Count('id', filter=Q(state='completed')) * 100.0 / Count('id'))
            ).order_by('-credits_created')
            
            return {
                'processing_times': processing_times,
                'seller_performance': list(seller_performance)
            }
        except Exception as e:
            logger.error(f"Error getting operational metrics: {e}")
            return {}
    
    @staticmethod
    def get_predictive_insights():
        """Insights predictivos"""
        try:
            # Predicción de demanda
            demand_prediction = Credit.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=90)
            ).annotate(
                month=TruncMonth('created_at')
            ).values('month').annotate(
                demand=Count('id'),
                total_amount=Sum('price')
            ).order_by('month')
            
            # Patrones de pago
            payment_patterns = Installment.objects.filter(
                paid=True,
                paid_on__gte=timezone.now() - timedelta(days=90)
            ).annotate(
                day_of_week=Extract('paid_on', 'dow'),
                day_of_month=Extract('paid_on', 'day')
            ).values('day_of_week', 'day_of_month').annotate(
                payment_count=Count('id')
            ).order_by('-payment_count')
            
            # Predicción de morosidad
            default_prediction = Credit.objects.filter(
                state='completed',
                created_at__gte=timezone.now() - timedelta(days=180)
            ).values('subcategory__name').annotate(
                total_credits=Count('id'),
                defaulted_credits=Count('id', filter=Q(is_in_default=True))
            ).annotate(
                default_rate=(Count('id', filter=Q(is_in_default=True)) * 100.0 / Count('id'))
            ).order_by('-default_rate')
            
            return {
                'demand_prediction': list(demand_prediction),
                'payment_patterns': list(payment_patterns),
                'default_prediction': list(default_prediction)
            }
        except Exception as e:
            logger.error(f"Error getting predictive insights: {e}")
            return {}

