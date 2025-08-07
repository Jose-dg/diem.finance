from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Notification, NotificationTemplate, NotificationPreference, NotificationLog

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'channels', 'is_active', 'created_at']
    list_filter = ['template_type', 'channels', 'is_active', 'created_at']
    search_fields = ['name', 'title', 'message']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'template_type', 'is_active')
        }),
        ('Contenido', {
            'fields': ('title', 'message', 'channels')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'priority', 'status', 'channels', 'created_at']
    list_filter = ['priority', 'status', 'channels', 'created_at', 'template__template_type']
    search_fields = ['user__username', 'user__email', 'title', 'message']
    readonly_fields = ['uid', 'created_at', 'updated_at', 'sent_at', 'delivered_at', 'read_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('uid', 'user', 'template', 'priority', 'channels')
        }),
        ('Contenido', {
            'fields': ('title', 'message', 'data')
        }),
        ('Estado', {
            'fields': ('status', 'sent_at', 'delivered_at', 'read_at')
        }),
        ('Relaciones', {
            'fields': ('credit', 'installment', 'transaction'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'template', 'credit')
    
    def notification_links(self, obj):
        """Enlaces a las entidades relacionadas"""
        links = []
        if obj.credit:
            links.append(f'<a href="{reverse("admin:fintech_credit_change", args=[obj.credit.id])}">Ver Crédito</a>')
        if obj.installment:
            links.append(f'<a href="{reverse("admin:fintech_installment_change", args=[obj.installment.id])}">Ver Cuota</a>')
        return mark_safe(' | '.join(links)) if links else '-'
    
    notification_links.short_description = 'Enlaces Relacionados'

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_enabled', 'sms_enabled', 'web_enabled', 'push_enabled']
    list_filter = ['email_enabled', 'sms_enabled', 'web_enabled', 'push_enabled', 'daily_digest', 'weekly_summary']
    search_fields = ['user__username', 'user__email']
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Canales Habilitados', {
            'fields': ('email_enabled', 'sms_enabled', 'web_enabled', 'push_enabled')
        }),
        ('Tipos de Notificación', {
            'fields': (
                'additional_interest_enabled', 'multiple_credits_enabled', 
                'high_morosidad_enabled', 'behavior_change_enabled',
                'overdue_installment_enabled', 'payment_reminder_enabled'
            )
        }),
        ('Configuración', {
            'fields': ('daily_digest', 'weekly_summary', 'min_priority')
        }),
        ('Horarios de Silencio', {
            'fields': ('quiet_hours_start', 'quiet_hours_end'),
            'classes': ('collapse',)
        }),
    )

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ['notification', 'log_type', 'channel', 'attempt_number', 'created_at']
    list_filter = ['log_type', 'channel', 'created_at']
    search_fields = ['notification__title', 'notification__user__username']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('notification', 'log_type', 'channel', 'attempt_number')
        }),
        ('Detalles', {
            'fields': ('error_message', 'response_data')
        }),
        ('Metadatos', {
            'fields': ('ip_address', 'user_agent', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('notification__user')

# Acciones personalizadas para el admin
@admin.action(description="Marcar notificaciones como leídas")
def mark_as_read(modeladmin, request, queryset):
    for notification in queryset:
        notification.mark_as_read()
    modeladmin.message_user(request, f"{queryset.count()} notificaciones marcadas como leídas")

@admin.action(description="Reenviar notificaciones")
def resend_notifications(modeladmin, request, queryset):
    from .services import NotificationService
    success_count = 0
    for notification in queryset:
        if NotificationService.send_notification(notification):
            success_count += 1
    modeladmin.message_user(request, f"{success_count} notificaciones reenviadas exitosamente")

# Agregar acciones al admin de Notification
NotificationAdmin.actions = [mark_as_read, resend_notifications]
