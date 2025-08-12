from django.db.models import Q, Count, Sum, Avg, Max, Min
from django.db.models.functions import TruncDate, TruncMonth, TruncYear, Extract
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal
from apps.fintech.models import Credit, Transaction, User, Installment, Expense, Seller
import logging

logger = logging.getLogger(__name__)

class DashboardService:
    """Servicio de dashboard con métricas específicas para el panel de control - Independiente de modelos de insights"""
    
    @staticmethod
    def get_executive_dashboard():
        """Dashboard ejecutivo con KPIs principales"""
        try:
            today = timezone.now().date()
            this_month = today.replace(day=1)
            last_month = (this_month - timedelta(days=1)).replace(day=1)
            
            # KPIs principales
            kpis = {
                'total_portfolio': Credit.objects.filter(state='completed').aggregate(
                    total=Sum('price')
                )['total'] or Decimal('0.00'),
                
                'active_credits': Credit.objects.filter(state='completed').count(),
                
                'monthly_disbursements': Credit.objects.filter(
                    state='completed',
                    created_at__gte=this_month
                ).aggregate(
                    total=Sum('price')
                )['total'] or Decimal('0.00'),
                
                'monthly_earnings': Credit.objects.filter(
                    state='completed',
                    created_at__gte=this_month
                ).aggregate(
                    total=Sum('earnings')
                )['total'] or Decimal('0.00'),
                
                'pending_amount': Credit.objects.filter(
                    state='completed'
                ).aggregate(
                    total=Sum('pending_amount')
                )['total'] or Decimal('0.00'),
                
                'overdue_credits': Credit.objects.filter(
                    state='completed',
                    pending_amount__gt=0
                ).count(),
                
                'new_users_this_month': User.objects.filter(
                    date_joined__gte=this_month
                ).count(),
                
                'total_users': User.objects.count()
            }
            
            # Cálculo de tasas
            if kpis['total_portfolio'] > 0:
                kpis['collection_rate'] = ((kpis['total_portfolio'] - kpis['pending_amount']) / kpis['total_portfolio'] * 100)
                kpis['default_rate'] = (kpis['overdue_credits'] / kpis['active_credits'] * 100) if kpis['active_credits'] > 0 else 0
            else:
                kpis['collection_rate'] = 0
                kpis['default_rate'] = 0
            
            return kpis
        except Exception as e:
            logger.error(f"Error getting executive dashboard: {e}")
            return {}
    
    @staticmethod
    def get_credit_analytics_dashboard():
        """Dashboard de analytics de créditos"""
        try:
            # Tendencias de créditos por mes (últimos 12 meses)
            monthly_trends = []
            for i in range(12):
                month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
                month_end = month_start.replace(day=28) + timedelta(days=4)
                month_end = month_end.replace(day=1) - timedelta(days=1)
                
                month_data = Credit.objects.filter(
                    created_at__gte=month_start,
                    created_at__lte=month_end
                ).aggregate(
                    total_credits=Count('id'),
                    total_amount=Sum('price'),
                    total_earnings=Sum('earnings'),
                    completed_credits=Count('id', filter=Q(state='completed'))
                )
                
                monthly_trends.append({
                    'month': month_start.strftime('%Y-%m'),
                    'total_credits': month_data['total_credits'] or 0,
                    'total_amount': month_data['total_amount'] or Decimal('0.00'),
                    'total_earnings': month_data['total_earnings'] or Decimal('0.00'),
                    'completed_credits': month_data['completed_credits'] or 0
                })
            
            # Distribución por categorías
            category_distribution = Credit.objects.filter(
                state='completed'
            ).values(
                'subcategory__name'
            ).annotate(
                count=Count('id'),
                total_amount=Sum('price'),
                avg_amount=Avg('price')
            ).order_by('-total_amount')[:10]
            
            # Estados de créditos
            credit_states = Credit.objects.values('state').annotate(
                count=Count('id'),
                total_amount=Sum('price')
            )
            
            # Top vendedores
            top_sellers = Credit.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=30)
            ).values(
                'seller__user__username'
            ).annotate(
                credits_created=Count('id'),
                total_amount=Sum('price'),
                completed_credits=Count('id', filter=Q(state='completed'))
            ).annotate(
                completion_rate=(Count('id', filter=Q(state='completed')) * 100.0 / Count('id'))
            ).order_by('-total_amount')[:10]
            
            return {
                'monthly_trends': list(reversed(monthly_trends)),
                'category_distribution': list(category_distribution),
                'credit_states': list(credit_states),
                'top_sellers': list(top_sellers)
            }
        except Exception as e:
            logger.error(f"Error getting credit analytics dashboard: {e}")
            return {}
    
    @staticmethod
    def get_risk_dashboard():
        """Dashboard de gestión de riesgos"""
        try:
            # Créditos en mora por días
            overdue_by_days = []
            for days in [1, 7, 15, 30, 60, 90]:
                overdue_credits = Credit.objects.filter(
                    state='completed',
                    pending_amount__gt=0,
                    updated_at__lte=timezone.now() - timedelta(days=days)
                ).count()
                
                overdue_amount = Credit.objects.filter(
                    state='completed',
                    pending_amount__gt=0,
                    updated_at__lte=timezone.now() - timedelta(days=days)
                ).aggregate(
                    total=Sum('pending_amount')
                )['total'] or Decimal('0.00')
                
                overdue_by_days.append({
                    'days': days,
                    'credits_count': overdue_credits,
                    'amount': overdue_amount
                })
            
            # Distribución de morosidad por categoría
            default_by_category = Credit.objects.filter(
                state='completed',
                pending_amount__gt=0
            ).values(
                'subcategory__name'
            ).annotate(
                total_credits=Count('id'),
                overdue_credits=Count('id', filter=Q(pending_amount__gt=0)),
                total_pending=Sum('pending_amount')
            ).annotate(
                default_rate=(Count('id', filter=Q(pending_amount__gt=0)) * 100.0 / Count('id'))
            ).order_by('-default_rate')
            
            # Cuotas vencidas
            overdue_installments = Installment.objects.filter(
                status='overdue'
            ).aggregate(
                count=Count('id'),
                total_amount=Sum('amount'),
                avg_days_overdue=Avg('days_overdue')
            )
            
            # Predicción de riesgo
            risk_prediction = Credit.objects.filter(
                state='completed',
                created_at__gte=timezone.now() - timedelta(days=90)
            ).values('subcategory__name').annotate(
                total_credits=Count('id'),
                defaulted_credits=Count('id', filter=Q(is_in_default=True))
            ).annotate(
                risk_score=(Count('id', filter=Q(is_in_default=True)) * 100.0 / Count('id'))
            ).filter(
                risk_score__gt=0
            ).order_by('-risk_score')[:5]
            
            return {
                'overdue_by_days': overdue_by_days,
                'default_by_category': list(default_by_category),
                'overdue_installments': overdue_installments,
                'risk_prediction': list(risk_prediction)
            }
        except Exception as e:
            logger.error(f"Error getting risk dashboard: {e}")
            return {}
    
    @staticmethod
    def get_user_insights_dashboard():
        """Dashboard de insights de usuarios"""
        try:
            # Segmentación de usuarios por valor
            user_segments = User.objects.annotate(
                total_credit_amount=Sum('credits__price'),
                credit_count=Count('credits'),
                last_activity=Max('credits__created_at')
            ).filter(
                total_credit_amount__isnull=False
            ).aggregate(
                high_value=Count('id', filter=Q(total_credit_amount__gte=10000)),
                medium_value=Count('id', filter=Q(total_credit_amount__gte=5000, total_credit_amount__lt=10000)),
                low_value=Count('id', filter=Q(total_credit_amount__lt=5000)),
                new_users=Count('id', filter=Q(date_joined__gte=timezone.now() - timedelta(days=30)))
            )
            
            # Usuarios más activos
            top_users = User.objects.annotate(
                credit_count=Count('credits'),
                total_amount=Sum('credits__price'),
                transaction_count=Count('transactions')
            ).filter(
                credit_count__gt=0
            ).order_by('-total_amount')[:10]
            
            return {
                'user_segments': user_segments,
                'top_users': list(top_users.values(
                    'id_user', 'username', 'credit_count', 'total_amount', 'transaction_count'
                ))
            }
        except Exception as e:
            logger.error(f"Error getting user insights dashboard: {e}")
            return {}
    
    @staticmethod
    def get_operational_dashboard():
        """Dashboard operacional"""
        try:
            # Eficiencia de procesamiento
            processing_efficiency = Credit.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=30)
            ).aggregate(
                total_credits=Count('id'),
                completed_credits=Count('id', filter=Q(state='completed')),
                pending_credits=Count('id', filter=Q(state='pending')),
                rejected_credits=Count('id', filter=Q(state='to_solve'))
            )
            
            if processing_efficiency['total_credits'] > 0:
                processing_efficiency['completion_rate'] = (
                    processing_efficiency['completed_credits'] * 100.0 / processing_efficiency['total_credits']
                )
            else:
                processing_efficiency['completion_rate'] = 0
            
            # Rendimiento de vendedores
            seller_performance = Credit.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=30)
            ).values(
                'seller__user__username'
            ).annotate(
                credits_created=Count('id'),
                total_amount=Sum('price'),
                completed_credits=Count('id', filter=Q(state='completed'))
            ).annotate(
                completion_rate=(Count('id', filter=Q(state='completed')) * 100.0 / Count('id')),
                avg_amount=Avg('price')
            ).order_by('-total_amount')[:10]
            
            # Alertas y notificaciones
            alerts = {
                'overdue_credits': Credit.objects.filter(
                    state='completed',
                    pending_amount__gt=0
                ).count(),
                
                'pending_approvals': Credit.objects.filter(
                    state='pending'
                ).count(),
                
                'low_balance_accounts': Credit.objects.filter(
                    state='completed',
                    pending_amount__gt=0
                ).count()
            }
            
            return {
                'processing_efficiency': processing_efficiency,
                'seller_performance': list(seller_performance),
                'alerts': alerts
            }
        except Exception as e:
            logger.error(f"Error getting operational dashboard: {e}")
            return {}
    
    @staticmethod
    def get_revenue_dashboard():
        """Dashboard de ingresos y rentabilidad"""
        try:
            # Ingresos por período
            revenue_trends = []
            for i in range(12):
                month_start = timezone.now().replace(day=1) - timedelta(days=30*i)
                month_end = month_start.replace(day=28) + timedelta(days=4)
                month_end = month_end.replace(day=1) - timedelta(days=1)
                
                month_revenue = Credit.objects.filter(
                    state='completed',
                    created_at__gte=month_start,
                    created_at__lte=month_end
                ).aggregate(
                    total_revenue=Sum('earnings'),
                    total_credits=Count('id'),
                    total_amount=Sum('price'),
                    avg_earnings=Avg('earnings')
                )
                
                revenue_trends.append({
                    'month': month_start.strftime('%Y-%m'),
                    'total_revenue': month_revenue['total_revenue'] or Decimal('0.00'),
                    'total_credits': month_revenue['total_credits'] or 0,
                    'total_amount': month_revenue['total_amount'] or Decimal('0.00'),
                    'avg_earnings': month_revenue['avg_earnings'] or Decimal('0.00')
                })
            
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
                profit_margin=(Sum('earnings') * 100.0 / Sum('price')),
                roi=(Sum('earnings') * 100.0 / Sum('cost'))
            ).order_by('-total_revenue')
            
            # Top productos por rentabilidad
            top_products = profitability_by_category[:10]
            
            # Proyección de ingresos
            current_month_revenue = Credit.objects.filter(
                state='completed',
                created_at__gte=timezone.now().replace(day=1)
            ).aggregate(
                total=Sum('earnings')
            )['total'] or Decimal('0.00')
            
            last_month_revenue = Credit.objects.filter(
                state='completed',
                created_at__gte=(timezone.now().replace(day=1) - timedelta(days=30)),
                created_at__lt=timezone.now().replace(day=1)
            ).aggregate(
                total=Sum('earnings')
            )['total'] or Decimal('0.00')
            
            growth_rate = ((current_month_revenue - last_month_revenue) / last_month_revenue * 100) if last_month_revenue > 0 else 0
            
            return {
                'revenue_trends': list(reversed(revenue_trends)),
                'profitability_by_category': list(profitability_by_category),
                'top_products': list(top_products),
                'current_month_revenue': current_month_revenue,
                'growth_rate': growth_rate
            }
        except Exception as e:
            logger.error(f"Error getting revenue dashboard: {e}")
            return {}

