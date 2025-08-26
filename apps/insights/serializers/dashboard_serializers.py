"""
Serializers para las vistas del dashboard de insights
"""
from rest_framework import serializers
from apps.fintech.models import Credit, Installment, User
from apps.insights.utils.dashboard_helpers import (
    get_client_info,
    get_credit_details,
    get_payment_info,
    get_installment_info,
    get_calculated_metrics,
    get_seller_info,
    get_installment_details,
    get_payment_tracking,
    get_periodicity_info,
    get_calculated_installment_metrics,
    get_client_history_for_installment,
    get_credit_info_for_installment
)

class ClientInfoSerializer(serializers.Serializer):
    """Serializer para información del cliente"""
    id = serializers.CharField()
    full_name = serializers.CharField()
    username = serializers.CharField()
    document_number = serializers.CharField()
    phone = serializers.CharField()

class CreditDetailsSerializer(serializers.Serializer):
    """Serializer para detalles del crédito"""
    subcategory = serializers.CharField()
    price = serializers.CharField()
    cost = serializers.CharField()
    earnings = serializers.CharField()
    currency = serializers.CharField()
    state = serializers.CharField()
    morosidad_level = serializers.CharField()
    created_at = serializers.CharField()

class PaymentInfoSerializer(serializers.Serializer):
    """Serializer para información de pagos"""
    total_abonos = serializers.CharField()
    pending_amount = serializers.CharField()
    percentage_paid = serializers.FloatField()
    payment_method = serializers.CharField()

class InstallmentInfoSerializer(serializers.Serializer):
    """Serializer para información de cuotas"""
    periodicity_name = serializers.CharField()
    periodicity_days = serializers.IntegerField()
    total_installments = serializers.IntegerField()
    installment_value = serializers.CharField()
    paid_installments = serializers.IntegerField()
    overdue_installments = serializers.IntegerField()
    next_due_date = serializers.DateField(allow_null=True)

class CalculatedMetricsSerializer(serializers.Serializer):
    """Serializer para métricas calculadas"""
    interest_rate = serializers.CharField()
    credit_days = serializers.IntegerField()
    days_since_creation = serializers.IntegerField()
    average_payment_delay = serializers.FloatField()
    risk_score = serializers.FloatField()

class SellerInfoSerializer(serializers.Serializer):
    """Serializer para información del vendedor"""
    seller_name = serializers.CharField()
    seller_id = serializers.CharField(allow_null=True)

class CreditDashboardSerializer(serializers.ModelSerializer):
    """Serializer para la vista de dashboard de créditos"""
    uid = serializers.CharField(source='uid')
    client_info = serializers.SerializerMethodField()
    credit_details = serializers.SerializerMethodField()
    payment_info = serializers.SerializerMethodField()
    installment_info = serializers.SerializerMethodField()
    calculated_metrics = serializers.SerializerMethodField()
    seller_info = serializers.SerializerMethodField()

    class Meta:
        model = Credit
        fields = [
            'uid',
            'client_info',
            'credit_details',
            'payment_info',
            'installment_info',
            'calculated_metrics',
            'seller_info'
        ]

    def get_client_info(self, obj):
        return get_client_info(obj.user)

    def get_credit_details(self, obj):
        return get_credit_details(obj)

    def get_payment_info(self, obj):
        return get_payment_info(obj)

    def get_installment_info(self, obj):
        return get_installment_info(obj)

    def get_calculated_metrics(self, obj):
        return get_calculated_metrics(obj, obj.installments.all())

    def get_seller_info(self, obj):
        return get_seller_info(obj)

class CreditInfoForInstallmentSerializer(serializers.Serializer):
    """Serializer para información del crédito en cuotas"""
    credit_uid = serializers.CharField()
    client_full_name = serializers.CharField()
    client_id = serializers.CharField()
    subcategory = serializers.CharField()
    credit_state = serializers.CharField()

class InstallmentDetailsSerializer(serializers.Serializer):
    """Serializer para detalles de cuota"""
    number = serializers.IntegerField()
    due_date = serializers.CharField(allow_null=True)
    amount = serializers.CharField()
    amount_paid = serializers.CharField()
    remaining_amount = serializers.CharField()
    status = serializers.CharField()
    late_fee = serializers.CharField()
    percentage_paid = serializers.FloatField()

class PaymentTrackingSerializer(serializers.Serializer):
    """Serializer para seguimiento de pagos"""
    paid_on = serializers.CharField(allow_null=True)
    days_overdue = serializers.IntegerField()
    is_overdue = serializers.BooleanField()
    principal_amount = serializers.CharField()
    interest_amount = serializers.CharField()

class PeriodicityInfoSerializer(serializers.Serializer):
    """Serializer para información de periodicidad"""
    periodicity_name = serializers.CharField()
    periodicity_days = serializers.IntegerField()
    currency = serializers.CharField()

class CalculatedInstallmentMetricsSerializer(serializers.Serializer):
    """Serializer para métricas calculadas de cuota"""
    days_until_due = serializers.IntegerField()
    collection_priority = serializers.CharField()
    expected_collection_date = serializers.DateField(allow_null=True)
    risk_level = serializers.CharField()
    payment_reliability = serializers.CharField()

class ClientHistorySerializer(serializers.Serializer):
    """Serializer para historial del cliente"""
    total_overdue_installments = serializers.IntegerField()
    average_delay_days = serializers.FloatField()

class InstallmentCollectionSerializer(serializers.ModelSerializer):
    """Serializer para la vista de recaudo esperado"""
    id = serializers.CharField(source='id')
    credit_info = serializers.SerializerMethodField()
    installment_details = serializers.SerializerMethodField()
    payment_tracking = serializers.SerializerMethodField()
    periodicity_info = serializers.SerializerMethodField()
    calculated_metrics = serializers.SerializerMethodField()
    client_history = serializers.SerializerMethodField()

    class Meta:
        model = Installment
        fields = [
            'id',
            'credit_info',
            'installment_details',
            'payment_tracking',
            'periodicity_info',
            'calculated_metrics',
            'client_history'
        ]

    def get_credit_info(self, obj):
        return get_credit_info_for_installment(obj)

    def get_installment_details(self, obj):
        return get_installment_details(obj)

    def get_payment_tracking(self, obj):
        return get_payment_tracking(obj)

    def get_periodicity_info(self, obj):
        if obj.credit:
            return get_periodicity_info(obj.credit)
        return {
            'periodicity_name': "No especificado",
            'periodicity_days': 0,
            'currency': "COP"
        }

    def get_calculated_metrics(self, obj):
        client_history = get_client_history_for_installment(obj)
        return get_calculated_installment_metrics(obj, client_history)

    def get_client_history(self, obj):
        return get_client_history_for_installment(obj)

class CreditsSummarySerializer(serializers.Serializer):
    """Serializer para resumen de créditos"""
    total_active_credits = serializers.IntegerField()
    total_amount_lent = serializers.CharField()
    total_pending_amount = serializers.CharField()
    total_collected = serializers.CharField()
    average_credit_amount = serializers.CharField()
    collection_percentage = serializers.FloatField()

class InstallmentsSummarySerializer(serializers.Serializer):
    """Serializer para resumen de cuotas"""
    due_today = serializers.IntegerField()
    due_this_week = serializers.IntegerField()
    overdue_total = serializers.IntegerField()
    expected_collection_today = serializers.CharField()
    expected_collection_week = serializers.CharField()

class PerformanceMetricsSerializer(serializers.Serializer):
    """Serializer para métricas de rendimiento"""
    on_time_payment_rate = serializers.FloatField()
    average_delay_days = serializers.FloatField()
    default_rate = serializers.FloatField()
    recovery_rate = serializers.FloatField()

class ByPeriodicitySerializer(serializers.Serializer):
    """Serializer para métricas por periodicidad"""
    periodicity = serializers.CharField()
    total_credits = serializers.IntegerField()
    pending_amount = serializers.CharField()
    overdue_percentage = serializers.FloatField()

class AlertSerializer(serializers.Serializer):
    """Serializer para alertas"""
    type = serializers.CharField()
    message = serializers.CharField()
    count = serializers.IntegerField()

class DashboardSummarySerializer(serializers.Serializer):
    """Serializer para resumen del dashboard"""
    credits_summary = CreditsSummarySerializer()
    installments_summary = InstallmentsSummarySerializer()
    performance_metrics = PerformanceMetricsSerializer()
    by_periodicity = ByPeriodicitySerializer(many=True)
    alerts = AlertSerializer(many=True)

class PageInfoSerializer(serializers.Serializer):
    """Serializer para información de paginación"""
    current_page = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    page_size = serializers.IntegerField()
    has_next = serializers.BooleanField()
    has_previous = serializers.BooleanField()

class PaginatedResponseSerializer(serializers.Serializer):
    """Serializer para respuesta paginada"""
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    page_info = PageInfoSerializer()
    results = serializers.ListField()
