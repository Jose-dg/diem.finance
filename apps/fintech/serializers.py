from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

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

from django.utils.timezone import localtime
from .models import Credit, AccountMethodAmount, CreditAdjustment
from .serializers import UserSerializer, AccountSerializer, SubCategorySerializer, CurrencySerializer

class CreditAdjustmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditAdjustment
        fields = ['type', 'amount', 'added_on', 'reason', 'created_at']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.created_at:
            ret['created_at'] = localtime(instance.created_at).isoformat()
        return ret

class CreditSerializer(serializers.ModelSerializer):
    # ① campos que ya tenías
    user       = UserSerializer()
    payments   = serializers.SerializerMethodField()
    subcategory = SubCategorySerializer()
    currency   = CurrencySerializer()

    periodicity_days = serializers.IntegerField(source='periodicity.days', read_only=True)
    adjustments = CreditAdjustmentSerializer(many=True, read_only=True)

    class Meta:
        model  = Credit
        fields = '__all__'        # DRF incluirá también periodicity_days

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
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
        }
        return data
