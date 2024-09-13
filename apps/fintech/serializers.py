from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['country_code', 'phone_number']

class UserSerializer(serializers.ModelSerializer):

    phone_1 = PhoneNumberSerializer() 

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_1']  # Ajusta los campos según tus necesidades


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id_payment_method', 'name', 'account_number', 'balance', 'currency']


class AccountMethodAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountMethodAmount
        fields = ['payment_method', 'amount', 'credit']

class TransactionSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    method_amount = AccountMethodAmountSerializer()  # Relación con AccountMethodAmount

    class Meta:
        model = Transaction
        fields = ['uid', 'transaction_type', 'account', 'date', 'amount', 'currency', 'method_amount']

class CreditSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Relación con el modelo User
    payments = AccountMethodAmountSerializer(many=True, read_only=True)  # Lista de pagos relacionados con el crédito

    class Meta:
        model = Credit
        fields = [
            'uid', 'user', 'cost', 'price', 'currency', 'total_abonos', 'pending_amount', 
            'first_date_payment', 'second_date_payment', 'credit_days', 'payments'
        ]

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
            'uid', 'state', 'credit_type', 'cost', 'price', 'earnings',
            'first_date_payment', 'second_date_payment', 'credit_days',
            'description', 'interest', 'refinancing', 'total_abonos',
            'pending_amount', 'installment_number', 'installment_value',
            'is_in_default', 'created_at', 'updated_at', 'morosidad_level',
            'category', 'user', 'currency', 'periodicity', 'payment', 'registered_by'
        ]
        # fields = ['uid', 'credit_type', 'client_name', 'price', 'first_date_payment', 'total_abonos', 'pending_amount', 'abonos']

    def get_abonos(self, obj):
        # Verificar si el crédito tiene pagos asociados
        abonos = obj.payments.all() if obj.payments.exists() else []
        return AccountMethodAmountSerializer(abonos, many=True).data