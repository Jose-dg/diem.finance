import uuid
from django.db import models
from django.conf import settings

INTERACTION_TYPES = [
    ('credit_delivery', 'Entrega de Crédito'),
    ('payment_full', 'Cobro completo'),
    ('payment_partial', 'Cobro parcial'),
    ('office_payment', 'Pago en oficina'),
    ('visit', 'Visita (sin cobro)'),
    ('promise', 'Promesa de pago'),
    ('call', 'Llamada'),
]

SOURCE_TYPES = [
    ('mobile', 'Dispositivo Móvil'),
    ('office', 'Oficina'),
]

class InteractionLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey('fintech.Seller', on_delete=models.CASCADE, related_name='interactions')
    credit = models.ForeignKey('fintech.Credit', on_delete=models.CASCADE, related_name='interactions')
    
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    distance_variance = models.IntegerField(null=True, blank=True, help_text="Distancia en metros al punto más cercano del cliente")
    
    promise_date = models.DateField(null=True, blank=True)
    promise_fulfilled = models.BooleanField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    source = models.CharField(max_length=10, choices=SOURCE_TYPES, default='mobile')
    
    captured_at = models.DateTimeField()
    synced_at = models.DateTimeField(auto_now_add=True)
    sync_lag_seconds = models.IntegerField(null=True, blank=True)
    offline_sync = models.BooleanField(default=False)
    
    transaction = models.ForeignKey('fintech.Transaction', on_delete=models.SET_NULL, null=True, blank=True, related_name='interaction_logs')

    def __str__(self):
        return f"{self.interaction_type} - {self.credit.uid} by {self.agent}"


class CollectionPoint(models.Model):
    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='collection_points')
    label = models.CharField(max_length=20, choices=[
        ('credit_delivery', 'Desembolso'),
        ('visit', 'Visita'),
        ('payment', 'Cobro'),
    ])
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address_text = models.CharField(max_length=255, blank=True)
    
    interaction = models.OneToOneField(InteractionLog, on_delete=models.CASCADE, related_name='collection_point')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Point {self.label} for {self.client.email}"
