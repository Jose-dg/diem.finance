from django.db import models
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from datetime import timedelta


class CreditManager(models.Manager):
    """Manager personalizado para el modelo Credit"""
    
    def active_credits(self):
        """Retorna créditos activos (pending)"""
        return self.filter(state='pending')
    
    def defaulted_credits(self):
        """Retorna créditos en mora"""
        return self.filter(is_in_default=True)
    
    def completed_credits(self):
        """Retorna créditos completados"""
        return self.filter(state='completed')
    
    def credits_by_date_range(self, start_date, end_date):
        """Retorna créditos creados en un rango de fechas"""
        return self.filter(created_at__date__range=[start_date, end_date])
    
    def credits_by_user(self, user_id):
        """Retorna créditos de un usuario específico"""
        return self.filter(user_id=user_id)
    
    def credits_by_morosidad_level(self, level):
        """Retorna créditos por nivel de morosidad"""
        return self.filter(morosidad_level=level)
    
    def with_payment_summary(self):
        """Annotate con resumen de pagos"""
        return self.annotate(
            total_payments=Sum('payments__amount_paid'),
            payment_count=Count('payments'),
            remaining_amount=models.F('price') - Sum('payments__amount_paid')
        )
    
    def high_risk_credits(self, days_overdue=30):
        """Retorna créditos de alto riesgo (más de X días en mora)"""
        cutoff_date = timezone.now().date() - timedelta(days=days_overdue)
        return self.filter(
            is_in_default=True,
            first_date_payment__lt=cutoff_date
        )


class UserProfileManager(models.Manager):
    """Manager personalizado para UserProfile"""
    
    def complete_profiles(self):
        """Retorna perfiles completos"""
        return self.filter(
            monthly_income__isnull=False,
            monthly_expenses__isnull=False,
            employment_type__isnull=False,
            income_source__isnull=False
        ).exclude(
            monthly_income='',
            monthly_expenses='',
            employment_type='',
            income_source=''
        )
    
    def eligible_for_credit(self):
        """Retorna usuarios elegibles para crédito"""
        return self.filter(
            can_request_credit=True,
            info_verified=True
        )
    
    def high_risk_profiles(self, debt_ratio_threshold=50):
        """Retorna perfiles de alto riesgo"""
        return self.filter(
            debt_to_income_ratio__gte=debt_ratio_threshold
        )
    
    def with_financial_health(self):
        """Annotate con categoría de salud financiera"""
        return self.annotate(
            health_category=models.Case(
                models.When(financial_health_score__gte=75, then=models.Value('Excelente')),
                models.When(financial_health_score__gte=50, then=models.Value('Buena')),
                models.When(financial_health_score__gte=25, then=models.Value('Regular')),
                default=models.Value('Necesita mejoras'),
                output_field=models.CharField(),
            )
        )


class TransactionManager(models.Manager):
    """Manager personalizado para Transaction"""
    
    def income_transactions(self):
        """Retorna transacciones de ingreso"""
        return self.filter(transaction_type='income')
    
    def expense_transactions(self):
        """Retorna transacciones de gasto"""
        return self.filter(transaction_type='expense')
    
    def confirmed_transactions(self):
        """Retorna transacciones confirmadas"""
        return self.filter(status='confirmed')
    
    def transactions_by_date_range(self, start_date, end_date):
        """Retorna transacciones en un rango de fechas"""
        return self.filter(date__date__range=[start_date, end_date])
    
    def transactions_by_user(self, user_id):
        """Retorna transacciones de un usuario"""
        return self.filter(user_id=user_id)
    
    def with_payment_details(self):
        """Annotate con detalles de pago"""
        return self.select_related('user', 'category').prefetch_related('account_method_amounts')


class InstallmentManager(models.Manager):
    """Manager personalizado para Installment con funcionalidades robustas"""
    
    def pending_installments(self):
        """Cuotas pendientes de pago"""
        return self.filter(status='pending', due_date__gte=timezone.now().date())
    
    def overdue_installments(self):
        """Cuotas vencidas"""
        return self.filter(status__in=['pending', 'partial'], due_date__lt=timezone.now().date())
    
    def due_this_week(self):
        """Cuotas que vencen esta semana"""
        today = timezone.now().date()
        week_end = today + timedelta(days=7)
        return self.filter(status='pending', due_date__range=[today, week_end])
    
    def due_today(self):
        """Cuotas que vencen hoy"""
        today = timezone.now().date()
        return self.filter(status='pending', due_date=today)
    
    def with_notification_needed(self):
        """Cuotas que necesitan notificación (3 días antes)"""
        today = timezone.now().date()
        notification_date = today + timedelta(days=3)
        return self.filter(
            notification_sent=False,
            status='pending',
            due_date__lte=notification_date,
            due_date__gte=today
        )
    
    def for_expected_collection(self, start_date, end_date):
        """Cuotas para cálculo de recaudo esperado"""
        return self.filter(
            due_date__range=[start_date, end_date],
            status__in=['pending', 'partial']
        )
    
    def high_risk_overdue(self, days_threshold=30):
        """Cuotas con alto riesgo de mora (más de X días)"""
        cutoff_date = timezone.now().date() - timedelta(days=days_threshold)
        return self.filter(
            status='overdue',
            due_date__lt=cutoff_date
        )
    
    def with_credit_details(self):
        """Annotate con detalles del crédito"""
        return self.select_related('credit__user', 'credit__currency')
    
    def summary_by_status(self):
        """Resumen de cuotas por estado"""
        return self.values('status').annotate(
            count=Count('id'),
            total_amount=Sum('amount'),
            total_remaining=Sum('remaining_amount')
        )
    
    def overdue_summary(self):
        """Resumen de cuotas vencidas"""
        return self.filter(status='overdue').aggregate(
            total_overdue=Count('id'),
            total_amount_overdue=Sum('remaining_amount'),
            total_fees=Sum('late_fee'),
            avg_days_overdue=Avg('days_overdue')
        ) 