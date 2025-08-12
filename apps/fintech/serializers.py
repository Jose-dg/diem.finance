from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.utils.timezone import localtime
from .models import Credit, AccountMethodAmount, CreditAdjustment
from rest_framework.pagination import PageNumberPagination

User = get_user_model()

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['country_code', 'phone_number']

class SubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')

    class Meta:
        model = SubCategory
        fields = ['name', 'category_name']  

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id_currency', 'currency', 'exchange_rate'] 

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['name', 'position'] 

class UserSerializer(serializers.ModelSerializer):
    phone_1 = PhoneNumberSerializer() 
    label = LabelSerializer() 

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_1', 'label']  

class AccountSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = Account
        fields = ['id_payment_method', 'name', 'account_number', 'balance', 'currency']

class AccountMethodAmountSerializer(serializers.ModelSerializer):
    payment_method = AccountSerializer()
    currency = serializers.StringRelatedField()
    transaction_date = serializers.DateTimeField(source='transaction.date', read_only=True)

    class Meta:
        model = AccountMethodAmount
        fields = ['payment_method', 'payment_code', 'amount', 'amount_paid', 'currency', 'transaction_date']

class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    agent = UserSerializer()
    category = SubCategorySerializer()
    payments = serializers.SerializerMethodField()
    credit = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            'uid', 'transaction_type', 'category', 'user', 'agent', 'status',
            'source', 'date', 'description', 'payments', 'credit'
        ]

    def get_payments(self, obj):
        payments = AccountMethodAmount.objects.filter(transaction=obj).order_by('transaction__date')
        return AccountMethodAmountSerializer(payments, many=True).data

class CreditAdjustmentSerializer(serializers.ModelSerializer):
    adjustment_type = serializers.SerializerMethodField()
    adjustment_name = serializers.SerializerMethodField()
    is_positive = serializers.SerializerMethodField()
    sign = serializers.SerializerMethodField()
    
    class Meta:
        model = CreditAdjustment
        fields = [
            'id', 'type', 'adjustment_type', 'adjustment_name', 'amount', 
            'added_on', 'reason', 'created_at', 'is_positive', 'sign'
        ]

    def get_adjustment_type(self, obj):
        """Obtiene el código del tipo de ajuste"""
        if obj.type:
            return obj.type.code
        return None
    
    def get_adjustment_name(self, obj):
        """Obtiene el nombre del tipo de ajuste"""
        if obj.type:
            return obj.type.name
        return "Tipo no especificado"
    
    def get_is_positive(self, obj):
        """Indica si el ajuste es positivo (descuento) o negativo (cargo)"""
        if obj.type:
            return obj.type.is_positive
        return True
    
    def get_sign(self, obj):
        """Retorna el signo del ajuste (+ para descuentos, - para cargos)"""
        if obj.type:
            return '+' if obj.type.is_positive else '-'
        return '+'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.created_at:
            ret['created_at'] = localtime(instance.created_at).isoformat()
        return ret

class InstallmentSerializer(serializers.ModelSerializer):
    credit_uid = serializers.CharField(source='credit.uid', read_only=True)
    user_name = serializers.SerializerMethodField()
    remaining_amount_calc = serializers.SerializerMethodField()
    days_overdue_calc = serializers.SerializerMethodField()
    late_fee_calc = serializers.SerializerMethodField()
    total_amount_due = serializers.SerializerMethodField()
    
    class Meta:
        model = Installment
        fields = [
            'id', 'number', 'due_date', 'amount', 'paid', 'paid_on',
            'principal_amount', 'interest_amount', 'late_fee', 'status',
            'credit_uid', 'user_name', 'remaining_amount_calc', 
            'days_overdue_calc', 'late_fee_calc', 'total_amount_due'
        ]
    
    def get_user_name(self, obj):
        """Obtiene el nombre completo del usuario"""
        if obj.credit and obj.credit.user:
            user = obj.credit.user
            full_name = f"{user.first_name} {user.last_name}".strip()
            return full_name if full_name else user.username
        return "Usuario no disponible"
    
    def get_remaining_amount_calc(self, obj):
        """Monto restante calculado"""
        from apps.fintech.services.utils import InstallmentCalculator
        return InstallmentCalculator.get_remaining_amount(obj)
    
    def get_days_overdue_calc(self, obj):
        """Días de mora calculados"""
        from apps.fintech.services.utils import InstallmentCalculator
        return InstallmentCalculator.get_days_overdue(obj)
    
    def get_late_fee_calc(self, obj):
        """Recargo por mora calculado"""
        from apps.fintech.services.utils import InstallmentCalculator
        return InstallmentCalculator.get_late_fee(obj)
    
    def get_total_amount_due(self, obj):
        """Total a pagar calculado"""
        from apps.fintech.services.utils import InstallmentCalculator
        return InstallmentCalculator.get_total_amount_due(obj)

class CreditFilterSerializer(serializers.Serializer):
    start_date = serializers.DateField(
        help_text="Fecha de inicio (YYYY-MM-DD) en America/Bogota",
        required=True
    )
    end_date = serializers.DateField(
        help_text="Fecha de fin (YYYY-MM-DD) en America/Bogota",
        required=True
    )
    status = serializers.ChoiceField(
        choices=Credit.ORDER_STATES, required=False,
        help_text="Filtra por estado de crédito"
    )

class CreditListSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%S%z",
        default_timezone=timezone.get_default_timezone()
    )

    class Meta:
        model = Credit
        fields = [
            'uid', 'user', 'state', 'cost', 'price',
            'pending_amount', 'total_abonos', 'created_at',
            # añade aquí los campos que necesites exponer
        ]
            
class CreditSerializer(serializers.ModelSerializer):
    # ① campos que ya tenías
    user       = UserSerializer()
    payments   = serializers.SerializerMethodField()
    subcategory = SubCategorySerializer()
    currency   = CurrencySerializer()

    periodicity_days = serializers.IntegerField(source='periodicity.days', read_only=True)
    adjustments = CreditAdjustmentSerializer(many=True, read_only=True)
    installments = InstallmentSerializer(many=True, read_only=True)
    
    # Campos calculados para ajustes
    total_adjustments = serializers.SerializerMethodField()
    total_discounts = serializers.SerializerMethodField()
    total_charges = serializers.SerializerMethodField()
    adjustments_summary = serializers.SerializerMethodField()

    class Meta:
        model  = Credit
        fields = '__all__'        

    def get_payments(self, obj):
        qs = AccountMethodAmount.objects.filter(
            credit=obj
        ).select_related('transaction', 'currency').order_by('transaction__date')

        return [
            {
                "payment_method": AccountSerializer(p.payment_method).data,
                "payment_code":   p.payment_code,
                "amount":         p.amount,
                "amount_paid":    p.amount_paid,
                "currency":       p.currency.currency if p.currency else "No currency",
                "transaction_date": p.transaction.date if p.transaction else None,
            }
            for p in qs
        ]
    
    def get_total_adjustments(self, obj):
        """Calcula el total de ajustes (descuentos - cargos)"""
        total = 0
        for adjustment in obj.adjustments.all():
            if adjustment.type and adjustment.type.is_positive:
                total += float(adjustment.amount)
            else:
                total -= float(adjustment.amount)
        return total
    
    def get_total_discounts(self, obj):
        """Calcula el total de descuentos aplicados"""
        total = 0
        for adjustment in obj.adjustments.all():
            if adjustment.type and adjustment.type.is_positive:
                total += float(adjustment.amount)
        return total
    
    def get_total_charges(self, obj):
        """Calcula el total de cargos aplicados"""
        total = 0
        for adjustment in obj.adjustments.all():
            if adjustment.type and not adjustment.type.is_positive:
                total += float(adjustment.amount)
        return total
    
    def get_adjustments_summary(self, obj):
        """Resumen de ajustes por tipo"""
        summary = {}
        for adjustment in obj.adjustments.all():
            if adjustment.type:
                type_name = adjustment.type.name
                if type_name not in summary:
                    summary[type_name] = {
                        'type_code': adjustment.type.code,
                        'total_amount': 0,
                        'count': 0,
                        'is_positive': adjustment.type.is_positive
                    }
                summary[type_name]['total_amount'] += float(adjustment.amount)
                summary[type_name]['count'] += 1
        return summary
 
class CreditSimpleSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    subcategory = SubCategorySerializer()
    currency = CurrencySerializer()
    periodicity_days = serializers.IntegerField(source='periodicity.days', read_only=True)

    class Meta:
        model = Credit
        fields = [
            'id', 'uid', 'user', 'state', 'price', 'pending_amount', 'currency',
            'subcategory', 'periodicity_days', 'installment_number', 'installment_value',
            'first_date_payment', 'second_date_payment', 'created_at'
        ]
        
class CreditDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    abonos = serializers.SerializerMethodField()

    class Meta:
        model = Credit
        abonos = serializers.SerializerMethodField()

        class Meta:
            model = Credit
            fields = '__all__'
    
    def get_abonos(self, obj):
        abonos = AccountMethodAmount.objects.filter(credit=obj).order_by('transaction__date')
        return AccountMethodAmountSerializer(abonos, many=True).data

class ExpenseSerializer(serializers.ModelSerializer):
    subcategory = SubCategorySerializer()
    user = UserSerializer()

    class Meta:
        model = Expense
        fields = ['ui', 'subcategory', 'amount', 'description', ' date']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    
    def get_token(cls, user):
        token = super().get_token(user)

        # Agrega información adicional del usuario al token
        token['id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        
        token['last_name'] = user.last_name

        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        token['is_active'] = user.is_active
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'is_staff': self.user.is_staff,
            'is_superuser': self.user.is_superuser,
            'is_active': self.user.is_active,

        }

        print(data)
        return data

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class ClientCreditsQuerySerializer(serializers.Serializer):
    """
    Serializer para consultar créditos de un cliente por documento y/o nombre
    """
    document_number = serializers.CharField(
        max_length=20, 
        required=False, 
        help_text="Número de documento del cliente"
    )
    first_name = serializers.CharField(
        max_length=150, 
        required=False, 
        help_text="Primer nombre del cliente"
    )
    last_name = serializers.CharField(
        max_length=150, 
        required=False, 
        help_text="Apellido del cliente"
    )
    
    def validate(self, attrs):
        """
        Valida que al menos se proporcione documento o nombre
        """
        document_number = attrs.get('document_number')
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        
        if not document_number and not first_name and not last_name:
            raise serializers.ValidationError(
                "Debe proporcionar al menos un criterio de búsqueda: "
                "document_number, first_name o last_name"
            )
        
        return attrs

class ClientCreditsResponseSerializer(serializers.ModelSerializer):
    """
    Serializer para la respuesta de créditos de un cliente
    """
    user = UserSerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    currency = CurrencySerializer(read_only=True)
    periodicity_days = serializers.IntegerField(source='periodicity.days', read_only=True)
    payments = serializers.SerializerMethodField()
    installments = InstallmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Credit
        fields = [
            'uid', 'user', 'state', 'subcategory', 'price', 'pending_amount',
            'total_abonos', 'currency', 'periodicity_days', 'installment_number',
            'installment_value', 'first_date_payment', 'second_date_payment',
            'created_at', 'payments', 'installments', 'is_in_default',
            'morosidad_level', 'earnings', 'interest'
        ]
    
    def get_payments(self, obj):
        """Obtiene los pagos del crédito"""
        qs = AccountMethodAmount.objects.filter(
            credit=obj
        ).select_related('transaction', 'currency').order_by('transaction__date')

        return [
            {
                "payment_method": AccountSerializer(p.payment_method).data,
                "payment_code": p.payment_code,
                "amount": p.amount,
                "amount_paid": p.amount_paid,
                "currency": p.currency.currency if p.currency else "No currency",
                "transaction_date": p.transaction.date if p.transaction else None,
            }
            for p in qs
        ]