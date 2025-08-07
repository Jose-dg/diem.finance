from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.test import override_settings
from .services import NotificationService, NotificationDetector

User = get_user_model()

# Variable para controlar si los signals están habilitados
NOTIFICATIONS_ENABLED = True

def disable_notifications():
    """Deshabilitar notificaciones temporalmente"""
    global NOTIFICATIONS_ENABLED
    NOTIFICATIONS_ENABLED = False

def enable_notifications():
    """Habilitar notificaciones"""
    global NOTIFICATIONS_ENABLED
    NOTIFICATIONS_ENABLED = True

@receiver(post_save, sender='fintech.Credit')
def detect_multiple_credits(sender, instance, created, **kwargs):
    """Detectar cuando un usuario tiene múltiples créditos"""
    if not NOTIFICATIONS_ENABLED:
        return
        
    if created:
        try:
            # Verificar si el usuario tiene múltiples créditos activos
            user_credits = instance.user.credits.filter(state='completed')
            
            if user_credits.count() > 1:
                # Notificar al administrador
                admin_users = User.objects.filter(is_staff=True)
                
                NotificationService.send_bulk_notifications(
                    admin_users,
                    'multiple_credits',
                    {
                        'user_id': instance.user.id,
                        'user_name': instance.user.get_full_name(),
                        'credit_count': user_credits.count(),
                        'new_credit_id': str(instance.uid),
                        'user_email': instance.user.email
                    },
                    priority='critical'
                )
                
        except Exception as e:
            print(f"Error detectando créditos múltiples: {str(e)}")

@receiver(post_save, sender='fintech.Installment')
def detect_overdue_installments(sender, instance, **kwargs):
    """Detectar cuotas vencidas y enviar notificaciones"""
    if not NOTIFICATIONS_ENABLED:
        return
        
    try:
        # Verificar si la cuota está vencida y no se ha notificado
        if instance.status == 'overdue' and not instance.notification_sent:
            # Notificar al cliente
            NotificationService.create_notification(
                instance.credit.user,
                'overdue_installment',
                {
                    'installment_number': instance.number,
                    'amount': float(instance.amount),
                    'days_overdue': instance.days_overdue,
                    'credit_id': str(instance.credit.uid),
                    'due_date': instance.due_date.strftime('%Y-%m-%d') if instance.due_date else None
                },
                priority='high',
                channels='email,web'
            )
            
            # Marcar como notificada
            instance.notification_sent = True
            instance.save(update_fields=['notification_sent'])
            
    except Exception as e:
        print(f"Error detectando cuotas vencidas: {str(e)}")

@receiver(post_save, sender='fintech.Transaction')
def detect_behavior_changes(sender, instance, created, **kwargs):
    """Detectar cambios en comportamiento de pago"""
    if not NOTIFICATIONS_ENABLED:
        return
        
    if created and instance.transaction_type == 'income' and instance.status == 'confirmed':
        try:
            # Verificar si hay cuotas vencidas para este usuario
            overdue_installments = instance.user.credits.filter(
                installments__status='overdue'
            ).distinct()
            
            if overdue_installments.exists():
                # Notificar cambio de comportamiento positivo
                admin_users = User.objects.filter(is_staff=True)
                
                NotificationService.send_bulk_notifications(
                    admin_users,
                    'behavior_change',
                    {
                        'user_id': instance.user.id,
                        'user_name': instance.user.get_full_name(),
                        'payment_amount': float(instance.amount) if hasattr(instance, 'amount') else 0,
                        'behavior_type': 'positive_payment',
                        'overdue_credits_count': overdue_installments.count()
                    },
                    priority='medium'
                )
                
        except Exception as e:
            print(f"Error detectando cambios de comportamiento: {str(e)}")

@receiver(post_save, sender='fintech.CreditAdjustment')
def detect_additional_interest(sender, instance, created, **kwargs):
    """Detectar cuando se aplica interés adicional"""
    if not NOTIFICATIONS_ENABLED:
        return
        
    if created and instance.type and 'interes' in instance.type.name.lower():
        try:
            # Notificar al administrador
            admin_users = User.objects.filter(is_staff=True)
            
            NotificationService.send_bulk_notifications(
                admin_users,
                'additional_interest',
                {
                    'credit_id': str(instance.credit.uid),
                    'user_name': instance.credit.user.get_full_name(),
                    'amount': float(instance.amount),
                    'reason': instance.reason or 'Interés adicional aplicado',
                    'adjustment_date': instance.added_on.strftime('%Y-%m-%d')
                },
                priority='high'
            )
            
            # Notificar al cliente
            NotificationService.create_notification(
                instance.credit.user,
                'additional_interest',
                {
                    'credit_id': str(instance.credit.uid),
                    'amount': float(instance.amount),
                    'reason': instance.reason or 'Interés adicional aplicado'
                },
                priority='medium',
                channels='email,web'
            )
            
        except Exception as e:
            print(f"Error detectando interés adicional: {str(e)}")

@receiver(post_save, sender='fintech.Credit')
def detect_high_morosidad(sender, instance, **kwargs):
    """Detectar alta morosidad en créditos"""
    if not NOTIFICATIONS_ENABLED:
        return
        
    try:
        # Verificar si el crédito está en mora alta
        if instance.is_in_default and instance.morosidad_level in ['alta', 'critica']:
            # Notificar al administrador
            admin_users = User.objects.filter(is_staff=True)
            
            NotificationService.send_bulk_notifications(
                admin_users,
                'high_morosidad',
                {
                    'user_id': instance.user.id,
                    'user_name': instance.user.get_full_name(),
                    'credit_id': str(instance.uid),
                    'morosidad_level': instance.morosidad_level,
                    'pending_amount': float(instance.pending_amount) if instance.pending_amount else 0,
                    'user_email': instance.user.email
                },
                priority='critical'
            )
            
    except Exception as e:
        print(f"Error detectando alta morosidad: {str(e)}")

@receiver(post_save, sender='fintech.Credit')
def detect_payment_reminders(sender, instance, **kwargs):
    """Detectar cuotas próximas a vencer para recordatorios"""
    if not NOTIFICATIONS_ENABLED:
        return
        
    try:
        from django.utils import timezone
        from datetime import timedelta
        
        # Buscar cuotas que vencen en los próximos 3 días
        upcoming_installments = instance.installments.filter(
            status='pending',
            due_date__lte=timezone.now().date() + timedelta(days=3),
            due_date__gte=timezone.now().date(),
            notification_sent=False
        )
        
        for installment in upcoming_installments:
            # Enviar recordatorio
            NotificationService.create_notification(
                instance.user,
                'payment_reminder',
                {
                    'installment_number': installment.number,
                    'amount': float(installment.amount),
                    'due_date': installment.due_date.strftime('%Y-%m-%d'),
                    'credit_id': str(instance.uid),
                    'days_until_due': (installment.due_date - timezone.now().date()).days
                },
                priority='medium',
                channels='email,web'
            )
            
            # Marcar como notificada
            installment.notification_sent = True
            installment.save(update_fields=['notification_sent'])
            
    except Exception as e:
        print(f"Error enviando recordatorios de pago: {str(e)}")

# Signal para crear preferencias de notificación automáticamente
@receiver(post_save, sender=User)
def create_notification_preferences(sender, instance, created, **kwargs):
    """Crear preferencias de notificación automáticamente para nuevos usuarios"""
    if not NOTIFICATIONS_ENABLED:
        return
        
    if created:
        try:
            from .models import NotificationPreference
            NotificationPreference.objects.get_or_create(user=instance)
        except Exception as e:
            print(f"Error creando preferencias de notificación: {str(e)}") 