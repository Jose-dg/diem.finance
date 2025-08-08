from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

class CreditEarnings(models.Model):
    """
    Modelo para rastrear únicamente las GANANCIAS de un crédito.
    No maneja pagos ni saldos - eso ya está en el modelo Credit.
    """
    credit = models.OneToOneField(
        'fintech.Credit',
        on_delete=models.CASCADE,
        verbose_name=_('crédito'),
        related_name='earnings_detail'
    )
    
    # Ganancia teórica total del crédito (intereses + margen)
    theoretical_earnings = models.DecimalField(
        _('ganancia teórica total'),
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=_('Ganancia total esperada: (precio - costo) + intereses')
    )
    
    # Ganancia ya realizada (parte proporcional de los pagos recibidos)
    realized_earnings = models.DecimalField(
        _('ganancia realizada'),
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=_('Ganancia efectivamente obtenida de los pagos recibidos')
    )
    
    # Tasa de ganancia sobre el monto total (para cálculos)
    earnings_rate = models.DecimalField(
        _('tasa de ganancia'),
        max_digits=5,
        decimal_places=4,
        default=Decimal('0.0000'),
        help_text=_('Porcentaje de ganancia sobre el precio total (0.0000-1.0000)')
    )

    updated_at = models.DateTimeField(
        _('última actualización'),
        auto_now=True,
        db_index=True
    )

    class Meta:
        verbose_name = _('ganancia de crédito')
        verbose_name_plural = _('ganancias de créditos')
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['credit']),
            models.Index(fields=['updated_at'])
        ]

    def __str__(self):
        return _('Ganancias del crédito %(credit_id)s') % {'credit_id': self.credit.uid}

    @property
    def pending_earnings(self):
        """Ganancia que falta por realizar"""
        return self.theoretical_earnings - self.realized_earnings

    @property
    def realization_percentage(self):
        """Porcentaje de ganancia realizada"""
        if self.theoretical_earnings > 0:
            return (self.realized_earnings / self.theoretical_earnings) * 100
        return Decimal('0.00')

    def clean(self):
        if self.realized_earnings > self.theoretical_earnings:
            raise ValidationError({
                'realized_earnings': _('La ganancia realizada no puede superar la teórica.')
            })
        
        if self.theoretical_earnings < Decimal('0.00'):
            raise ValidationError({
                'theoretical_earnings': _('La ganancia teórica no puede ser negativa.')
            })
            
        if not (Decimal('0.0000') <= self.earnings_rate <= Decimal('1.0000')):
            raise ValidationError({
                'earnings_rate': _('La tasa de ganancia debe estar entre 0.0000 y 1.0000')
            })
            
class EarningsAdjustment(models.Model):
    """
    Ajustes a las ganancias teóricas (por cambios en intereses, descuentos, etc.)
    """
    ADJUSTMENT_TYPES = [
        ('interest_change', _('Cambio de interés')),
        ('discount', _('Descuento aplicado')),
        ('penalty', _('Penalización')),
        ('correction', _('Corrección contable')),
        ('manual', _('Ajuste manual')),
    ]

    credit_earnings = models.ForeignKey(
        CreditEarnings,
        on_delete=models.CASCADE,
        verbose_name=_('ganancias del crédito'),
        related_name='adjustments'
    )
    
    amount = models.DecimalField(
        _('monto del ajuste'),
        max_digits=12,
        decimal_places=2,
        help_text=_('Valor positivo aumenta ganancia, negativo la disminuye')
    )
    
    adjustment_type = models.CharField(
        _('tipo de ajuste'),
        max_length=20,
        choices=ADJUSTMENT_TYPES
    )
    
    reason = models.TextField(
        _('motivo'),
        help_text=_('Descripción detallada del ajuste')
    )
    
    created_at = models.DateTimeField(
        _('fecha de creación'),
        auto_now_add=True
    )
    
    created_by = models.ForeignKey(
        'fintech.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('creado por'),
        related_name='earnings_adjustments'
    )

    class Meta:
        verbose_name = _('ajuste de ganancias')
        verbose_name_plural = _('ajustes de ganancias')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['credit_earnings', 'created_at']),
            models.Index(fields=['adjustment_type'])
        ]

    def __str__(self):
        return _('Ajuste %(type)s: %(amount).2f para %(credit)s') % {
            'type': self.get_adjustment_type_display(),
            'amount': self.amount,
            'credit': self.credit_earnings.credit.uid
        }

class EarningsMetrics(models.Model):
    """
    Métricas agregadas de ganancias por período.
    """
    period_start = models.DateTimeField(
        _('inicio del período'),
        db_index=True
    )
    period_end = models.DateTimeField(
        _('fin del período'),
        db_index=True
    )
    
    # Métricas de ganancias
    total_theoretical_earnings = models.DecimalField(
        _('total ganancias teóricas'),
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    total_realized_earnings = models.DecimalField(
        _('total ganancias realizadas'),
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00')
    )
    
    # Métricas de créditos
    credits_count = models.IntegerField(
        _('cantidad de créditos'),
        default=0
    )
    
    # Tasa promedio de realización
    avg_realization_rate = models.DecimalField(
        _('tasa promedio de realización'),
        max_digits=5,
        decimal_places=2,
        help_text=_('Porcentaje promedio de ganancias realizadas')
    )

    created_at = models.DateTimeField(
        _('fecha de creación'),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _('métrica de ganancias')
        verbose_name_plural = _('métricas de ganancias')
        ordering = ['-period_start']
        indexes = [
            models.Index(fields=['period_start', 'period_end']),
            models.Index(fields=['created_at'])
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(period_end__gt=models.F('period_start')),
                name='valid_earnings_period_range'
            )
        ]

    def __str__(self):
        return _('Métricas de ganancias %(start)s - %(end)s') % {
            'start': self.period_start.date(),
            'end': self.period_end.date()
        }

    @property
    def pending_earnings(self):
        """Ganancias pendientes en el período"""
        return self.total_theoretical_earnings - self.total_realized_earnings

    def clean(self):
        if self.period_end <= self.period_start:
            raise ValidationError({
                'period_end': _('El fin del período debe ser posterior al inicio.')
            }) 