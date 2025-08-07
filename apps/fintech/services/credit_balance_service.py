from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from django.db.models import Sum
from typing import Dict, List, Tuple, Optional
import logging

from apps.fintech.models import Credit, Transaction, AccountMethodAmount, CreditAdjustment
from apps.fintech.utils.root import recalculate_credit

logger = logging.getLogger(__name__)

class CreditBalanceService:
    """
    Servicio centralizado para gestión de saldos de créditos
    Implementa mejores prácticas y validaciones robustas
    """
    
    @staticmethod
    def calculate_real_payments(credit: Credit) -> Decimal:
        """
        Calcula el total real de pagos confirmados para un crédito
        
        Args:
            credit: Crédito a analizar
            
        Returns:
            Decimal: Total de pagos confirmados
        """
        try:
            real_payments = Transaction.objects.filter(
                account_method_amounts__credit=credit,
                transaction_type='income',
                status='confirmed'
            ).aggregate(
                total=Sum('account_method_amounts__amount_paid')
            )['total'] or Decimal('0.00')
            
            return real_payments
        except Exception as e:
            logger.error(f"Error calculando pagos reales para crédito {credit.uid}: {str(e)}")
            return Decimal('0.00')
    
    @staticmethod
    def calculate_total_adjustments(credit: Credit) -> Decimal:
        """
        Calcula el total de ajustes para un crédito
        
        Args:
            credit: Crédito a analizar
            
        Returns:
            Decimal: Total de ajustes
        """
        try:
            total_adjustments = credit.adjustments.aggregate(
                total=Sum('amount')
            )['total'] or Decimal('0.00')
            
            return total_adjustments
        except Exception as e:
            logger.error(f"Error calculando ajustes para crédito {credit.uid}: {str(e)}")
            return Decimal('0.00')
    
    @staticmethod
    def calculate_expected_pending(credit: Credit) -> Decimal:
        """
        Calcula el saldo pendiente esperado basado en pagos reales
        
        Args:
            credit: Crédito a analizar
            
        Returns:
            Decimal: Saldo pendiente esperado
        """
        real_payments = CreditBalanceService.calculate_real_payments(credit)
        total_adjustments = CreditBalanceService.calculate_total_adjustments(credit)
        
        expected_pending = credit.price + total_adjustments - real_payments
        return expected_pending
    
    @staticmethod
    def validate_credit_balance(credit: Credit) -> Dict[str, any]:
        """
        Valida la consistencia del saldo de un crédito
        
        Args:
            credit: Crédito a validar
            
        Returns:
            Dict con información de validación
        """
        real_payments = CreditBalanceService.calculate_real_payments(credit)
        total_adjustments = CreditBalanceService.calculate_total_adjustments(credit)
        expected_pending = CreditBalanceService.calculate_expected_pending(credit)
        
        # Calcular diferencias
        abonos_difference = abs(credit.total_abonos - real_payments)
        pending_difference = abs(credit.pending_amount - expected_pending)
        
        is_consistent = (
            abonos_difference <= Decimal('0.01') and 
            pending_difference <= Decimal('0.01')
        )
        
        return {
            'is_consistent': is_consistent,
            'real_payments': real_payments,
            'total_adjustments': total_adjustments,
            'expected_pending': expected_pending,
            'abonos_difference': abonos_difference,
            'pending_difference': pending_difference,
            'current_total_abonos': credit.total_abonos,
            'current_pending_amount': credit.pending_amount
        }
    
    @staticmethod
    def fix_credit_balance(credit: Credit) -> Dict[str, any]:
        """
        Corrige el saldo de un crédito usando recalculate_credit
        
        Args:
            credit: Crédito a corregir
            
        Returns:
            Dict con información del resultado
        """
        try:
            # Guardar estado anterior
            old_state = {
                'total_abonos': credit.total_abonos,
                'pending_amount': credit.pending_amount,
                'is_in_default': credit.is_in_default,
                'morosidad_level': credit.morosidad_level
            }
            
            # Ejecutar recálculo
            with transaction.atomic():
                recalculate_credit(credit)
                credit.refresh_from_db()
            
            # Verificar cambios
            changes = {}
            for field, old_value in old_state.items():
                new_value = getattr(credit, field)
                if old_value != new_value:
                    changes[field] = {
                        'old': old_value,
                        'new': new_value
                    }
            
            return {
                'success': True,
                'changes': changes,
                'credit_uid': credit.uid
            }
            
        except Exception as e:
            logger.error(f"Error corrigiendo saldo del crédito {credit.uid}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'credit_uid': credit.uid
            }
    
    @staticmethod
    def process_payment_safely(credit: Credit, amount: Decimal, payment_date: Optional[timezone.datetime] = None) -> Dict[str, any]:
        """
        Procesa un pago de manera segura con validaciones completas
        
        Args:
            credit: Crédito a procesar
            amount: Monto del pago
            payment_date: Fecha del pago (opcional)
            
        Returns:
            Dict con resultado del procesamiento
        """
        try:
            with transaction.atomic():
                # Validaciones
                if amount <= 0:
                    return {
                        'success': False,
                        'error': 'El monto debe ser mayor a 0'
                    }
                
                if amount > credit.pending_amount:
                    return {
                        'success': False,
                        'error': f'El monto excede el saldo pendiente (${credit.pending_amount:,.2f})'
                    }
                
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
                
                # Recalcular crédito de manera segura
                recalculate_credit(credit)
                credit.refresh_from_db()
                
                # Validar que el pago se procesó correctamente
                validation = CreditBalanceService.validate_credit_balance(credit)
                
                return {
                    'success': True,
                    'transaction': transaction_obj,
                    'payment_method': payment_method,
                    'remaining_amount': credit.pending_amount,
                    'validation': validation
                }
                
        except Exception as e:
            logger.error(f"Error procesando pago para crédito {credit.uid}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def get_credit_summary(credit: Credit) -> Dict[str, any]:
        """
        Obtiene un resumen completo del estado de un crédito
        
        Args:
            credit: Crédito a analizar
            
        Returns:
            Dict con resumen completo
        """
        validation = CreditBalanceService.validate_credit_balance(credit)
        
        return {
            'credit_uid': credit.uid,
            'user': str(credit.user),
            'price': float(credit.price),
            'cost': float(credit.cost),
            'state': credit.state,
            'is_in_default': credit.is_in_default,
            'morosidad_level': credit.morosidad_level,
            'validation': validation,
            'transactions_count': Transaction.objects.filter(
                account_method_amounts__credit=credit,
                transaction_type='income',
                status='confirmed'
            ).count(),
            'adjustments_count': credit.adjustments.count(),
            'installments_count': credit.installments.count()
        }
    
    @staticmethod
    def batch_validate_credits(credits: List[Credit]) -> Dict[str, any]:
        """
        Valida un lote de créditos
        
        Args:
            credits: Lista de créditos a validar
            
        Returns:
            Dict con resultados de validación
        """
        results = {
            'total_credits': len(credits),
            'consistent_credits': 0,
            'inconsistent_credits': 0,
            'errors': 0,
            'details': []
        }
        
        for credit in credits:
            try:
                validation = CreditBalanceService.validate_credit_balance(credit)
                
                if validation['is_consistent']:
                    results['consistent_credits'] += 1
                else:
                    results['inconsistent_credits'] += 1
                
                results['details'].append({
                    'credit_uid': credit.uid,
                    'user': str(credit.user),
                    'validation': validation
                })
                
            except Exception as e:
                results['errors'] += 1
                logger.error(f"Error validando crédito {credit.uid}: {str(e)}")
        
        return results 