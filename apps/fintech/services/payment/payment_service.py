from decimal import Decimal
from django.utils import timezone
from django.contrib.auth import get_user_model
from typing import Dict, Optional, Tuple, Any
import logging

from apps.fintech.services.transaction.transaction_manager import TransactionManager
from apps.fintech.services.utils.audit.audit_logger import AuditLogger

User = get_user_model()
logger = logging.getLogger(__name__)

class PaymentService:
    """
    Servicio principal de pagos que integra transacciones y auditoría
    Maneja todas las operaciones de pago de manera segura y auditada
    """
    
    def __init__(self):
        self.transaction_manager = TransactionManager()
        self.audit_logger = AuditLogger()
    
    def process_payment(
        self,
        credit,
        amount: Decimal,
        payment_date: Optional[timezone.datetime] = None,
        user: Optional[User] = None,
        payment_method: Optional[str] = None,
        description: Optional[str] = None
    ) -> Tuple[bool, Dict[str, Any], str]:
        """
        Procesa un pago de manera segura y auditada
        
        Args:
            credit: Crédito a procesar
            amount: Monto del pago
            payment_date: Fecha del pago
            user: Usuario que ejecuta el pago
            payment_method: Método de pago
            description: Descripción del pago
            
        Returns:
            Tuple[bool, Dict, str]: (éxito, datos, mensaje)
        """
        # Validar contexto de transacción
        is_valid, validation_message = self.transaction_manager.validate_transaction_context(
            credit=credit,
            amount=amount
        )
        
        if not is_valid:
            self.audit_logger.log_error(
                'payment_validation_failed',
                validation_message,
                {'credit_uid': credit.uid, 'amount': float(amount)},
                user
            )
            return False, {}, validation_message
        
        # Crear instantánea antes de la transacción
        snapshot = self.transaction_manager.create_transaction_snapshot(
            credit_uid=credit.uid,
            amount=float(amount),
            user_id=user.id if user else None
        )
        
        # Log de inicio de operación
        self.audit_logger.log_payment_operation(
            'payment_started',
            credit,
            amount,
            user,
            {
                'payment_method': payment_method,
                'description': description,
                'payment_date': payment_date
            }
        )
        
        try:
            # Ejecutar transacción de pago
            success, result, message = self.transaction_manager.execute_payment_transaction(
                credit,
                amount,
                payment_date
            )
            
            if success:
                # Log de éxito
                self.audit_logger.log_payment_operation(
                    'payment_successful',
                    credit,
                    amount,
                    user,
                    {
                        'transaction_id': result.get('transaction_id'),
                        'payment_method': payment_method,
                        'description': description
                    }
                )
                
                # Log de cambio de saldo
                old_balance = credit.pending_amount
                credit.refresh_from_db()
                new_balance = credit.pending_amount
                
                if old_balance != new_balance:
                    self.audit_logger.log_balance_change(
                        credit,
                        old_balance,
                        new_balance,
                        f"Pago de ${amount:,.2f}",
                        user
                    )
                
                return True, result, message
            else:
                # Log de error
                self.audit_logger.log_error(
                    'payment_failed',
                    message,
                    {
                        'credit_uid': credit.uid,
                        'amount': float(amount),
                        'result': result
                    },
                    user
                )
                
                return False, result, message
                
        except Exception as e:
            # Log de excepción
            self.audit_logger.log_error(
                'payment_exception',
                str(e),
                {
                    'credit_uid': credit.uid,
                    'amount': float(amount)
                },
                user
            )
            
            # Intentar rollback
            self.transaction_manager.rollback_transaction(snapshot)
            
            return False, {}, f"Error procesando pago: {str(e)}"
    
    def process_refund(
        self,
        credit,
        amount: Decimal,
        reason: str,
        user: Optional[User] = None,
        original_transaction_id: Optional[str] = None
    ) -> Tuple[bool, Dict[str, Any], str]:
        """
        Procesa un reembolso
        
        Args:
            credit: Crédito a procesar
            amount: Monto del reembolso
            reason: Razón del reembolso
            user: Usuario que ejecuta el reembolso
            original_transaction_id: ID de la transacción original
            
        Returns:
            Tuple[bool, Dict, str]: (éxito, datos, mensaje)
        """
        # Validar que el reembolso no exceda el total de abonos
        if amount > credit.total_abonos:
            error_msg = f"El reembolso (${amount:,.2f}) excede el total de abonos (${credit.total_abonos:,.2f})"
            self.audit_logger.log_error(
                'refund_validation_failed',
                error_msg,
                {'credit_uid': credit.uid, 'amount': float(amount)},
                user
            )
            return False, {}, error_msg
        
        # Log de inicio de reembolso
        self.audit_logger.log_payment_operation(
            'refund_started',
            credit,
            amount,
            user,
            {
                'reason': reason,
                'original_transaction_id': original_transaction_id
            }
        )
        
        try:
            # Ejecutar transacción de reembolso (lógica similar a pago pero negativa)
            success, result, message = self.transaction_manager.execute_atomic_operation(
                self._refund_operation,
                f"refund_{credit.uid}_{amount}",
                credit,
                amount,
                reason,
                original_transaction_id
            )
            
            if success:
                self.audit_logger.log_payment_operation(
                    'refund_successful',
                    credit,
                    amount,
                    user,
                    result
                )
                return True, result, message
            else:
                self.audit_logger.log_error(
                    'refund_failed',
                    message,
                    {'credit_uid': credit.uid, 'amount': float(amount)},
                    user
                )
                return False, result, message
                
        except Exception as e:
            self.audit_logger.log_error(
                'refund_exception',
                str(e),
                {'credit_uid': credit.uid, 'amount': float(amount)},
                user
            )
            return False, {}, f"Error procesando reembolso: {str(e)}"
    
    def process_adjustment(
        self,
        credit,
        amount: Decimal,
        reason: str,
        adjustment_type: str = 'credit',  # credit o debit
        user: Optional[User] = None
    ) -> Tuple[bool, Dict[str, Any], str]:
        """
        Procesa un ajuste al crédito
        
        Args:
            credit: Crédito a procesar
            amount: Monto del ajuste
            reason: Razón del ajuste
            adjustment_type: Tipo de ajuste (credit o debit)
            user: Usuario que ejecuta el ajuste
            
        Returns:
            Tuple[bool, Dict, str]: (éxito, datos, mensaje)
        """
        # Log de inicio de ajuste
        self.audit_logger.log_payment_operation(
            'adjustment_started',
            credit,
            amount,
            user,
            {
                'reason': reason,
                'adjustment_type': adjustment_type
            }
        )
        
        try:
            success, result, message = self.transaction_manager.execute_atomic_operation(
                self._adjustment_operation,
                f"adjustment_{credit.uid}_{amount}_{adjustment_type}",
                credit,
                amount,
                reason,
                adjustment_type
            )
            
            if success:
                self.audit_logger.log_payment_operation(
                    'adjustment_successful',
                    credit,
                    amount,
                    user,
                    result
                )
                return True, result, message
            else:
                self.audit_logger.log_error(
                    'adjustment_failed',
                    message,
                    {'credit_uid': credit.uid, 'amount': float(amount)},
                    user
                )
                return False, result, message
                
        except Exception as e:
            self.audit_logger.log_error(
                'adjustment_exception',
                str(e),
                {'credit_uid': credit.uid, 'amount': float(amount)},
                user
            )
            return False, {}, f"Error procesando ajuste: {str(e)}"
    
    def validate_payment(
        self,
        credit,
        amount: Decimal,
        payment_method: Optional[str] = None
    ) -> Tuple[bool, Dict[str, Any], str]:
        """
        Valida si un pago es válido antes de procesarlo
        
        Args:
            credit: Crédito a validar
            amount: Monto a validar
            payment_method: Método de pago
            
        Returns:
            Tuple[bool, Dict, str]: (válido, datos, mensaje)
        """
        validation_result = {
            'credit_uid': credit.uid,
            'amount': float(amount),
            'payment_method': payment_method,
            'validations': {}
        }
        
        # Validaciones básicas
        if amount <= 0:
            return False, validation_result, "El monto debe ser mayor a 0"
        
        if amount > credit.pending_amount:
            return False, validation_result, f"El monto excede el saldo pendiente (${credit.pending_amount:,.2f})"
        
        if credit.state not in ['pending', 'completed']:
            return False, validation_result, f"El crédito no está en estado válido para pagos ({credit.state})"
        
        # Validaciones adicionales
        validation_result['validations']['amount_positive'] = True
        validation_result['validations']['amount_within_limit'] = True
        validation_result['validations']['credit_state_valid'] = True
        
        return True, validation_result, "Pago válido"
    
    def get_payment_summary(
        self,
        credit,
        start_date: Optional[timezone.datetime] = None,
        end_date: Optional[timezone.datetime] = None
    ) -> Dict[str, Any]:
        """
        Obtiene un resumen de pagos para un crédito
        
        Args:
            credit: Crédito a analizar
            start_date: Fecha de inicio
            end_date: Fecha de fin
            
        Returns:
            Dict con resumen de pagos
        """
        # Aquí se implementaría la lógica para obtener resumen
        # Por ahora retornamos datos básicos
        
        summary = {
            'credit_uid': credit.uid,
            'total_payments': 0,
            'total_amount': 0.0,
            'last_payment_date': None,
            'payment_methods': {},
            'period': {
                'start_date': start_date,
                'end_date': end_date
            }
        }
        
        return summary
    
    def _refund_operation(self, credit, amount, reason, original_transaction_id):
        """
        Operación interna para reembolso
        """
        # Aquí iría la lógica específica de reembolso
        return {
            'transaction_id': f"REF_{timezone.now().timestamp()}",
            'amount': amount,
            'reason': reason,
            'original_transaction_id': original_transaction_id,
            'status': 'success'
        }
    
    def _adjustment_operation(self, credit, amount, reason, adjustment_type):
        """
        Operación interna para ajuste
        """
        # Aquí iría la lógica específica de ajuste
        return {
            'transaction_id': f"ADJ_{timezone.now().timestamp()}",
            'amount': amount,
            'reason': reason,
            'adjustment_type': adjustment_type,
            'status': 'success'
        } 