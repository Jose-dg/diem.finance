from rest_framework import viewsets
from .models import Client, Category, Account, Transaction, Credit, Expense
from ..fintech.serializers import (
    ClientSerializer,
    CategorySerializer,
    AccountSerializer,
    TransactionSerializer,
    CreditSerializer,
    ExpenseSerializer
)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class CreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer