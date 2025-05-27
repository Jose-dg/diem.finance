from django.urls import path
from .views import (
   CreditsAPIView,
   FinanceView,
   SellerChartDataAPIView,
   TransactionsAPIView, 
   MonthlyChartDataAPIView
   )

urlpatterns = [
    path('credits/', CreditsAPIView.as_view(), name='credits'),
    path('transactions/', TransactionsAPIView.as_view(), name='transactions'),
    
    # Rutas para APIViews
    path('data/', FinanceView.as_view(), name='finance-summary'),
    path("chart/sellers/", SellerChartDataAPIView.as_view(), name="chart-sellers"),
    path("chart/monthly/", MonthlyChartDataAPIView.as_view(), name="monthly-chart-data")
]

