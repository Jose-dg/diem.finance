from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from apps.fintech.models import Credit, CreditAdjustment, Adjustment


class CreditAdjustmentService:
    """Servicio para manejar ajustes de crédito, especialmente intereses adicionales"""
    
    ADDITIONAL_INTEREST_CODE = 'C0001'
    
    @classmethod
    def get_adjustment_type(cls):
        """Obtiene el tipo de ajuste para interés adicional"""
        try:
            return Adjustment.objects.get(code=cls.ADDITIONAL_INTEREST_CODE)
        except Adjustment.DoesNotExist:
            raise ValueError(f"Adjustment con código {cls.ADDITIONAL_INTEREST_CODE} no existe")
    
    @classmethod
    def calculate_additional_interest(cls, credit):
        """Calcula interés adicional basado en price - cost"""
        if credit.price <= credit.cost:
            return Decimal('0.00')
        
        # Interés adicional = price - cost
        additional_interest = credit.price - credit.cost
        
        # Verificar si ya se aplicó este ajuste
        existing_adjustment = CreditAdjustment.objects.filter(
            credit=credit,
            type__code=cls.ADDITIONAL_INTEREST_CODE
        ).first()
        
        if existing_adjustment:
            return existing_adjustment.amount
        
        return additional_interest
    
    @classmethod
    def should_apply_additional_interest(cls, credit):
        """Determina si se debe aplicar interés adicional"""
        # Calcular total pagado vs total pactado
        total_pactado = credit.price
        total_pagado = credit.total_abonos or Decimal('0.00')
        
        # Si no se ha pagado el monto pactado, aplicar interés
        return total_pagado < total_pactado
    
    @classmethod
    def apply_additional_interest(cls, credit, reason=None):
        """Aplica interés adicional al crédito"""
        additional_interest = cls.calculate_additional_interest(credit)
        
        if additional_interest > 0:
            # Verificar si ya existe el ajuste
            existing_adjustment = CreditAdjustment.objects.filter(
                credit=credit,
                type__code=cls.ADDITIONAL_INTEREST_CODE
            ).first()
            
            if existing_adjustment:
                return existing_adjustment.amount
            
            # Crear ajuste
            adjustment_type = cls.get_adjustment_type()
            
            with transaction.atomic():
                credit_adjustment = CreditAdjustment.objects.create(
                    credit=credit,
                    type=adjustment_type,
                    amount=additional_interest,
                    reason=reason or f"Interés adicional por incumplimiento. Price: {credit.price}, Cost: {credit.cost}"
                )
                
                # Actualizar pending_amount del crédito usando update_fields para evitar signals
                current_pending = credit.pending_amount or Decimal('0.00')
                credit.pending_amount = current_pending + additional_interest
                credit.save(update_fields=['pending_amount'])
                
                return credit_adjustment.amount
        
        return Decimal('0.00')
    
    @classmethod
    def get_total_adjustments(cls, credit):
        """Obtiene el total de ajustes aplicados al crédito"""
        adjustments = CreditAdjustment.objects.filter(credit=credit)
        
        total_positive = sum(adj.amount for adj in adjustments if adj.type.is_positive)
        total_negative = sum(adj.amount for adj in adjustments if not adj.type.is_positive)
        
        return total_positive - total_negative
    
    @classmethod
    def get_adjustment_history(cls, credit):
        """Obtiene el historial de ajustes del crédito"""
        return CreditAdjustment.objects.filter(credit=credit).order_by('-added_on')
    
    @classmethod
    def remove_adjustment(cls, credit_adjustment_id):
        """Elimina un ajuste específico"""
        try:
            adjustment = CreditAdjustment.objects.get(id=credit_adjustment_id)
            
            with transaction.atomic():
                # Revertir el pending_amount
                credit = adjustment.credit
                if adjustment.type.is_positive:
                    credit.pending_amount = (credit.pending_amount or Decimal('0.00')) - adjustment.amount
                else:
                    credit.pending_amount = (credit.pending_amount or Decimal('0.00')) + adjustment.amount
                
                credit.save(update_fields=['pending_amount'])
                adjustment.delete()
                
                return True
        except CreditAdjustment.DoesNotExist:
            return False
    
    @classmethod
    def apply_discount(cls, credit, amount, reason, discount_code='D0001'):
        """Aplica un descuento al crédito (pronto pago, etc.)"""
        try:
            discount_type = Adjustment.objects.get(code=discount_code)
        except Adjustment.DoesNotExist:
            raise ValueError(f"Adjustment con código {discount_code} no existe")
        
        with transaction.atomic():
            credit_adjustment = CreditAdjustment.objects.create(
                credit=credit,
                type=discount_type,
                amount=amount,
                reason=reason
            )
            
            # Actualizar pending_amount del crédito (descuento reduce el monto)
            current_pending = credit.pending_amount or Decimal('0.00')
            credit.pending_amount = max(Decimal('0.00'), current_pending - amount)
            credit.save(update_fields=['pending_amount'])
            
            return credit_adjustment.amount 