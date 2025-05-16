from django.urls import path
from .views import (
   CreditsAPIView,
   FinanceView,
   SellerChartDataAPIView,
   TransactionsAPIView, 
   ClientsWithDefaultAPIView,
   SortedCreditsByLabelAPIView,
   MonthlyChartDataAPIView
   )

urlpatterns = [
    path('credits/', CreditsAPIView.as_view(), name='credits'),
    path('transactions/', TransactionsAPIView.as_view(), name='transactions'),
    path('clients/defaults/', ClientsWithDefaultAPIView.as_view(), name='clients_with_default'),
    
    # Rutas para APIViews
    path('data/', FinanceView.as_view(), name='finance-summary'),
    path('sheet/', SortedCreditsByLabelAPIView.as_view(), name='creditw'),
    path("chart/sellers/", SellerChartDataAPIView.as_view(), name="chart-sellers"),
    path("chart/monthly/", MonthlyChartDataAPIView.as_view(), name="monthly-chart-data")
]

