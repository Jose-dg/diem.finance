from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import CreditEarnings, EarningsMetrics, EarningsAdjustment

@admin.register(CreditEarnings)
class CreditEarningsAdmin(admin.ModelAdmin):
    list_display = ('credit', 'theoretical_earnings', 'realized_earnings', 
                   'pending_earnings', 'realization_percentage', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('credit__uid',)
    readonly_fields = ('pending_earnings', 'realization_percentage', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('credit',)
        }),
        (_('Ganancias'), {
            'fields': ('theoretical_earnings', 'realized_earnings', 'earnings_rate')
        }),
        (_('Métricas Calculadas'), {
            'fields': ('pending_earnings', 'realization_percentage'),
            'classes': ('collapse',)
        }),
        (_('Información Temporal'), {
            'fields': ('updated_at',)
        })
    )
    
    def pending_earnings(self, obj):
        return obj.pending_earnings
    pending_earnings.short_description = _('Ganancia Pendiente')
    
    def realization_percentage(self, obj):
        return f"{obj.realization_percentage:.2f}%"
    realization_percentage.short_description = _('% Realización')

@admin.register(EarningsMetrics)
class EarningsMetricsAdmin(admin.ModelAdmin):
    list_display = ('period_start', 'period_end', 'total_theoretical_earnings', 
                   'total_realized_earnings', 'credits_count', 'avg_realization_rate')
    list_filter = ('period_start', 'period_end', 'created_at')
    readonly_fields = ('pending_earnings', 'created_at')
    
    fieldsets = (
        (_('Período'), {
            'fields': ('period_start', 'period_end')
        }),
        (_('Métricas de Ganancias'), {
            'fields': ('total_theoretical_earnings', 'total_realized_earnings', 
                      'pending_earnings')
        }),
        (_('Métricas de Créditos'), {
            'fields': ('credits_count', 'avg_realization_rate')
        }),
        (_('Información Temporal'), {
            'fields': ('created_at',)
        })
    )
    
    def pending_earnings(self, obj):
        return obj.pending_earnings
    pending_earnings.short_description = _('Ganancias Pendientes')

@admin.register(EarningsAdjustment)
class EarningsAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('credit_earnings', 'amount', 'adjustment_type', 
                   'created_by', 'created_at')
    list_filter = ('adjustment_type', 'created_at')
    search_fields = ('credit_earnings__credit__uid', 'reason')
    readonly_fields = ('created_at', 'created_by')
    
    fieldsets = (
        (None, {
            'fields': ('credit_earnings', 'amount')
        }),
        (_('Detalles del Ajuste'), {
            'fields': ('adjustment_type', 'reason')
        }),
        (_('Información de Auditoría'), {
            'fields': ('created_by', 'created_at')
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva instancia
            obj.created_by = request.user
        super().save_model(request, obj, form, change) 