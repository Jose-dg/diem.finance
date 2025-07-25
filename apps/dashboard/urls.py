from django.urls import path
from .views import (
   CreditsAPIView,
   CreditFilterAPIView,
   FinanceView,
   SellerChartDataAPIView,
   MonthlyChartDataAPIView,
   CreditKPIView
   )

urlpatterns = [
    path('credits/', CreditsAPIView.as_view(), name='credits'),
    path('credits/filter/', CreditFilterAPIView.as_view(), name='credit-filter'),
    
    # Roots for charts 
    path('data/', FinanceView.as_view(), name='finance-summary'),
    path("chart/sellers/", SellerChartDataAPIView.as_view(), name="chart-sellers"),
    path("chart/monthly/", MonthlyChartDataAPIView.as_view(), name="monthly-chart-data"),

    # Roots for KPIs
    path('kpi/summary/', CreditKPIView.as_view(), name='kpi-summary')
]

