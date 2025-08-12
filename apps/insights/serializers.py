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

