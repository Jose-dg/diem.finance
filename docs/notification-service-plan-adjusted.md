# 🎯 Plan Ajustado: Aplicación `notification` para Modelo de Negocio Fintech

## 📊 Análisis de Nuestro Modelo de Negocio

### **Entidades Principales Identificadas:**

1. **User** - Usuarios del sistema
2. **Credit** - Créditos otorgados
3. **Transaction** - Transacciones financieras
4. **Installment** - Cuotas de créditos
5. **Account** - Cuentas bancarias
6. **Seller** - Vendedores/Agentes
7. **Expense** - Gastos
8. **Adjustment** - Ajustes de créditos

### **Flujos de Negocio Principales:**
- Solicitud de crédito → Aprobación → Desembolso → Pagos → Finalización
- Transacciones → Categorización → Reportes
- Gastos → Categorización → Control
- Ajustes → Aplicación → Recalculo

---

## 🏗️ Modelos Abstractos Adaptados a Fintech

### **1. NotificationTemplate (Plantillas Específicas de Fintech)**

```python
class NotificationTemplate(models.Model):
    """Plantillas de notificaciones específicas para fintech"""
    
    TEMPLATE_TYPES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App Notification'),
    ]
    
    # Categorías específicas de fintech
    NOTIFICATION_CATEGORIES = [
        ('credit', 'Créditos'),
        ('payment', 'Pagos'),
        ('transaction', 'Transacciones'),
        ('user', 'Usuario'),
        ('system', 'Sistema'),
        ('marketing', 'Marketing'),
        ('security', 'Seguridad'),
        ('expense', 'Gastos'),
        ('adjustment', 'Ajustes'),
    ]
    
    # Identificación
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    category = models.CharField(max_length=20, choices=NOTIFICATION_CATEGORIES)
    
    # Contenido
    subject = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    variables = models.JSONField(default=list)  # Variables disponibles
    
    # Configuración específica de fintech
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    rate_limit_per_hour = models.IntegerField(default=10)
    rate_limit_per_day = models.IntegerField(default=50)
    
    # Configuración de negocio
    requires_user_consent = models.BooleanField(default=False)  # GDPR
    is_marketing = models.BooleanField(default=False)  # Marketing vs Operacional
    can_be_disabled = models.BooleanField(default=True)  # Si el usuario puede desactivarla
    
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
        return f"{self.name} ({self.get_category_display()})"
```

### **2. UserNotification (Notificaciones para Usuarios Fintech)**

```python
class UserNotification(models.Model):
    """Notificaciones para usuarios del sistema fintech"""
    
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
    
    # Destinatario (abstracción por UUID)
    user_id = models.UUIDField(db_index=True)  # UUID del usuario fintech
    user_email = models.EmailField(blank=True)
    user_phone = models.CharField(max_length=20, blank=True)
    
    # Referencias
    template = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE)
    
    # Estado y datos
    status = models.CharField(max_length=20, choices=NOTIFICATION_STATUS, default='pending')
    data = models.JSONField(default=dict)  # Datos específicos de fintech
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
    
    # Contexto específico de fintech
    source_module = models.CharField(max_length=50, blank=True)  # 'credit', 'payment', 'transaction'
    source_id = models.UUIDField(null=True, blank=True)  # ID del objeto origen
    business_context = models.JSONField(default=dict)  # Contexto adicional de negocio
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'notification'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id', 'status']),
            models.Index(fields=['status', 'scheduled_at']),
            models.Index(fields=['template', 'status']),
            models.Index(fields=['source_module', 'source_id']),
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

### **3. UserNotificationPreference (Preferencias Específicas de Fintech)**

```python
class UserNotificationPreference(models.Model):
    """Preferencias de notificación específicas para usuarios fintech"""
    
    # Abstracción de usuario
    user_id = models.UUIDField(unique=True, db_index=True)
    
    # Canales habilitados
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=True)
    push_enabled = models.BooleanField(default=True)
    in_app_enabled = models.BooleanField(default=True)
    
    # Categorías específicas de fintech
    credit_notifications = models.BooleanField(default=True)
    payment_notifications = models.BooleanField(default=True)
    transaction_notifications = models.BooleanField(default=True)
    user_notifications = models.BooleanField(default=True)
    system_notifications = models.BooleanField(default=True)
    marketing_notifications = models.BooleanField(default=False)
    security_notifications = models.BooleanField(default=True)
    expense_notifications = models.BooleanField(default=True)
    adjustment_notifications = models.BooleanField(default=True)
    
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
    
    # Configuración específica de fintech
    urgent_payment_reminders = models.BooleanField(default=True)  # Recordatorios urgentes de pago
    credit_limit_alerts = models.BooleanField(default=True)  # Alertas de límite de crédito
    security_alerts = models.BooleanField(default=True)  # Alertas de seguridad
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'notification'
        db_table = 'notification_user_preference'
    
    def __str__(self):
        return f"Preferencias de usuario {self.user_id}"
```

### **4. NotificationDeliveryLog (Auditoría Específica de Fintech)**

```python
class NotificationDeliveryLog(models.Model):
    """Log de entregas para auditoría específica de fintech"""
    
    DELIVERY_STATUS = [
        ('success', 'Exitoso'),
        ('failed', 'Fallido'),
        ('pending', 'Pendiente'),
        ('retry', 'Reintento'),
        ('rate_limited', 'Rate Limited'),
        ('user_disabled', 'Usuario Deshabilitado'),
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
    
    # Contexto específico de fintech
    business_context = models.JSONField(default=dict)  # Contexto adicional
    
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

## 🔧 Servicios Adaptados a Fintech

### **1. NotificationService (Servicio Principal para Fintech)**

```python
class NotificationService:
    """Servicio de notificaciones específico para fintech"""
    
    @staticmethod
    def notify_user(
        user_id: UUID,
        template_name: str,
        data: dict = None,
        scheduled_at: datetime = None,
        source_module: str = None,
        source_id: UUID = None,
        user_email: str = None,
        user_phone: str = None,
        business_context: dict = None
    ) -> UserNotification:
        """
        Notificar a un usuario usando una plantilla específica de fintech
        
        Args:
            user_id: UUID del usuario fintech
            template_name: Nombre de la plantilla
            data: Datos específicos para la plantilla
            scheduled_at: Cuándo enviar (None = inmediato)
            source_module: Módulo que origina la notificación ('credit', 'payment', etc.)
            source_id: ID del objeto origen
            user_email: Email del usuario (opcional)
            user_phone: Teléfono del usuario (opcional)
            business_context: Contexto adicional de negocio
        """
        try:
            # 1. Validar datos específicos de fintech
            ValidationService.validate_fintech_notification_data(data or {})
            
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
                source_module=source_module,
                source_id=source_id,
                business_context=business_context or {}
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
    def notify_credit_payment_reminder(credit, installment=None):
        """Notificar recordatorio de pago de crédito"""
        try:
            # Obtener datos del usuario
            user_data = NotificationService._get_user_data(credit.user_id)
            
            # Preparar datos específicos de fintech
            data = {
                'credit_id': str(credit.uid),
                'credit_amount': str(credit.price),
                'pending_amount': str(credit.pending_amount),
                'due_date': installment.due_date.strftime('%Y-%m-%d') if installment else credit.second_date_payment.strftime('%Y-%m-%d'),
                'installment_number': installment.number if installment else None,
                'payment_url': f"/payments/{credit.uid}"
            }
            
            # Contexto de negocio
            business_context = {
                'credit_status': credit.state,
                'is_overdue': installment.is_overdue() if installment else False,
                'days_overdue': installment.days_overdue if installment else 0
            }
            
            NotificationService.notify_user(
                user_id=credit.user_id,
                template_name='credit_payment_reminder',
                data=data,
                source_module='credit',
                source_id=credit.uid,
                user_email=user_data.get('email'),
                user_phone=user_data.get('phone'),
                business_context=business_context
            )
        except Exception as e:
            logger.error(f"Error sending payment reminder: {e}")
    
    @staticmethod
    def notify_credit_approved(credit):
        """Notificar crédito aprobado"""
        try:
            user_data = NotificationService._get_user_data(credit.user_id)
            
            data = {
                'credit_id': str(credit.uid),
                'amount': str(credit.price),
                'interest_rate': str(credit.interest),
                'term_days': credit.credit_days,
                'first_payment_date': credit.first_date_payment.strftime('%Y-%m-%d'),
                'disbursement_url': f"/credits/{credit.uid}/disbursement"
            }
            
            business_context = {
                'credit_type': credit.subcategory.name if credit.subcategory else 'General',
                'seller_name': credit.seller.user.get_full_name() if credit.seller else None
            }
            
            NotificationService.notify_user(
                user_id=credit.user_id,
                template_name='credit_approved',
                data=data,
                source_module='credit',
                source_id=credit.uid,
                user_email=user_data.get('email'),
                user_phone=user_data.get('phone'),
                business_context=business_context
            )
        except Exception as e:
            logger.error(f"Error sending credit approval: {e}")
    
    @staticmethod
    def notify_transaction_completed(transaction):
        """Notificar transacción completada"""
        try:
            user_data = NotificationService._get_user_data(transaction.user.id_user)
            
            data = {
                'transaction_id': str(transaction.uid),
                'amount': str(transaction.amount),
                'type': transaction.get_transaction_type_display(),
                'description': transaction.description,
                'date': transaction.date.strftime('%Y-%m-%d %H:%M'),
                'transaction_url': f"/transactions/{transaction.uid}"
            }
            
            business_context = {
                'transaction_category': transaction.category.name if transaction.category else 'Sin categoría',
                'source': transaction.source
            }
            
            NotificationService.notify_user(
                user_id=transaction.user.id_user,
                template_name='transaction_completed',
                data=data,
                source_module='transaction',
                source_id=transaction.uid,
                user_email=user_data.get('email'),
                user_phone=user_data.get('phone'),
                business_context=business_context
            )
        except Exception as e:
            logger.error(f"Error sending transaction notification: {e}")
    
    @staticmethod
    def _get_user_data(user_id: UUID) -> dict:
        """Obtener datos del usuario (abstracción)"""
        # Aquí se implementaría la lógica para obtener datos del usuario
        # sin crear dependencias circulares
        # Por ejemplo, usando una API interna o cache
        pass
    
    @staticmethod
    def _should_send_notification(preferences: UserNotificationPreference, template: NotificationTemplate) -> bool:
        """Verificar si se debe enviar la notificación basado en preferencias de fintech"""
        # Verificar canal
        if template.template_type == 'email' and not preferences.email_enabled:
            return False
        elif template.template_type == 'sms' and not preferences.sms_enabled:
            return False
        elif template.template_type == 'push' and not preferences.push_enabled:
            return False
        elif template.template_type == 'in_app' and not preferences.in_app_enabled:
            return False
        
        # Verificar categoría específica de fintech
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

---

## 📋 Plantillas Específicas de Fintech

### **1. Plantillas para Créditos**

```python
CREDIT_TEMPLATES = [
    {
        'name': 'credit_payment_reminder',
        'template_type': 'email',
        'category': 'payment',
        'subject': 'Recordatorio de Pago - Crédito {{credit_id}}',
        'content': """
        Hola,
        
        Te recordamos que tienes un pago pendiente:
        
        - Crédito: {{credit_id}}
        - Monto pendiente: ${{pending_amount}}
        - Fecha límite: {{due_date}}
        {% if installment_number %}
        - Cuota: {{installment_number}}
        {% endif %}
        
        Para realizar el pago, visita: {{payment_url}}
        
        Saludos,
        Equipo Fintech
        """,
        'variables': ['credit_id', 'pending_amount', 'due_date', 'installment_number', 'payment_url'],
        'requires_user_consent': False,
        'is_marketing': False,
        'can_be_disabled': True
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
        - Primer pago: {{first_payment_date}}
        
        Para acceder al desembolso, visita: {{disbursement_url}}
        
        Saludos,
        Equipo Fintech
        """,
        'variables': ['credit_id', 'amount', 'interest_rate', 'term_days', 'first_payment_date', 'disbursement_url'],
        'requires_user_consent': False,
        'is_marketing': False,
        'can_be_disabled': False
    },
    {
        'name': 'credit_overdue_alert',
        'template_type': 'sms',
        'category': 'payment',
        'subject': 'Alerta de Mora',
        'content': """
        ALERTA: Tu crédito {{credit_id}} está en mora.
        Monto pendiente: ${{pending_amount}}
        Días de mora: {{days_overdue}}
        Paga ahora: {{payment_url}}
        """,
        'variables': ['credit_id', 'pending_amount', 'days_overdue', 'payment_url'],
        'requires_user_consent': False,
        'is_marketing': False,
        'can_be_disabled': False
    }
]
```

### **2. Plantillas para Transacciones**

```python
TRANSACTION_TEMPLATES = [
    {
        'name': 'transaction_completed',
        'template_type': 'email',
        'category': 'transaction',
        'subject': 'Transacción Completada - {{transaction_id}}',
        'content': """
        Tu transacción ha sido completada exitosamente:
        
        - ID: {{transaction_id}}
        - Tipo: {{type}}
        - Monto: ${{amount}}
        - Fecha: {{date}}
        - Descripción: {{description}}
        
        Ver detalles: {{transaction_url}}
        
        Saludos,
        Equipo Fintech
        """,
        'variables': ['transaction_id', 'type', 'amount', 'date', 'description', 'transaction_url'],
        'requires_user_consent': False,
        'is_marketing': False,
        'can_be_disabled': True
    }
]
```

### **3. Plantillas para Usuarios**

```python
USER_TEMPLATES = [
    {
        'name': 'user_welcome',
        'template_type': 'email',
        'category': 'user',
        'subject': '¡Bienvenido a Fintech!',
        'content': """
        ¡Bienvenido a nuestra plataforma!
        
        Tu cuenta ha sido creada exitosamente.
        
        Para comenzar a solicitar créditos, completa tu perfil.
        
        Saludos,
        Equipo Fintech
        """,
        'variables': [],
        'requires_user_consent': True,
        'is_marketing': True,
        'can_be_disabled': True
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
        'variables': ['profile_url'],
        'requires_user_consent': False,
        'is_marketing': False,
        'can_be_disabled': True
    }
]
```

---

## 🔄 Integración con Aplicaciones Fintech

### **1. Integración con Credit (Sin Dependencias)**

```python
# apps/fintech/services/credit_service.py
from apps.notification.services import NotificationService
from uuid import UUID

class CreditService:
    @staticmethod
    def notify_payment_reminder(credit, installment=None):
        """Notificar recordatorio de pago"""
        NotificationService.notify_credit_payment_reminder(credit, installment)
    
    @staticmethod
    def notify_credit_approved(credit):
        """Notificar crédito aprobado"""
        NotificationService.notify_credit_approved(credit)
    
    @staticmethod
    def notify_credit_overdue(credit, installment):
        """Notificar crédito en mora"""
        NotificationService.notify_user(
            user_id=credit.user.id_user,
            template_name='credit_overdue_alert',
            data={
                'credit_id': str(credit.uid),
                'pending_amount': str(credit.pending_amount),
                'days_overdue': installment.days_overdue,
                'payment_url': f"/payments/{credit.uid}"
            },
            source_module='credit',
            source_id=credit.uid
        )
```

### **2. Integración con Transaction (Sin Dependencias)**

```python
# apps/fintech/services/transaction_service.py
from apps.notification.services import NotificationService

class TransactionService:
    @staticmethod
    def notify_transaction_completed(transaction):
        """Notificar transacción completada"""
        NotificationService.notify_transaction_completed(transaction)
    
    @staticmethod
    def notify_large_transaction(transaction):
        """Notificar transacción de monto alto"""
        if transaction.amount > 10000:  # Transacción de más de $10,000
            NotificationService.notify_user(
                user_id=transaction.user.id_user,
                template_name='large_transaction_alert',
                data={
                    'transaction_id': str(transaction.uid),
                    'amount': str(transaction.amount),
                    'date': transaction.date.strftime('%Y-%m-%d %H:%M')
                },
                source_module='transaction',
                source_id=transaction.uid
            )
```

---

## 📅 Plan de Implementación Ajustado

### **Fase 1: Base Fintech (Semana 1-2)**
- [ ] Crear aplicación `notification`
- [ ] Implementar modelos específicos de fintech
- [ ] Configurar admin de Django
- [ ] Crear servicios básicos
- [ ] Testing unitario

### **Fase 2: Plantillas Fintech (Semana 3-4)**
- [ ] Crear plantillas específicas de créditos
- [ ] Crear plantillas específicas de transacciones
- [ ] Crear plantillas específicas de usuarios
- [ ] Implementar canales (email, in-app)
- [ ] Integrar con Celery

### **Fase 3: Integración Fintech (Semana 5-6)**
- [ ] Integrar con aplicación credit
- [ ] Integrar con aplicación transaction
- [ ] Integrar con aplicación user
- [ ] Testing de integración
- [ ] Optimización de performance

### **Fase 4: Funcionalidades Avanzadas (Semana 7-8)**
- [ ] Implementar rate limiting
- [ ] Implementar canales avanzados (SMS, push)
- [ ] Monitoreo y alertas
- [ ] Testing completo
- [ ] Documentación

---

## 🛡️ Beneficios de esta Implementación Ajustada

### **1. Específica para Fintech**
- ✅ Plantillas adaptadas al negocio de créditos
- ✅ Categorías específicas de fintech
- ✅ Contexto de negocio incluido
- ✅ Validaciones específicas del dominio

### **2. Mantiene Abstracción**
- ✅ No depende de modelos específicos
- ✅ Usa UUIDs para referencias
- ✅ Servicios reutilizables
- ✅ Fácil de extender

### **3. Escalable**
- ✅ Una sola implementación para todo fintech
- ✅ Fácil agregar nuevas notificaciones
- ✅ Performance optimizada
- ✅ Monitoreo centralizado

**Esta implementación combina lo mejor de ambos mundos: abstracción técnica con especificidad de negocio.**

