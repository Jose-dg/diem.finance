from django.contrib import admin
from .models import CustomerLifetimeValue, CustomerActivity, CreditRecommendation

@admin.register(CustomerLifetimeValue)
class CustomerLifetimeValueAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_clv', 'predicted_clv', 'clv_tier', 'updated_at']
    search_fields = ['user__username']
    list_filter = ['clv_tier', 'updated_at']

@admin.register(CustomerActivity)
class CustomerActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'activity_date', 'credit', 'transaction', 'amount']
    search_fields = ['user__username', 'activity_type']
    list_filter = ['activity_type', 'activity_date']

@admin.register(CreditRecommendation)
class CreditRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'recommendation_type', 'priority', 'confidence_score', 'is_active', 'created_at']
    search_fields = ['user__username', 'recommendation_type', 'title']
    list_filter = ['recommendation_type', 'priority', 'is_active', 'created_at']
