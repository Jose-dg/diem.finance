from decimal import Decimal
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from datetime import timedelta
from django.db.models import F

from apps.fintech.models import Credit, Transaction, SubCategory, AccountMethodAmount, Installment
from apps.fintech.utils.root import recalculate_credit


class CreditService:
    """Service class for credit-related business logic"""
    
    @staticmethod
    def create_credit(user, amount, terms, **kwargs):
        """
        Creación integral de crédito con validaciones completas
        
        Args:
            user: Usuario del crédito
            amount: Monto del crédito
            terms: Plazo en días
            **kwargs: Parámetros adicionales (currency, periodicity, etc.)
        
        Returns:
            tuple: (success, result, status_code)
        """
        try:
            with transaction.atomic():
                # Validaciones básicas
                if amount <= 0:
                    return False, "El monto debe ser mayor a 0", status.HTTP_400_BAD_REQUEST
                
                if terms <= 0:
                    return False, "El plazo debe ser mayor a 0", status.HTTP_400_BAD_REQUEST
                
                # Calcular costos y ganancias
                cost = amount * Decimal('0.8')  # 80% del monto como costo
                price = amount
                earnings = price - cost
                
                # Crear crédito
                credit = Credit.objects.create(
                    user=user,
                    cost=cost,
                    price=price,
                    earnings=earnings,
                    credit_days=terms,
                    pending_amount=price,
                    **kwargs
                )
                
                # Generar cuotas automáticamente
                InstallmentService.generate_installments_for_credit(credit)
                
                return True, credit, status.HTTP_201_CREATED
                
        except Exception as e:
            return False, str(e), status.HTTP_500_INTERNAL_SERVER_ERROR
    
    @staticmethod
    def process_payment(credit, amount, payment_date=None):
        """
        Procesamiento completo de pagos con validaciones
        
        Args:
            credit: Crédito a procesar
            amount: Monto del pago
            payment_date: Fecha del pago (opcional)
        
        Returns:
            tuple: (success, result, status_code)
        """
        try:
            with transaction.atomic():
                # Validaciones
                if amount <= 0:
                    return False, "El monto debe ser mayor a 0", status.HTTP_400_BAD_REQUEST
                
                if amount > credit.pending_amount:
                    return False, "El monto excede el saldo pendiente", status.HTTP_400_BAD_REQUEST
                
                # Usar fecha actual si no se proporciona
                if not payment_date:
                    payment_date = timezone.now()
                
                # Crear transacción
                transaction_obj = Transaction.objects.create(
                    transaction_type="income",
                    user=credit.user,
                    category=credit.subcategory,
                    description=f"Pago de crédito {credit.uid}",
                    date=payment_date,
                    source="admin"
                )
                
                # Crear método de pago
                payment_method = AccountMethodAmount.objects.create(
                    payment_method=credit.payment,
                    payment_code=f"PAY_{transaction_obj.uid}",
                    amount=amount,
                    amount_paid=amount,
                    credit=credit,
                    transaction=transaction_obj
                )
                
                # Actualizar crédito
                credit.update_total_abonos(amount)
                credit.update_pending_amount()
                
                # Procesar cuotas
                InstallmentService.distribute_payment_to_installments(credit, amount, payment_date)
                
                # Recalcular estado
                recalculate_credit(credit)
                
                return True, {
                    'transaction': transaction_obj,
                    'payment_method': payment_method,
                    'remaining_amount': credit.pending_amount
                }, status.HTTP_200_OK
                
        except Exception as e:
            return False, str(e), status.HTTP_500_INTERNAL_SERVER_ERROR
    
    @staticmethod
    def calculate_late_fees(credit):
        """
        Cálculo de mora para un crédito
        
        Args:
            credit: Crédito a calcular
        
        Returns:
            Decimal: Monto de mora
        """
        total_late_fees = Decimal('0.00')
        
        for installment in credit.installments.filter(status='overdue'):
            if installment.days_overdue > 0:
                # 5% por mes de mora
                months_overdue = installment.days_overdue / 30
                late_fee = installment.remaining_amount * Decimal('0.05') * Decimal(str(months_overdue))
                total_late_fees += late_fee
        
        return total_late_fees
    
    @staticmethod
    def update_credit_status(credit):
        """
        Actualización completa del estado de un crédito
        
        Args:
            credit: Crédito a actualizar
        
        Returns:
            tuple: (success, message)
        """
        try:
            with transaction.atomic():
                # Actualizar estados de cuotas
                InstallmentService.update_credit_installment_statuses(credit)
                
                # Verificar condiciones de mora
                CreditService.check_default_conditions(credit)
                
                # Recalcular métricas
                recalculate_credit(credit)
                
                return True, "Crédito actualizado exitosamente"
                
        except Exception as e:
            return False, f"Error actualizando crédito: {str(e)}"
    
    @staticmethod
    def check_default_conditions(credit):
        """
        Verificación de condiciones de morosidad
        
        Args:
            credit: Crédito a verificar
        """
        # Contar cuotas vencidas
        overdue_installments = credit.installments.filter(status='overdue')
        total_overdue_days = sum(i.days_overdue for i in overdue_installments)
        
        # Determinar nivel de morosidad
        if total_overdue_days >= 120:
            credit.morosidad_level = 'critica'
        elif total_overdue_days >= 90:
            credit.morosidad_level = 'alta'
        elif total_overdue_days >= 60:
            credit.morosidad_level = 'moderada'
        elif total_overdue_days >= 30:
            credit.morosidad_level = 'leve'
        else:
            credit.morosidad_level = 'al_dia'
        
        # Marcar como en mora si hay cuotas vencidas
        credit.is_in_default = overdue_installments.exists()
        
        credit.save(update_fields=['morosidad_level', 'is_in_default'])
    
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
    
    @staticmethod
    def get_credit_metrics(credit):
        """
        Obtiene métricas completas de un crédito
        
        Args:
            credit: Crédito a analizar
        
        Returns:
            dict: Métricas del crédito
        """
        installments = credit.installments.all()
        payments = AccountMethodAmount.objects.filter(credit=credit)
        
        total_paid = sum(p.amount_paid for p in payments)
        overdue_installments = installments.filter(status='overdue')
        
        return {
            'total_amount': credit.price,
            'total_paid': total_paid,
            'remaining_amount': credit.pending_amount,
            'installment_count': installments.count(),
            'paid_installments': installments.filter(status='paid').count(),
            'overdue_installments': overdue_installments.count(),
            'total_overdue_days': sum(i.days_overdue for i in overdue_installments),
            'late_fees': CreditService.calculate_late_fees(credit),
            'morosidad_level': credit.morosidad_level,
            'is_in_default': credit.is_in_default
        } 

    @staticmethod
    def reconcile_transaction(transaction):
        """
        Reconcilia una transacción huérfana con su crédito correspondiente
        """
        try:
            # Buscar el crédito relacionado con esta transacción
            credit = None
            
            # Intentar encontrar por AccountMethodAmount
            account_method = transaction.account_method_amounts.first()
            if account_method and account_method.credit:
                credit = account_method.credit
            else:
                # Buscar por descripción o monto
                amount = getattr(transaction, 'amount', 0)
                if amount > 0:
                    # Buscar créditos que coincidan con el monto
                    matching_credits = Credit.objects.filter(
                        total_abonos__lt=F('price'),
                        price__gte=amount
                    )
                    if matching_credits.exists():
                        credit = matching_credits.first()
            
            if not credit:
                return False, "No se pudo encontrar el crédito relacionado"
            
            # Crear AccountMethodAmount si no existe
            if not transaction.account_method_amounts.exists():
                payment_method = credit.payment
                
                AccountMethodAmount.objects.create(
                    payment_method=payment_method,
                    payment_code=f"REC_{transaction.uid}",
                    amount=amount,
                    amount_paid=amount,
                    credit=credit,
                    transaction=transaction
                )
            
            # Actualizar el crédito
            success, message = CreditService.update_credit_status(credit)
            
            if success:
                return True, f"Transacción reconciliada con crédito {credit.uid}"
            else:
                return False, f"Error actualizando crédito: {message}"
                
        except Exception as e:
            return False, f"Error reconciliando transacción: {str(e)}" 