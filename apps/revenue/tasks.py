from celery import shared_task
from django.utils import timezone
from django.db import transaction
from django.db.models import Q, F
from django.db import models

from .models import CreditEarnings, EarningsMetrics
from .services.revenue_service import RevenueService
from .services.earnings_service import EarningsService
from .services.calculation_service import CalculationService

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    acks_late=True,
    autoretry_for=(Exception,)
)
def update_credit_earnings(self, credit_id):
    """
    Actualiza las ganancias de un crédito específico.
    """
    try:
        with transaction.atomic():
            credit_earnings = CreditEarnings.objects.select_for_update().get(
                credit_id=credit_id
            )
            EarningsService.recalculate_earnings(credit_earnings)
            
        return {
            'status': 'success',
            'credit_id': credit_id,
            'updated_at': timezone.now().isoformat()
        }
        
    except Exception as e:
        self.retry(exc=e)

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=300,
    acks_late=True
)
def calculate_revenue_metrics(self, start_date=None, end_date=None):
    """
    Calcula métricas de ingresos para un período.
    """
    try:
        if not start_date:
            start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if not end_date:
            end_date = timezone.now()
            
        metrics = RevenueService.calculate_period_metrics(start_date, end_date)
        
        return {
            'status': 'success',
            'period_start': start_date.isoformat(),
            'period_end': end_date.isoformat(),
            'metrics_id': metrics.id
        }
        
    except Exception as e:
        self.retry(exc=e)

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    acks_late=True
)
def generate_earnings_snapshots(self, batch_size=100):
    """
    Genera snapshots de ganancias para créditos activos.
    """
    try:
        # Obtener créditos que necesitan snapshot
        earnings = CreditEarnings.objects.filter(
            Q(snapshots__isnull=True) |  # Sin snapshots
            Q(updated_at__gt=models.F('snapshots__timestamp'))  # Actualizados después del último snapshot
        )[:batch_size]
        
        snapshots_created = 0
        for earning in earnings:
            EarningsSnapshot.objects.create(
                credit_earnings=earning,
                theoretical_at_time=earning.theoretical,
                realized_at_time=earning.realized,
                pending_at_time=earning.pending
            )
            snapshots_created += 1
            
        return {
            'status': 'success',
            'snapshots_created': snapshots_created,
            'timestamp': timezone.now().isoformat()
        }
        
    except Exception as e:
        self.retry(exc=e)

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=3600,
    acks_late=True
)
def analyze_earnings_trends(self, days=30):
    """
    Analiza tendencias en las ganancias.
    """
    try:
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=days)
        
        # Obtener todos los CreditEarnings con snapshots en el período
        earnings = CreditEarnings.objects.filter(
            snapshots__timestamp__range=(start_date, end_date)
        ).distinct()
        
        results = []
        for earning in earnings:
            trend = EarningsService.get_earnings_trends(earning, days)
            if trend:
                results.append({
                    'credit_id': earning.credit.uid,
                    'trend': trend
                })
                
        return {
            'status': 'success',
            'trends_analyzed': len(results),
            'period_days': days,
            'results': results
        }
        
    except Exception as e:
        self.retry(exc=e)

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    acks_late=True
)
def validate_earnings_consistency(self, batch_size=100):
    """
    Valida la consistencia de los registros de ganancias.
    """
    try:
        earnings = CreditEarnings.objects.all()[:batch_size]
        
        inconsistencies = []
        for earning in earnings:
            try:
                EarningsService.validate_earnings_state(earning)
            except ValidationError as e:
                inconsistencies.append({
                    'credit_id': earning.credit.uid,
                    'errors': e.message_dict
                })
                
        return {
            'status': 'success',
            'records_checked': batch_size,
            'inconsistencies_found': len(inconsistencies),
            'details': inconsistencies
        }
        
    except Exception as e:
        self.retry(exc=e) 