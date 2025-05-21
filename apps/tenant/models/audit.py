from django.db import models
from django.conf import settings

from apps.tenant.models.tenant import Tenant

class TenantAuditLog(models.Model):
    """
    Registro de auditoría para acciones importantes en un tenant.
    """
    ACTION_CHOICES = (
        ('create', 'Creación'),
        ('update', 'Actualización'),
        ('delete', 'Eliminación'),
        ('login', 'Inicio de sesión'),
        ('logout', 'Cierre de sesión'),
        ('invite', 'Invitación'),
        ('join', 'Unirse'),
        ('leave', 'Salir'),
        ('payment', 'Pago'),
        ('subscription_change', 'Cambio de suscripción'),
        ('settings_change', 'Cambio de configuración'),
        ('api_access', 'Acceso API'),
        ('other', 'Otro'),
    )
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='audit_logs'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    entity_type = models.CharField(max_length=100, blank=True, null=True,help_text="Tipo de entidad afectada")
    entity_id = models.CharField(max_length=100, blank=True, null=True,help_text="ID de la entidad afectada")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    details = models.JSONField(blank=True, null=True,help_text="Detalles adicionales de la acción")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Registro de auditoría"
        verbose_name_plural = "Registros de auditoría"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_action_display()} por {self.user} en {self.tenant.name}"