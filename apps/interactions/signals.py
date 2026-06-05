import math
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InteractionLog, CollectionPoint

def haversine_distance(lat1, lon1, lat2, lon2):
    # Radio de la tierra en metros
    R = 6371000
    phi1 = math.radians(float(lat1))
    phi2 = math.radians(float(lat2))
    delta_phi = math.radians(float(lat2) - float(lat1))
    delta_lambda = math.radians(float(lon2) - float(lon1))
    
    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@receiver(post_save, sender=InteractionLog)
def process_interaction_log(sender, instance, created, **kwargs):
    if not created:
        return
            
    # Calcular sync_lag_seconds
    if instance.captured_at and instance.synced_at:
        lag = (instance.synced_at - instance.captured_at).total_seconds()
        InteractionLog.objects.filter(pk=instance.pk).update(sync_lag_seconds=int(lag))
        
    # Calcular distance_variance
    if instance.latitude and instance.longitude:
        closest_distance = None
        
        # Buscar puntos históricos del cliente
        historical_points = CollectionPoint.objects.filter(client=instance.credit.user)
        for point in historical_points:
            dist = haversine_distance(instance.latitude, instance.longitude, point.latitude, point.longitude)
            if closest_distance is None or dist < closest_distance:
                closest_distance = dist
                
        if closest_distance is not None:
            InteractionLog.objects.filter(pk=instance.pk).update(distance_variance=int(closest_distance))

    # Crear CollectionPoint si amerita y tiene coordenadas
    if instance.latitude and instance.longitude:
        TYPES_TO_LABEL_MAP = {
            'credit_delivery': 'credit_delivery',
            'visit': 'visit',
            'payment_full': 'payment',
            'payment_partial': 'payment',
            'promise': 'visit',
        }
        
        label = TYPES_TO_LABEL_MAP.get(instance.interaction_type)
        if label:
            CollectionPoint.objects.create(
                client=instance.credit.user,
                label=label,
                latitude=instance.latitude,
                longitude=instance.longitude,
                interaction=instance
            )
