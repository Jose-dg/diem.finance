from django.urls import path, include
from . import views

app_name = 'insights'

urlpatterns = [
    # Dashboards principales (independientes de modelos insights)
    path('dashboard/executive/', views.ExecutiveDashboardView.as_view(), name='executive_dashboard'),
    path('dashboard/credits/', views.CreditAnalyticsView.as_view(), name='credit_analytics'),
    path('dashboard/risk/', views.RiskDashboardView.as_view(), name='risk_dashboard'),
    path('dashboard/users/', views.UserInsightsView.as_view(), name='user_insights'),
    path('dashboard/operational/', views.OperationalDashboardView.as_view(), name='operational_dashboard'),
    path('dashboard/revenue/', views.RevenueDashboardView.as_view(), name='revenue_dashboard'),
    
    # Analytics específicos (independientes de modelos insights)
    path('portfolio/overview/', views.PortfolioOverviewView.as_view(), name='portfolio_overview'),
    path('predictive/insights/', views.PredictiveInsightsView.as_view(), name='predictive_insights'),
    
    # Análisis de créditos con parámetros de fechas
    path('credits/analysis/', views.CreditAnalysisView.as_view(), name='credit_analysis'),
    path('credits/analysis/summary/', views.CreditAnalysisSummaryView.as_view(), name='credit_analysis_summary'),
    path('credits/analysis/clients/', views.CreditAnalysisClientsView.as_view(), name='credit_analysis_clients'),
    path('credits/analysis/clients-without-payments/', views.ClientsWithoutPaymentsView.as_view(), name='clients_without_payments'),
    
    # Resumen y utilidades (independientes de modelos insights)
    path('summary/', views.InsightsSummaryView.as_view(), name='insights_summary'),
    path('health-check/', views.insights_health_check, name='health_check'),
    path('export/', views.insights_export, name='export_data'),
    
    # FINANCIAL CONTROL SYSTEM - Nuevas URLs
    path('financial-control/dashboard/', views.FinancialControlDashboardView.as_view(), name='financial_control_dashboard'),
    path('financial-control/defaulters/', views.DefaultersListView.as_view(), name='defaulters_list'),
    path('financial-control/defaulters/enhanced/', views.EnhancedDefaultersInsightsView.as_view(), name='enhanced_defaulters_insights'),
    path('financial-control/metrics/user/', views.UserFinancialMetricsView.as_view(), name='user_financial_metrics'),
    path('financial-control/metrics/user/<int:user_id>/', views.UserFinancialMetricsView.as_view(), name='user_financial_metrics_detail'),
    path('financial-control/alerts/', views.FinancialAlertsView.as_view(), name='financial_alerts'),
    path('financial-control/reports/', views.DefaultersReportsView.as_view(), name='defaulters_reports'),
    
    # NUEVAS VISTAS DE DASHBOARD OPTIMIZADAS
    path('api/credits/dashboard/', views.CreditDashboardViewSet.as_view({'get': 'list'}), name='credits_dashboard'),
    path('api/installments/expected-collection/', views.InstallmentCollectionViewSet.as_view({'get': 'list'}), name='installments_collection'),
    path('api/dashboard/summary/', views.DashboardSummaryView.as_view(), name='dashboard_summary'),
    path('api/credits/analytics/', views.CreditAnalyticsAdvancedView.as_view(), name='credits_analytics_advanced'),
    path('api/risk/analysis/', views.RiskAnalysisAdvancedView.as_view(), name='risk_analysis_advanced'),
]

