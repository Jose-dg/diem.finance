from decimal import Decimal
from django.utils import timezone
from datetime import timedelta, date
from django.db import transaction
from django.core.cache import cache
from apps.fintech.models import Installment, Credit


class InstallmentCalculator:
    """Servicio para calcular campos de cuotas con cache inteligente"""
    
    CACHE_TIMEOUT = 3600  # 1 hora
    CACHE_PREFIX = "installment_calc_"
    
    @classmethod
    def get_remaining_amount(cls, installment):
        """Obtiene remaining_amount con cache"""
        cache_key = f"{cls.CACHE_PREFIX}remaining_{installment.id}"
        cached_value = cache.get(cache_key)
        
        if cached_value is not None:
            return cached_value
        
        # Calcular y cachear
        remaining = installment.amount - installment.amount_paid
        cache.set(cache_key, remaining, cls.CACHE_TIMEOUT)
        return remaining
    
    @classmethod
    def get_days_overdue(cls, installment):
        """Obtiene days_overdue con cache"""
        if installment.status not in ['pending', 'partial']:
            return 0
            
        cache_key = f"{cls.CACHE_PREFIX}overdue_{installment.id}"
        cached_value = cache.get(cache_key)
        
        if cached_value is not None:
            return cached_value
        
        # Calcular y cachear
        if installment.due_date:
            days = max(0, (timezone.now().date() - installment.due_date).days)
            cache.set(cache_key, days, cls.CACHE_TIMEOUT)
            return days
        return 0
    
    @classmethod
    def get_late_fee(cls, installment):
        """Obtiene late_fee con cache"""
        days_overdue = cls.get_days_overdue(installment)
        if days_overdue == 0:
            return Decimal('0.00')
        
        cache_key = f"{cls.CACHE_PREFIX}late_fee_{installment.id}"
        cached_value = cache.get(cache_key)
        
        if cached_value is not None:
            return cached_value
        
        # Calcular y cachear (5% por mes)
        remaining = cls.get_remaining_amount(installment)
        months_overdue = days_overdue / 30
        late_fee = remaining * Decimal('0.05') * Decimal(str(months_overdue))
        cache.set(cache_key, late_fee, cls.CACHE_TIMEOUT)
        return late_fee
    
    @classmethod
    def get_total_amount_due(cls, installment):
        """Obtiene total a pagar con cache"""
        remaining = cls.get_remaining_amount(installment)
        late_fee = cls.get_late_fee(installment)
        return remaining + late_fee
    
    @classmethod
    def clear_cache(cls, installment_id):
        """Limpia cache de una cuota específica"""
        cache_keys = [
            f"{cls.CACHE_PREFIX}remaining_{installment_id}",
            f"{cls.CACHE_PREFIX}overdue_{installment_id}",
            f"{cls.CACHE_PREFIX}late_fee_{installment_id}",
        ]
        cache.delete_many(cache_keys)
    
    @classmethod
    def should_recalculate(cls, installment):
        """Determina si una cuota necesita recálculo"""
        # Si es nueva o tiene cambios recientes
        if installment.updated_at > timezone.now() - timedelta(hours=1):
            return True
        
        # Si está pendiente y vence pronto
        if (installment.status == 'pending' and 
            installment.due_date and 
            installment.due_date <= timezone.now().date() + timedelta(days=7)):
            return True
        
        # Si tiene mora alta
        days_overdue = cls.get_days_overdue(installment)
        if days_overdue > 30:
            return True
        
        return False
    
    @classmethod
    def update_credit_status(cls, credit):
        """Actualiza el estado del crédito basado en sus cuotas"""
        installments = credit.installments.all()
        
        # Contar cuotas por estado
        pending_count = installments.filter(status='pending').count()
        overdue_count = installments.filter(status='overdue').count()
        paid_count = installments.filter(status='paid').count()
        total_count = installments.count()
        
        # Determinar morosidad
        if overdue_count > 0:
            morosidad_rate = (overdue_count / total_count) * 100
        else:
            morosidad_rate = 0
        
        # Actualizar campos del crédito
        credit.is_in_default = overdue_count > 0
        
        # Determinar nivel de morosidad
        if morosidad_rate >= 50:
            credit.morosidad_level = 'high'
        elif morosidad_rate >= 25:
            credit.morosidad_level = 'medium'
        elif morosidad_rate > 0:
            credit.morosidad_level = 'low'
        else:
            credit.morosidad_level = 'none'
        
        credit.save(update_fields=['is_in_default', 'morosidad_level']) 