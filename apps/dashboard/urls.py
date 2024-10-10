from django.urls import path
from .views import (
   CreditsAPIView,
   TransactionsAPIView, 
   ClientsWithDefaultAPIView
   )

urlpatterns = [
    path('credits/', CreditsAPIView.as_view(), name='credits'),
    path('transactions/', TransactionsAPIView.as_view(), name='transactions'),
    path('clients/defaults/', ClientsWithDefaultAPIView.as_view(), name='clients_with_default'),
]

