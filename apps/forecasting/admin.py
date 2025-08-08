from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import CreditPrediction, SeasonalPattern, RiskAssessment

@admin.register(CreditPrediction)
class CreditPredictionAdmin(admin.ModelAdmin):
    list_display = [
        'credit_link',
        'prediction_type',
        'predicted_date',
        'predicted_amount',
        'risk_score',
        'confidence_level',
        'is_expired',
        'created_at'
    ]
    
    list_filter = [
        'prediction_type',
        'confidence_level',
        'created_at',
        'expires_at'
    ]
    
    search_fields = [
        'credit__uid',
        'credit__user__username',
        'prediction_type'
    ]
    
    readonly_fields = [
        'credit_link',
        'created_at',
        'is_expired'
    ]
    
    fieldsets = (
        (_('Información del Crédito'), {
            'fields': ('credit_link',)
        }),
        (_('Predicción'), {
            'fields': (
                'prediction_type',
                'predicted_date',
                'predicted_amount',
                'risk_score'
            )
        }),
        (_('Confianza'), {
            'fields': (
                'confidence_level',
                'confidence_percentage'
            )
        }),
        (_('Metadatos'), {
            'fields': (
                'model_version',
                'features_used',
                'expires_at',
                'created_at'
            )
        }),
    )
    
    def credit_link(self, obj):
        if obj.credit:
            url = reverse('admin:fintech_credit_change', args=[obj.credit.id])
            return format_html('<a href="{}">{}</a>', url, obj.credit.uid)
        return '-'
    credit_link.short_description = _('Crédito')
    
    def is_expired(self, obj):
        if obj.is_expired:
            return format_html('<span style="color: red;">{}</span>', _('Expirada'))
        return format_html('<span style="color: green;">{}</span>', _('Activa'))
    is_expired.short_description = _('Estado')

@admin.register(SeasonalPattern)
class SeasonalPatternAdmin(admin.ModelAdmin):
    list_display = [
        'pattern_name',
        'pattern_type',
        'confidence_score',
        'identified_from',
        'identified_to',
        'next_expected_peak',
        'created_at'
    ]
    
    list_filter = [
        'pattern_type',
        'confidence_score',
        'created_at'
    ]
    
    search_fields = [
        'pattern_name',
        'description'
    ]
    
    readonly_fields = [
        'created_at'
    ]
    
    fieldsets = (
        (_('Información del Patrón'), {
            'fields': (
                'pattern_name',
                'pattern_type',
                'description'
            )
        }),
        (_('Períodos'), {
            'fields': (
                'peak_periods',
                'low_periods',
                'identified_from',
                'identified_to'
            )
        }),
        (_('Predicciones'), {
            'fields': (
                'next_expected_peak',
                'next_expected_low'
            )
        }),
        (_('Métricas'), {
            'fields': (
                'amplitude',
                'confidence_score'
            )
        }),
        (_('Metadatos'), {
            'fields': ('created_at',)
        }),
    )

@admin.register(RiskAssessment)
class RiskAssessmentAdmin(admin.ModelAdmin):
    list_display = [
        'risk_type',
        'target_link',
        'risk_level',
        'risk_score',
        'probability',
        'potential_impact',
        'is_expired',
        'assessment_date'
    ]
    
    list_filter = [
        'risk_type',
        'risk_level',
        'assessment_date',
        'valid_until'
    ]
    
    search_fields = [
        'risk_type',
        'credit__uid',
        'user__username'
    ]
    
    readonly_fields = [
        'target_link',
        'assessment_date',
        'is_expired',
        'expected_loss'
    ]
    
    fieldsets = (
        (_('Información del Riesgo'), {
            'fields': (
                'risk_type',
                'target_link'
            )
        }),
        (_('Evaluación'), {
            'fields': (
                'risk_level',
                'risk_score',
                'probability',
                'potential_impact',
                'expected_loss'
            )
        }),
        (_('Factores'), {
            'fields': (
                'risk_factors',
                'mitigation_actions'
            )
        }),
        (_('Validez'), {
            'fields': (
                'assessment_date',
                'valid_until',
                'is_expired'
            )
        }),
        (_('Evaluador'), {
            'fields': ('assessed_by',)
        }),
    )
    
    def target_link(self, obj):
        if obj.credit:
            url = reverse('admin:fintech_credit_change', args=[obj.credit.id])
            return format_html('<a href="{}">{}</a>', url, f"Crédito {obj.credit.uid}")
        elif obj.user:
            url = reverse('admin:fintech_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return _('Portfolio General')
    target_link.short_description = _('Objetivo')
    
    def is_expired(self, obj):
        if obj.is_expired:
            return format_html('<span style="color: red;">{}</span>', _('Expirada'))
        return format_html('<span style="color: green;">{}</span>', _('Válida'))
    is_expired.short_description = _('Estado') 