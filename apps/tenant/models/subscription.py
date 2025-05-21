from django.utils import timezone
from django.db import models
from django.conf import settings

from apps.tenant.models.tenant import Tenant

class SubscriptionPlan(models.Model):
    """
    Representa un plan de suscripción disponible para los tenants.
    """
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubscriptionStatus(models.Model):
    """
    Representa el estado de una suscripción.
    """
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TenantSubscription(models.Model):
   """
   Gestión de suscripciones para tenants.
   """

   tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='subscription')
   plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
   status = models.ForeignKey(SubscriptionStatus, on_delete=models.PROTECT)
   start_date = models.DateTimeField(default=timezone.now)
   end_date = models.DateTimeField(null=True, blank=True)
   auto_renew = models.BooleanField(default=True)
    
   # Campos para integración con sistema de pagos
   payment_provider = models.CharField(max_length=50, blank=True, null=True,help_text="Proveedor de pagos (Stripe, PayPal, etc.)")
   subscription_id = models.CharField(max_length=255, blank=True, null=True,help_text="ID de suscripción en el sistema de pagos")
   customer_id = models.CharField(max_length=255, blank=True, null=True,help_text="ID de cliente en el sistema de pagos")
    
   created_at = models.DateTimeField(default=timezone.now)
   updated_at = models.DateTimeField(default=timezone.now)
    
   class Meta:
      verbose_name = "Suscripción de tenant"
      verbose_name_plural = "Suscripciones de tenant"
    
   def __str__(self):
      return f"{self.tenant.name} - {self.get_plan_display()}"
    
   def is_active(self):
      return self.status in ['active', 'trialing']
    
   def days_remaining(self):
      if not self.end_date:
         return None
      delta = self.end_date - timezone.now()
      return max(0, delta.days)
     