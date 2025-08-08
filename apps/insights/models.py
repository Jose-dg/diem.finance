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
