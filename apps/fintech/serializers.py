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

# class AccountMethodAmountSerializer(serializers.ModelSerializer):
#     payment_method = AccountSerializer()
#     transaction_date = serializers.DateTimeField(source='transaction.date', read_only=True)

#     class Meta:
#         model = AccountMethodAmount
#         fields = ['payment_method', 'amount', 'credit', 'transaction_date']

class AccountMethodAmountSerializer(serializers.ModelSerializer):
    payment_method = AccountSerializer()
    currency = serializers.StringRelatedField()

    class Meta:
        model = AccountMethodAmount
        fields = ['payment_method', 'payment_code', 'amount', 'amount_paid', 'currency', 'transaction_date']

# class TransactionSerializer(serializers.ModelSerializer):
#     account = AccountSerializer()
#     method_amount = AccountMethodAmountSerializer()
#     currency = CurrencySerializer()  

#     class Meta:
#         model = Transaction
#         fields = '__all__'


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
        payments = obj.account_method_amounts.all().order_by('transaction__date')
        return AccountMethodAmountSerializer(payments, many=True).data

    def get_credit(self, obj):
        # Attempt to fetch the credit associated with the transaction
        related_credit = obj.account_method_amounts.first()
        return CreditSerializer(related_credit.credit).data if related_credit else None

class CreditSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    payments = serializers.SerializerMethodField()
    subcategory = SubCategorySerializer()
    currency = CurrencySerializer()

    class Meta:
        model = Credit
        fields = '__all__'

        # fields = [
        #     'created_at', 'uid', 'user', 'state', 'subcategory', 'cost', 'installment_number', 'installment_value', 'price', 'currency', 'total_abonos', 'pending_amount',
        #     'first_date_payment', 'second_date_payment', 'credit_days', 'payments', 'description', 'morosidad_level'
        # ]

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
        fields = '__all__'
        # fields = [
        #     'uid', 'state', 'subcategory', 'cost', 'price', 'earnings',
        #     'first_date_payment', 'second_date_payment', 'credit_days',
        #     'description', 'interest', 'refinancing', 'total_abonos',
        #     'pending_amount', 'installment_number', 'installment_value',
        #     'is_in_default', 'created_at', 'updated_at', 'morosidad_level',
        #     'category', 'user', 'currency', 'periodicity', 'payment', 'registered_by',
        #     'abonos'
        # ]

    def get_abonos(self, obj):
        abonos = obj.payments.all().order_by('transaction__date') if obj.payments.exists() else []
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
