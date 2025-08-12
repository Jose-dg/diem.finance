from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import datetime, date
from django.core.exceptions import ValidationError

from apps.insights.services.analytics_service import AnalyticsService
from apps.insights.services.dashboard_service import DashboardService
from apps.insights.services.credit_analysis_service import CreditAnalysisService

class ExecutiveDashboardView(APIView):
    """Vista para dashboard ejecutivo"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        """Obtener KPIs principales del dashboard ejecutivo"""
        try:
            dashboard_data = DashboardService.get_executive_dashboard()
            return Response({
                'success': True,
                'data': dashboard_data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreditAnalyticsView(APIView):
    """Vista para analytics de créditos"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Obtener analytics de créditos"""
        try:
            days = int(request.query_params.get('days', 30))
            analytics_data = DashboardService.get_credit_analytics_dashboard()
            
            # Agregar métricas de rendimiento
            performance_metrics = AnalyticsService.get_credit_performance_metrics(days)
            analytics_data.update(performance_metrics)
            
            return Response({
                'success': True,
                'data': analytics_data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RiskDashboardView(APIView):
    """Vista para dashboard de riesgos"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        """Obtener métricas de riesgo"""
        try:
            risk_data = DashboardService.get_risk_dashboard()
            
            # Agregar analytics de riesgo
            risk_analytics = AnalyticsService.get_risk_analytics()
            risk_data.update(risk_analytics)
            
            return Response({
                'success': True,
                'data': risk_data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserInsightsView(APIView):
    """Vista para insights de usuarios"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Obtener insights de usuarios"""
        try:
            user_data = DashboardService.get_user_insights_dashboard()
            
            # Agregar analytics de comportamiento
            behavior_analytics = AnalyticsService.get_user_behavior_analytics()
            user_data.update(behavior_analytics)
            
            return Response({
                'success': True,
                'data': user_data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OperationalDashboardView(APIView):
    """Vista para dashboard operacional"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        """Obtener métricas operacionales"""
        try:
            operational_data = DashboardService.get_operational_dashboard()
            
            # Agregar métricas operacionales
            operational_metrics = AnalyticsService.get_operational_metrics()
            operational_data.update(operational_metrics)
            
            return Response({
                'success': True,
                'data': operational_data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RevenueDashboardView(APIView):
    """Vista para dashboard de ingresos"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        """Obtener métricas de ingresos"""
        try:
            revenue_data = DashboardService.get_revenue_dashboard()
            
            # Agregar analytics de ingresos
            revenue_analytics = AnalyticsService.get_revenue_analytics()
            revenue_data.update(revenue_analytics)
            
            return Response({
                'success': True,
                'data': revenue_data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PortfolioOverviewView(APIView):
    """Vista para vista general del portafolio"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Obtener vista general del portafolio"""
        try:
            portfolio_data = AnalyticsService.get_portfolio_overview()
            return Response({
                'success': True,
                'data': portfolio_data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PredictiveInsightsView(APIView):
    """Vista para insights predictivos"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        """Obtener insights predictivos"""
        try:
            predictive_data = AnalyticsService.get_predictive_insights()
            return Response({
                'success': True,
                'data': predictive_data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InsightsSummaryView(APIView):
    """Vista resumen de todos los insights independientes"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Obtener resumen de todos los insights independientes"""
        try:
            summary = {
                'portfolio': AnalyticsService.get_portfolio_overview(),
                'user_behavior': AnalyticsService.get_user_behavior_analytics(),
                'risk': AnalyticsService.get_risk_analytics(),
                'revenue': AnalyticsService.get_revenue_analytics(),
                'operational': AnalyticsService.get_operational_metrics(),
                'predictive': AnalyticsService.get_predictive_insights()
            }
            
            return Response({
                'success': True,
                'data': summary
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def insights_health_check(request):
    """Health check para el sistema de insights independientes"""
    try:
        # Verificar que los servicios están funcionando
        portfolio_data = AnalyticsService.get_portfolio_overview()
        dashboard_data = DashboardService.get_executive_dashboard()
        
        health_status = {
            'status': 'healthy',
            'services': {
                'analytics_service': 'operational',
                'dashboard_service': 'operational'
            },
            'data_sources': {
                'credits': 'available',
                'transactions': 'available',
                'users': 'available',
                'installments': 'available'
            },
            'last_updated': timezone.now().isoformat()
        }
        
        return Response({
            'success': True,
            'data': health_status
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'status': 'unhealthy'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def insights_export(request):
    """Exportar datos de insights independientes"""
    try:
        export_type = request.query_params.get('type', 'summary')
        format_type = request.query_params.get('format', 'json')
        
        if export_type == 'portfolio':
            data = AnalyticsService.get_portfolio_overview()
        elif export_type == 'user_behavior':
            data = AnalyticsService.get_user_behavior_analytics()
        elif export_type == 'risk':
            data = AnalyticsService.get_risk_analytics()
        elif export_type == 'revenue':
            data = AnalyticsService.get_revenue_analytics()
        elif export_type == 'operational':
            data = AnalyticsService.get_operational_metrics()
        elif export_type == 'predictive':
            data = AnalyticsService.get_predictive_insights()
        else:
            # Summary por defecto
            data = {
                'portfolio': AnalyticsService.get_portfolio_overview(),
                'user_behavior': AnalyticsService.get_user_behavior_analytics(),
                'risk': AnalyticsService.get_risk_analytics(),
                'revenue': AnalyticsService.get_revenue_analytics(),
                'operational': AnalyticsService.get_operational_metrics(),
                'predictive': AnalyticsService.get_predictive_insights()
            }
        
        if format_type == 'csv':
            # Implementar exportación a CSV
            pass
        elif format_type == 'excel':
            # Implementar exportación a Excel
            pass
        
        return Response({
            'success': True,
            'data': data,
            'export_type': export_type,
            'format': format_type
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreditAnalysisView(APIView):
    """Vista para análisis detallado de créditos con parámetros de fechas"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        """
        Obtener análisis detallado de créditos
        
        Parámetros:
        - start_date: Fecha de inicio (YYYY-MM-DD)
        - end_date: Fecha de fin (YYYY-MM-DD)
        - limit: Límite de clientes en la tabla (opcional)
        - include_payments: Incluir análisis de pagos (true/false)
        - include_defaults: Incluir análisis de morosidad (true/false)
        """
        try:
            # Validar y parsear fechas
            start_date_str = request.query_params.get('start_date')
            end_date_str = request.query_params.get('end_date')
            
            if not start_date_str or not end_date_str:
                return Response({
                    'success': False,
                    'error': 'start_date y end_date son parámetros requeridos (formato: YYYY-MM-DD)'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({
                    'success': False,
                    'error': 'Formato de fecha inválido. Use YYYY-MM-DD'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar que start_date <= end_date
            if start_date > end_date:
                return Response({
                    'success': False,
                    'error': 'start_date debe ser menor o igual a end_date'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Obtener parámetros opcionales
            limit = request.query_params.get('limit')
            if limit:
                try:
                    limit = int(limit)
                    if limit <= 0:
                        raise ValueError("Limit debe ser positivo")
                except ValueError:
                    return Response({
                        'success': False,
                        'error': 'limit debe ser un número entero positivo'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            include_payments = request.query_params.get('include_payments', 'true').lower() == 'true'
            include_defaults = request.query_params.get('include_defaults', 'true').lower() == 'true'
            
            # Obtener datos del análisis
            analysis_data = {
                'summary': CreditAnalysisService.get_credit_analysis_summary(start_date, end_date),
                'clients_table': CreditAnalysisService.get_detailed_clients_table(start_date, end_date, limit)
            }
            
            # Agregar análisis de pagos si se solicita
            if include_payments:
                analysis_data['payments_analysis'] = CreditAnalysisService.get_payment_analysis(start_date, end_date)
            
            # Agregar análisis de morosidad si se solicita
            if include_defaults:
                analysis_data['default_analysis'] = CreditAnalysisService.get_default_analysis(start_date, end_date)
            
            return Response({
                'success': True,
                'data': analysis_data,
                'parameters': {
                    'start_date': start_date_str,
                    'end_date': end_date_str,
                    'limit': limit,
                    'include_payments': include_payments,
                    'include_defaults': include_defaults
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreditAnalysisSummaryView(APIView):
    """Vista para resumen rápido del análisis de créditos"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Obtener resumen rápido del análisis de créditos
        
        Parámetros:
        - start_date: Fecha de inicio (YYYY-MM-DD)
        - end_date: Fecha de fin (YYYY-MM-DD)
        """
        try:
            # Validar y parsear fechas
            start_date_str = request.query_params.get('start_date')
            end_date_str = request.query_params.get('end_date')
            
            if not start_date_str or not end_date_str:
                return Response({
                    'success': False,
                    'error': 'start_date y end_date son parámetros requeridos (formato: YYYY-MM-DD)'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({
                    'success': False,
                    'error': 'Formato de fecha inválido. Use YYYY-MM-DD'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar que start_date <= end_date
            if start_date > end_date:
                return Response({
                    'success': False,
                    'error': 'start_date debe ser menor o igual a end_date'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Obtener solo el resumen
            summary_data = CreditAnalysisService.get_credit_analysis_summary(start_date, end_date)
            
            return Response({
                'success': True,
                'data': summary_data,
                'parameters': {
                    'start_date': start_date_str,
                    'end_date': end_date_str
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreditAnalysisClientsView(APIView):
    """Vista específica para la tabla de clientes del análisis de créditos"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        """
        Obtener tabla detallada de clientes
        
        Parámetros:
        - start_date: Fecha de inicio (YYYY-MM-DD)
        - end_date: Fecha de fin (YYYY-MM-DD)
        - limit: Límite de clientes (opcional)
        - sort_by: Campo para ordenar (opcional)
        - risk_level: Filtrar por nivel de riesgo (LOW/MEDIUM/HIGH)
        """
        try:
            # Validar y parsear fechas
            start_date_str = request.query_params.get('start_date')
            end_date_str = request.query_params.get('end_date')
            
            if not start_date_str or not end_date_str:
                return Response({
                    'success': False,
                    'error': 'start_date y end_date son parámetros requeridos (formato: YYYY-MM-DD)'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({
                    'success': False,
                    'error': 'Formato de fecha inválido. Use YYYY-MM-DD'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar que start_date <= end_date
            if start_date > end_date:
                return Response({
                    'success': False,
                    'error': 'start_date debe ser menor o igual a end_date'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Obtener parámetros opcionales
            limit = request.query_params.get('limit')
            if limit:
                try:
                    limit = int(limit)
                    if limit <= 0:
                        raise ValueError("Limit debe ser positivo")
                except ValueError:
                    return Response({
                        'success': False,
                        'error': 'limit debe ser un número entero positivo'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            risk_level = request.query_params.get('risk_level')
            if risk_level and risk_level not in ['LOW', 'MEDIUM', 'HIGH']:
                return Response({
                    'success': False,
                    'error': 'risk_level debe ser LOW, MEDIUM o HIGH'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Obtener tabla de clientes
            clients_table = CreditAnalysisService.get_detailed_clients_table(start_date, end_date, limit)
            
            # Filtrar por nivel de riesgo si se especifica
            if risk_level:
                clients_table = [client for client in clients_table if client['risk_level'] == risk_level]
            
            # Ordenar si se especifica
            sort_by = request.query_params.get('sort_by')
            if sort_by and clients_table:
                valid_sort_fields = [
                    'total_credits', 'total_requested', 'total_paid', 'total_pending',
                    'payment_percentage', 'credits_in_default', 'avg_days_overdue'
                ]
                if sort_by in valid_sort_fields:
                    reverse = sort_by in ['total_requested', 'total_paid', 'total_pending', 'credits_in_default', 'avg_days_overdue']
                    clients_table.sort(key=lambda x: x[sort_by], reverse=reverse)
            
            return Response({
                'success': True,
                'data': {
                    'clients': clients_table,
                    'total_clients': len(clients_table)
                },
                'parameters': {
                    'start_date': start_date_str,
                    'end_date': end_date_str,
                    'limit': limit,
                    'risk_level': risk_level,
                    'sort_by': sort_by
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# mtyht6-ub.myshopify.com
# 4bbe3fe6a5aea88f93919b1e33170ee1

# k6Kav~SPE$