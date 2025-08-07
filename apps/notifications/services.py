import logging
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Notification, NotificationTemplate, NotificationPreference, NotificationLog

User = get_user_model()
logger = logging.getLogger(__name__)

class NotificationService:
    """Servicio principal para gestionar notificaciones"""
    
    @staticmethod
    def create_notification(user, template_type, data=None, priority='medium', channels='web'):
        """Crea una nueva notificación"""
        try:
            # Verificar preferencias del usuario
            preferences = NotificationPreference.objects.get_or_create(user=user)[0]
            
            if not preferences.is_type_enabled(template_type):
                logger.info(f"Notificación {template_type} deshabilitada para usuario {user.id}")
                return None
            
            # Obtener template
            template = NotificationTemplate.objects.filter(
                template_type=template_type,
                is_active=True
            ).first()
            
            if not template:
                logger.warning(f"Template {template_type} no encontrado o inactivo")
                return None
            
            # Crear notificación
            notification = Notification.objects.create(
                user=user,
                template=template,
                title=template.title,
                message=template.message,
                data=data or {},
                priority=priority,
                channels=channels
            )
            
            logger.info(f"Notificación creada: {notification.uid} para usuario {user.id}")
            return notification
            
        except Exception as e:
            logger.error(f"Error creando notificación: {str(e)}")
            return None
    
    @staticmethod
    def send_notification(notification):
        """Envía una notificación por los canales configurados"""
        try:
            channels = notification.channels.split(',') if ',' in notification.channels else [notification.channels]
            
            for channel in channels:
                channel = channel.strip()
                try:
                    if channel == 'email':
                        NotificationService._send_email(notification)
                    elif channel == 'sms':
                        NotificationService._send_sms(notification)
                    elif channel == 'push':
                        NotificationService._send_push(notification)
                    elif channel == 'web':
                        NotificationService._send_web(notification)
                    
                    # Log exitoso
                    NotificationLog.objects.create(
                        notification=notification,
                        log_type='delivery_success',
                        channel=channel
                    )
                    
                    notification.mark_as_delivered()
                    
                except Exception as e:
                    # Log de error
                    NotificationLog.objects.create(
                        notification=notification,
                        log_type='delivery_failed',
                        channel=channel,
                        error_message=str(e)
                    )
                    logger.error(f"Error enviando notificación por {channel}: {str(e)}")
            
            notification.mark_as_sent()
            return True
            
        except Exception as e:
            logger.error(f"Error general enviando notificación: {str(e)}")
            return False
    
    @staticmethod
    def send_bulk_notifications(users, template_type, data=None, priority='medium'):
        """Envía notificaciones masivas"""
        notifications = []
        success_count = 0
        
        for user in users:
            notification = NotificationService.create_notification(
                user, template_type, data, priority
            )
            if notification:
                notifications.append(notification)
        
        # Enviar en batch
        for notification in notifications:
            if NotificationService.send_notification(notification):
                success_count += 1
        
        logger.info(f"Enviadas {success_count}/{len(notifications)} notificaciones masivas")
        return success_count
    
    @staticmethod
    def schedule_notification(user, template_type, data=None, schedule_time=None, priority='medium'):
        """Programa una notificación para envío futuro"""
        notification = NotificationService.create_notification(
            user, template_type, data, priority
        )
        
        if notification and schedule_time:
            # Aquí se podría integrar con Celery para envío programado
            # Por ahora, solo creamos la notificación
            logger.info(f"Notificación programada para {schedule_time}")
        
        return notification
    
    @staticmethod
    def get_user_preferences(user):
        """Obtiene las preferencias de notificación de un usuario"""
        preferences, created = NotificationPreference.objects.get_or_create(user=user)
        return preferences
    
    @staticmethod
    def mark_as_read(notification_id):
        """Marca una notificación como leída"""
        try:
            notification = Notification.objects.get(uid=notification_id)
            notification.mark_as_read()
            return True
        except Notification.DoesNotExist:
            return False
    
    @staticmethod
    def get_unread_count(user):
        """Obtiene el número de notificaciones no leídas de un usuario"""
        return Notification.objects.filter(
            user=user,
            status__in=['pending', 'sent', 'delivered']
        ).count()
    
    @staticmethod
    def cleanup_old_notifications(days=30):
        """Limpia notificaciones antiguas"""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        deleted_count = Notification.objects.filter(
            created_at__lt=cutoff_date,
            status__in=['read', 'failed']
        ).delete()[0]
        
        logger.info(f"Eliminadas {deleted_count} notificaciones antiguas")
        return deleted_count
    
    # Métodos privados para envío por canal
    @staticmethod
    def _send_email(notification):
        """Envía notificación por email"""
        # TODO: Integrar con sistema de email
        logger.info(f"Enviando email a {notification.user.email}: {notification.title}")
        # Aquí se implementaría la lógica de envío de email
    
    @staticmethod
    def _send_sms(notification):
        """Envía notificación por SMS"""
        # TODO: Integrar con servicio de SMS
        logger.info(f"Enviando SMS a {notification.user.phone_1}: {notification.title}")
        # Aquí se implementaría la lógica de envío de SMS
    
    @staticmethod
    def _send_push(notification):
        """Envía notificación push"""
        # TODO: Integrar con servicio de push notifications
        logger.info(f"Enviando push notification a {notification.user.id}: {notification.title}")
        # Aquí se implementaría la lógica de push notifications
    
    @staticmethod
    def _send_web(notification):
        """Envía notificación web (dashboard)"""
        # Las notificaciones web se muestran automáticamente en el dashboard
        logger.info(f"Notificación web creada para {notification.user.id}: {notification.title}")
        return True


class NotificationDetector:
    """Clase para detectar eventos que requieren notificaciones"""
    
    @staticmethod
    def detect_additional_interest_applied(credit):
        """Detecta cuando se aplica interés adicional a un crédito"""
        try:
            # Obtener administradores
            admin_users = User.objects.filter(is_staff=True)
            
            # Notificar a administradores
            NotificationService.send_bulk_notifications(
                admin_users,
                'additional_interest',
                {
                    'credit_id': credit.uid,
                    'user_name': credit.user.get_full_name(),
                    'amount': credit.price,
                    'interest_applied': credit.interest or 0
                },
                priority='high'
            )
            
            # Notificar al cliente
            NotificationService.create_notification(
                credit.user,
                'additional_interest',
                {
                    'credit_id': credit.uid,
                    'amount': credit.interest or 0,
                    'reason': 'Pago parcial detectado'
                },
                priority='medium',
                channels='email,web'
            )
            
        except Exception as e:
            logger.error(f"Error detectando interés adicional: {str(e)}")
    
    @staticmethod
    def detect_multiple_credits(user):
        """Detecta cuando un usuario tiene múltiples créditos"""
        try:
            from apps.fintech.models import Credit
            
            user_credits = Credit.objects.filter(user=user, state='completed')
            
            if user_credits.count() > 1:
                # Notificar a administradores
                admin_users = User.objects.filter(is_staff=True)
                
                NotificationService.send_bulk_notifications(
                    admin_users,
                    'multiple_credits',
                    {
                        'user_id': user.id,
                        'user_name': user.get_full_name(),
                        'credit_count': user_credits.count(),
                        'credits': [str(credit.uid) for credit in user_credits]
                    },
                    priority='critical'
                )
                
        except Exception as e:
            logger.error(f"Error detectando créditos múltiples: {str(e)}")
    
    @staticmethod
    def detect_high_morosidad(user):
        """Detecta usuarios con alta morosidad"""
        try:
            from apps.fintech.models import Credit
            
            high_risk_credits = Credit.objects.filter(
                user=user,
                is_in_default=True,
                morosidad_level__in=['alta', 'critica']
            )
            
            if high_risk_credits.exists():
                # Notificar a administradores
                admin_users = User.objects.filter(is_staff=True)
                
                NotificationService.send_bulk_notifications(
                    admin_users,
                    'high_morosidad',
                    {
                        'user_id': user.id,
                        'user_name': user.get_full_name(),
                        'credits_count': high_risk_credits.count(),
                        'risk_level': 'alta'
                    },
                    priority='critical'
                )
                
        except Exception as e:
            logger.error(f"Error detectando alta morosidad: {str(e)}")
    
    @staticmethod
    def detect_behavior_change(user):
        """Detecta cambios en el comportamiento de pago"""
        try:
            from apps.fintech.models import Transaction, Installment
            from django.utils import timezone
            from datetime import timedelta
            
            # Buscar transacciones recientes
            recent_transactions = Transaction.objects.filter(
                user=user,
                transaction_type='income',
                date__gte=timezone.now() - timedelta(days=30)
            )
            
            # Buscar cuotas vencidas
            overdue_installments = Installment.objects.filter(
                credit__user=user,
                status='overdue'
            )
            
            # Si hay cuotas vencidas y no hay transacciones recientes
            if overdue_installments.exists() and not recent_transactions.exists():
                admin_users = User.objects.filter(is_staff=True)
                
                NotificationService.send_bulk_notifications(
                    admin_users,
                    'behavior_change',
                    {
                        'user_id': user.id,
                        'user_name': user.get_full_name(),
                        'overdue_count': overdue_installments.count(),
                        'last_payment_days': 30
                    },
                    priority='high'
                )
                
        except Exception as e:
            logger.error(f"Error detectando cambio de comportamiento: {str(e)}") 