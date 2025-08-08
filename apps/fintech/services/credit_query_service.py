from django.db.models import QuerySet
from apps.fintech.models import Credit
from django.db.models import Sum


class CreditQueryService:
    """
    Servicio para consultas de créditos con detección inteligente del tipo de usuario.
    """
    
    @staticmethod
    def get_user_credits(user) -> QuerySet:
        """
        Obtiene créditos según el rol del usuario:
        - Super admin: Ve TODO
        - Admin: Ve TODO (pero no es superuser)
        - Vendedor: Ve solo créditos que vendió
        - Cliente: Ve solo sus créditos
        """
        if user.is_superuser:
            # Super admin: Ve TODO
            return Credit.objects.all()
        
        elif user.is_staff:
            # Admin: Ve TODO (pero no es superuser)
            return Credit.objects.all()
        
        elif hasattr(user, 'seller_profile'):
            # Vendedor: Ve solo créditos que vendió
            return Credit.objects.filter(seller__user=user)
        
        else:
            # Cliente: Ve solo sus créditos
            return Credit.objects.filter(user=user)
    
    @staticmethod
    def get_user_credits_with_filters(user, **filters) -> QuerySet:
        """
        Obtiene créditos con filtros adicionales.
        
        Args:
            user: Usuario autenticado
            **filters: Filtros adicionales (ej: state='pending')
            
        Returns:
            QuerySet filtrado de créditos
        """
        base_qs = CreditQueryService.get_user_credits(user)
        return base_qs.filter(**filters)
    
    @staticmethod
    def get_user_credits_by_date_range(user, start_date, end_date) -> QuerySet:
        """
        Obtiene créditos en un rango de fechas.
        
        Args:
            user: Usuario autenticado
            start_date: Fecha de inicio
            end_date: Fecha de fin
            
        Returns:
            QuerySet filtrado de créditos por rango de fechas
        """
        base_qs = CreditQueryService.get_user_credits(user)
        return base_qs.filter(created_at__date__range=[start_date, end_date])
    
    @staticmethod
    def get_user_credits_summary(user) -> dict:
        """Obtiene resumen de créditos del usuario según su rol"""
        credits = CreditQueryService.get_user_credits(user)
        
        return {
            'total_credits': credits.count(),
            'pending_credits': credits.filter(status='pending').count(),
            'active_credits': credits.filter(status='active').count(),
            'completed_credits': credits.filter(status='completed').count(),
            'total_amount': credits.aggregate(total=Sum('price'))['total'] or 0,
            'pending_amount': credits.filter(status='pending').aggregate(total=Sum('price'))['total'] or 0,
        } 