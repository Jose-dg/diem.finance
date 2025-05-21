from django.utils import timezone
import uuid
from django.db import models
from django.conf import settings

from apps.tenant.models.tenant import Tenant, TenantMembership

class TenantInvitationRole(models.Model):
    """
    Roles posibles durante el proceso de invitación a un tenant.
    Independientes de los roles funcionales activos en el sistema.
    """
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class TenantInvitation(models.Model):
   """
   Invitaciones para unirse a un tenant.
   """
   
   tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='invitations')
   email = models.EmailField()
   role = models.ForeignKey(TenantInvitationRole, on_delete=models.PROTECT, related_name='invitations')
   invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='sent_invitations')
   token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
   is_accepted = models.BooleanField(default=False)
   accepted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_invitations')
    
   created_at = models.DateTimeField(auto_now_add=True)
   expires_at = models.DateTimeField()
   accepted_at = models.DateTimeField(null=True, blank=True)
    
   class Meta:
      verbose_name = "Invitación de tenant"
      verbose_name_plural = "Invitaciones de tenant"
      unique_together = ('tenant', 'email')
    
   def __str__(self):
      return f"Invitación para {self.email} a {self.tenant.name}"
    
   def is_expired(self):
      return timezone.now() > self.expires_at
    
   @property
   def status(self):
      if self.is_accepted:
         return "Aceptada"
      elif self.is_expired():
         return "Expirada"
      else:
         return "Pendiente"