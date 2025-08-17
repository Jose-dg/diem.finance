from rest_framework import serializers

class PortfolioOverviewSerializer(serializers.Serializer):
    """Serializer para Portfolio Overview"""
    total_credits = serializers.IntegerField()
    active_credits = serializers.IntegerField()
    pending_credits = serializers.IntegerField()
    total_portfolio_value = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_pending_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    avg_credit_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    collection_rate = serializers.DecimalField(max_digits=5, decimal_places=2)

class CreditPerformanceSerializer(serializers.Serializer):
    """Serializer para Credit Performance Metrics"""
    credits_by_status = serializers.ListField()
    credits_by_category = serializers.ListField()
    daily_trends = serializers.ListField()
    period_days = serializers.IntegerField()

class UserBehaviorSerializer(serializers.Serializer):
    """Serializer para User Behavior Analytics"""
    active_users = serializers.ListField()
    user_segments = serializers.DictField()

class RiskAnalyticsSerializer(serializers.Serializer):
    """Serializer para Risk Analytics"""
    overdue_credits = serializers.IntegerField()
    overdue_installments = serializers.IntegerField()
    default_distribution = serializers.ListField()
    risk_by_category = serializers.ListField()

class RevenueAnalyticsSerializer(serializers.Serializer):
    """Serializer para Revenue Analytics"""
    monthly_revenue = serializers.ListField()
    profitability_by_category = serializers.ListField()
    earnings_trend = serializers.ListField()

class OperationalMetricsSerializer(serializers.Serializer):
    """Serializer para Operational Metrics"""
    processing_times = serializers.DictField()
    seller_performance = serializers.ListField()

class PredictiveInsightsSerializer(serializers.Serializer):
    """Serializer para Predictive Insights"""
    demand_prediction = serializers.ListField()
    payment_patterns = serializers.ListField()
    default_prediction = serializers.ListField()

class ExecutiveDashboardSerializer(serializers.Serializer):
    """Serializer para Executive Dashboard"""
    total_portfolio = serializers.DecimalField(max_digits=15, decimal_places=2)
    active_credits = serializers.IntegerField()
    monthly_disbursements = serializers.DecimalField(max_digits=15, decimal_places=2)
    monthly_earnings = serializers.DecimalField(max_digits=15, decimal_places=2)
    pending_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    overdue_credits = serializers.IntegerField()
    new_users_this_month = serializers.IntegerField()
    total_users = serializers.IntegerField()
    collection_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    default_rate = serializers.DecimalField(max_digits=5, decimal_places=2)

class CreditAnalyticsDashboardSerializer(serializers.Serializer):
    """Serializer para Credit Analytics Dashboard"""
    monthly_trends = serializers.ListField()
    category_distribution = serializers.ListField()
    credit_states = serializers.ListField()
    top_sellers = serializers.ListField()

class RiskDashboardSerializer(serializers.Serializer):
    """Serializer para Risk Dashboard"""
    overdue_by_days = serializers.ListField()
    default_by_category = serializers.ListField()
    overdue_installments = serializers.DictField()
    risk_prediction = serializers.ListField()

class UserInsightsDashboardSerializer(serializers.Serializer):
    """Serializer para User Insights Dashboard"""
    user_segments = serializers.DictField()
    top_users = serializers.ListField()

class OperationalDashboardSerializer(serializers.Serializer):
    """Serializer para Operational Dashboard"""
    processing_efficiency = serializers.DictField()
    seller_performance = serializers.ListField()
    alerts = serializers.DictField()

class RevenueDashboardSerializer(serializers.Serializer):
    """Serializer para Revenue Dashboard"""
    revenue_trends = serializers.ListField()
    profitability_by_category = serializers.ListField()
    top_products = serializers.ListField()
    current_month_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    growth_rate = serializers.DecimalField(max_digits=5, decimal_places=2)

class InsightsSummarySerializer(serializers.Serializer):
    """Serializer para Insights Summary"""
    portfolio = serializers.DictField()
    user_behavior = serializers.DictField()
    risk = serializers.DictField()
    revenue = serializers.DictField()
    operational = serializers.DictField()
    predictive = serializers.DictField()

class HealthCheckSerializer(serializers.Serializer):
    """Serializer para Health Check"""
    status = serializers.CharField()
    services = serializers.DictField()
    data_sources = serializers.DictField()
    last_updated = serializers.DateTimeField()

class ExportDataSerializer(serializers.Serializer):
    """Serializer para Export Data"""
    export_type = serializers.CharField()
    format = serializers.CharField()
    data = serializers.DictField()

class FinancialControlMetricsSerializer(serializers.ModelSerializer):
    """Serializer para métricas de control financiero"""
    user = serializers.SerializerMethodField()
    overdue_percentage = serializers.SerializerMethodField()
    is_high_risk = serializers.SerializerMethodField()
    
    class Meta:
        model = FinancialControlMetrics
        fields = [
            'id', 'user', 'total_overdue_amount', 'overdue_credits_count',
            'days_in_default', 'max_days_overdue', 'risk_level', 'risk_score',
            'payment_frequency', 'avg_payment_delay', 'overdue_percentage',
            'is_high_risk', 'last_calculation'
        ]
    
    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'email': obj.user.email,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name
        }
    
    def get_overdue_percentage(self, obj):
        return obj.overdue_percentage
    
    def get_is_high_risk(self, obj):
        return obj.is_high_risk

class FinancialAlertSerializer(serializers.ModelSerializer):
    """Serializer para alertas financieras"""
    user = serializers.SerializerMethodField()
    assigned_to = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    
    class Meta:
        model = FinancialAlert
        fields = [
            'id', 'user', 'alert_type', 'priority', 'status', 'title',
            'description', 'alert_data', 'created_at', 'acknowledged_at',
            'resolved_at', 'expires_at', 'assigned_to', 'is_expired',
            'is_active', 'notification_sent', 'notification_channels'
        ]
    
    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'email': obj.user.email
        }
    
    def get_assigned_to(self, obj):
        if obj.assigned_to:
            return {
                'id': obj.assigned_to.id,
                'username': obj.assigned_to.username,
                'email': obj.assigned_to.email
            }
        return None
    
    def get_is_expired(self, obj):
        return obj.is_expired
    
    def get_is_active(self, obj):
        return obj.is_active

class DefaultersReportSerializer(serializers.ModelSerializer):
    """Serializer para reportes de morosos"""
    generated_by = serializers.SerializerMethodField()
    total_risk_count = serializers.SerializerMethodField()
    high_risk_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = DefaultersReport
        fields = [
            'id', 'report_type', 'report_date', 'total_defaulters',
            'total_overdue_amount', 'avg_days_overdue', 'low_risk_count',
            'medium_risk_count', 'high_risk_count', 'critical_risk_count',
            'total_risk_count', 'high_risk_percentage', 'defaulters_data',
            'risk_distribution', 'recovery_potential', 'generated_by',
            'generation_metadata'
        ]
    
    def get_generated_by(self, obj):
        if obj.generated_by:
            return {
                'id': obj.generated_by.id,
                'username': obj.generated_by.username,
                'email': obj.generated_by.email
            }
        return None
    
    def get_total_risk_count(self, obj):
        return obj.total_risk_count
    
    def get_high_risk_percentage(self, obj):
        return obj.high_risk_percentage

class DefaultersListSerializer(serializers.Serializer):
    """Serializer para lista paginada de morosos"""
    results = FinancialControlMetricsSerializer(many=True)
    pagination = serializers.DictField()

class FinancialControlDashboardSerializer(serializers.Serializer):
    """Serializer para dashboard de control financiero"""
    total_metrics = serializers.IntegerField()
    active_defaulters = serializers.IntegerField()
    total_overdue_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    risk_distribution = serializers.ListField()
    active_alerts = serializers.IntegerField()
    new_defaulters_30_days = serializers.IntegerField()
    default_rate = serializers.DecimalField(max_digits=5, decimal_places=2)

