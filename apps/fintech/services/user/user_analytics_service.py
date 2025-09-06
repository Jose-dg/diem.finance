"""
Servicio para cálculos analíticos de usuarios
Optimiza las consultas costosas y evita N+1 queries
"""
from django.db.models import Sum, Count, Avg, Q
from django.core.cache import cache
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone


class UserAnalyticsService:
    """Servicio para cálculos analíticos de usuarios con optimización de performance"""
    
    CACHE_TIMEOUT = 300  # 5 minutos
    
    @classmethod
    def get_user_credit_stats(cls, user_id):
        """
        Obtiene estadísticas de créditos del usuario con una sola consulta optimizada
        """
        cache_key = f"user_credit_stats_{user_id}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return cached_result
        
        from apps.fintech.models import Credit
        
        # Una sola consulta optimizada con agregaciones
        stats = Credit.objects.filter(user_id=user_id).aggregate(
            total_credits=Count('id'),
            active_credits=Count('id', filter=Q(state='pending')),
            completed_credits=Count('id', filter=Q(state='completed')),
            total_amount=Sum('price'),
            pending_amount=Sum('pending_amount'),
            avg_amount=Avg('price')
        )
        
        # Convertir None a 0 para evitar errores
        result = {
            'total_credits_count': stats['total_credits'] or 0,
            'active_credits_count': stats['active_credits'] or 0,
            'completed_credits_count': stats['completed_credits'] or 0,
            'total_credit_amount': stats['total_amount'] or Decimal('0.00'),
            'total_pending_amount': stats['pending_amount'] or Decimal('0.00'),
            'average_credit_amount': stats['avg_amount'] or Decimal('0.00')
        }
        
        # Cachear resultado
        cache.set(cache_key, result, cls.CACHE_TIMEOUT)
        return result
    
    @classmethod
    def get_user_overdue_status(cls, user_id):
        """
        Verifica si el usuario tiene créditos vencidos
        """
        cache_key = f"user_overdue_{user_id}"
        cached_result = cache.get(cache_key)
        
        if cached_result is not None:
            return cached_result
        
        from apps.fintech.models import Credit
        
        has_overdue = Credit.objects.filter(
            user_id=user_id,
            morosidad_level__in=[
                'mild_default', 'moderate_default', 'severe_default', 
                'recurrent_default', 'critical_default'
            ]
        ).exists()
        
        cache.set(cache_key, has_overdue, cls.CACHE_TIMEOUT)
        return has_overdue
    
    @classmethod
    def calculate_customer_lifetime_value(cls, user_id, date_joined):
        """
        Calcula el valor de vida del cliente (CLV) de forma optimizada
        """
        cache_key = f"user_clv_{user_id}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return cached_result
        
        stats = cls.get_user_credit_stats(user_id)
        
        if stats['total_credits_count'] == 0:
            return Decimal('0.00')
        
        # Calcular factor de frecuencia
        years_active = max(1, (timezone.now() - date_joined).days / 365)
        frequency_factor = stats['total_credits_count'] / years_active
        
        # CLV = monto promedio * frecuencia * años estimados
        estimated_years = 5  # Estimación conservadora
        clv = stats['average_credit_amount'] * frequency_factor * estimated_years
        
        cache.set(cache_key, clv, cls.CACHE_TIMEOUT)
        return clv
    
    @classmethod
    def determine_customer_segment(cls, user_id):
        """
        Determina el segmento del cliente basado en comportamiento
        """
        cache_key = f"user_segment_{user_id}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return cached_result
        
        stats = cls.get_user_credit_stats(user_id)
        has_overdue = cls.get_user_overdue_status(user_id)
        
        # Lógica de segmentación
        if stats['total_credit_amount'] > 5000000 and not has_overdue:
            segment = 'premium'
        elif stats['total_credits_count'] >= 3 and not has_overdue:
            segment = 'loyal'
        elif has_overdue:
            segment = 'at_risk'
        elif stats['total_credits_count'] == 1:
            segment = 'new'
        else:
            segment = 'regular'
        
        cache.set(cache_key, segment, cls.CACHE_TIMEOUT)
        return segment
    
    @classmethod
    def invalidate_user_cache(cls, user_id):
        """
        Invalida el cache de un usuario específico
        """
        cache_keys = [
            f"user_credit_stats_{user_id}",
            f"user_overdue_{user_id}",
            f"user_clv_{user_id}",
            f"user_segment_{user_id}"
        ]
        
        for key in cache_keys:
            cache.delete(key)
    
    @classmethod
    def get_bulk_user_stats(cls, user_ids):
        """
        Obtiene estadísticas para múltiples usuarios de forma eficiente
        """
        from apps.fintech.models import Credit
        
        # Consulta optimizada para múltiples usuarios
        stats = Credit.objects.filter(user_id__in=user_ids).values('user_id').annotate(
            total_credits=Count('id'),
            active_credits=Count('id', filter=Q(state='pending')),
            completed_credits=Count('id', filter=Q(state='completed')),
            total_amount=Sum('price'),
            pending_amount=Sum('pending_amount'),
            avg_amount=Avg('price')
        )
        
        # Convertir a diccionario para acceso rápido
        result = {}
        for stat in stats:
            user_id = stat['user_id']
            result[user_id] = {
                'total_credits_count': stat['total_credits'] or 0,
                'active_credits_count': stat['active_credits'] or 0,
                'completed_credits_count': stat['completed_credits'] or 0,
                'total_credit_amount': stat['total_amount'] or Decimal('0.00'),
                'total_pending_amount': stat['pending_amount'] or Decimal('0.00'),
                'average_credit_amount': stat['avg_amount'] or Decimal('0.00')
            }
        
        return result
