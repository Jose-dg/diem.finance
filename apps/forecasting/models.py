from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from decimal import Decimal
import json

class CreditPrediction(models.Model):
    """
    Predicciones sobre el comportamiento futuro de un crédito.
    """
    PREDICTION_TYPES = [
        ('payment_date', _('Fecha de próximo pago')),
        ('completion_date', _('Fecha de completación')),
        ('default_risk', _('Riesgo de impago')),
        ('payment_amount', _('Monto de próximo pago')),
    ]
    
    CONFIDENCE_LEVELS = [
        ('high', _('Alta (>80%)')),
        ('medium', _('Media (60-80%)')),
        ('low', _('Baja (<60%)')),
    ]

    credit = models.ForeignKey(
        'fintech.Credit',
        on_delete=models.CASCADE,
        verbose_name=_('crédito'),
        related_name='predictions'
    )
    
    prediction_type = models.CharField(
        _('tipo de predicción'),
        max_length=20,
        choices=PREDICTION_TYPES
    )
    
    # Predicción de fecha
    predicted_date = models.DateField(
        _('fecha predicha'),
        null=True,
        blank=True,
        help_text=_('Para predicciones de fechas')
    )
    
    # Predicción de monto
    predicted_amount = models.DecimalField(
        _('monto predicho'),
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Para predicciones de montos')
    )
    
    # Predicción de riesgo
    risk_score = models.DecimalField(
        _('puntuación de riesgo'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('0.00 = Sin riesgo, 100.00 = Alto riesgo')
    )
    
    confidence_level = models.CharField(
        _('nivel de confianza'),
        max_length=10,
        choices=CONFIDENCE_LEVELS,
        default='medium'
    )
    
    confidence_percentage = models.DecimalField(
        _('porcentaje de confianza'),
        max_digits=5,
        decimal_places=2,
        help_text=_('0.00-100.00')
    )
    
    # Metadatos del modelo
    model_version = models.CharField(
        _('versión del modelo'),
        max_length=50,
        default='1.0'
    )
    
    features_used = models.JSONField(
        _('características utilizadas'),
        default=dict,
        help_text=_('Factores considerados en la predicción')
    )
    
    created_at = models.DateTimeField(
        _('fecha de creación'),
        auto_now_add=True
    )
    
    expires_at = models.DateTimeField(
        _('fecha de expiración'),
        help_text=_('Cuándo la predicción deja de ser válida')
    )

    class Meta:
        verbose_name = _('predicción de crédito')
        verbose_name_plural = _('predicciones de créditos')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['credit', 'prediction_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return _('Predicción %(type)s para crédito %(credit)s') % {
            'type': self.get_prediction_type_display(),
            'credit': self.credit.uid
        }

    def clean(self):
        if self.prediction_type in ['payment_date', 'completion_date'] and not self.predicted_date:
            raise ValidationError({
                'predicted_date': _('Fecha predicha requerida para predicciones de fecha')
            })
        
        if self.prediction_type == 'payment_amount' and not self.predicted_amount:
            raise ValidationError({
                'predicted_amount': _('Monto predicho requerido para predicciones de monto')
            })
        
        if self.prediction_type == 'default_risk' and not self.risk_score:
            raise ValidationError({
                'risk_score': _('Puntuación de riesgo requerida para predicciones de riesgo')
            })

    @property
    def is_expired(self):
        """Verifica si la predicción ha expirado"""
        from django.utils import timezone
        return timezone.now() > self.expires_at

class SeasonalPattern(models.Model):
    """
    Patrones estacionales identificados en los datos.
    """
    PATTERN_TYPES = [
        ('monthly', _('Mensual')),
        ('quarterly', _('Trimestral')),
        ('yearly', _('Anual')),
        ('weekly', _('Semanal')),
    ]

    pattern_name = models.CharField(
        _('nombre del patrón'),
        max_length=100
    )
    
    pattern_type = models.CharField(
        _('tipo de patrón'),
        max_length=15,
        choices=PATTERN_TYPES
    )
    
    description = models.TextField(
        _('descripción'),
        help_text=_('Descripción detallada del patrón identificado')
    )
    
    # Datos del patrón
    peak_periods = models.JSONField(
        _('períodos pico'),
        default=list,
        help_text=_('Períodos donde el patrón es más fuerte')
    )
    
    low_periods = models.JSONField(
        _('períodos bajos'),
        default=list,
        help_text=_('Períodos donde el patrón es más débil')
    )
    
    amplitude = models.DecimalField(
        _('amplitud'),
        max_digits=10,
        decimal_places=2,
        help_text=_('Diferencia entre picos y valles')
    )
    
    confidence_score = models.DecimalField(
        _('puntuación de confianza'),
        max_digits=5,
        decimal_places=2,
        help_text=_('Qué tan confiable es este patrón (0-100)')
    )
    
    # Fechas de validez
    identified_from = models.DateField(
        _('identificado desde'),
        help_text=_('Fecha desde la cual se identificó el patrón')
    )
    
    identified_to = models.DateField(
        _('identificado hasta'),
        help_text=_('Fecha hasta la cual se validó el patrón')
    )
    
    next_expected_peak = models.DateField(
        _('próximo pico esperado'),
        null=True,
        blank=True
    )
    
    next_expected_low = models.DateField(
        _('próximo valle esperado'),
        null=True,
        blank=True
    )
    
    created_at = models.DateTimeField(
        _('fecha de creación'),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _('patrón estacional')
        verbose_name_plural = _('patrones estacionales')
        ordering = ['-confidence_score', '-created_at']
        indexes = [
            models.Index(fields=['pattern_type', 'confidence_score']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return _('Patrón %(type)s: %(name)s') % {
            'type': self.get_pattern_type_display(),
            'name': self.pattern_name
        }

class RiskAssessment(models.Model):
    """
    Evaluación de riesgos para créditos y carteras.
    """
    RISK_TYPES = [
        ('credit_default', _('Riesgo de impago de crédito')),
        ('portfolio_concentration', _('Riesgo de concentración')),
        ('liquidity_risk', _('Riesgo de liquidez')),
        ('market_risk', _('Riesgo de mercado')),
        ('operational_risk', _('Riesgo operacional')),
    ]
    
    RISK_LEVELS = [
        ('low', _('Bajo')),
        ('medium', _('Medio')),
        ('high', _('Alto')),
        ('critical', _('Crítico')),
    ]

    # Relaciones opcionales
    credit = models.ForeignKey(
        'fintech.Credit',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('crédito'),
        related_name='risk_assessments'
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('usuario'),
        related_name='forecast_risk_assessments'
    )
    
    risk_type = models.CharField(
        _('tipo de riesgo'),
        max_length=25,
        choices=RISK_TYPES
    )
    
    risk_level = models.CharField(
        _('nivel de riesgo'),
        max_length=10,
        choices=RISK_LEVELS
    )
    
    risk_score = models.DecimalField(
        _('puntuación de riesgo'),
        max_digits=5,
        decimal_places=2,
        help_text=_('0.00 = Sin riesgo, 100.00 = Riesgo máximo')
    )
    
    probability = models.DecimalField(
        _('probabilidad'),
        max_digits=5,
        decimal_places=2,
        help_text=_('Probabilidad de que el riesgo se materialice (0-100%)')
    )
    
    potential_impact = models.DecimalField(
        _('impacto potencial'),
        max_digits=15,
        decimal_places=2,
        help_text=_('Impacto financiero estimado si se materializa')
    )
    
    # Factores de riesgo
    risk_factors = models.JSONField(
        _('factores de riesgo'),
        default=dict,
        help_text=_('Factores que contribuyen al riesgo')
    )
    
    mitigation_actions = models.JSONField(
        _('acciones de mitigación'),
        default=list,
        help_text=_('Acciones recomendadas para mitigar el riesgo')
    )
    
    assessment_date = models.DateTimeField(
        _('fecha de evaluación'),
        auto_now_add=True
    )
    
    valid_until = models.DateTimeField(
        _('válido hasta'),
        help_text=_('Cuándo debe reevaluarse este riesgo')
    )
    
    assessed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('evaluado por'),
        related_name='assessed_forecast_risks'
    )

    class Meta:
        verbose_name = _('evaluación de riesgo')
        verbose_name_plural = _('evaluaciones de riesgo')
        ordering = ['-risk_score', '-assessment_date']
        indexes = [
            models.Index(fields=['risk_type', 'risk_level']),
            models.Index(fields=['assessment_date']),
            models.Index(fields=['valid_until']),
        ]

    def __str__(self):
        target = self.credit.uid if self.credit else (self.user.username if self.user else 'Portfolio')
        return _('Riesgo %(type)s para %(target)s: %(level)s') % {
            'type': self.get_risk_type_display(),
            'target': target,
            'level': self.get_risk_level_display()
        }

    @property
    def is_expired(self):
        """Verifica si la evaluación ha expirado"""
        from django.utils import timezone
        return timezone.now() > self.valid_until
    
    @property
    def expected_loss(self):
        """Calcula la pérdida esperada (Probabilidad × Impacto)"""
        return (self.probability / 100) * self.potential_impact 