from django.urls import path
from .views import (
   CreditsAPIView,
   CreditsVsRecaudosChart,
   FinanceView,
   TransactionsAPIView, 
   ClientsWithDefaultAPIView
   )

urlpatterns = [
    path('credits/', CreditsAPIView.as_view(), name='credits'),
    path('transactions/', TransactionsAPIView.as_view(), name='transactions'),
    path('clients/defaults/', ClientsWithDefaultAPIView.as_view(), name='clients_with_default'),
    
    # Rutas para APIViews
    path('data/', FinanceView.as_view(), name='finance-summary'),
    path('charts/credits-vs-recaudos/', CreditsVsRecaudosChart.as_view(), name='credits-vs-recaudos-chart'),
]

