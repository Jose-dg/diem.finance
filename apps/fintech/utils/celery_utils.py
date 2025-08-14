"""
Utilidades para manejar tareas de Celery de manera segura
"""

import logging
from functools import wraps

logger = logging.getLogger(__name__)

def safe_delay_task(task, *args, **kwargs):
    """
    Ejecuta una tarea de Celery de manera segura, manejando errores de conexión.
    
    Args:
        task: Tarea de Celery a ejecutar
        *args: Argumentos posicionales para la tarea
        **kwargs: Argumentos nombrados para la tarea
    
    Returns:
        Resultado de la tarea o None si falla
    """
    try:
        # Verificar si Celery está configurado correctamente
        from django.conf import settings
        if not hasattr(settings, 'CELERY_BROKER_URL') or not settings.CELERY_BROKER_URL:
            logger.warning("Celery no está configurado correctamente")
            return None
            
        # Intentar ejecutar la tarea de forma asíncrona
        return task.delay(*args, **kwargs)
    except ConnectionError as e:
        if "redis" in str(e).lower() or "6379" in str(e):
            logger.warning(f"Error de conexión a Redis en tarea {task.__name__}: {e}")
            # Continuar sin ejecutar la tarea
            return None
        else:
            # Re-lanzar otros errores de conexión
            raise
    except Exception as e:
        logger.warning(f"No se pudo ejecutar tarea asíncrona {task.__name__}: {e}")
        
        # En caso de error, ejecutar la tarea sincrónicamente
        try:
            return task.apply(args=args, kwargs=kwargs)
        except Exception as sync_error:
            logger.error(f"Error ejecutando tarea sincrónicamente {task.__name__}: {sync_error}")
            return None

def safe_task_execution(func):
    """
    Decorador para ejecutar funciones que usan tareas de Celery de manera segura.
    
    Args:
        func: Función a decorar
    
    Returns:
        Función decorada
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error en función {func.__name__}: {e}")
            return None
    return wrapper

def handle_redis_connection_error(func):
    """
    Decorador específico para manejar errores de conexión a Redis.
    
    Args:
        func: Función a decorar
    
    Returns:
        Función decorada
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError as e:
            if "redis" in str(e).lower() or "6379" in str(e):
                logger.warning(f"Error de conexión a Redis en {func.__name__}: {e}")
                # Continuar sin ejecutar la tarea
                return None
            else:
                # Re-lanzar otros errores de conexión
                raise
        except Exception as e:
            logger.error(f"Error inesperado en {func.__name__}: {e}")
            return None
    return wrapper
