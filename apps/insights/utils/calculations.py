"""
Utilidades para cálculos complejos del dashboard de insights
"""
from django.db.models import Q, Count, Sum, Avg, F, ExpressionWrapper, DecimalField
from django.utils import timezone
from django.db.models.functions import Coalesce, ExtractDay
from decimal import Decimal
from datetime import timedelta
import math

def calculate_percentage_paid(total_abonos, price):
    """Calcula el porcentaje pagado de un crédito"""
    if price and price > 0:
        return (total_abonos / price) * 100
    return 0

def calculate_days_since_creation(created_at):
    """Calcula los días transcurridos desde la creación"""
    if created_at:
        return (timezone.now() - created_at).days
    return 0

def calculate_average_payment_delay(installments):
    """Calcula el promedio de días de retraso en pagos"""
    overdue_installments = installments.filter(
        status='overdue',
        paid_on__isnull=False
    )
    
    if overdue_installments.exists():
        total_delay = 0
        count = 0
        
        for installment in overdue_installments:
            if installment.due_date and installment.paid_on:
                delay = (installment.paid_on - installment.due_date).days
                if delay > 0:
                    total_delay += delay
                    count += 1
        
        return total_delay / count if count > 0 else 0
    
    return 0

def calculate_risk_score(credit, installments):
    """Calcula la puntuación de riesgo basada en mora y pagos"""
    score = 50  # Puntuación base
    
    # Factor por nivel de morosidad
    morosidad_factors = {
        'on_time': 0,
        'mild_default': -10,
        'moderate_default': -20,
        'severe_default': -30,
        'recurrent_default': -40,
        'critical_default': -50
    }
    
    score += morosidad_factors.get(credit.morosidad_level, 0)
    
    # Factor por cuotas vencidas
    overdue_count = installments.filter(status='overdue').count()
    score -= overdue_count * 5
    
    # Factor por porcentaje pagado
    percentage_paid = calculate_percentage_paid(credit.total_abonos, credit.price)
    if percentage_paid < 25:
        score -= 20
    elif percentage_paid < 50:
        score -= 10
    elif percentage_paid > 75:
        score += 10
    
    # Factor por días desde creación
    days_since_creation = calculate_days_since_creation(credit.created_at)
    if days_since_creation > 365:
        score -= 10
    
    return max(0, min(100, score))

def calculate_collection_priority(installment):
    """Calcula la prioridad de recaudo de una cuota"""
    if not installment.due_date:
        return 'low'
    
    days_until_due = (installment.due_date - timezone.now().date()).days
    
    # Alta prioridad si está vencida o vence en menos de 3 días
    if days_until_due < 0 or days_until_due <= 3:
        return 'high'
    
    # Media prioridad si vence en menos de 7 días
    if days_until_due <= 7:
        return 'medium'
    
    return 'low'

def calculate_expected_collection_date(installment, client_history):
    """Calcula la fecha esperada de recaudo basada en historial"""
    if not installment.due_date:
        return None
    
    # Si ya está pagada, retornar fecha de pago
    if installment.status == 'paid' and installment.paid_on:
        return installment.paid_on
    
    # Calcular promedio de días de retraso del cliente
    avg_delay = client_history.get('average_delay_days', 0)
    
    # Fecha esperada = fecha de vencimiento + promedio de retraso
    expected_date = installment.due_date + timedelta(days=avg_delay)
    
    return expected_date

def calculate_risk_level(installment, client_history):
    """Calcula el nivel de riesgo de no pago"""
    risk_factors = 0
    
    # Factor por estado de la cuota
    if installment.status == 'overdue':
        risk_factors += 30
    
    # Factor por historial del cliente
    total_overdue = client_history.get('total_overdue_installments', 0)
    if total_overdue > 5:
        risk_factors += 25
    elif total_overdue > 2:
        risk_factors += 15
    
    # Factor por monto
    if installment.amount and installment.amount > 500000:  # Más de 500k
        risk_factors += 10
    
    # Factor por días de retraso
    if installment.days_overdue > 30:
        risk_factors += 20
    elif installment.days_overdue > 15:
        risk_factors += 10
    
    # Clasificar nivel de riesgo
    if risk_factors >= 50:
        return 'high'
    elif risk_factors >= 25:
        return 'medium'
    else:
        return 'low'

def calculate_payment_reliability(client_history):
    """Calcula la confiabilidad de pago del cliente"""
    total_overdue = client_history.get('total_overdue_installments', 0)
    avg_delay = client_history.get('average_delay_days', 0)
    
    if total_overdue == 0 and avg_delay == 0:
        return 'high'
    elif total_overdue <= 2 and avg_delay <= 3:
        return 'medium'
    else:
        return 'low'

def get_client_history(user):
    """Obtiene el historial de pagos de un cliente"""
    from apps.fintech.models import Installment
    
    # Obtener todas las cuotas del cliente
    client_installments = Installment.objects.filter(
        credit__user=user
    )
    
    # Cuotas vencidas
    total_overdue = client_installments.filter(status='overdue').count()
    
    # Calcular promedio de días de retraso
    overdue_paid = client_installments.filter(
        status='overdue',
        paid_on__isnull=False
    )
    
    total_delay = 0
    count = 0
    
    for installment in overdue_paid:
        if installment.due_date and installment.paid_on:
            delay = (installment.paid_on - installment.due_date).days
            if delay > 0:
                total_delay += delay
                count += 1
    
    average_delay_days = total_delay / count if count > 0 else 0
    
    return {
        'total_overdue_installments': total_overdue,
        'average_delay_days': average_delay_days
    }

def calculate_performance_metrics():
    """Calcula métricas de rendimiento generales"""
    from apps.fintech.models import Credit, Installment
    
    # Créditos activos
    active_credits = Credit.objects.filter(state='pending')
    total_active_credits = active_credits.count()
    
    # Montos totales
    total_amount_lent = active_credits.aggregate(
        total=Coalesce(Sum('price'), 0)
    )['total'] or 0
    
    total_pending_amount = active_credits.aggregate(
        total=Coalesce(Sum('pending_amount'), 0)
    )['total'] or 0
    
    total_collected = total_amount_lent - total_pending_amount
    
    # Cuotas
    due_today = Installment.objects.filter(
        due_date=timezone.now().date(),
        status='pending'
    ).count()
    
    due_this_week = Installment.objects.filter(
        due_date__range=[
            timezone.now().date(),
            timezone.now().date() + timedelta(days=7)
        ],
        status='pending'
    ).count()
    
    overdue_total = Installment.objects.filter(
        status='overdue'
    ).count()
    
    # Tasas de rendimiento
    on_time_payments = Installment.objects.filter(
        status='paid',
        paid_on__lte=F('due_date')
    ).count()
    
    total_paid = Installment.objects.filter(status='paid').count()
    on_time_payment_rate = (on_time_payments / total_paid * 100) if total_paid > 0 else 0
    
    # Promedio de días de retraso
    overdue_paid = Installment.objects.filter(
        status='paid',
        paid_on__gt=F('due_date')
    )
    
    total_delay = 0
    count = 0
    
    for installment in overdue_paid:
        if installment.due_date and installment.paid_on:
            delay = (installment.paid_on - installment.due_date).days
            if delay > 0:
                total_delay += delay
                count += 1
    
    average_delay_days = total_delay / count if count > 0 else 0
    
    return {
        'total_active_credits': total_active_credits,
        'total_amount_lent': total_amount_lent,
        'total_pending_amount': total_pending_amount,
        'total_collected': total_collected,
        'average_credit_amount': total_amount_lent / total_active_credits if total_active_credits > 0 else 0,
        'collection_percentage': (total_collected / total_amount_lent * 100) if total_amount_lent > 0 else 0,
        'due_today': due_today,
        'due_this_week': due_this_week,
        'overdue_total': overdue_total,
        'on_time_payment_rate': on_time_payment_rate,
        'average_delay_days': average_delay_days
    }
