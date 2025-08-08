from decimal import Decimal
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..models import CreditEarnings, EarningsMetrics, EarningsAdjustment

class EarningsMetricsService:
    """
    Servicio para calcular métricas de ganancias.
    """
    
    @staticmethod
    def calculate_portfolio_metrics():
        """
        Calcula métricas generales del portfolio de ganancias.
        """
        earnings_qs = CreditEarnings.objects.all()
        
        if not earnings_qs.exists():
            return {
                'total_credits': 0,
                'total_theoretical_earnings': Decimal('0.00'),
                'total_realized_earnings': Decimal('0.00'),
                'total_pending_earnings': Decimal('0.00'),
                'avg_realization_rate': Decimal('0.00'),
                'portfolio_value': Decimal('0.00')
            }
        
        aggregations = earnings_qs.aggregate(
            total_credits=Count('id'),
            total_theoretical=Sum('theoretical_earnings'),
            total_realized=Sum('realized_earnings'),
            avg_earnings_rate=Avg('earnings_rate')
        )
        
        total_theoretical = aggregations['total_theoretical'] or Decimal('0.00')
        total_realized = aggregations['total_realized'] or Decimal('0.00')
        total_pending = total_theoretical - total_realized
        
        # Calcular tasa de realización promedio
        if total_theoretical > 0:
            portfolio_realization_rate = (total_realized / total_theoretical) * 100
        else:
            portfolio_realization_rate = Decimal('0.00')
        
        return {
            'total_credits': aggregations['total_credits'],
            'total_theoretical_earnings': total_theoretical,
            'total_realized_earnings': total_realized,
            'total_pending_earnings': total_pending,
            'portfolio_realization_rate': portfolio_realization_rate,
            'avg_earnings_rate': aggregations['avg_earnings_rate'] or Decimal('0.00'),
            'calculated_at': timezone.now()
        }

    @staticmethod
    def get_earnings_by_performance():
        """
        Segmenta créditos por performance de realización de ganancias.
        """
        earnings_qs = CreditEarnings.objects.all()
        
        # Calcular porcentajes de realización para cada crédito
        high_performers = earnings_qs.filter(
            theoretical_earnings__gt=0
        ).extra(
            where=["(realized_earnings / theoretical_earnings) >= 0.8"]
        ).count()
        
        medium_performers = earnings_qs.filter(
            theoretical_earnings__gt=0
        ).extra(
            where=["(realized_earnings / theoretical_earnings) >= 0.5 AND (realized_earnings / theoretical_earnings) < 0.8"]
        ).count()
        
        low_performers = earnings_qs.filter(
            theoretical_earnings__gt=0
        ).extra(
            where=["(realized_earnings / theoretical_earnings) < 0.5"]
        ).count()
        
        total = high_performers + medium_performers + low_performers
        
        return {
            'high_performers': {
                'count': high_performers,
                'percentage': (high_performers / total * 100) if total > 0 else 0,
                'description': 'Realización >= 80%'
            },
            'medium_performers': {
                'count': medium_performers,
                'percentage': (medium_performers / total * 100) if total > 0 else 0,
                'description': 'Realización 50-79%'
            },
            'low_performers': {
                'count': low_performers,
                'percentage': (low_performers / total * 100) if total > 0 else 0,
                'description': 'Realización < 50%'
            },
            'total_analyzed': total
        }

    @staticmethod
    def get_adjustment_impact():
        """
        Analiza el impacto de los ajustes en las ganancias.
        """
        adjustments = EarningsAdjustment.objects.all()
        
        if not adjustments.exists():
            return {
                'total_adjustments': 0,
                'total_impact': Decimal('0.00'),
                'by_type': {}
            }
        
        total_impact = adjustments.aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')
        
        by_type = {}
        for adj_type, adj_label in EarningsAdjustment.ADJUSTMENT_TYPES:
            type_data = adjustments.filter(adjustment_type=adj_type).aggregate(
                count=Count('id'),
                total_amount=Sum('amount')
            )
            
            by_type[adj_type] = {
                'label': adj_label,
                'count': type_data['count'],
                'total_amount': type_data['total_amount'] or Decimal('0.00'),
                'avg_amount': (type_data['total_amount'] / type_data['count']) 
                             if type_data['count'] > 0 else Decimal('0.00')
            }
        
        return {
            'total_adjustments': adjustments.count(),
            'total_impact': total_impact,
            'by_type': by_type,
            'calculated_at': timezone.now()
        }

    @staticmethod
    def create_period_metrics(start_date, end_date):
        """
        Crea un registro de métricas para un período específico.
        """
        if end_date <= start_date:
            raise ValueError(_('End date must be after start date'))
        
        # Obtener ganancias actualizadas en el período
        earnings_in_period = CreditEarnings.objects.filter(
            updated_at__range=(start_date, end_date)
        )
        
        aggregations = earnings_in_period.aggregate(
            total_theoretical=Sum('theoretical_earnings'),
            total_realized=Sum('realized_earnings'),
            count=Count('id'),
            avg_rate=Avg('earnings_rate')
        )
        
        total_theoretical = aggregations['total_theoretical'] or Decimal('0.00')
        total_realized = aggregations['total_realized'] or Decimal('0.00')
        
        # Calcular tasa de realización
        if total_theoretical > 0:
            realization_rate = (total_realized / total_theoretical) * 100
        else:
            realization_rate = Decimal('0.00')
        
        metrics = EarningsMetrics.objects.create(
            period_start=start_date,
            period_end=end_date,
            total_theoretical_earnings=total_theoretical,
            total_realized_earnings=total_realized,
            credits_count=aggregations['count'],
            avg_realization_rate=realization_rate
        )
        
        return metrics

    @staticmethod
    def get_top_earning_credits(limit=10):
        """
        Obtiene los créditos con mayores ganancias realizadas.
        """
        return CreditEarnings.objects.select_related('credit').order_by(
            '-realized_earnings'
        )[:limit]

    @staticmethod
    def get_underperforming_credits(limit=10):
        """
        Obtiene los créditos con menor tasa de realización.
        """
        return CreditEarnings.objects.select_related('credit').filter(
            theoretical_earnings__gt=0
        ).extra(
            select={'realization_rate': 'realized_earnings / theoretical_earnings'}
        ).order_by('realization_rate')[:limit] 