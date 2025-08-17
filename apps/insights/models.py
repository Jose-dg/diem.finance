from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from decimal import Decimal

class CustomerLifetimeValue(models.Model):
    CLV_TIERS = [
        ('bronze', _('Bronce (<$1,000)')),
        ('silver', _('Plata ($1,000-$5,000)')),
        ('gold', _('Oro ($5,000-$15,000)')),
        ('platinum', _('Platino (>$15,000)')),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('usuario'),
        related_name='lifetime_value'
    )
    current_clv = models.DecimalField(_('CLV actual'), max_digits=15, decimal_places=2, default=Decimal('0.00'))
    predicted_clv = models.DecimalField(_('CLV predicho'), max_digits=15, decimal_places=2, default=Decimal('0.00'))
    clv_tier = models.CharField(_('nivel CLV'), max_length=10, choices=CLV_TIERS, default='bronze')
    total_revenue = models.DecimalField(_('ingresos totales'), max_digits=15, decimal_places=2, default=Decimal('0.00'))
    total_credits = models.IntegerField(_('total créditos'), default=0)
    avg_credit_amount = models.DecimalField(_('monto promedio crédito'), max_digits=12, decimal_places=2, default=Decimal('0.00'))
    avg_credit_frequency = models.DecimalField(_('frecuencia promedio (por año)'), max_digits=6, decimal_places=2, default=Decimal('0.00'))
    first_credit_date = models.DateTimeField(_('fecha primer crédito'), null=True, blank=True)
    last_credit_date = models.DateTimeField(_('fecha último crédito'), null=True, blank=True)
    next_credit_prediction = models.DateField(_('predicción próximo crédito'), null=True, blank=True)
    churn_probability = models.DecimalField(_('probabilidad de abandono'), max_digits=5, decimal_places=2, default=Decimal('0.00'))
    calculation_metadata = models.JSONField(_('metadatos de cálculo'), default=dict)
    updated_at = models.DateTimeField(_('última actualización'), auto_now=True)

    class Meta:
        verbose_name = _('valor de vida del cliente')
        verbose_name_plural = _('valores de vida de clientes')
        ordering = ['-current_clv']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['clv_tier']),
            models.Index(fields=['current_clv']),
            models.Index(fields=['updated_at'])
        ]

    def __str__(self):
        return _('CLV de %(username)s: %(clv)s') % {'username': self.user.username, 'clv': self.current_clv}

    def clean(self):
        if self.current_clv < 0 or self.predicted_clv < 0:
            raise ValidationError(_('El CLV no puede ser negativo.'))

class CustomerActivity(models.Model):
    ACTIVITY_TYPES = [
        ('credit_request', _('Solicitud de crédito')),
        ('credit_approved', _('Crédito aprobado')),
        ('credit_rejected', _('Crédito rechazado')),
        ('payment_made', _('Pago realizado')),
        ('payment_missed', _('Pago perdido')),
        ('account_login', _('Inicio de sesión')),
        ('profile_update', _('Actualización de perfil')),
        ('support_contact', _('Contacto con soporte')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('usuario'), related_name='activities')
    activity_type = models.CharField(_('tipo de actividad'), max_length=20, choices=ACTIVITY_TYPES)
    activity_date = models.DateTimeField(_('fecha de actividad'), auto_now_add=True)
    credit = models.ForeignKey('fintech.Credit', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('crédito'), related_name='customer_activities')
    transaction = models.ForeignKey('fintech.Transaction', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('transacción'), related_name='customer_activities')
    description = models.TextField(_('descripción'), blank=True)
    amount = models.DecimalField(_('monto'), max_digits=12, decimal_places=2, null=True, blank=True)
    activity_metadata = models.JSONField(_('metadatos de actividad'), default=dict)
    ip_address = models.GenericIPAddressField(_('dirección IP'), null=True, blank=True)
    user_agent = models.TextField(_('user agent'), blank=True)

    class Meta:
        verbose_name = _('actividad del cliente')
        verbose_name_plural = _('actividades de clientes')
        ordering = ['-activity_date']
        indexes = [
            models.Index(fields=['user', 'activity_type']),
            models.Index(fields=['activity_date']),
            models.Index(fields=['activity_type', 'activity_date'])
        ]

    def __str__(self):
        from django.utils import timezone
        return _('%(type)s - %(user)s - %(date)s') % {
            'type': self.get_activity_type_display(),
            'user': self.user.username,
            'date': self.activity_date.strftime('%Y-%m-%d %H:%M')
        }

class CreditRecommendation(models.Model):
    RECOMMENDATION_TYPES = [
        ('credit_limit_increase', _('Aumento de límite de crédito')),
        ('new_credit_offer', _('Nueva oferta de crédito')),
        ('refinancing', _('Refinanciamiento')),
        ('payment_plan', _('Plan de pagos')),
        ('credit_education', _('Educación crediticia')),
        ('no_recommendation', _('Sin recomendación')),
    ]

    RECOMMENDATION_PRIORITIES = [
        ('low', _('Baja')),
        ('medium', _('Media')),
        ('high', _('Alta')),
        ('urgent', _('Urgente')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('usuario'), related_name='credit_recommendations')
    recommendation_type = models.CharField(_('tipo de recomendación'), max_length=25, choices=RECOMMENDATION_TYPES)
    priority = models.CharField(_('prioridad'), max_length=10, choices=RECOMMENDATION_PRIORITIES, default='medium')
    title = models.CharField(_('título'), max_length=200)
    description = models.TextField(_('descripción'))
    suggested_amount = models.DecimalField(_('monto sugerido'), max_digits=12, decimal_places=2, null=True, blank=True)
    suggested_terms = models.IntegerField(_('plazo sugerido (días)'), null=True, blank=True)
    influencing_factors = models.JSONField(_('factores influyentes'), default=dict)
    confidence_score = models.DecimalField(_('puntuación de confianza'), max_digits=5, decimal_places=2)
    is_active = models.BooleanField(_('activa'), default=True)
    is_implemented = models.BooleanField(_('implementada'), default=False)
    implemented_date = models.DateTimeField(_('fecha de implementación'), null=True, blank=True)
    created_at = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    expires_at = models.DateTimeField(_('fecha de expiración'), null=True, blank=True)

    class Meta:
        verbose_name = _('recomendación de crédito')
        verbose_name_plural = _('recomendaciones de crédito')
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['user', 'recommendation_type']),
            models.Index(fields=['priority', 'is_active']),
            models.Index(fields=['created_at']),
            models.Index(fields=['expires_at'])
        ]

    def __str__(self):
        return _('%(type)s para %(user)s - %(priority)s') % {
            'type': self.get_recommendation_type_display(),
            'user': self.user.username,
            'priority': self.get_priority_display()
        }

    @property
    def is_expired(self):
        if self.expires_at:
            from django.utils import timezone
            return timezone.now() > self.expires_at
        return False

    def clean(self):
        if self.suggested_amount is not None and self.suggested_amount < 0:
            raise ValidationError({'suggested_amount': _('El monto sugerido no puede ser negativo.')})
        if self.suggested_terms is not None and self.suggested_terms < 0:
            raise ValidationError({'suggested_terms': _('El plazo sugerido no puede ser negativo.')})
        if not (Decimal('0') <= self.confidence_score <= Decimal('100')):
            raise ValidationError({'confidence_score': _('La confianza debe estar entre 0 y 100.')})

class FinancialControlMetrics(models.Model):
    """Métricas de control financiero para seguimiento de morosidad"""
    
    RISK_LEVELS = [
        ('low', _('Bajo')),
        ('medium', _('Medio')),
        ('high', _('Alto')),
        ('critical', _('Crítico')),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('usuario'),
        related_name='financial_metrics'
    )
    
    # Métricas de morosidad
    total_overdue_amount = models.DecimalField(
        _('monto total en mora'), 
        max_digits=15, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    overdue_credits_count = models.IntegerField(_('número de créditos en mora'), default=0)
    days_in_default = models.IntegerField(_('días en mora'), default=0)
    max_days_overdue = models.IntegerField(_('máximo días en mora'), default=0)
    
    # Métricas de riesgo
    risk_level = models.CharField(
        _('nivel de riesgo'), 
        max_length=10, 
        choices=RISK_LEVELS, 
        default='low'
    )
    risk_score = models.DecimalField(
        _('puntuación de riesgo'), 
        max_digits=5, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    
    # Métricas de comportamiento
    payment_frequency = models.DecimalField(
        _('frecuencia de pagos (por mes)'), 
        max_digits=6, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    avg_payment_delay = models.DecimalField(
        _('retraso promedio de pagos (días)'), 
        max_digits=6, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    
    # Historial de morosidad
    default_history = models.JSONField(
        _('historial de morosidad'), 
        default=list
    )
    
    # Metadatos
    last_calculation = models.DateTimeField(_('último cálculo'), auto_now=True)
    calculation_metadata = models.JSONField(_('metadatos de cálculo'), default=dict)
    
    class Meta:
        verbose_name = _('métrica de control financiero')
        verbose_name_plural = _('métricas de control financiero')
        ordering = ['-risk_score', '-total_overdue_amount']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['risk_level']),
            models.Index(fields=['risk_score']),
            models.Index(fields=['total_overdue_amount']),
            models.Index(fields=['last_calculation'])
        ]
    
    def __str__(self):
        return _('Control financiero de %(username)s - Riesgo: %(risk)s') % {
            'username': self.user.username,
            'risk': self.get_risk_level_display()
        }
    
    @property
    def is_high_risk(self):
        return self.risk_level in ['high', 'critical']
    
    @property
    def overdue_percentage(self):
        """Porcentaje de morosidad sobre el total de créditos"""
        total_credits = self.user.credits.count()
        if total_credits > 0:
            return (self.overdue_credits_count / total_credits) * 100
        return 0

class FinancialAlert(models.Model):
    """Alertas financieras para seguimiento de clientes morosos"""
    
    ALERT_TYPES = [
        ('payment_overdue', _('Pago vencido')),
        ('multiple_overdue', _('Múltiples pagos vencidos')),
        ('risk_increase', _('Incremento de riesgo')),
        ('payment_pattern_change', _('Cambio en patrón de pagos')),
        ('credit_limit_exceeded', _('Límite de crédito excedido')),
        ('recovery_opportunity', _('Oportunidad de recuperación')),
    ]
    
    ALERT_PRIORITIES = [
        ('low', _('Baja')),
        ('medium', _('Media')),
        ('high', _('Alta')),
        ('urgent', _('Urgente')),
    ]
    
    ALERT_STATUSES = [
        ('active', _('Activa')),
        ('acknowledged', _('Reconocida')),
        ('resolved', _('Resuelta')),
        ('expired', _('Expirada')),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('usuario'),
        related_name='financial_alerts'
    )
    
    alert_type = models.CharField(_('tipo de alerta'), max_length=25, choices=ALERT_TYPES)
    priority = models.CharField(_('prioridad'), max_length=10, choices=ALERT_PRIORITIES, default='medium')
    status = models.CharField(_('estado'), max_length=15, choices=ALERT_STATUSES, default='active')
    
    title = models.CharField(_('título'), max_length=200)
    description = models.TextField(_('descripción'))
    
    # Datos específicos de la alerta
    alert_data = models.JSONField(_('datos de la alerta'), default=dict)
    
    # Fechas
    created_at = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    acknowledged_at = models.DateTimeField(_('fecha de reconocimiento'), null=True, blank=True)
    resolved_at = models.DateTimeField(_('fecha de resolución'), null=True, blank=True)
    expires_at = models.DateTimeField(_('fecha de expiración'), null=True, blank=True)
    
    # Usuario que gestiona la alerta
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('asignado a'),
        related_name='assigned_alerts'
    )
    
    # Notificaciones
    notification_sent = models.BooleanField(_('notificación enviada'), default=False)
    notification_channels = models.JSONField(_('canales de notificación'), default=list)
    
    class Meta:
        verbose_name = _('alerta financiera')
        verbose_name_plural = _('alertas financieras')
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['user', 'alert_type']),
            models.Index(fields=['priority', 'status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['assigned_to'])
        ]
    
    def __str__(self):
        return _('%(type)s - %(user)s - %(priority)s') % {
            'type': self.get_alert_type_display(),
            'user': self.user.username,
            'priority': self.get_priority_display()
        }
    
    @property
    def is_expired(self):
        if self.expires_at:
            from django.utils import timezone
            return timezone.now() > self.expires_at
        return False
    
    @property
    def is_active(self):
        return self.status == 'active' and not self.is_expired
    
    def acknowledge(self, user=None):
        """Reconocer la alerta"""
        from django.utils import timezone
        self.status = 'acknowledged'
        self.acknowledged_at = timezone.now()
        if user:
            self.assigned_to = user
        self.save(update_fields=['status', 'acknowledged_at', 'assigned_to'])
    
    def resolve(self, resolution_notes=None):
        """Resolver la alerta"""
        from django.utils import timezone
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        if resolution_notes:
            self.alert_data['resolution_notes'] = resolution_notes
        self.save(update_fields=['status', 'resolved_at', 'alert_data'])

class DefaultersReport(models.Model):
    """Reporte detallado de clientes morosos"""
    
    REPORT_TYPES = [
        ('daily', _('Diario')),
        ('weekly', _('Semanal')),
        ('monthly', _('Mensual')),
        ('quarterly', _('Trimestral')),
        ('custom', _('Personalizado')),
    ]
    
    report_type = models.CharField(_('tipo de reporte'), max_length=15, choices=REPORT_TYPES)
    report_date = models.DateField(_('fecha del reporte'), auto_now_add=True)
    
    # Métricas del reporte
    total_defaulters = models.IntegerField(_('total de morosos'), default=0)
    total_overdue_amount = models.DecimalField(
        _('monto total en mora'), 
        max_digits=15, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    avg_days_overdue = models.DecimalField(
        _('promedio días en mora'), 
        max_digits=6, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    
    # Distribución por niveles de riesgo
    low_risk_count = models.IntegerField(_('bajo riesgo'), default=0)
    medium_risk_count = models.IntegerField(_('riesgo medio'), default=0)
    high_risk_count = models.IntegerField(_('alto riesgo'), default=0)
    critical_risk_count = models.IntegerField(_('riesgo crítico'), default=0)
    
    # Datos detallados
    defaulters_data = models.JSONField(_('datos de morosos'), default=list)
    risk_distribution = models.JSONField(_('distribución de riesgo'), default=dict)
    recovery_potential = models.JSONField(_('potencial de recuperación'), default=dict)
    
    # Metadatos
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('generado por'),
        related_name='generated_reports'
    )
    generation_metadata = models.JSONField(_('metadatos de generación'), default=dict)
    
    class Meta:
        verbose_name = _('reporte de morosos')
        verbose_name_plural = _('reportes de morosos')
        ordering = ['-report_date', '-report_type']
        indexes = [
            models.Index(fields=['report_type', 'report_date']),
            models.Index(fields=['total_defaulters']),
            models.Index(fields=['total_overdue_amount']),
            models.Index(fields=['generated_by'])
        ]
    
    def __str__(self):
        return _('Reporte %(type)s - %(date)s - %(count)s morosos') % {
            'type': self.get_report_type_display(),
            'date': self.report_date.strftime('%Y-%m-%d'),
            'count': self.total_defaulters
        }
    
    @property
    def total_risk_count(self):
        return self.low_risk_count + self.medium_risk_count + self.high_risk_count + self.critical_risk_count
    
    @property
    def high_risk_percentage(self):
        if self.total_defaulters > 0:
            return ((self.high_risk_count + self.critical_risk_count) / self.total_defaulters) * 100
        return 0
