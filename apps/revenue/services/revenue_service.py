from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models

from ..models import CreditEarnings, EarningsMetrics, EarningsAdjustment

class RevenueService:
    """
    Servicio principal para la gestión de ingresos y ganancias.
    """
    
    @staticmethod
    @transaction.atomic
    def create_credit_earnings(credit, theoretical_earnings):
        """
        Crea un nuevo registro de ganancias para un crédito.
        """
        if hasattr(credit, 'earnings_detail'):
            raise ValidationError(_('El crédito ya tiene un registro de ganancias asociado.'))
            
        earnings = CreditEarnings(
            credit=credit,
            theoretical=theoretical_earnings,
            realized=Decimal('0.00'),
            pending=theoretical_earnings
        )
        earnings.full_clean()
        earnings.save()
        
        # Crear snapshot inicial
        EarningsSnapshot.objects.create(
            credit_earnings=earnings,
            theoretical_at_time=earnings.theoretical,
            realized_at_time=earnings.realized,
            pending_at_time=earnings.pending
        )
        
        return earnings

    @staticmethod
    @transaction.atomic
    def update_realized_earnings(credit_earnings, amount):
        """
        Actualiza las ganancias realizadas y crea un snapshot.
        """
        credit_earnings.realized += amount
        credit_earnings.full_clean()
        credit_earnings.save()
        
        # Crear snapshot del cambio
        EarningsSnapshot.objects.create(
            credit_earnings=credit_earnings,
            theoretical_at_time=credit_earnings.theoretical,
            realized_at_time=credit_earnings.realized,
            pending_at_time=credit_earnings.pending
        )
        
        return credit_earnings

    @staticmethod
    @transaction.atomic
    def create_adjustment(credit_earnings, amount, adjustment_type, reason, user=None):
        """
        Crea un ajuste de ganancias y actualiza los totales.
        """
        adjustment = RevenueAdjustment.objects.create(
            credit_earnings=credit_earnings,
            amount=amount,
            adjustment_type=adjustment_type,
            reason=reason,
            created_by=user
        )
        
        # Actualizar ganancias según el ajuste
        if adjustment_type in ['manual', 'correction']:
            credit_earnings.theoretical += amount
            credit_earnings.full_clean()
            credit_earnings.save()
            
            # Crear snapshot después del ajuste
            EarningsSnapshot.objects.create(
                credit_earnings=credit_earnings,
                theoretical_at_time=credit_earnings.theoretical,
                realized_at_time=credit_earnings.realized,
                pending_at_time=credit_earnings.pending
            )
        
        return adjustment

    @staticmethod
    def calculate_period_metrics(start_date, end_date):
        """
        Calcula métricas de ingresos para un período específico.
        """
        if end_date <= start_date:
            raise ValidationError(_('El fin del período debe ser posterior al inicio.'))
            
        # Obtener todas las ganancias actualizadas en el período
        earnings_in_period = CreditEarnings.objects.filter(
            updated_at__range=(start_date, end_date)
        ).aggregate(
            total_theoretical=models.Sum('theoretical'),
            total_realized=models.Sum('realized'),
            total_pending=models.Sum('pending')
        )
        
        metrics = RevenueMetrics(
            period_start=start_date,
            period_end=end_date,
            total_theoretical=earnings_in_period['total_theoretical'] or Decimal('0.00'),
            total_realized=earnings_in_period['total_realized'] or Decimal('0.00'),
            total_pending=earnings_in_period['total_pending'] or Decimal('0.00')
        )
        metrics.full_clean()
        metrics.save()
        
        return metrics

    @staticmethod
    def get_earnings_history(credit_earnings, start_date=None, end_date=None):
        """
        Obtiene el historial de cambios en las ganancias.
        """
        snapshots = credit_earnings.snapshots.all()
        
        if start_date:
            snapshots = snapshots.filter(timestamp__gte=start_date)
        if end_date:
            snapshots = snapshots.filter(timestamp__lte=end_date)
            
        return snapshots.order_by('timestamp') 