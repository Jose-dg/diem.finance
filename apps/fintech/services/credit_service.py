from decimal import Decimal
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response

from apps.fintech.models import Credit, Transaction, SubCategory, AccountMethodAmount
from apps.fintech.utils.root import recalculate_credit


class CreditService:
    """Service class for credit-related business logic"""
    
    @staticmethod
    def create_transaction_from_payment(credit_uid, amount, description, user_id, subcategory_name, payment_type):
        """
        Creates a transaction from a credit payment
        """
        try:
            # Validate credit exists
            credit = get_object_or_404(Credit, uid=credit_uid)
            
            # Validate amount
            if amount <= 0:
                return False, "El monto debe ser mayor a 0", status.HTTP_400_BAD_REQUEST
            
            # Find subcategory
            try:
                subcategory = SubCategory.objects.get(name=subcategory_name)
            except ObjectDoesNotExist:
                return False, f"No se encontró una subcategoría con nombre {subcategory_name}", status.HTTP_400_BAD_REQUEST
            
            # Create transaction
            with transaction.atomic():
                transaction_obj = Transaction.objects.create(
                    transaction_type="income",
                    description=description or f"Pago registrado: {payment_type}",
                    category=subcategory,
                    user_id=user_id,
                    source="admin"
                )
                
                # Create payment method amount
                AccountMethodAmount.objects.create(
                    payment_method_id=1,  # Default payment method
                    payment_code=f"PAY_{transaction_obj.uid}",
                    amount=amount,
                    amount_paid=amount,
                    credit=credit,
                    transaction=transaction_obj
                )
                
                # Update credit totals
                credit.update_total_abonos(amount)
                
                # Recalculate credit status
                recalculate_credit(credit)
                
                return True, transaction_obj, status.HTTP_201_CREATED
                
        except Exception as e:
            return False, str(e), status.HTTP_500_INTERNAL_SERVER_ERROR
    
    @staticmethod
    def get_credit_summary(credit_uid):
        """
        Gets comprehensive credit summary
        """
        try:
            credit = get_object_or_404(Credit, uid=credit_uid)
            
            # Get payments
            payments = AccountMethodAmount.objects.filter(credit=credit).select_related('payment_method', 'transaction')
            
            # Calculate metrics
            total_paid = sum(payment.amount_paid for payment in payments)
            remaining_amount = credit.price - total_paid
            
            return {
                'credit': credit,
                'payments': payments,
                'total_paid': total_paid,
                'remaining_amount': remaining_amount,
                'payment_count': payments.count()
            }
            
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def update_credit_status(credit_uid):
        """
        Updates credit status and recalculates metrics
        """
        try:
            credit = get_object_or_404(Credit, uid=credit_uid)
            recalculate_credit(credit)
            return True, "Crédito actualizado exitosamente"
        except Exception as e:
            return False, str(e) 