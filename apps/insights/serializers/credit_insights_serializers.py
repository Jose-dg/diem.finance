from rest_framework import serializers
from decimal import Decimal
from typing import Dict, Any, List

class CreditBasicInfoSerializer(serializers.Serializer):
    """Serializer para información básica del crédito"""
    uid = serializers.CharField()
    user = serializers.DictField()
    subcategory = serializers.DictField()
    amounts = serializers.DictField()
    terms = serializers.DictField()
    dates = serializers.DictField()
    status = serializers.DictField()

class PaymentAnalysisSerializer(serializers.Serializer):
    """Serializer para análisis de pagos"""
    installment_summary = serializers.DictField()
    payment_behavior = serializers.DictField()
    amounts = serializers.DictField()

class RiskAssessmentSerializer(serializers.Serializer):
    """Serializer para evaluación de riesgo"""
    risk_score = serializers.IntegerField()
    risk_level = serializers.CharField()
    days_in_default = serializers.IntegerField()
    overdue_installments_count = serializers.IntegerField()
    overdue_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    morosidad_history = serializers.IntegerField()
    risk_factors = serializers.ListField(child=serializers.CharField())

class PerformanceMetricsSerializer(serializers.Serializer):
    """Serializer para métricas de rendimiento"""
    roi = serializers.DecimalField(max_digits=5, decimal_places=2)
    collection_efficiency = serializers.DecimalField(max_digits=5, decimal_places=2)
    avg_payment_interval_days = serializers.DecimalField(max_digits=5, decimal_places=2)
    expected_vs_actual_payments = serializers.DictField()

class InstallmentBreakdownSerializer(serializers.Serializer):
    """Serializer para desglose de cuotas"""
    number = serializers.IntegerField(allow_null=True)
    due_date = serializers.DateField(allow_null=True)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    paid = serializers.BooleanField()
    paid_on = serializers.DateField(allow_null=True)
    status = serializers.CharField()
    days_overdue = serializers.IntegerField()
    principal_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    interest_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    late_fee = serializers.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = serializers.DecimalField(max_digits=12, decimal_places=2)

class TimelineAnalysisSerializer(serializers.Serializer):
    """Serializer para análisis temporal"""
    credit_lifecycle = serializers.DictField()
    monthly_payment_trends = serializers.ListField()

class ComparativeAnalysisSerializer(serializers.Serializer):
    """Serializer para análisis comparativo"""
    user_comparison = serializers.DictField()
    category_comparison = serializers.DictField()

class CreditRecommendationSerializer(serializers.Serializer):
    """Serializer para recomendaciones de crédito"""
    type = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    action = serializers.CharField()

class CreditDetailedInsightsSerializer(serializers.Serializer):
    """Serializer principal para insights detallados del crédito"""
    credit_basic_info = CreditBasicInfoSerializer()
    payment_analysis = PaymentAnalysisSerializer()
    risk_assessment = RiskAssessmentSerializer()
    performance_metrics = PerformanceMetricsSerializer()
    installment_breakdown = InstallmentBreakdownSerializer(many=True)
    timeline_analysis = TimelineAnalysisSerializer()
    comparative_analysis = ComparativeAnalysisSerializer()
    recommendations = CreditRecommendationSerializer(many=True)

class CreditComparativeSummarySerializer(serializers.Serializer):
    """Serializer para resumen comparativo de créditos"""
    total_credits = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_pending = serializers.DecimalField(max_digits=12, decimal_places=2)
    default_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    collection_rate = serializers.DecimalField(max_digits=5, decimal_places=2)

class CategoryAnalysisSerializer(serializers.Serializer):
    """Serializer para análisis por categoría"""
    subcategory__name = serializers.CharField(allow_null=True)
    count = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    default_count = serializers.IntegerField()
    avg_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)

class StateAnalysisSerializer(serializers.Serializer):
    """Serializer para análisis por estado"""
    state = serializers.CharField()
    count = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)

class MorosidadAnalysisSerializer(serializers.Serializer):
    """Serializer para análisis por nivel de morosidad"""
    morosidad_level = serializers.CharField()
    count = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)

class TopCreditSerializer(serializers.Serializer):
    """Serializer para top créditos"""
    uid = serializers.CharField()
    user__username = serializers.CharField()
    subcategory__name = serializers.CharField(allow_null=True)
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    pending_amount = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    is_in_default = serializers.BooleanField()

class CreditsComparativeAnalysisSerializer(serializers.Serializer):
    """Serializer principal para análisis comparativo de créditos"""
    summary = CreditComparativeSummarySerializer()
    category_analysis = CategoryAnalysisSerializer(many=True)
    state_analysis = StateAnalysisSerializer(many=True)
    morosidad_analysis = MorosidadAnalysisSerializer(many=True)
    top_credits = TopCreditSerializer(many=True)

class CreditInsightsResponseSerializer(serializers.Serializer):
    """Serializer para respuesta de insights de crédito"""
    success = serializers.BooleanField()
    data = CreditDetailedInsightsSerializer(allow_null=True)
    error = serializers.CharField(allow_null=True, required=False)

class CreditAnalysisResponseSerializer(serializers.Serializer):
    """Serializer para respuesta de análisis de créditos"""
    success = serializers.BooleanField()
    data = CreditsComparativeAnalysisSerializer(allow_null=True)
    error = serializers.CharField(allow_null=True, required=False)
