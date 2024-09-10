from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
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
    client = UserSerializer()  # Relación con el modelo User
    payments = AccountMethodAmountSerializer(many=True, read_only=True)  # Lista de pagos relacionados con el crédito

    class Meta:
        model = Credit
        fields = [
            'uid', 'client', 'cost', 'price', 'currency', 'total_abonos', 'pending_amount', 
            'first_date_payment', 'second_date_payment', 'credit_days', 'payments'
        ]

    def update(self, instance, validated_data):
        # Lógica personalizada para actualizar el saldo pendiente y los pagos
        total_abonos = sum(payment['amount'] for payment in validated_data.get('payments', []))
        instance.total_abonos = total_abonos
        instance.pending_amount = instance.price - total_abonos
        instance.save()
        return instance
