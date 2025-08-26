"""
Helpers para el dashboard de insights
"""
from django.db.models import Q, Count, Sum, Avg, F, ExpressionWrapper, DecimalField
from django.utils import timezone
from django.db.models.functions import Coalesce, ExtractDay
from decimal import Decimal
from datetime import timedelta
import math

def get_optimized_credit_queryset():
    """Retorna un queryset optimizado para créditos con todas las relaciones necesarias"""
    from apps.fintech.models import Credit
    
    return Credit.objects.select_related(
        'user',
        'user__document',
        'user__phone_1',
        'currency',
        'subcategory',
        'periodicity',
        'seller__user',
        'payment'
    ).prefetch_related(
        'installments'
    ).annotate(
        paid_installments_count=Count(
            'installments', 
            filter=Q(installments__status='paid')
        ),
        overdue_installments_count=Count(
            'installments', 
            filter=Q(installments__status='overdue')
        ),
        total_installments_count=Count('installments')
    ).order_by('-created_at')

def get_optimized_installment_queryset():
    """Retorna un queryset optimizado para cuotas con todas las relaciones necesarias"""
    from apps.fintech.models import Installment
    
    return Installment.objects.select_related(
        'credit',
        'credit__user',
        'credit__currency',
        'credit__subcategory',
        'credit__periodicity'
    ).annotate(
        days_until_due=ExpressionWrapper(
            F('due_date') - timezone.now().date(),
            output_field=DecimalField()
        ),
        is_overdue=ExpressionWrapper(
            Q(due_date__lt=timezone.now().date()) & Q(status='pending'),
            output_field=DecimalField()
        )
    ).order_by('due_date')

def get_next_due_date(credit):
    """Obtiene la próxima fecha de vencimiento de cuota pendiente"""
    next_installment = credit.installments.filter(
        status='pending'
    ).order_by('due_date').first()
    
    return next_installment.due_date if next_installment else None

def get_credit_days(credit):
    """Calcula los días totales del crédito"""
    if credit.first_date_payment and credit.second_date_payment:
        return (credit.second_date_payment - credit.first_date_payment).days
    return credit.credit_days or 0

def get_interest_rate(credit):
    """Calcula la tasa de interés del crédito"""
    if credit.interest:
        return float(credit.interest)
    
    # Calcular tasa de interés basada en earnings y cost
    if credit.cost and credit.cost > 0:
        return float((credit.earnings / credit.cost) * 100)
    
    return 0

def get_payment_method_name(credit):
    """Obtiene el nombre del método de pago"""
    if credit.payment:
        return credit.payment.name
    return "No especificado"

def get_seller_info(credit):
    """Obtiene información del vendedor"""
    if credit.seller and credit.seller.user:
        seller_name = f"{credit.seller.user.first_name} {credit.seller.user.last_name}".strip()
        if not seller_name:
            seller_name = credit.seller.user.username
        return {
            'seller_name': seller_name,
            'seller_id': str(credit.seller.user.id_user)
        }
    return {
        'seller_name': "No asignado",
        'seller_id': None
    }

def get_client_info(user):
    """Obtiene información del cliente"""
    full_name = f"{user.first_name} {user.last_name}".strip()
    if not full_name:
        full_name = user.username
    
    document_number = user.document.document_number if user.document else "No especificado"
    
    phone = ""
    if user.phone_1:
        phone = f"{user.phone_1.country_code} {user.phone_1.phone_number}"
    
    return {
        'id': str(user.id_user),
        'full_name': full_name,
        'username': user.username,
        'document_number': document_number,
        'phone': phone
    }

def get_credit_details(credit):
    """Obtiene detalles del crédito"""
    return {
        'subcategory': credit.subcategory.name if credit.subcategory else "No especificado",
        'price': str(credit.price),
        'cost': str(credit.cost),
        'earnings': str(credit.earnings),
        'currency': credit.currency.currency if credit.currency else "COP",
        'state': credit.state,
        'morosidad_level': credit.morosidad_level,
        'created_at': credit.created_at.isoformat()
    }

def get_payment_info(credit):
    """Obtiene información de pagos del crédito"""
    percentage_paid = 0
    if credit.price and credit.price > 0:
        percentage_paid = (credit.total_abonos / credit.price) * 100
    
    return {
        'total_abonos': str(credit.total_abonos),
        'pending_amount': str(credit.pending_amount),
        'percentage_paid': round(percentage_paid, 2),
        'payment_method': get_payment_method_name(credit)
    }

def get_installment_info(credit):
    """Obtiene información de cuotas del crédito"""
    paid_installments = credit.installments.filter(status='paid').count()
    overdue_installments = credit.installments.filter(status='overdue').count()
    
    return {
        'periodicity_name': credit.periodicity.name if credit.periodicity else "No especificado",
        'periodicity_days': credit.periodicity.days if credit.periodicity else 0,
        'total_installments': credit.installment_number or 0,
        'installment_value': str(credit.installment_value) if credit.installment_value else "0.00",
        'paid_installments': paid_installments,
        'overdue_installments': overdue_installments,
        'next_due_date': get_next_due_date(credit)
    }

def get_calculated_metrics(credit, installments):
    """Obtiene métricas calculadas del crédito"""
    from .calculations import (
        calculate_days_since_creation,
        calculate_average_payment_delay,
        calculate_risk_score
    )
    
    return {
        'interest_rate': str(get_interest_rate(credit)),
        'credit_days': get_credit_days(credit),
        'days_since_creation': calculate_days_since_creation(credit.created_at),
        'average_payment_delay': round(calculate_average_payment_delay(installments), 1),
        'risk_score': round(calculate_risk_score(credit, installments), 1)
    }

def get_installment_details(installment):
    """Obtiene detalles de una cuota"""
    percentage_paid = 0
    if installment.amount and installment.amount > 0:
        percentage_paid = (installment.amount_paid / installment.amount) * 100
    
    return {
        'number': installment.number,
        'due_date': installment.due_date.isoformat() if installment.due_date else None,
        'amount': str(installment.amount) if installment.amount else "0.00",
        'amount_paid': str(installment.amount_paid),
        'remaining_amount': str(installment.remaining_amount),
        'status': installment.status,
        'late_fee': str(installment.late_fee) if installment.late_fee else "0.00",
        'percentage_paid': round(percentage_paid, 2)
    }

def get_payment_tracking(installment):
    """Obtiene información de seguimiento de pagos de una cuota"""
    days_overdue = 0
    is_overdue = False
    
    if installment.due_date:
        days_until_due = (installment.due_date - timezone.now().date()).days
        days_overdue = abs(days_until_due) if days_until_due < 0 else 0
        is_overdue = days_until_due < 0 and installment.status == 'pending'
    
    return {
        'paid_on': installment.paid_on.isoformat() if installment.paid_on else None,
        'days_overdue': days_overdue,
        'is_overdue': is_overdue,
        'principal_amount': str(installment.principal_amount) if installment.principal_amount else "0.00",
        'interest_amount': str(installment.interest_amount) if installment.interest_amount else "0.00"
    }

def get_periodicity_info(credit):
    """Obtiene información de periodicidad"""
    return {
        'periodicity_name': credit.periodicity.name if credit.periodicity else "No especificado",
        'periodicity_days': credit.periodicity.days if credit.periodicity else 0,
        'currency': credit.currency.currency if credit.currency else "COP"
    }

def get_calculated_installment_metrics(installment, client_history):
    """Obtiene métricas calculadas de una cuota"""
    from .calculations import (
        calculate_collection_priority,
        calculate_expected_collection_date,
        calculate_risk_level,
        calculate_payment_reliability
    )
    
    days_until_due = 0
    if installment.due_date:
        days_until_due = (installment.due_date - timezone.now().date()).days
    
    return {
        'days_until_due': days_until_due,
        'collection_priority': calculate_collection_priority(installment),
        'expected_collection_date': calculate_expected_collection_date(installment, client_history),
        'risk_level': calculate_risk_level(installment, client_history),
        'payment_reliability': calculate_payment_reliability(client_history)
    }

def get_client_history_for_installment(installment):
    """Obtiene el historial del cliente para una cuota específica"""
    from .calculations import get_client_history
    
    if installment.credit and installment.credit.user:
        return get_client_history(installment.credit.user)
    return {
        'total_overdue_installments': 0,
        'average_delay_days': 0
    }

def get_credit_info_for_installment(installment):
    """Obtiene información del crédito para una cuota"""
    if not installment.credit:
        return {
            'credit_uid': None,
            'client_full_name': "No asignado",
            'client_id': None,
            'subcategory': "No especificado",
            'credit_state': "No especificado"
        }
    
    credit = installment.credit
    client_name = f"{credit.user.first_name} {credit.user.last_name}".strip()
    if not client_name:
        client_name = credit.user.username
    
    return {
        'credit_uid': str(credit.uid),
        'client_full_name': client_name,
        'client_id': str(credit.user.id_user),
        'subcategory': credit.subcategory.name if credit.subcategory else "No especificado",
        'credit_state': credit.state
    }

def get_alerts():
    """Obtiene alertas del sistema"""
    from apps.fintech.models import Credit, Installment
    
    alerts = []
    
    # Créditos con más de 30 días de mora
    critical_overdue = Credit.objects.filter(
        morosidad_level__in=['severe_default', 'critical_default']
    ).count()
    
    if critical_overdue > 0:
        alerts.append({
            'type': 'high_risk',
            'message': f'{critical_overdue} créditos con más de 30 días de mora',
            'count': critical_overdue
        })
    
    # Cuotas vencidas sin pago
    overdue_installments = Installment.objects.filter(
        status='overdue',
        due_date__lt=timezone.now().date() - timedelta(days=7)
    ).count()
    
    if overdue_installments > 0:
        alerts.append({
            'type': 'overdue_payments',
            'message': f'{overdue_installments} cuotas vencidas por más de 7 días',
            'count': overdue_installments
        })
    
    # Créditos próximos a vencer
    upcoming_due = Installment.objects.filter(
        status='pending',
        due_date__range=[
            timezone.now().date(),
            timezone.now().date() + timedelta(days=3)
        ]
    ).count()
    
    if upcoming_due > 0:
        alerts.append({
            'type': 'upcoming_due',
            'message': f'{upcoming_due} cuotas vencen en los próximos 3 días',
            'count': upcoming_due
        })
    
    return alerts

def get_by_periodicity_metrics():
    """Obtiene métricas agrupadas por periodicidad"""
    from apps.fintech.models import Credit, Periodicity
    
    periodicity_data = []
    
    for periodicity in Periodicity.objects.all():
        credits = Credit.objects.filter(
            periodicity=periodicity,
            state='pending'
        )
        
        total_credits = credits.count()
        pending_amount = credits.aggregate(
            total=Coalesce(Sum('pending_amount'), 0)
        )['total'] or 0
        
        overdue_credits = credits.filter(
            morosidad_level__in=['mild_default', 'moderate_default', 'severe_default', 'critical_default']
        ).count()
        
        overdue_percentage = (overdue_credits / total_credits * 100) if total_credits > 0 else 0
        
        periodicity_data.append({
            'periodicity': periodicity.name,
            'total_credits': total_credits,
            'pending_amount': str(pending_amount),
            'overdue_percentage': round(overdue_percentage, 1)
        })
    
    return periodicity_data
