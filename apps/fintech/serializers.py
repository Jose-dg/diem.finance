from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

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
    transaction_date = serializers.DateTimeField(source='transaction.date', read_only=True)

    class Meta:
        model = AccountMethodAmount
        fields = ['payment_method', 'amount', 'credit']

class TransactionSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    method_amount = AccountMethodAmountSerializer()
    currency = CurrencySerializer()  

    class Meta:
        model = Transaction
        fields = ['uid', 'transaction_type', 'account', 'date', 'amount', 'currency', 'method_amount']

class CreditSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    payments = serializers.SerializerMethodField()
    subcategory = SubCategorySerializer()
    currency = CurrencySerializer()

    class Meta:
        model = Credit
        fields = [
            'created_at', 'uid', 'user', 'state', 'subcategory', 'cost', 'installment_number', 'installment_value', 'price', 'currency', 'total_abonos', 'pending_amount',
            'first_date_payment', 'second_date_payment', 'credit_days', 'payments', 'description'
        ]

    def get_payments(self, obj):
        payments = obj.payments.all().order_by('transaction__date')
        return AccountMethodAmountSerializer(payments, many=True).data

    def update(self, instance, validated_data):
        # Lógica personalizada para actualizar el saldo pendiente y los pagos
        total_abonos = sum(payment['amount'] for payment in validated_data.get('payments', []))
        instance.total_abonos = total_abonos
        instance.pending_amount = instance.price - total_abonos
        instance.save()
        return instance
    
class CreditDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    abonos = serializers.SerializerMethodField()

    class Meta:
        model = Credit
        fields = [
            'uid', 'state', 'subcategory', 'cost', 'price', 'earnings',
            'first_date_payment', 'second_date_payment', 'credit_days',
            'description', 'interest', 'refinancing', 'total_abonos',
            'pending_amount', 'installment_number', 'installment_value',
            'is_in_default', 'created_at', 'updated_at', 'morosidad_level',
            'category', 'user', 'currency', 'periodicity', 'payment', 'registered_by',
            'abonos'
        ]

    def get_abonos(self, obj):
        abonos = obj.payments.all().order_by('transaction__date') if obj.payments.exists() else []
        return AccountMethodAmountSerializer(abonos, many=True).data
    
class ExpenseSerializer(serializers.ModelSerializer):
    subcategory = SubCategorySerializer()
    user = UserSerializer()

    class Meta:
        model = Expense
        fields = ['ui', 'subcategory', 'amount', 'description', ' date']