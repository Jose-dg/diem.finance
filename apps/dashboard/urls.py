from django.urls import path
from .views import (
   CreditDetailAPIView, 
   FinanceView, 
   NewCreditsAPIView, 
   PendingCreditsAPIView, 
   TransactionsAPIView, 
   ClientsWithDefaultAPIView, 
   FinancialCreditsAPIView, 
   ProductCreditsAPIView, 
   FilteredDataView)

urlpatterns = [
    path('finance/', FinanceView.as_view(), name='finance'),
    path('transactions/', TransactionsAPIView.as_view(), name='transactions'),
    path('credits/new/', NewCreditsAPIView.as_view(), name='new_credits'),
    path('credits/pending/', PendingCreditsAPIView.as_view(), name='pending_credits'),
    path('clients/defaults/', ClientsWithDefaultAPIView.as_view(), name='clients_with_default'),
    path('credits/financial/', FinancialCreditsAPIView.as_view(), name='financial_credits'),
    path('credits/products/', ProductCreditsAPIView.as_view(), name='product_credits'),
    path('credit/', CreditDetailAPIView.as_view(), name='credit-detail'),
]

