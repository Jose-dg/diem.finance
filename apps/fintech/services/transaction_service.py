from decimal import Decimal
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status

from apps.fintech.models import (
    Transaction, AccountMethodAmount, Credit, SubCategory, Account
)


class TransactionService:
    """Service class for transaction-related business logic"""
    
    @staticmethod
    def create_payment_transaction(credit, amount, method, **kwargs):
        """
        Crear transacción de pago completa
        
        Args:
            credit: Crédito asociado
            amount: Monto del pago
            method: Método de pago
            **kwargs: Parámetros adicionales
        
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
                
                # Crear transacción
                transaction_obj = Transaction.objects.create(
                    transaction_type="income",
                    user=credit.user,
                    category=credit.subcategory,
                    description=kwargs.get('description', f"Pago de crédito {credit.uid}"),
                    date=kwargs.get('date', timezone.now()),
                    source=kwargs.get('source', 'admin'),
                    status='confirmed'
                )
                
                # Crear método de pago
                payment_method = AccountMethodAmount.objects.create(
                    payment_method=method,
                    payment_code=kwargs.get('payment_code', f"PAY_{transaction_obj.uid}"),
                    amount=amount,
                    amount_paid=amount,
                    credit=credit,
                    transaction=transaction_obj
                )
                
                # Actualizar crédito
                credit.update_total_abonos(amount)
                credit.update_pending_amount()
                credit.save()
                
                return True, {
                    'transaction': transaction_obj,
                    'payment_method': payment_method
                }, status.HTTP_201_CREATED
                
        except Exception as e:
            return False, str(e), status.HTTP_500_INTERNAL_SERVER_ERROR
    
    @staticmethod
    def reverse_transaction(transaction_id):
        """
        Reversar una transacción
        
        Args:
            transaction_id: ID de la transacción a reversar
        
        Returns:
            tuple: (success, result, status_code)
        """
        try:
            with transaction.atomic():
                transaction_obj = get_object_or_404(Transaction, id=transaction_id)
                
                # Verificar que la transacción sea reversible
                if transaction_obj.status != 'confirmed':
                    return False, "La transacción no puede ser reversada", status.HTTP_400_BAD_REQUEST
                
                # Obtener método de pago asociado
                payment_method = AccountMethodAmount.objects.filter(
                    transaction=transaction_obj
                ).first()
                
                if not payment_method:
                    return False, "No se encontró método de pago asociado", status.HTTP_400_BAD_REQUEST
                
                # Reversar transacción
                transaction_obj.status = 'reversed'
                transaction_obj.save()
                
                # Actualizar crédito
                credit = payment_method.credit
                credit.update_total_abonos(-payment_method.amount_paid)
                credit.update_pending_amount()
                credit.save()
                
                # Crear transacción de reverso
                reversal_transaction = Transaction.objects.create(
                    transaction_type="expense",
                    user=transaction_obj.user,
                    category=transaction_obj.category,
                    description=f"Reverso de transacción {transaction_obj.uid}",
                    date=timezone.now(),
                    source='admin',
                    status='confirmed'
                )
                
                return True, {
                    'original_transaction': transaction_obj,
                    'reversal_transaction': reversal_transaction
                }, status.HTTP_200_OK
                
        except Exception as e:
            return False, str(e), status.HTTP_500_INTERNAL_SERVER_ERROR
    
    @staticmethod
    def reconcile_payments(credit):
        """
        Conciliar pagos de un crédito
        
        Args:
            credit: Crédito a conciliar
        
        Returns:
            tuple: (success, reconciliation_data)
        """
        try:
            # Obtener todas las transacciones del crédito
            payments = AccountMethodAmount.objects.filter(
                credit=credit,
                transaction__status='confirmed'
            ).select_related('transaction')
            
            # Calcular totales
            total_paid = sum(p.amount_paid for p in payments)
            expected_total = credit.price
            difference = total_paid - expected_total
            
            # Verificar conciliación
            is_reconciled = abs(difference) < Decimal('0.01')  # Tolerancia de 1 centavo
            
            reconciliation_data = {
                'total_paid': total_paid,
                'expected_total': expected_total,
                'difference': difference,
                'is_reconciled': is_reconciled,
                'payment_count': payments.count(),
                'payments': list(payments.values('amount_paid', 'transaction__date'))
            }
            
            return True, reconciliation_data
            
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_transaction_summary(credit):
        """
        Obtener resumen de transacciones de un crédito
        
        Args:
            credit: Crédito a analizar
        
        Returns:
            dict: Resumen de transacciones
        """
        try:
            transactions = Transaction.objects.filter(
                account_method_amounts__credit=credit
            ).distinct().select_related('category')
            
            payments = AccountMethodAmount.objects.filter(
                credit=credit
            ).select_related('payment_method', 'transaction')
            
            # Agrupar por tipo de transacción
            income_transactions = transactions.filter(transaction_type='income')
            expense_transactions = transactions.filter(transaction_type='expense')
            
            # Calcular totales
            total_income = sum(p.amount_paid for p in payments if p.transaction.transaction_type == 'income')
            total_expense = sum(p.amount_paid for p in payments if p.transaction.transaction_type == 'expense')
            
            return {
                'total_transactions': transactions.count(),
                'income_transactions': income_transactions.count(),
                'expense_transactions': expense_transactions.count(),
                'total_income': total_income,
                'total_expense': total_expense,
                'net_amount': total_income - total_expense,
                'transactions': list(transactions.values(
                    'transaction_type', 'amount', 'date', 'status', 'description'
                ))
            }
            
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def validate_transaction(transaction_data):
        """
        Validar datos de transacción
        
        Args:
            transaction_data: Datos de la transacción
        
        Returns:
            tuple: (is_valid, errors)
        """
        errors = []
        
        # Validar monto
        if 'amount' not in transaction_data or transaction_data['amount'] <= 0:
            errors.append("El monto debe ser mayor a 0")
        
        # Validar tipo de transacción
        if 'transaction_type' not in transaction_data:
            errors.append("El tipo de transacción es requerido")
        elif transaction_data['transaction_type'] not in ['income', 'expense']:
            errors.append("Tipo de transacción inválido")
        
        # Validar usuario
        if 'user_id' not in transaction_data:
            errors.append("El usuario es requerido")
        
        # Validar categoría
        if 'category_id' not in transaction_data:
            errors.append("La categoría es requerida")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def get_transaction_history(credit, start_date=None, end_date=None):
        """
        Obtener historial de transacciones de un crédito
        
        Args:
            credit: Crédito a consultar
            start_date: Fecha de inicio (opcional)
            end_date: Fecha de fin (opcional)
        
        Returns:
            QuerySet: Transacciones filtradas
        """
        transactions = Transaction.objects.filter(
            account_method_amounts__credit=credit
        ).distinct().select_related('category', 'user').order_by('-date')
        
        if start_date:
            transactions = transactions.filter(date__gte=start_date)
        
        if end_date:
            transactions = transactions.filter(date__lte=end_date)
        
        return transactions
    
    @staticmethod
    def calculate_payment_schedule(credit):
        """
        Calcular cronograma de pagos de un crédito
        
        Args:
            credit: Crédito a calcular
        
        Returns:
            list: Cronograma de pagos
        """
        installments = credit.installments.all().order_by('due_date')
        schedule = []
        
        for installment in installments:
            schedule.append({
                'installment_number': installment.number,
                'due_date': installment.due_date,
                'amount': installment.amount,
                'status': installment.status,
                'paid_amount': installment.amount_paid,
                'remaining_amount': installment.remaining_amount,
                'days_overdue': installment.days_overdue,
                'late_fee': installment.late_fee
            })
        
        return schedule 