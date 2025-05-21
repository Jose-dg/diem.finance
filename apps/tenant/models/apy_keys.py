from django.utils import timezone
from django.db import models
from django.conf import settings

from apps.tenant.models.tenant import Tenant

class TenantApiKey(models.Model):
    """
    Claves API para integración con servicios externos.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=100,help_text="Nombre descriptivo para la clave API")
    prefix = models.CharField(max_length=8, editable=False,help_text="Prefijo visible de la clave API")
    key = models.CharField(max_length=64, editable=False,help_text="Clave API encriptada")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Clave API de tenant"
        verbose_name_plural = "Claves API de tenant"
        unique_together = ('tenant', 'prefix')
    
    def __str__(self):
        return f"{self.name} ({self.prefix}...)"
    
    def is_expired(self):
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at
    
    @property
    def status(self):
        if not self.is_active:
            return "Inactiva"
        elif self.is_expired():
            return "Expirada"
        else:
            return "Activa"
