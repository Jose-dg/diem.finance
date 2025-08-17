from django.contrib import admin
from .models import CustomerLifetimeValue, CustomerActivity, CreditRecommendation, FinancialControlMetrics, FinancialAlert, DefaultersReport

@admin.register(CustomerLifetimeValue)
class CustomerLifetimeValueAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_clv', 'clv_tier', 'total_revenue', 'churn_probability', 'updated_at']
    list_filter = ['clv_tier', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['updated_at']
    ordering = ['-current_clv']

@admin.register(CustomerActivity)
class CustomerActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'activity_date', 'amount', 'ip_address']
    list_filter = ['activity_type', 'activity_date']
    search_fields = ['user__username', 'description']
    readonly_fields = ['activity_date']
    ordering = ['-activity_date']

@admin.register(CreditRecommendation)
class CreditRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'recommendation_type', 'priority', 'is_active', 'is_implemented', 'created_at']
    list_filter = ['recommendation_type', 'priority', 'is_active', 'is_implemented', 'created_at']
    search_fields = ['user__username', 'title', 'description']
    readonly_fields = ['created_at']
    ordering = ['-priority', '-created_at']

@admin.register(FinancialControlMetrics)
class FinancialControlMetricsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_overdue_amount', 'overdue_credits_count', 'risk_level', 'risk_score', 'days_in_default', 'last_calculation']
    list_filter = ['risk_level', 'last_calculation']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['last_calculation', 'calculation_metadata']
    ordering = ['-risk_score', '-total_overdue_amount']
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user',)
        }),
        ('Métricas de Morosidad', {
            'fields': ('total_overdue_amount', 'overdue_credits_count', 'days_in_default', 'max_days_overdue')
        }),
        ('Evaluación de Riesgo', {
            'fields': ('risk_level', 'risk_score')
        }),
        ('Comportamiento de Pagos', {
            'fields': ('payment_frequency', 'avg_payment_delay')
        }),
        ('Historial', {
            'fields': ('default_history', 'calculation_metadata', 'last_calculation')
        })
    )

@admin.register(FinancialAlert)
class FinancialAlertAdmin(admin.ModelAdmin):
    list_display = ['user', 'alert_type', 'priority', 'status', 'assigned_to', 'created_at', 'is_expired']
    list_filter = ['alert_type', 'priority', 'status', 'created_at']
    search_fields = ['user__username', 'title', 'description']
    readonly_fields = ['created_at', 'is_expired', 'is_active']
    ordering = ['-priority', '-created_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('user', 'alert_type', 'priority', 'status')
        }),
        ('Detalles', {
            'fields': ('title', 'description', 'alert_data')
        }),
        ('Gestión', {
            'fields': ('assigned_to', 'acknowledged_at', 'resolved_at')
        }),
        ('Fechas', {
            'fields': ('created_at', 'expires_at')
        }),
        ('Notificaciones', {
            'fields': ('notification_sent', 'notification_channels')
        })
    )
    
    def is_expired(self, obj):
        return obj.is_expired
    is_expired.boolean = True
    is_expired.short_description = 'Expirada'

@admin.register(DefaultersReport)
class DefaultersReportAdmin(admin.ModelAdmin):
    list_display = ['report_type', 'report_date', 'total_defaulters', 'total_overdue_amount', 'high_risk_percentage', 'generated_by']
    list_filter = ['report_type', 'report_date']
    search_fields = ['generated_by__username']
    readonly_fields = ['report_date', 'generation_metadata']
    ordering = ['-report_date']
    
    fieldsets = (
        ('Información del Reporte', {
            'fields': ('report_type', 'report_date', 'generated_by')
        }),
        ('Métricas Generales', {
            'fields': ('total_defaulters', 'total_overdue_amount', 'avg_days_overdue')
        }),
        ('Distribución por Riesgo', {
            'fields': ('low_risk_count', 'medium_risk_count', 'high_risk_count', 'critical_risk_count')
        }),
        ('Datos Detallados', {
            'fields': ('defaulters_data', 'risk_distribution', 'recovery_potential', 'generation_metadata')
        })
    )
    
    def high_risk_percentage(self, obj):
        return f"{obj.high_risk_percentage:.1f}%"
    high_risk_percentage.short_description = '% Alto Riesgo'
