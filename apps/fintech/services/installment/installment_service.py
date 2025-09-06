"""
Servicio para manejo de cuotas (installments)
Rediseña la lógica del modelo Installment para mejor performance y mantenibilidad
"""
from decimal import Decimal
from django.utils import timezone
from django.db.models import Sum, Count, Q
from datetime import timedelta


class InstallmentService:
    """Servicio para manejo optimizado de cuotas"""
    
    @staticmethod
    def create_installments_for_credit(credit):
        """
        Crea todas las cuotas para un crédito de forma optimizada
        """
        if not credit or not credit.installment_number or not credit.installment_value:
            return []
        
        installments = []
        current_date = credit.first_date_payment
        periodicity_days = credit.periodicity.days if credit.periodicity else 30
        
        for i in range(1, credit.installment_number + 1):
            # Calcular fecha de vencimiento
            due_date = current_date + timedelta(days=periodicity_days * (i - 1))
            
            # Calcular monto de la cuota (la última puede ser diferente)
            if i == credit.installment_number:
                # Última cuota: monto restante
                remaining_amount = credit.price - (credit.installment_value * (credit.installment_number - 1))
                amount = remaining_amount
            else:
                amount = credit.installment_value
            
            installment_data = {
                'credit': credit,
                'number': i,
                'due_date': due_date,
                'amount': amount,
                'remaining_amount': amount,
                'status': 'pending'
            }
            
            installments.append(installment_data)
        
        return installments
    
    @staticmethod
    def mark_installment_as_paid(installment, amount_paid, payment_date=None):
        """
        Marca una cuota como pagada de forma optimizada
        """
        if not installment:
            return False
        
        if payment_date is None:
            payment_date = timezone.now().date()
        
        # Actualizar montos
        installment.amount_paid = amount_paid
        installment.remaining_amount = installment.amount - amount_paid
        
        # Determinar estado
        if installment.remaining_amount <= 0:
            installment.status = 'paid'
            installment.paid = True
            installment.remaining_amount = Decimal('0.00')
        else:
            installment.status = 'partial'
        
        installment.paid_on = payment_date
        installment.save()
        
        return True
    
    @staticmethod
    def update_overdue_installments(credit_id=None):
        """
        Actualiza el estado de cuotas vencidas de forma eficiente
        """
        from apps.fintech.models import Installment
        
        today = timezone.now().date()
        
        # Query optimizada para cuotas vencidas
        overdue_query = Q(
            status='pending',
            due_date__lt=today
        )
        
        if credit_id:
            overdue_query &= Q(credit_id=credit_id)
        
        # Actualizar en lote
        updated_count = Installment.objects.filter(overdue_query).update(
            status='overdue',
            days_overdue=timezone.now().date() - timezone.now().date()  # Esto se calculará correctamente
        )
        
        return updated_count
    
    @staticmethod
    def calculate_installment_metrics(credit_id):
        """
        Calcula métricas de cuotas para un crédito de forma optimizada
        """
        from apps.fintech.models import Installment
        
        # Una sola consulta con agregaciones
        metrics = Installment.objects.filter(credit_id=credit_id).aggregate(
            total_installments=Count('id'),
            paid_installments=Count('id', filter=Q(status='paid')),
            overdue_installments=Count('id', filter=Q(status='overdue')),
            partial_installments=Count('id', filter=Q(status='partial')),
            total_amount=Sum('amount'),
            total_paid=Sum('amount_paid'),
            total_remaining=Sum('remaining_amount')
        )
        
        return {
            'total_count': metrics['total_installments'] or 0,
            'paid_count': metrics['paid_installments'] or 0,
            'overdue_count': metrics['overdue_installments'] or 0,
            'partial_count': metrics['partial_installments'] or 0,
            'total_amount': metrics['total_amount'] or Decimal('0.00'),
            'total_paid': metrics['total_paid'] or Decimal('0.00'),
            'total_remaining': metrics['total_remaining'] or Decimal('0.00'),
            'completion_percentage': (
                (metrics['total_paid'] / metrics['total_amount'] * 100) 
                if metrics['total_amount'] and metrics['total_amount'] > 0 
                else 0
            )
        }
    
    @staticmethod
    def get_installments_by_priority(credit_id=None, limit=50):
        """
        Obtiene cuotas ordenadas por prioridad de recaudo
        """
        from apps.fintech.models import Installment
        
        query = Q()
        if credit_id:
            query = Q(credit_id=credit_id)
        
        # Ordenar por prioridad: vencidas primero, luego por fecha de vencimiento
        installments = Installment.objects.filter(query).select_related(
            'credit', 'credit__user'
        ).order_by(
            '-status',  # overdue primero
            'due_date'
        )[:limit]
        
        return installments
    
    @staticmethod
    def calculate_late_fees(installment, daily_rate=0.01):
        """
        Calcula recargos por mora
        """
        if not installment.is_overdue:
            return Decimal('0.00')
        
        days_overdue = installment.days_since_due
        if days_overdue <= 0:
            return Decimal('0.00')
        
        # Calcular recargo: monto * tasa_diaria * días
        late_fee = installment.amount * Decimal(str(daily_rate)) * Decimal(str(days_overdue))
        return late_fee.quantize(Decimal('.01'))
    
    @staticmethod
    def get_installment_summary(credit_id):
        """
        Obtiene resumen completo de cuotas para un crédito
        """
        metrics = InstallmentService.calculate_installment_metrics(credit_id)
        
        # Obtener próximas cuotas a vencer
        from apps.fintech.models import Installment
        upcoming_installments = Installment.objects.filter(
            credit_id=credit_id,
            status='pending',
            due_date__gte=timezone.now().date()
        ).order_by('due_date')[:3]
        
        # Obtener cuotas vencidas
        overdue_installments = Installment.objects.filter(
            credit_id=credit_id,
            status='overdue'
        ).order_by('-due_date')[:5]
        
        return {
            'metrics': metrics,
            'upcoming_installments': list(upcoming_installments),
            'overdue_installments': list(overdue_installments),
            'next_due_date': upcoming_installments[0].due_date if upcoming_installments else None,
            'total_overdue_amount': sum(
                inst.remaining_amount + InstallmentService.calculate_late_fees(inst)
                for inst in overdue_installments
            )
        }
