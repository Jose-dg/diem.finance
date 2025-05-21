from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MinLengthValidator
from django.utils import timezone

class Tenant(models.Model):
   """
   Modelo principal para representar un tenant (inquilino) en el sistema.
   Cada tenant tiene su propio conjunto de datos aislado.
   """

   # Información básica del tenant
   name = models.CharField(max_length=100, unique=True, validators=[MinLengthValidator(3)],help_text="Nombre único del tenant")
   slug = models.SlugField(max_length=100, unique=True, blank=True, help_text="Identificador URL-friendly del tenant")

   # Información de contacto
   contact_email = models.EmailField(verbose_name="Email de contacto", help_text="Email principal para comunicaciones con el tenant")
   contact_phone = models.CharField(max_length=20, blank=True, null=True, help_text="Teléfono de contacto")

   # Configuración y estado
   is_active = models.BooleanField(default=True, help_text="Indica si el tenant está activo")
   is_trial = models.BooleanField(default=False, help_text="Indica si el tenant está en período de prueba")
   trial_expiry_date = models.DateTimeField(null=True,blank=True, help_text="Fecha de expiración del período de prueba")

   created_at = models.DateTimeField(default=timezone.now)
   updated_at = models.DateTimeField(default=timezone.now)

   # Límites y configuraciones
   max_users = models.PositiveIntegerField(default=10,help_text="Número máximo de usuarios permitidos")
   storage_limit_mb = models.PositiveIntegerField(default=1024, help_text="Límite de almacenamiento en MB")
   current_storage_usage_mb = models.FloatField(default=0,help_text="Uso actual de almacenamiento en MB")

   class Meta:
      verbose_name = "Tenant"
      verbose_name_plural = "Tenants"
      ordering = ['name']

   def __str__(self):
      return self.name

   def save(self, *args, **kwargs):
      # Generar slug automáticamente si no se proporciona
      if not self.slug:
         self.slug = slugify(self.name)

      super().save(*args, **kwargs)

   def is_trial_expired(self):
      """Comprueba si el período de prueba ha expirado"""
      return self.is_trial and self.trial_expiry_date and timezone.now() > self.trial_expiry_date

class TenantRole(models.Model):
   """
   Roles disponibles para los usuarios en un tenant.
   """
   name = models.CharField(max_length=50)
   slug = models.CharField(max_length=50)
   description = models.TextField(blank=True, null=True)
   is_system_role = models.BooleanField(default=False, help_text="Indica si es un rol del sistema (no puede ser eliminado)")
   permissions = models.JSONField(default=dict,blank=True,help_text="Permisos asociados a este rol")

   created_at = models.DateTimeField(default=timezone.now)
   updated_at = models.DateTimeField(default=timezone.now)
    
   class Meta:
      verbose_name = "Rol de tenant"
      verbose_name_plural = "Roles de tenant"
    
   def __str__(self):
      return f"{self.name} ({self.tenant.name})"
    

class TenantMembership(models.Model):
   """
   Relación entre usuarios, tenants y roles funcionales.
   """
   tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='memberships')
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tenant_memberships')
   role = models.ForeignKey(TenantRole, on_delete=models.PROTECT)
   is_active = models.BooleanField(default=True,help_text="Indica si el usuario está activo en este tenant")
   invitation_accepted = models.BooleanField(default=False,help_text="Indica si el usuario ha aceptado la invitación")
    
   invitation_sent_at = models.DateTimeField(null=True, blank=True,help_text="Fecha en que se envió la invitación")
   invitation_accepted_at = models.DateTimeField(null=True, blank=True,help_text="Fecha en que se aceptó la invitación")
   
   created_at = models.DateTimeField(default=timezone.now)
   updated_at = models.DateTimeField(default=timezone.now)
    
   class Meta:
      verbose_name = "Membresía de tenant"
      verbose_name_plural = "Membresías de tenant"
      unique_together = ('tenant', 'user')
    
   def __str__(self):
        return f"{self.user.username} - {self.tenant.name} ({self.role})"


class TenantSettings(models.Model):
   """
   Configuraciones personalizadas para cada tenant.
   """
   tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='settings')
   # Personalización de la interfaz
   theme = models.CharField(max_length=50, default='default',help_text="Tema visual del tenant")
   logo = models.ImageField(upload_to='tenant_logos/', null=True, blank=True,help_text="Logo del tenant")
   favicon = models.ImageField(upload_to='tenant_favicons/', null=True, blank=True,help_text="Favicon del tenant")
   primary_color = models.CharField(max_length=7, default='#007bff',help_text="Color primario en formato hexadecimal")
    
   # Configuraciones de notificaciones
   email_notifications_enabled = models.BooleanField(default=True,help_text="Habilitar notificaciones por email")
    
   # Configuraciones regionales
   time_zone = models.CharField(max_length=50, default='UTC',help_text="Zona horaria del tenant")
   date_format = models.CharField(max_length=20, default='DD/MM/YYYY',help_text="Formato de fecha")
    
   # Políticas de seguridad
   password_expiry_days = models.PositiveIntegerField(default=90,help_text="Días antes de expiración de contraseñas")
   mfa_required = models.BooleanField(default=False,help_text="Requerir autenticación de dos factores")
   session_timeout_minutes = models.PositiveIntegerField(default=60,help_text="Tiempo de expiración de sesión en minutos")
    
   created_at = models.DateTimeField(default=timezone.now)
   updated_at = models.DateTimeField(default=timezone.now)
    
   class Meta:
      verbose_name = "Configuración de tenant"
      verbose_name_plural = "Configuraciones de tenant"
    
   def __str__(self):
        return f"Configuración de {self.tenant.name}"
