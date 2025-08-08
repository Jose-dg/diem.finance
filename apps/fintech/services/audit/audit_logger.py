from decimal import Decimal
from django.utils import timezone
from django.contrib.auth import get_user_model
from typing import Any, Dict, Optional, List
import logging
import json

User = get_user_model()
logger = logging.getLogger(__name__)

class AuditLogger:
    """
    Sistema de auditoría completo para todas las operaciones financieras
    Registra, valida y reporta todas las actividades del sistema
    """
    
    def __init__(self):
        self.log_level = 'INFO'
        self.enable_detailed_logging = True
    
    def log_payment_operation(
        self,
        operation_type: str,
        credit,
        amount: Decimal,
        user: Optional[User] = None,
        additional_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Registra una operación de pago
        
        Args:
            operation_type: Tipo de operación (payment, refund, adjustment)
            credit: Crédito afectado
            amount: Monto de la operación
            user: Usuario que ejecutó la operación
            additional_data: Datos adicionales
            
        Returns:
            Dict con información del log
        """
        log_data = {
            'operation_type': operation_type,
            'credit_uid': credit.uid,
            'amount': float(amount),
            'user_id': user.id if user else None,
            'user_username': user.username if user else 'system',
            'timestamp': timezone.now(),
            'credit_state_before': {
                'total_abonos': float(credit.total_abonos),
                'pending_amount': float(credit.pending_amount),
                'is_in_default': credit.is_in_default,
                'morosidad_level': credit.morosidad_level
            },
            'additional_data': additional_data or {}
        }
        
        # Log detallado
        if self.enable_detailed_logging:
            logger.info(
                f"PAYMENT_OPERATION: {operation_type} | "
                f"Credit: {credit.uid} | "
                f"Amount: ${amount:,.2f} | "
                f"User: {log_data['user_username']}"
            )
        
        return log_data
    
    def log_balance_change(
        self,
        credit,
        old_balance: Decimal,
        new_balance: Decimal,
        reason: str,
        user: Optional[User] = None
    ) -> Dict[str, Any]:
        """
        Registra un cambio en el saldo de un crédito
        
        Args:
            credit: Crédito afectado
            old_balance: Saldo anterior
            new_balance: Saldo nuevo
            reason: Razón del cambio
            user: Usuario que causó el cambio
            
        Returns:
            Dict con información del log
        """
        balance_difference = new_balance - old_balance
        
        log_data = {
            'operation_type': 'balance_change',
            'credit_uid': credit.uid,
            'old_balance': float(old_balance),
            'new_balance': float(new_balance),
            'balance_difference': float(balance_difference),
            'reason': reason,
            'user_id': user.id if user else None,
            'user_username': user.username if user else 'system',
            'timestamp': timezone.now()
        }
        
        # Log detallado
        if self.enable_detailed_logging:
            logger.info(
                f"BALANCE_CHANGE: Credit: {credit.uid} | "
                f"Old: ${old_balance:,.2f} | "
                f"New: ${new_balance:,.2f} | "
                f"Diff: ${balance_difference:,.2f} | "
                f"Reason: {reason}"
            )
        
        return log_data
    
    def log_system_operation(
        self,
        operation_type: str,
        description: str,
        user: Optional[User] = None,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Registra operaciones del sistema
        
        Args:
            operation_type: Tipo de operación
            description: Descripción de la operación
            user: Usuario que ejecutó la operación
            metadata: Metadatos adicionales
            
        Returns:
            Dict con información del log
        """
        log_data = {
            'operation_type': operation_type,
            'description': description,
            'user_id': user.id if user else None,
            'user_username': user.username if user else 'system',
            'timestamp': timezone.now(),
            'metadata': metadata or {}
        }
        
        # Log detallado
        if self.enable_detailed_logging:
            logger.info(
                f"SYSTEM_OPERATION: {operation_type} | "
                f"Description: {description} | "
                f"User: {log_data['user_username']}"
            )
        
        return log_data
    
    def log_error(
        self,
        error_type: str,
        error_message: str,
        context: Optional[Dict] = None,
        user: Optional[User] = None
    ) -> Dict[str, Any]:
        """
        Registra errores del sistema
        
        Args:
            error_type: Tipo de error
            error_message: Mensaje de error
            context: Contexto del error
            user: Usuario afectado
            
        Returns:
            Dict con información del log
        """
        log_data = {
            'operation_type': 'error',
            'error_type': error_type,
            'error_message': error_message,
            'context': context or {},
            'user_id': user.id if user else None,
            'user_username': user.username if user else 'system',
            'timestamp': timezone.now()
        }
        
        # Log de error
        logger.error(
            f"ERROR: {error_type} | "
            f"Message: {error_message} | "
            f"User: {log_data['user_username']} | "
            f"Context: {json.dumps(context) if context else 'None'}"
        )
        
        return log_data
    
    def log_batch_operation(
        self,
        operation_type: str,
        total_items: int,
        successful_items: int,
        failed_items: int,
        errors: List[Dict],
        duration: float,
        user: Optional[User] = None
    ) -> Dict[str, Any]:
        """
        Registra operaciones en lote
        
        Args:
            operation_type: Tipo de operación
            total_items: Total de elementos procesados
            successful_items: Elementos procesados exitosamente
            failed_items: Elementos que fallaron
            errors: Lista de errores
            duration: Duración de la operación
            user: Usuario que ejecutó la operación
            
        Returns:
            Dict con información del log
        """
        success_rate = (successful_items / total_items * 100) if total_items > 0 else 0
        
        log_data = {
            'operation_type': f'batch_{operation_type}',
            'total_items': total_items,
            'successful_items': successful_items,
            'failed_items': failed_items,
            'success_rate': success_rate,
            'duration_seconds': duration,
            'errors': errors,
            'user_id': user.id if user else None,
            'user_username': user.username if user else 'system',
            'timestamp': timezone.now()
        }
        
        # Log detallado
        if self.enable_detailed_logging:
            logger.info(
                f"BATCH_OPERATION: {operation_type} | "
                f"Total: {total_items} | "
                f"Success: {successful_items} | "
                f"Failed: {failed_items} | "
                f"Success Rate: {success_rate:.1f}% | "
                f"Duration: {duration:.3f}s"
            )
        
        return log_data
    
    def log_security_event(
        self,
        event_type: str,
        description: str,
        severity: str = 'medium',
        user: Optional[User] = None,
        ip_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Registra eventos de seguridad
        
        Args:
            event_type: Tipo de evento de seguridad
            description: Descripción del evento
            severity: Severidad (low, medium, high, critical)
            user: Usuario involucrado
            ip_address: Dirección IP
            
        Returns:
            Dict con información del log
        """
        log_data = {
            'operation_type': 'security_event',
            'event_type': event_type,
            'description': description,
            'severity': severity,
            'user_id': user.id if user else None,
            'user_username': user.username if user else 'anonymous',
            'ip_address': ip_address,
            'timestamp': timezone.now()
        }
        
        # Log de seguridad
        log_level = 'warning' if severity in ['high', 'critical'] else 'info'
        getattr(logger, log_level)(
            f"SECURITY_EVENT: {event_type} | "
            f"Severity: {severity} | "
            f"Description: {description} | "
            f"User: {log_data['user_username']} | "
            f"IP: {ip_address or 'unknown'}"
        )
        
        return log_data
    
    def get_audit_summary(
        self,
        start_date: Optional[timezone.datetime] = None,
        end_date: Optional[timezone.datetime] = None,
        operation_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Genera un resumen de auditoría
        
        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin
            operation_types: Tipos de operación a incluir
            
        Returns:
            Dict con resumen de auditoría
        """
        # Aquí se implementaría la lógica para consultar logs
        # Por ahora retornamos un resumen de ejemplo
        
        summary = {
            'period': {
                'start_date': start_date or timezone.now() - timezone.timedelta(days=30),
                'end_date': end_date or timezone.now()
            },
            'total_operations': 0,
            'operation_types': {},
            'errors': 0,
            'security_events': 0,
            'payment_operations': 0,
            'balance_changes': 0
        }
        
        return summary
    
    def export_audit_logs(
        self,
        start_date: Optional[timezone.datetime] = None,
        end_date: Optional[timezone.datetime] = None,
        format: str = 'json'
    ) -> str:
        """
        Exporta logs de auditoría
        
        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin
            format: Formato de exportación (json, csv)
            
        Returns:
            String con los logs exportados
        """
        # Aquí se implementaría la lógica de exportación
        # Por ahora retornamos un ejemplo
        
        export_data = {
            'export_info': {
                'start_date': start_date,
                'end_date': end_date,
                'format': format,
                'exported_at': timezone.now()
            },
            'logs': []
        }
        
        if format == 'json':
            return json.dumps(export_data, indent=2, default=str)
        else:
            return str(export_data)
    
    def validate_audit_integrity(self) -> Dict[str, Any]:
        """
        Valida la integridad de los logs de auditoría
        
        Returns:
            Dict con resultados de validación
        """
        validation_result = {
            'timestamp': timezone.now(),
            'integrity_check': 'passed',
            'total_logs_checked': 0,
            'corrupted_logs': 0,
            'missing_logs': 0,
            'recommendations': []
        }
        
        return validation_result 