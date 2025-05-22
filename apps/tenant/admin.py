from django.contrib import admin

from apps.tenant.models.apy_keys import TenantApiKey
from apps.tenant.models.audit import TenantAuditLog
from apps.tenant.models.invitation import TenantInvitation, TenantInvitationRole
from apps.tenant.models.subscription import SubscriptionPlan, SubscriptionStatus, TenantSubscription
from .models import Tenant, TenantRole, TenantMembership, TenantSettings

class TenantScopedAdmin(admin.ModelAdmin):
    """
    Base admin para mostrar datos solo del tenant del usuario autenticado.
    Requiere que el usuario esté relacionado a un TenantMembership.
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'tenant_memberships'):
            return qs.filter(tenant__in=[m.tenant for m in request.user.tenant_memberships.all()])
        return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if not request.user.is_superuser and db_field.name == 'tenant':
            tenant_ids = [m.tenant.id for m in request.user.tenant_memberships.all()]
            field.queryset = field.queryset.filter(id__in=tenant_ids)
        return field

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'is_active', 'created_at')
    search_fields = ('name', 'contact_email')

@admin.register(TenantRole)
class TenantRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_system_role')
    search_fields = ('name', 'slug')

@admin.register(TenantMembership)
class TenantMembershipAdmin(TenantScopedAdmin):
    list_display = ('tenant', 'user', 'role', 'is_active', 'invitation_accepted')
    search_fields = ('user__username', 'tenant__name')

@admin.register(TenantSettings)
class TenantSettingsAdmin(TenantScopedAdmin):
    list_display = ('tenant', 'theme', 'primary_color', 'time_zone')
    search_fields = ('tenant__name',)



@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(SubscriptionStatus)
class SubscriptionStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(TenantSubscription)
class TenantSubscriptionAdmin(TenantScopedAdmin):
    list_display = ('tenant', 'plan', 'status', 'start_date', 'end_date', 'auto_renew')
    search_fields = ('tenant__name', 'plan__name', 'status__name')
    

@admin.register(TenantInvitationRole)
class TenantInvitationRoleAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(TenantInvitation)
class TenantInvitationAdmin(TenantScopedAdmin):
    list_display = ('tenant', 'email', 'role', 'invited_by', 'is_accepted', 'expires_at')
    search_fields = ('email', 'tenant__name', 'invited_by__username')


@admin.register(TenantApiKey)
class APIKeyAdmin(TenantScopedAdmin):
    list_display = ('tenant', 'prefix', 'created_at')
    list_filter = ('created_at',)

@admin.register(TenantAuditLog)
class AuditLogAdmin(TenantScopedAdmin):
    list_display = ('tenant', 'action', 'user', 'created_at')
    search_fields = ('action', 'user__username')
    list_filter = ('action', 'created_at')