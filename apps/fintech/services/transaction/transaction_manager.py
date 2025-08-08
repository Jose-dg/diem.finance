from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from typing import Any, Callable, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class TransactionManager:
    """
    Gestor de transacciones con rollback automático y logging detallado
    Maneja todas las operaciones atómicas del sistema
    """
    
    def __init__(self):
        self.audit_logger = None  # Se conectará con AuditLogger
    
    def execute_atomic_operation(
        self, 
        operation: Callable, 
        operation_name: str,
        *args, 
        **kwargs
    ) -> Tuple[bool, Any, str]:
        """
        Ejecuta una operación de manera atómica con rollback automático
        
        Args:
            operation: Función a ejecutar
            operation_name: Nombre de la operación para logging
            *args: Argumentos de la operación
            **kwargs: Argumentos nombrados de la operación
            
        Returns:
            Tuple[bool, Any, str]: (éxito, resultado, mensaje)
        """
        start_time = timezone.now()
        
        try:
            with transaction.atomic():
                # Ejecutar la operación
                result = operation(*args, **kwargs)
                
                # Log de éxito
                duration = timezone.now() - start_time
                logger.info(
                    f"Operación '{operation_name}' ejecutada exitosamente en {duration.total_seconds():.3f}s"
                )
                
                return True, result, "Operación ejecutada exitosamente"
                
        except Exception as e:
            # Log de error
            duration = timezone.now() - start_time
            error_msg = f"Error en operación '{operation_name}': {str(e)}"
            logger.error(error_msg)
            
            return False, None, error_msg
    
    def execute_payment_transaction(
        self,
        credit,
        amount: Decimal,
        payment_date: Optional[timezone.datetime] = None,
        **kwargs
    ) -> Tuple[bool, Dict, str]:
        """
        Ejecuta una transacción de pago de manera atómica
        
        Args:
            credit: Crédito a procesar
            amount: Monto del pago
            payment_date: Fecha del pago
            **kwargs: Argumentos adicionales
            
        Returns:
            Tuple[bool, Dict, str]: (éxito, datos, mensaje)
        """
        def payment_operation():
            # Aquí irá la lógica de pago
            # Por ahora retornamos datos de ejemplo
            return {
                'transaction_id': f"TXN_{timezone.now().timestamp()}",
                'amount': amount,
                'credit_uid': credit.uid,
                'status': 'success'
            }
        
        return self.execute_atomic_operation(
            payment_operation,
            f"payment_{credit.uid}_{amount}",
            credit,
            amount,
            payment_date,
            **kwargs
        )
    
    def execute_balance_recalculation(
        self,
        credit,
        **kwargs
    ) -> Tuple[bool, Dict, str]:
        """
        Ejecuta recálculo de saldo de manera atómica
        
        Args:
            credit: Crédito a recalcular
            **kwargs: Argumentos adicionales
            
        Returns:
            Tuple[bool, Dict, str]: (éxito, datos, mensaje)
        """
        def recalculation_operation():
            # Importar aquí para evitar dependencias circulares
            from apps.fintech.utils.root import recalculate_credit
            
            # Guardar estado anterior
            old_state = {
                'total_abonos': credit.total_abonos,
                'pending_amount': credit.pending_amount,
                'is_in_default': credit.is_in_default,
                'morosidad_level': credit.morosidad_level
            }
            
            # Ejecutar recálculo
            recalculate_credit(credit)
            credit.refresh_from_db()
            
            # Calcular cambios
            changes = {}
            for field, old_value in old_state.items():
                new_value = getattr(credit, field)
                if old_value != new_value:
                    changes[field] = {
                        'old': old_value,
                        'new': new_value
                    }
            
            return {
                'credit_uid': credit.uid,
                'changes': changes,
                'recalculation_time': timezone.now()
            }
        
        return self.execute_atomic_operation(
            recalculation_operation,
            f"recalculation_{credit.uid}",
            credit,
            **kwargs
        )
    
    def execute_batch_operation(
        self,
        items: list,
        operation: Callable,
        operation_name: str,
        batch_size: int = 100
    ) -> Dict[str, Any]:
        """
        Ejecuta operaciones en lotes de manera atómica
        
        Args:
            items: Lista de elementos a procesar
            operation: Función a ejecutar por elemento
            operation_name: Nombre de la operación
            batch_size: Tamaño del lote
            
        Returns:
            Dict con resultados del procesamiento
        """
        results = {
            'total_items': len(items),
            'processed': 0,
            'successful': 0,
            'failed': 0,
            'errors': [],
            'start_time': timezone.now()
        }
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            
            for item in batch:
                try:
                    success, result, message = self.execute_atomic_operation(
                        operation,
                        f"{operation_name}_{item.uid if hasattr(item, 'uid') else i}",
                        item
                    )
                    
                    results['processed'] += 1
                    
                    if success:
                        results['successful'] += 1
                    else:
                        results['failed'] += 1
                        results['errors'].append({
                            'item': str(item),
                            'error': message
                        })
                        
                except Exception as e:
                    results['processed'] += 1
                    results['failed'] += 1
                    results['errors'].append({
                        'item': str(item),
                        'error': str(e)
                    })
        
        results['end_time'] = timezone.now()
        results['duration'] = results['end_time'] - results['start_time']
        results['success_rate'] = (results['successful'] / results['total_items'] * 100) if results['total_items'] > 0 else 0
        
        return results
    
    def validate_transaction_context(self, **kwargs) -> Tuple[bool, str]:
        """
        Valida el contexto de una transacción antes de ejecutarla
        
        Args:
            **kwargs: Parámetros de validación
            
        Returns:
            Tuple[bool, str]: (válido, mensaje)
        """
        # Validaciones básicas
        if 'amount' in kwargs and kwargs['amount'] <= 0:
            return False, "El monto debe ser mayor a 0"
        
        if 'credit' in kwargs and not kwargs['credit']:
            return False, "El crédito es requerido"
        
        return True, "Contexto válido"
    
    def create_transaction_snapshot(self, **kwargs) -> Dict[str, Any]:
        """
        Crea una instantánea del estado antes de una transacción
        
        Args:
            **kwargs: Datos para la instantánea
            
        Returns:
            Dict con la instantánea
        """
        snapshot = {
            'timestamp': timezone.now(),
            'context': kwargs,
            'system_state': {
                'database_connections': 1,  # Simplificado
                'memory_usage': 'normal',
                'cpu_usage': 'normal'
            }
        }
        
        return snapshot
    
    def rollback_transaction(self, snapshot: Dict[str, Any]) -> bool:
        """
        Ejecuta rollback basado en una instantánea
        
        Args:
            snapshot: Instantánea creada antes de la transacción
            
        Returns:
            bool: True si el rollback fue exitoso
        """
        try:
            logger.info(f"Ejecutando rollback para transacción de {snapshot['timestamp']}")
            
            # Aquí iría la lógica de rollback específica
            # Por ahora solo loggeamos
            
            return True
            
        except Exception as e:
            logger.error(f"Error en rollback: {str(e)}")
            return False 