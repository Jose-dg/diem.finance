# 🎯 Plan de Implementación: Aplicación `notification` como Servicio Universal

## 📊 Matriz de Riesgos Detallada

### **Riesgos Críticos (Prioridad 1-3)**

| # | Riesgo | Probabilidad | Impacto | Riesgo Total | Mitigación |
|---|--------|-------------|---------|--------------|------------|
| 1 | **Dependencias Circulares** | Alta | Crítico | 🔴 CRÍTICO | Event-Driven Architecture |
| 2 | **Acoplamiento con fintech.User** | Alta | Alto | 🔴 CRÍTICO | Abstracción por UUID |
| 3 | **Transacciones Distribuidas** | Media | Crítico | 🔴 CRÍTICO | Eventos + Celery |
| 4 | **Falta de Validación de Datos** | Media | Crítico | 🔴 CRÍTICO | Validación estricta |
| 5 | **Procesamiento Síncrono** | Alta | Alto | 🟡 ALTO | Celery Tasks |
| 6 | **Consultas N+1** | Alta | Medio | 🟡 ALTO | Bulk Operations |
| 7 | **Estados Inconsistentes** | Media | Medio | 🟡 ALTO | State Machine |
| 8 | **Falta de Idempotencia** | Media | Medio | 🟡 ALTO | Unique Constraints |
| 9 | **Rate Limiting** | Baja | Medio | 🟢 BAJO | Rate Limiting Service |
| 10 | **Costos Excesivos** | Baja | Medio | 🟢 BAJO | Batching + Optimization |

---

## 🏗️ Arquitectura Propuesta: Servicio Universal

### **Principios de Diseño**

1. **Independencia Total**: La aplicación `notification` no depende de ninguna otra aplicación
2. **Abstracción por UUID**: Usa UUIDs en lugar de ForeignKeys para referencias
3. **Event-Driven**: Comunicación a través de eventos del sistema
4. **Service-Oriented**: API clara para que cualquier aplicación pueda usarla
5. **Async-First**: Procesamiento asíncrono desde el inicio

---

## 📁 Estructura de la Aplicación

```
apps/notification/
├── models.py                    # Modelos de notificaciones
├── services/                    # Servicios de negocio
│   ├── notification_service.py  # Servicio principal
│   ├── channel_service.py       # Gestión de canales
│   ├── template_service.py      # Gestión de plantillas
│   ├── rate_limiting.py         # Control de límites
│   └── validation_service.py    # Validación de datos
├── channels/                    # Implementaciones de canales
│   ├── email_service.py         # Email (SendGrid)
│   ├── sms_service.py          # SMS (Twilio)
│   ├── push_service.py         # Push (Firebase)
│   └── in_app_service.py       # Notificaciones in-app
├── events/                      # Eventos de notificación
│   ├── notification_events.py   # Definición de eventos
│   └── event_handlers.py        # Manejadores de eventos
├── api/                         # API para otras aplicaciones
│   ├── views.py                 # Vistas de API
│   ├── serializers.py           # Serializers
│   └── urls.py                  # URLs de API
├── tasks.py                     # Tareas Celery
├── admin.py                     # Admin de Django
├── apps.py                      # Configuración de la app
└── tests/                       # Tests unitarios
    ├── test_models.py
    ├── test_services.py
    └── test_api.py
```

---

## 🗄️ Modelos con Abstracciones

### **1. NotificationTemplate (Plantillas Reutilizables)**

```python
class NotificationTemplate(models.Model):
    """Plantillas de notificaciones reutilizables"""
    
    TEMPLATE_TYPES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App Notification'),
    ]
    
    NOTIFICATION_CATEGORIES = [
        ('system', 'Sistema'),
        ('payment', 'Pagos'),
        ('credit', 'Créditos'),
        ('user', 'Usuario'),
        ('marketing', 'Marketing'),
        ('security', 'Seguridad'),
    ]
    
    # Identificación
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    category = models.CharField(max_length=20, choices=NOTIFICATION_CATEGORIES)
    
    # Contenido
    subject = models.CharField(max_length=200, blank=True)  # Para email
    content = models.TextField()
    variables = models.JSONField(default=list)  # Variables disponibles
    
    # Configuración
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)  # Prioridad de envío
    rate_limit_per_hour = models.IntegerField(default=10)  # Límite por hora
    rate_limit_per_day = models.IntegerField(default=50)   # Límite por día
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'notification'
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['template_type', 'is_active']),
            models.Index(fields=['category', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
```

### **2. UserNotification (Notificaciones Individuales)**

```python
class UserNotification(models.Model):
    """Notificaciones individuales para usuarios"""
    
    NOTIFICATION_STATUS = [
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('sent', 'Enviada'),
        ('delivered', 'Entregada'),
        ('failed', 'Fallida'),
        ('read', 'Leída'),
        ('cancelled', 'Cancelada'),
    ]
    
    # Identificación
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Abstracción de usuario (NO ForeignKey)
    user_id = models.UUIDField(db_index=True)  # UUID del usuario
    user_email = models.EmailField(blank=True)  # Email para envío
    user_phone = models.CharField(max_length=20, blank=True)  # Teléfono para SMS
    
    # Referencias
    template = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE)
    
    # Estado y datos
    status = models.CharField(max_length=20, choices=NOTIFICATION_STATUS, default='pending')
    data = models.JSONField(default=dict)  # Datos específicos
    data_hash = models.CharField(max_length=64, blank=True)  # Hash para idempotencia
    
    # Programación
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Reintentos
    retry_count = models.PositiveIntegerField(default=0)
    max_retries = models.PositiveIntegerField(default=3)
    next_retry_at = models.DateTimeField(null=True, blank=True)
    
    # Metadatos
    source_app = models.CharField(max_length=50, blank=True)  # App que originó la notificación
    source_id = models.UUIDField(null=True, blank=True)  # ID del objeto origen
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'notification'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id', 'status']),
            models.Index(fields=['status', 'scheduled_at']),
            models.Index(fields=['template', 'status']),
            models.Index(fields=['source_app', 'source_id']),
        ]
        # Idempotencia: evitar notificaciones duplicadas
        unique_together = [
            ['user_id', 'template', 'data_hash', 'created_at'],
        ]
    
    def __str__(self):
        return f"Notificación {self.uid} para usuario {self.user_id}"
    
    def save(self, *args, **kwargs):
        # Generar hash para idempotencia
        if not self.data_hash:
            import hashlib
            data_str = str(sorted(self.data.items()))
            self.data_hash = hashlib.sha256(data_str.encode()).hexdigest()
        super().save(*args, **kwargs)
```

### **3. UserNotificationPreference (Preferencias)**

```python
class UserNotificationPreference(models.Model):
    """Preferencias de notificación por usuario"""
    
    # Abstracción de usuario (NO ForeignKey)
    user_id = models.UUIDField(unique=True, db_index=True)
    
    # Canales habilitados
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=True)
    push_enabled = models.BooleanField(default=True)
    in_app_enabled = models.BooleanField(default=True)
    
    # Categorías habilitadas
    system_notifications = models.BooleanField(default=True)
    payment_notifications = models.BooleanField(default=True)
    credit_notifications = models.BooleanField(default=True)
    user_notifications = models.BooleanField(default=True)
    marketing_notifications = models.BooleanField(default=False)
    security_notifications = models.BooleanField(default=True)
    
    # Configuración de frecuencia
    email_frequency = models.CharField(max_length=20, choices=[
        ('immediate', 'Inmediato'),
        ('daily', 'Diario'),
        ('weekly', 'Semanal'),
    ], default='immediate')
    
    # Horas silenciosas
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    quiet_hours_enabled = models.BooleanField(default=False)
    
    # Límites personalizados
    max_notifications_per_day = models.PositiveIntegerField(default=50)
    max_notifications_per_hour = models.PositiveIntegerField(default=10)
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'notification'
        db_table = 'notification_user_preference'
    
    def __str__(self):
        return f"Preferencias de usuario {self.user_id}"
```

### **4. NotificationDeliveryLog (Auditoría)**

```python
class NotificationDeliveryLog(models.Model):
    """Log de entregas para auditoría y debugging"""
    
    DELIVERY_STATUS = [
        ('success', 'Exitoso'),
        ('failed', 'Fallido'),
        ('pending', 'Pendiente'),
        ('retry', 'Reintento'),
        ('rate_limited', 'Rate Limited'),
    ]
    
    # Referencias
    notification = models.ForeignKey(UserNotification, on_delete=models.CASCADE, related_name='delivery_logs')
    
    # Detalles del envío
    channel = models.CharField(max_length=20)  # 'email', 'sms', 'push', 'in_app'
    service_used = models.CharField(max_length=50)  # 'sendgrid', 'twilio', 'firebase'
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS)
    
    # Respuesta del servicio
    response_data = models.JSONField(default=dict)
    error_message = models.TextField(blank=True)
    error_code = models.CharField(max_length=50, blank=True)
    
    # Métricas
    delivery_time = models.DurationField(null=True, blank=True)
    retry_count = models.PositiveIntegerField(default=0)
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'notification'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['channel', 'status']),
            models.Index(fields=['service_used', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Log {self.id}: {self.channel} - {self.status}"
```

---

## 🔧 Servicios con Abstracciones

### **1. NotificationService (Servicio Principal)**

```python
class NotificationService:
    """Servicio centralizado de notificaciones"""
    
    @staticmethod
    def notify_user(
        user_id: UUID,
        template_name: str,
        data: dict = None,
        scheduled_at: datetime = None,
        source_app: str = None,
        source_id: UUID = None,
        user_email: str = None,
        user_phone: str = None
    ) -> UserNotification:
        """
        Notificar a un usuario usando una plantilla
        
        Args:
            user_id: UUID del usuario (abstracción)
            template_name: Nombre de la plantilla
            data: Datos específicos para la plantilla
            scheduled_at: Cuándo enviar (None = inmediato)
            source_app: Aplicación que originó la notificación
            source_id: ID del objeto origen
            user_email: Email del usuario (opcional)
            user_phone: Teléfono del usuario (opcional)
        """
        try:
            # 1. Validar datos
            ValidationService.validate_notification_data(data or {})
            
            # 2. Obtener plantilla
            template = NotificationTemplate.objects.get(
                name=template_name,
                is_active=True
            )
            
            # 3. Verificar rate limiting
            if RateLimitingService.is_rate_limited(user_id, template):
                raise RateLimitExceeded(f"Rate limit exceeded for user {user_id}")
            
            # 4. Verificar preferencias del usuario
            preferences = UserNotificationPreference.objects.filter(user_id=user_id).first()
            if preferences and not NotificationService._should_send_notification(preferences, template):
                raise NotificationDisabled(f"Notifications disabled for user {user_id}")
            
            # 5. Crear notificación
            notification = UserNotification.objects.create(
                user_id=user_id,
                user_email=user_email,
                user_phone=user_phone,
                template=template,
                data=data or {},
                scheduled_at=scheduled_at,
                source_app=source_app,
                source_id=source_id
            )
            
            # 6. Programar envío
            if scheduled_at:
                send_notification_task.apply_async(
                    args=[notification.id],
                    eta=scheduled_at
                )
            else:
                send_notification_task.delay(notification.id)
            
            return notification
            
        except NotificationTemplate.DoesNotExist:
            raise TemplateNotFound(f"Template '{template_name}' not found")
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            raise
    
    @staticmethod
    def notify_bulk_users(
        user_data: List[dict],
        template_name: str,
        data: dict = None,
        scheduled_at: datetime = None,
        source_app: str = None,
        source_id: UUID = None
    ) -> List[UserNotification]:
        """
        Notificar a múltiples usuarios
        
        Args:
            user_data: Lista de diccionarios con user_id, user_email, user_phone
            template_name: Nombre de la plantilla
            data: Datos específicos para la plantilla
            scheduled_at: Cuándo enviar
            source_app: Aplicación que originó la notificación
            source_id: ID del objeto origen
        """
        notifications = []
        
        for user_info in user_data:
            try:
                notification = NotificationService.notify_user(
                    user_id=user_info['user_id'],
                    template_name=template_name,
                    data=data,
                    scheduled_at=scheduled_at,
                    source_app=source_app,
                    source_id=source_id,
                    user_email=user_info.get('user_email'),
                    user_phone=user_info.get('user_phone')
                )
                notifications.append(notification)
            except Exception as e:
                logger.error(f"Error notifying user {user_info['user_id']}: {e}")
                continue
        
        return notifications
    
    @staticmethod
    def cancel_notification(notification_id: int) -> bool:
        """Cancelar notificación pendiente"""
        try:
            notification = UserNotification.objects.get(id=notification_id)
            
            if notification.status in ['pending', 'processing']:
                notification.status = 'cancelled'
                notification.save()
                
                # Cancelar tarea Celery si existe
                # (implementar lógica de cancelación de tareas)
                
                return True
            else:
                return False
                
        except UserNotification.DoesNotExist:
            return False
    
    @staticmethod
    def mark_as_read(notification_id: int, user_id: UUID) -> bool:
        """Marcar notificación como leída"""
        try:
            notification = UserNotification.objects.get(
                id=notification_id,
                user_id=user_id
            )
            
            if notification.status in ['sent', 'delivered']:
                notification.status = 'read'
                notification.read_at = timezone.now()
                notification.save()
                return True
            else:
                return False
                
        except UserNotification.DoesNotExist:
            return False
    
    @staticmethod
    def _should_send_notification(preferences: UserNotificationPreference, template: NotificationTemplate) -> bool:
        """Verificar si se debe enviar la notificación basado en preferencias"""
        # Verificar canal
        if template.template_type == 'email' and not preferences.email_enabled:
            return False
        elif template.template_type == 'sms' and not preferences.sms_enabled:
            return False
        elif template.template_type == 'push' and not preferences.push_enabled:
            return False
        elif template.template_type == 'in_app' and not preferences.in_app_enabled:
            return False
        
        # Verificar categoría
        category_enabled = getattr(preferences, f"{template.category}_notifications", True)
        if not category_enabled:
            return False
        
        # Verificar horas silenciosas
        if preferences.quiet_hours_enabled:
            now = timezone.now().time()
            if preferences.quiet_hours_start and preferences.quiet_hours_end:
                if preferences.quiet_hours_start <= now <= preferences.quiet_hours_end:
                    return False
        
        return True
```

### **2. RateLimitingService (Control de Límites)**

```python
class RateLimitingService:
    """Servicio para control de rate limiting"""
    
    @staticmethod
    def is_rate_limited(user_id: UUID, template: NotificationTemplate) -> bool:
        """Verificar si el usuario está rate limited"""
        from django.core.cache import cache
        
        # Claves de cache para rate limiting
        hourly_key = f"notification_rate_hourly:{user_id}:{template.id}"
        daily_key = f"notification_rate_daily:{user_id}:{template.id}"
        
        # Verificar límites
        hourly_count = cache.get(hourly_key, 0)
        daily_count = cache.get(daily_key, 0)
        
        if hourly_count >= template.rate_limit_per_hour:
            return True
        
        if daily_count >= template.rate_limit_per_day:
            return True
        
        return False
    
    @staticmethod
    def increment_rate_limit(user_id: UUID, template: NotificationTemplate):
        """Incrementar contadores de rate limiting"""
        from django.core.cache import cache
        
        hourly_key = f"notification_rate_hourly:{user_id}:{template.id}"
        daily_key = f"notification_rate_daily:{user_id}:{template.id}"
        
        # Incrementar contadores
        cache.incr(hourly_key, 1)
        cache.incr(daily_key, 1)
        
        # Establecer expiración
        cache.expire(hourly_key, 3600)  # 1 hora
        cache.expire(daily_key, 86400)  # 1 día
```

### **3. ValidationService (Validación de Datos)**

```python
class ValidationService:
    """Servicio para validación de datos"""
    
    @staticmethod
    def validate_notification_data(data: dict):
        """Validar datos de notificación"""
        import re
        
        # Verificar que data es un diccionario
        if not isinstance(data, dict):
            raise ValidationError("Data must be a dictionary")
        
        # Validar cada campo
        for key, value in data.items():
            # Validar nombre del campo
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', key):
                raise ValidationError(f"Invalid field name: {key}")
            
            # Validar tipo de valor
            if not isinstance(value, (str, int, float, bool, list, dict)):
                raise ValidationError(f"Invalid value type for {key}")
            
            # Validar longitud de strings
            if isinstance(value, str) and len(value) > 1000:
                raise ValidationError(f"String too long for {key}")
            
            # Validar contenido de strings (prevenir XSS)
            if isinstance(value, str):
                dangerous_patterns = [
                    r'<script',
                    r'javascript:',
                    r'on\w+\s*=',
                    r'data:text/html',
                ]
                for pattern in dangerous_patterns:
                    if re.search(pattern, value, re.IGNORECASE):
                        raise ValidationError(f"Dangerous content in {key}")
    
    @staticmethod
    def validate_user_data(user_id: UUID, user_email: str = None, user_phone: str = None):
        """Validar datos del usuario"""
        import re
        
        # Validar UUID
        try:
            UUID(str(user_id))
        except ValueError:
            raise ValidationError("Invalid user_id format")
        
        # Validar email si se proporciona
        if user_email:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, user_email):
                raise ValidationError("Invalid email format")
        
        # Validar teléfono si se proporciona
        if user_phone:
            phone_pattern = r'^\+?[1-9]\d{1,14}$'
            if not re.match(phone_pattern, user_phone):
                raise ValidationError("Invalid phone format")
```

---

## 📡 API para Otras Aplicaciones

### **1. API Views**

```python
# apps/notification/api/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.notification.services import NotificationService
from apps.notification.api.serializers import NotificationRequestSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_notification(request):
    """API para enviar notificación"""
    serializer = NotificationRequestSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            notification = NotificationService.notify_user(
                user_id=serializer.validated_data['user_id'],
                template_name=serializer.validated_data['template_name'],
                data=serializer.validated_data.get('data', {}),
                scheduled_at=serializer.validated_data.get('scheduled_at'),
                source_app=serializer.validated_data.get('source_app'),
                source_id=serializer.validated_data.get('source_id'),
                user_email=serializer.validated_data.get('user_email'),
                user_phone=serializer.validated_data.get('user_phone')
            )
            
            return Response({
                'success': True,
                'notification_id': notification.id,
                'notification_uid': str(notification.uid)
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_bulk_notifications(request):
    """API para enviar notificaciones en lote"""
    # Implementar lógica similar para múltiples usuarios
    pass

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_notification(request, notification_id):
    """API para cancelar notificación"""
    success = NotificationService.cancel_notification(notification_id)
    
    return Response({
        'success': success
    }, status=status.HTTP_200_OK if success else status.HTTP_404_NOT_FOUND)
```

### **2. API Serializers**

```python
# apps/notification/api/serializers.py
from rest_framework import serializers
from uuid import UUID
from datetime import datetime

class NotificationRequestSerializer(serializers.Serializer):
    """Serializer para solicitudes de notificación"""
    
    user_id = serializers.UUIDField()
    template_name = serializers.CharField(max_length=100)
    data = serializers.DictField(required=False, default=dict)
    scheduled_at = serializers.DateTimeField(required=False, allow_null=True)
    source_app = serializers.CharField(max_length=50, required=False, allow_blank=True)
    source_id = serializers.UUIDField(required=False, allow_null=True)
    user_email = serializers.EmailField(required=False, allow_blank=True)
    user_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    
    def validate_user_id(self, value):
        """Validar UUID del usuario"""
        try:
            UUID(str(value))
            return value
        except ValueError:
            raise serializers.ValidationError("Invalid user_id format")
    
    def validate_template_name(self, value):
        """Validar que la plantilla existe"""
        from apps.notification.models import NotificationTemplate
        
        if not NotificationTemplate.objects.filter(name=value, is_active=True).exists():
            raise serializers.ValidationError(f"Template '{value}' not found or inactive")
        
        return value
    
    def validate_data(self, value):
        """Validar datos de la notificación"""
        from apps.notification.services import ValidationService
        
        try:
            ValidationService.validate_notification_data(value)
            return value
        except Exception as e:
            raise serializers.ValidationError(str(e))
```

---

## 🔄 Integración con Otras Aplicaciones

### **1. Integración con Credit (Sin Dependencias)**

```python
# apps/credit/services.py
from apps.notification.services import NotificationService
from uuid import UUID

class CreditService:
    @staticmethod
    def notify_payment_reminder(credit):
        """Notificar recordatorio de pago"""
        try:
            # Obtener datos del usuario (sin dependencia directa)
            user_data = CreditService._get_user_data(credit.user_id)
            
            NotificationService.notify_user(
                user_id=credit.user_id,
                template_name='payment_reminder',
                data={
                    'credit_id': str(credit.uid),
                    'amount': str(credit.pending_amount),
                    'due_date': credit.next_payment_date.strftime('%Y-%m-%d'),
                    'payment_url': f"/payments/{credit.uid}"
                },
                source_app='credit',
                source_id=credit.uid,
                user_email=user_data.get('email'),
                user_phone=user_data.get('phone')
            )
        except Exception as e:
            logger.error(f"Error sending payment reminder: {e}")
    
    @staticmethod
    def notify_credit_approved(credit):
        """Notificar crédito aprobado"""
        try:
            user_data = CreditService._get_user_data(credit.user_id)
            
            NotificationService.notify_user(
                user_id=credit.user_id,
                template_name='credit_approved',
                data={
                    'credit_id': str(credit.uid),
                    'amount': str(credit.amount),
                    'interest_rate': str(credit.interest_rate),
                    'term_days': credit.term_days
                },
                source_app='credit',
                source_id=credit.uid,
                user_email=user_data.get('email'),
                user_phone=user_data.get('phone')
            )
        except Exception as e:
            logger.error(f"Error sending credit approval: {e}")
    
    @staticmethod
    def _get_user_data(user_id: UUID) -> dict:
        """Obtener datos del usuario (abstracción)"""
        # Aquí se implementaría la lógica para obtener datos del usuario
        # sin crear dependencias circulares
        # Por ejemplo, usando una API interna o cache
        pass
```

### **2. Integración con User (Sin Dependencias)**

```python
# apps/user/services.py
from apps.notification.services import NotificationService
from uuid import UUID

class UserService:
    @staticmethod
    def notify_user_registration(user_id: UUID, user_email: str):
        """Notificar registro de usuario"""
        try:
            NotificationService.notify_user(
                user_id=user_id,
                template_name='user_welcome',
                data={
                    'welcome_message': '¡Bienvenido a nuestra plataforma!',
                    'next_steps': 'Completa tu perfil para acceder a créditos'
                },
                source_app='user',
                source_id=user_id,
                user_email=user_email
            )
        except Exception as e:
            logger.error(f"Error sending welcome notification: {e}")
    
    @staticmethod
    def notify_credit_available(user_id: UUID, user_email: str, available_amount: float):
        """Notificar crédito disponible"""
        try:
            NotificationService.notify_user(
                user_id=user_id,
                template_name='credit_available',
                data={
                    'available_amount': str(available_amount),
                    'apply_url': f"/credits/apply?user_id={user_id}"
                },
                source_app='user',
                source_id=user_id,
                user_email=user_email
            )
        except Exception as e:
            logger.error(f"Error sending credit available notification: {e}")
```

---

## 📋 Plantillas de Notificación

### **1. Plantillas para Créditos**

```python
# Plantillas que se crearán en la base de datos

CREDIT_TEMPLATES = [
    {
        'name': 'payment_reminder',
        'template_type': 'email',
        'category': 'payment',
        'subject': 'Recordatorio de Pago - Crédito {{credit_id}}',
        'content': """
        Hola,
        
        Te recordamos que tienes un pago pendiente:
        
        - Crédito: {{credit_id}}
        - Monto: ${{amount}}
        - Fecha límite: {{due_date}}
        
        Para realizar el pago, visita: {{payment_url}}
        
        Saludos,
        Equipo Fintech
        """,
        'variables': ['credit_id', 'amount', 'due_date', 'payment_url']
    },
    {
        'name': 'credit_approved',
        'template_type': 'email',
        'category': 'credit',
        'subject': '¡Tu crédito ha sido aprobado!',
        'content': """
        ¡Felicitaciones!
        
        Tu solicitud de crédito ha sido aprobada:
        
        - Crédito: {{credit_id}}
        - Monto: ${{amount}}
        - Tasa de interés: {{interest_rate}}%
        - Plazo: {{term_days}} días
        
        Pronto recibirás más detalles sobre el desembolso.
        
        Saludos,
        Equipo Fintech
        """,
        'variables': ['credit_id', 'amount', 'interest_rate', 'term_days']
    },
    {
        'name': 'credit_available',
        'template_type': 'email',
        'category': 'credit',
        'subject': '¡Tienes crédito disponible!',
        'content': """
        ¡Excelentes noticias!
        
        Tienes crédito disponible por ${{available_amount}}.
        
        Aplica ahora: {{apply_url}}
        
        Saludos,
        Equipo Fintech
        """,
        'variables': ['available_amount', 'apply_url']
    }
]
```

### **2. Plantillas para Usuarios**

```python
USER_TEMPLATES = [
    {
        'name': 'user_welcome',
        'template_type': 'email',
        'category': 'user',
        'subject': '¡Bienvenido a Fintech!',
        'content': """
        ¡Bienvenido a nuestra plataforma!
        
        {{welcome_message}}
        
        {{next_steps}}
        
        Saludos,
        Equipo Fintech
        """,
        'variables': ['welcome_message', 'next_steps']
    },
    {
        'name': 'profile_completion_reminder',
        'template_type': 'in_app',
        'category': 'user',
        'subject': 'Completa tu perfil',
        'content': """
        📝 Completa tu perfil
        
        Para acceder a mejores créditos, completa tu información personal.
        
        Completa ahora: {{profile_url}}
        """,
        'variables': ['profile_url']
    }
]
```

---

## 📅 Plan de Implementación

### **Fase 1: Base (Semana 1-2)**
- [ ] Crear aplicación `notification`
- [ ] Implementar modelos con abstracciones
- [ ] Configurar admin de Django
- [ ] Crear servicios básicos
- [ ] Testing unitario

### **Fase 2: Funcionalidad (Semana 3-4)**
- [ ] Implementar API para otras aplicaciones
- [ ] Crear plantillas básicas
- [ ] Implementar canales (email, in-app)
- [ ] Integrar con Celery
- [ ] Testing de integración

### **Fase 3: Optimización (Semana 5-6)**
- [ ] Implementar rate limiting
- [ ] Optimizar performance
- [ ] Implementar canales avanzados (SMS, push)
- [ ] Monitoreo y alertas
- [ ] Testing completo

### **Fase 4: Integración (Semana 7-8)**
- [ ] Integrar con aplicación credit
- [ ] Integrar con aplicación user
- [ ] Testing end-to-end
- [ ] Documentación
- [ ] Deployment

---

## 🛡️ Medidas de Mitigación de Riesgos

### **Riesgo 1: Dependencias Circulares**
- **Mitigación**: Usar UUIDs en lugar de ForeignKeys
- **Verificación**: Testing de independencia

### **Riesgo 2: Transacciones Distribuidas**
- **Mitigación**: Procesamiento asíncrono con Celery
- **Verificación**: Testing de consistencia

### **Riesgo 3: Falta de Validación**
- **Mitigación**: Validación estricta en servicios
- **Verificación**: Testing de seguridad

### **Riesgo 4: Performance**
- **Mitigación**: Rate limiting y batching
- **Verificación**: Testing de carga

### **Riesgo 5: Costos**
- **Mitigación**: Optimización de envíos
- **Verificación**: Monitoreo de costos

---

## 📊 Métricas de Éxito

### **Técnicas:**
- ✅ 0 dependencias circulares
- ✅ < 100ms tiempo de respuesta API
- ✅ < 1% tasa de error en envíos
- ✅ 100% cobertura de tests

### **Funcionales:**
- ✅ Notificaciones de créditos funcionando
- ✅ Notificaciones de usuarios funcionando
- ✅ Preferencias de usuario respetadas
- ✅ Rate limiting funcionando

### **Operacionales:**
- ✅ Monitoreo en tiempo real
- ✅ Alertas automáticas
- ✅ Logs completos para auditoría
- ✅ Dashboard de métricas

---

**Este plan garantiza una aplicación `notification` robusta, escalable y sin dependencias circulares que puede ser utilizada por cualquier aplicación del sistema.**

