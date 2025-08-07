import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

# Constantes compartidas
CHANNEL_CHOICES = [
    ('email', 'Email'),
    ('sms', 'SMS'),
    ('push', 'Push Notification'),
    ('web', 'Web Dashboard'),
    ('all', 'Todos los Canales'),
]

PRIORITY_CHOICES = [
    ('low', 'Baja'),
    ('medium', 'Media'),
    ('high', 'Alta'),
    ('critical', 'Crítica'),
]

STATUS_CHOICES = [
    ('pending', 'Pendiente'),
    ('sent', 'Enviada'),
    ('delivered', 'Entregada'),
    ('read', 'Leída'),
    ('failed', 'Fallida'),
]

TEMPLATE_TYPES = [
    ('additional_interest', 'Interés Adicional'),
    ('multiple_credits', 'Créditos Múltiples'),
    ('high_morosidad', 'Alta Morosidad'),
    ('behavior_change', 'Cambio de Comportamiento'),
    ('overdue_installment', 'Cuota Vencida'),
    ('payment_reminder', 'Recordatorio de Pago'),
    ('credit_approved', 'Crédito Aprobado'),
    ('credit_rejected', 'Crédito Rechazado'),
    ('ai_collection_call', 'Llamada AI Cobranza'),
]

LOG_TYPES = [
    ('send_attempt', 'Intento de Envío'),
    ('delivery_success', 'Entrega Exitosa'),
    ('delivery_failed', 'Entrega Fallida'),
    ('read_received', 'Lectura Recibida'),
]


class NotificationTemplate(models.Model):
    """Plantillas reutilizables para notificaciones"""
    
    name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    channels = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='web')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ['template_type', 'is_active']  # Solo una plantilla activa por tipo
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"


class Notification(models.Model):
    """Notificaciones individuales enviadas a usuarios"""
    
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey('fintech.User', on_delete=models.CASCADE, related_name='notifications')
    template = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE, null=True, blank=True)
    
    # Contenido de la notificación (puede sobrescribir template)
    title = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    data = models.JSONField(default=dict, blank=True)
    
    # Configuración
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    channels = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='web')
    
    # Estado y seguimiento
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Relación con entidades del sistema (opcional)
    credit = models.ForeignKey('fintech.Credit', on_delete=models.CASCADE, null=True, blank=True)
    installment = models.ForeignKey('fintech.Installment', on_delete=models.CASCADE, null=True, blank=True)
    transaction = models.ForeignKey('fintech.Transaction', on_delete=models.CASCADE, null=True, blank=True)
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['priority']),
            models.Index(fields=['template']),
        ]
    
    def __str__(self):
        return f"Notificación para {self.user} - {self.get_title()}"
    
    def get_title(self):
        """Obtiene el título del template o del campo personalizado"""
        return self.title or (self.template.title if self.template else 'Sin título')
    
    def get_message(self):
        """Obtiene el mensaje del template o del campo personalizado"""
        return self.message or (self.template.message if self.template else 'Sin mensaje')
    
    def mark_as_sent(self):
        self.status = 'sent'
        self.sent_at = timezone.now()
        self.save(update_fields=['status', 'sent_at'])
    
    def mark_as_delivered(self):
        self.status = 'delivered'
        self.delivered_at = timezone.now()
        self.save(update_fields=['status', 'delivered_at'])
    
    def mark_as_read(self):
        self.status = 'read'
        self.read_at = timezone.now()
        self.save(update_fields=['status', 'read_at'])
    
    @property
    def is_read(self):
        """Propiedad para verificar si está leída"""
        return self.status == 'read'
    
    @property
    def is_unread(self):
        """Propiedad para verificar si no está leída"""
        return self.status in ['pending', 'sent', 'delivered']


class NotificationPreference(models.Model):
    """Preferencias de notificación por usuario"""
    
    user = models.OneToOneField('fintech.User', on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Canales habilitados
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    push_enabled = models.BooleanField(default=True)
    web_enabled = models.BooleanField(default=True)
    
    # Tipos de notificación habilitados (usando choices de TEMPLATE_TYPES)
    notification_types_enabled = models.JSONField(
        default=dict,
        help_text="Diccionario con tipos de notificación habilitados"
    )
    
    # Configuración de frecuencia
    daily_digest = models.BooleanField(default=False)
    weekly_summary = models.BooleanField(default=True)
    
    # Horarios de silencio
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    
    # Configuración de prioridad
    min_priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Preferencia de Notificación'
        verbose_name_plural = 'Preferencias de Notificaciones'
    
    def __str__(self):
        return f"Preferencias de {self.user}"
    
    def is_channel_enabled(self, channel):
        """Verifica si un canal está habilitado"""
        channel_map = {
            'email': self.email_enabled,
            'sms': self.sms_enabled,
            'push': self.push_enabled,
            'web': self.web_enabled,
        }
        return channel_map.get(channel, False)
    
    def is_type_enabled(self, notification_type):
        """Verifica si un tipo de notificación está habilitado"""
        # Si no hay configuración específica, habilitar por defecto
        if not self.notification_types_enabled:
            return True
        
        return self.notification_types_enabled.get(notification_type, True)
    
    def enable_notification_type(self, notification_type):
        """Habilita un tipo de notificación"""
        if not self.notification_types_enabled:
            self.notification_types_enabled = {}
        self.notification_types_enabled[notification_type] = True
        self.save(update_fields=['notification_types_enabled'])
    
    def disable_notification_type(self, notification_type):
        """Deshabilita un tipo de notificación"""
        if not self.notification_types_enabled:
            self.notification_types_enabled = {}
        self.notification_types_enabled[notification_type] = False
        self.save(update_fields=['notification_types_enabled'])


class NotificationLog(models.Model):
    """Log de intentos de envío de notificaciones"""
    
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='logs')
    log_type = models.CharField(max_length=20, choices=LOG_TYPES)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    
    # Detalles del intento
    attempt_number = models.PositiveIntegerField(default=1)
    error_message = models.TextField(blank=True, null=True)
    response_data = models.JSONField(default=dict, blank=True)
    
    # Metadatos
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['notification', 'log_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Log {self.log_type} para {self.notification}"
