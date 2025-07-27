from django.db.models import Sum, Avg, Count
from datetime import timedelta
from apps.fintech.models import Credit, Installment


class KPIService:
    """Service class for KPI calculations and business metrics"""
    
    @staticmethod
    def get_credit_kpi_summary(start_date, end_date):
        """
        Calcula los KPIs principales entre dos fechas y el comparativo con el periodo anterior.
        """
        # Créditos en rango
        credits = Credit.objects.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)
        total_credit_amount = credits.aggregate(total=Sum('price'))['total'] or 0
        credit_count = credits.count()
        avg_credit_amount = credits.aggregate(avg=Avg('price'))['avg'] or 0
        avg_credit_days = credits.aggregate(avg=Avg('credit_days'))['avg'] or 0

        # Abonos realizados en rango
        abonos = credits.aggregate(total=Sum('total_abonos'))['total'] or 0

        # Recaudo esperado: suma de installment_value de cuotas con due_date en rango
        expected_recaudo = Installment.objects.filter(
            credit__in=credits,
            due_date__gte=start_date,
            due_date__lte=end_date
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Créditos en mora en rango
        morosos = credits.filter(is_in_default=True)
        morosos_count = morosos.count()
        morosidad_rate = (morosos_count / credit_count * 100) if credit_count else 0

        # Porcentaje de cumplimiento de recaudo
        cumplimiento_recaudo = (abonos / expected_recaudo * 100) if expected_recaudo else 0

        # Comparativo con periodo anterior
        delta = end_date - start_date
        prev_start = start_date - delta
        prev_end = start_date - timedelta(days=1)
        prev_credits = Credit.objects.filter(created_at__date__gte=prev_start, created_at__date__lte=prev_end)
        prev_total_credit_amount = prev_credits.aggregate(total=Sum('price'))['total'] or 0
        prev_abonos = prev_credits.aggregate(total=Sum('total_abonos'))['total'] or 0
        prev_expected_recaudo = Installment.objects.filter(
            credit__in=prev_credits,
            due_date__gte=prev_start,
            due_date__lte=prev_end
        ).aggregate(total=Sum('amount'))['total'] or 0
        prev_credit_count = prev_credits.count()
        prev_morosos_count = prev_credits.filter(is_in_default=True).count()
        prev_morosidad_rate = (prev_morosos_count / prev_credit_count * 100) if prev_credit_count else 0
        prev_cumplimiento_recaudo = (prev_abonos / prev_expected_recaudo * 100) if prev_expected_recaudo else 0

        return {
            'total_credit_amount': total_credit_amount,
            'credit_count': credit_count,
            'avg_credit_amount': avg_credit_amount,
            'avg_credit_days': avg_credit_days,
            'abonos': abonos,
            'expected_recaudo': expected_recaudo,
            'cumplimiento_recaudo': round(cumplimiento_recaudo, 2),
            'morosos_count': morosos_count,
            'morosidad_rate': round(morosidad_rate, 2),
            'prev_total_credit_amount': prev_total_credit_amount,
            'prev_abonos': prev_abonos,
            'prev_expected_recaudo': prev_expected_recaudo,
            'prev_cumplimiento_recaudo': round(prev_cumplimiento_recaudo, 2),
            'prev_morosos_count': prev_morosos_count,
            'prev_morosidad_rate': round(prev_morosidad_rate, 2),
        }
    
    @staticmethod
    def get_user_financial_metrics(user_id):
        """
        Calcula métricas financieras específicas del usuario
        """
        user_credits = Credit.objects.filter(user_id=user_id)
        
        total_credits = user_credits.count()
        total_credit_amount = user_credits.aggregate(total=Sum('price'))['total'] or 0
        total_paid = user_credits.aggregate(total=Sum('total_abonos'))['total'] or 0
        active_credits = user_credits.filter(state='pending').count()
        defaulted_credits = user_credits.filter(is_in_default=True).count()
        
        return {
            'total_credits': total_credits,
            'total_credit_amount': total_credit_amount,
            'total_paid': total_paid,
            'active_credits': active_credits,
            'defaulted_credits': defaulted_credits,
            'payment_ratio': (total_paid / total_credit_amount * 100) if total_credit_amount else 0
        }
    
    @staticmethod
    def get_portfolio_health_metrics():
        """
        Calcula métricas de salud del portafolio
        """
        total_credits = Credit.objects.count()
        active_credits = Credit.objects.filter(state='pending').count()
        defaulted_credits = Credit.objects.filter(is_in_default=True).count()
        completed_credits = Credit.objects.filter(state='completed').count()
        
        total_portfolio = Credit.objects.aggregate(total=Sum('price'))['total'] or 0
        total_received = Credit.objects.aggregate(total=Sum('total_abonos'))['total'] or 0
        
        return {
            'total_credits': total_credits,
            'active_credits': active_credits,
            'defaulted_credits': defaulted_credits,
            'completed_credits': completed_credits,
            'total_portfolio': total_portfolio,
            'total_received': total_received,
            'collection_rate': (total_received / total_portfolio * 100) if total_portfolio else 0,
            'default_rate': (defaulted_credits / total_credits * 100) if total_credits else 0
        } 