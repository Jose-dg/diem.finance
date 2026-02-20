from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import datetime, date, timedelta
from django.core.exceptions import ValidationError
from django.db.models import Sum, Count, Avg
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

from apps.fintech.models import User
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

class ClientsWithoutPaymentsView(APIView):
    """Vista específica para obtener lista de clientes sin pagos en un período"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        """
        Obtener lista específica de clientes que no han realizado ningún pago en el período
        
        Parámetros:
        - start_date: Fecha de inicio (YYYY-MM-DD)
        - end_date: Fecha de fin (YYYY-MM-DD)
        - limit: Límite de clientes (opcional, default: 100)
        - sort_by: Campo para ordenar (total_requested, total_pending, days_since_first_credit, etc.)
        - include_summary: Incluir resumen estadístico (true/false, default: true)
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
            limit = request.query_params.get('limit', 100)
            try:
                limit = int(limit)
                if limit <= 0:
                    raise ValueError("Limit debe ser positivo")
                # Limitar a máximo 500 para evitar sobrecarga
                limit = min(limit, 500)
            except ValueError:
                return Response({
                    'success': False,
                    'error': 'limit debe ser un número entero positivo'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            include_summary = request.query_params.get('include_summary', 'true').lower() == 'true'
            
            # Obtener lista de clientes sin pagos
            clients_without_payments = CreditAnalysisService.get_clients_without_payments(
                start_date, end_date, limit
            )
            
            # Ordenar si se especifica
            sort_by = request.query_params.get('sort_by')
            if sort_by and clients_without_payments:
                valid_sort_fields = [
                    'total_credits', 'total_requested', 'total_pending', 
                    'days_since_first_credit', 'avg_days_overdue', 'overdue_installments_count'
                ]
                if sort_by in valid_sort_fields:
                    reverse = sort_by in ['total_requested', 'total_pending', 'days_since_first_credit', 'avg_days_overdue', 'overdue_installments_count']
                    clients_without_payments.sort(key=lambda x: x[sort_by], reverse=reverse)
            
            # Preparar respuesta
            response_data = {
                'clients': clients_without_payments,
                'total_clients': len(clients_without_payments)
            }
            
            # Agregar resumen si se solicita
            if include_summary and clients_without_payments:
                total_requested = sum(client['total_requested'] for client in clients_without_payments)
                total_pending = sum(client['total_pending'] for client in clients_without_payments)
                total_credits = sum(client['total_credits'] for client in clients_without_payments)
                avg_days_overdue = sum(client['avg_days_overdue'] for client in clients_without_payments) / len(clients_without_payments)
                
                # Distribución por nivel de riesgo
                risk_distribution = {}
                for client in clients_without_payments:
                    risk = client['risk_level']
                    if risk not in risk_distribution:
                        risk_distribution[risk] = 0
                    risk_distribution[risk] += 1
                
                response_data['summary'] = {
                    'total_clients_without_payments': len(clients_without_payments),
                    'total_credits': total_credits,
                    'total_requested_amount': total_requested,
                    'total_pending_amount': total_pending,
                    'average_days_overdue': round(avg_days_overdue, 1),
                    'risk_distribution': risk_distribution,
                    'period': {
                        'start_date': start_date_str,
                        'end_date': end_date_str
                    }
                }
            
            return Response({
                'success': True,
                'data': response_data,
                'parameters': {
                    'start_date': start_date_str,
                    'end_date': end_date_str,
                    'limit': limit,
                    'sort_by': sort_by,
                    'include_summary': include_summary
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FinancialControlDashboardView(APIView):
    """Vista para dashboard de control financiero"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        """Obtener dashboard de control financiero"""
        try:
            from apps.insights.services.financial_control_service import FinancialControlService
            
            dashboard_data = FinancialControlService.get_financial_control_dashboard()
            
            return Response({
                'success': True,
                'data': dashboard_data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DefaultersListView(APIView):
    """Vista para lista paginada de clientes morosos"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        """Obtener lista paginada de clientes morosos"""
        try:
            from apps.insights.services.financial_control_service import FinancialControlService
            
            # Parámetros de paginación
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))
            
            # Validar límites de paginación
            page_size = min(max(page_size, 1), 100)  # Entre 1 y 100
            
            # Filtros
            filters = {}
            if request.query_params.get('risk_level'):
                filters['risk_level'] = request.query_params.get('risk_level')
            if request.query_params.get('min_overdue_amount'):
                filters['min_overdue_amount'] = request.query_params.get('min_overdue_amount')
            if request.query_params.get('max_overdue_amount'):
                filters['max_overdue_amount'] = request.query_params.get('max_overdue_amount')
            if request.query_params.get('min_days_overdue'):
                filters['min_days_overdue'] = request.query_params.get('min_days_overdue')
            
            # Obtener datos paginados
            result = FinancialControlService.get_defaulters_list(
                page=page, 
                page_size=page_size, 
                filters=filters
            )
            
            return Response({
                'success': True,
                'data': result
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserFinancialMetricsView(APIView):
    """Vista para métricas financieras de un usuario específico"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id=None):
        """Obtener métricas financieras de un usuario"""
        try:
            from apps.insights.services.financial_control_service import FinancialControlService
            
            # Si no se especifica user_id, usar el usuario actual
            if user_id is None:
                user = request.user
            else:
                from apps.fintech.models import User
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return Response({
                        'success': False,
                        'error': 'Usuario no encontrado'
                    }, status=status.HTTP_404_NOT_FOUND)
            
            # Calcular métricas
            metrics = FinancialControlService.calculate_user_financial_metrics(user)
            
            if metrics:
                from apps.insights.serializers import FinancialControlMetricsSerializer
                serializer = FinancialControlMetricsSerializer(metrics)
                
                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'error': 'No se pudieron calcular las métricas'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FinancialAlertsView(APIView):
    """Vista para alertas financieras"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        """Obtener alertas financieras con paginación"""
        try:
            from apps.insights.models import FinancialAlert
            from apps.insights.serializers import FinancialAlertSerializer
            
            # Parámetros de paginación
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))
            page_size = min(max(page_size, 1), 100)
            
            # Filtros
            queryset = FinancialAlert.objects.select_related('user', 'assigned_to').order_by('-created_at')
            
            if request.query_params.get('status'):
                queryset = queryset.filter(status=request.query_params.get('status'))
            
            if request.query_params.get('priority'):
                queryset = queryset.filter(priority=request.query_params.get('priority'))
            
            if request.query_params.get('alert_type'):
                queryset = queryset.filter(alert_type=request.query_params.get('alert_type'))
            
            # Paginación
            from django.core.paginator import Paginator
            paginator = Paginator(queryset, page_size)
            page_obj = paginator.get_page(page)
            
            # Serializar resultados
            serializer = FinancialAlertSerializer(page_obj, many=True)
            
            return Response({
                'success': True,
                'data': {
                    'results': serializer.data,
                    'pagination': {
                        'count': paginator.count,
                        'num_pages': paginator.num_pages,
                        'current_page': page_obj.number,
                        'has_next': page_obj.has_next(),
                        'has_previous': page_obj.has_previous(),
                        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
                        'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
                    }
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Crear nueva alerta financiera"""
        try:
            from apps.insights.services.financial_control_service import FinancialControlService
            from apps.fintech.models import User
            
            # Validar datos requeridos
            user_id = request.data.get('user_id')
            alert_type = request.data.get('alert_type')
            title = request.data.get('title')
            description = request.data.get('description')
            
            if not all([user_id, alert_type, title, description]):
                return Response({
                    'success': False,
                    'error': 'Faltan campos requeridos: user_id, alert_type, title, description'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Obtener usuario
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({
                    'success': False,
                    'error': 'Usuario no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Crear alerta
            alert = FinancialControlService.create_financial_alert(
                user=user,
                alert_type=alert_type,
                title=title,
                description=description,
                priority=request.data.get('priority', 'medium'),
                alert_data=request.data.get('alert_data', {})
            )
            
            if alert:
                from apps.insights.serializers import FinancialAlertSerializer
                serializer = FinancialAlertSerializer(alert)
                
                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'error': 'No se pudo crear la alerta'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DefaultersReportsView(APIView):
    """Vista para reportes de morosos"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        """Obtener reportes de morosos con paginación"""
        try:
            from apps.insights.models import DefaultersReport
            from apps.insights.serializers import DefaultersReportSerializer
            
            # Parámetros de paginación
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))
            page_size = min(max(page_size, 1), 50)
            
            # Filtros
            queryset = DefaultersReport.objects.select_related('generated_by').order_by('-report_date')
            
            if request.query_params.get('report_type'):
                queryset = queryset.filter(report_type=request.query_params.get('report_type'))
            
            # Paginación
            from django.core.paginator import Paginator
            paginator = Paginator(queryset, page_size)
            page_obj = paginator.get_page(page)
            
            # Serializar resultados
            serializer = DefaultersReportSerializer(page_obj, many=True)
            
            return Response({
                'success': True,
                'data': {
                    'results': serializer.data,
                    'pagination': {
                        'count': paginator.count,
                        'num_pages': paginator.num_pages,
                        'current_page': page_obj.number,
                        'has_next': page_obj.has_next(),
                        'has_previous': page_obj.has_previous(),
                        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
                        'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
                    }
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Generar nuevo reporte de morosos"""
        try:
            from apps.insights.services.financial_control_service import FinancialControlService
            
            report_type = request.data.get('report_type', 'daily')
            
            # Generar reporte
            report = FinancialControlService.generate_defaulters_report(
                report_type=report_type,
                generated_by=request.user
            )
            
            if report:
                from apps.insights.serializers import DefaultersReportSerializer
                serializer = DefaultersReportSerializer(report)
                
                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'error': 'No se pudo generar el reporte'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EnhancedDefaultersInsightsView(APIView):
    """Vista mejorada para insights de clientes morosos"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        """Obtener insights mejorados de clientes morosos"""
        try:
            from apps.insights.services.financial_control_service import FinancialControlService
            from apps.insights.models import FinancialControlMetrics, FinancialAlert
            
            # Métricas generales
            total_defaulters = FinancialControlMetrics.objects.filter(
                overdue_credits_count__gt=0
            ).count()
            
            total_overdue_amount = FinancialControlMetrics.objects.aggregate(
                total=Sum('total_overdue_amount')
            )['total'] or Decimal('0.00')
            
            # Distribución por riesgo
            risk_distribution = FinancialControlMetrics.objects.values('risk_level').annotate(
                count=Count('id'),
                total_amount=Sum('total_overdue_amount'),
                avg_days=Avg('days_in_default')
            )
            
            # Top 10 morosos por monto
            top_defaulters = FinancialControlMetrics.objects.filter(
                overdue_credits_count__gt=0
            ).select_related('user').order_by('-total_overdue_amount')[:10]
            
            # Alertas activas por prioridad
            alerts_by_priority = FinancialAlert.objects.filter(
                status='active'
            ).values('priority').annotate(count=Count('id'))
            
            # Tendencias (últimos 7 días)
            seven_days_ago = timezone.now() - timedelta(days=7)
            new_defaulters_7_days = FinancialControlMetrics.objects.filter(
                last_calculation__gte=seven_days_ago,
                overdue_credits_count__gt=0
            ).count()
            
            # Potencial de recuperación
            high_recovery = FinancialControlMetrics.objects.filter(
                risk_level__in=['low', 'medium'],
                days_in_default__lte=30
            ).count()
            
            medium_recovery = FinancialControlMetrics.objects.filter(
                risk_level='high',
                days_in_default__lte=60
            ).count()
            
            insights = {
                'summary': {
                    'total_defaulters': total_defaulters,
                    'total_overdue_amount': total_overdue_amount,
                    'new_defaulters_7_days': new_defaulters_7_days,
                    'default_rate': (total_defaulters / User.objects.count() * 100) if User.objects.count() > 0 else 0
                },
                'risk_distribution': list(risk_distribution),
                'top_defaulters': [
                    {
                        'user': {
                            'id': str(metric.user.id_user),
                            'username': metric.user.username,
                            'email': metric.user.email
                        },
                        'total_overdue_amount': float(metric.total_overdue_amount),
                        'overdue_credits_count': metric.overdue_credits_count,
                        'days_in_default': metric.days_in_default,
                        'risk_level': metric.risk_level,
                        'risk_score': float(metric.risk_score)
                    }
                    for metric in top_defaulters
                ],
                'alerts_by_priority': list(alerts_by_priority),
                'recovery_potential': {
                    'high': high_recovery,
                    'medium': medium_recovery,
                    'total_recoverable': high_recovery + medium_recovery
                }
            }
            
            return Response({
                'success': True,
                'data': insights
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# mtyht6-ub.myshopify.com
# 4bbe3fe6a5aea88f93919b1e33170ee1

# k6Kav~SPE$

# =============================================================================
# NUEVAS VISTAS DE DASHBOARD OPTIMIZADAS
# =============================================================================

from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Q, F, ExpressionWrapper, DecimalField
from django.db.models.functions import Coalesce, ExtractDay
from apps.insights.serializers.dashboard_serializers import (
    CreditDashboardSerializer,
    InstallmentCollectionSerializer,
    DashboardSummarySerializer
)
from apps.insights.utils.pagination import CustomPageNumberPagination
from apps.insights.utils.dashboard_helpers import (
    get_optimized_credit_queryset,
    get_optimized_installment_queryset,
    get_alerts,
    get_by_periodicity_metrics
)
from apps.insights.utils.calculations import (
    calculate_performance_metrics
)

class CreditDashboardViewSet(ReadOnlyModelViewSet):
    """ViewSet para dashboard de créditos con cálculos optimizados"""
    serializer_class = CreditDashboardSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna queryset optimizado para créditos"""
        queryset = get_optimized_credit_queryset()
        
        # Aplicar ordenamiento si se especifica
        ordering = self.request.query_params.get('ordering', '-created_at')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """Lista paginada de créditos con cálculos"""
        try:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InstallmentCollectionViewSet(ReadOnlyModelViewSet):
    """ViewSet para recaudo esperado con proyecciones"""
    serializer_class = InstallmentCollectionSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna queryset optimizado para cuotas"""
        queryset = get_optimized_installment_queryset()
        
        # Aplicar ordenamiento si se especifica
        ordering = self.request.query_params.get('ordering', 'due_date')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """Lista paginada de cuotas con información de recaudo"""
        try:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DashboardSummaryView(APIView):
    """Vista para métricas resumidas del dashboard"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Obtener métricas calculadas para el dashboard"""
        try:
            from apps.fintech.models import Credit, Installment
            
            # Calcular métricas de rendimiento
            performance_metrics = calculate_performance_metrics()
            
            # Obtener alertas
            alerts = get_alerts()
            
            # Obtener métricas por periodicidad
            by_periodicity = get_by_periodicity_metrics()
            
            # Calcular recaudo esperado
            expected_collection_today = Installment.objects.filter(
                due_date=timezone.now().date(),
                status='pending'
            ).aggregate(
                total=Coalesce(Sum('amount'), 0, output_field=DecimalField())
            )['total'] or 0
            
            expected_collection_week = Installment.objects.filter(
                due_date__range=[
                    timezone.now().date(),
                    timezone.now().date() + timedelta(days=7)
                ],
                status='pending'
            ).aggregate(
                total=Coalesce(Sum('amount'), 0, output_field=DecimalField())
            )['total'] or 0
            
            # Calcular tasa de mora
            total_credits = Credit.objects.filter(state='pending').count()
            defaulted_credits = Credit.objects.filter(
                state='pending',
                morosidad_level__in=['mild_default', 'moderate_default', 'severe_default', 'critical_default']
            ).count()
            
            default_rate = (defaulted_credits / total_credits * 100) if total_credits > 0 else 0
            
            # Calcular tasa de recuperación
            recovered_credits = Credit.objects.filter(
                state='completed'
            ).count()
            
            total_historical_credits = Credit.objects.count()
            recovery_rate = (recovered_credits / total_historical_credits * 100) if total_historical_credits > 0 else 0
            
            # Construir respuesta
            summary_data = {
                'credits_summary': {
                    'total_active_credits': performance_metrics['total_active_credits'],
                    'total_amount_lent': str(performance_metrics['total_amount_lent']),
                    'total_pending_amount': str(performance_metrics['total_pending_amount']),
                    'total_collected': str(performance_metrics['total_collected']),
                    'average_credit_amount': str(performance_metrics['average_credit_amount']),
                    'collection_percentage': performance_metrics['collection_percentage']
                },
                'installments_summary': {
                    'due_today': performance_metrics['due_today'],
                    'due_this_week': performance_metrics['due_this_week'],
                    'overdue_total': performance_metrics['overdue_total'],
                    'expected_collection_today': str(expected_collection_today),
                    'expected_collection_week': str(expected_collection_week)
                },
                'performance_metrics': {
                    'on_time_payment_rate': performance_metrics['on_time_payment_rate'],
                    'average_delay_days': performance_metrics['average_delay_days'],
                    'default_rate': round(default_rate, 1),
                    'recovery_rate': round(recovery_rate, 1)
                },
                'by_periodicity': by_periodicity,
                'alerts': alerts
            }
            
            serializer = DashboardSummarySerializer(summary_data)
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreditAnalyticsAdvancedView(APIView):
    """Vista para analytics avanzados de créditos"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Obtener analytics detallados de créditos con filtros y agrupaciones"""
        try:
            # Parámetros de consulta
            days = int(request.query_params.get('days', 30))
            periodicity_filter = request.query_params.get('periodicity')
            state_filter = request.query_params.get('state')
            
            # Queryset base
            queryset = get_optimized_credit_queryset()
            
            # Aplicar filtros
            if periodicity_filter:
                queryset = queryset.filter(periodicity__name=periodicity_filter)
            
            if state_filter:
                queryset = queryset.filter(state=state_filter)
            
            # Analytics por estado
            analytics_by_state = queryset.values('state').annotate(
                count=Count('id'),
                total_amount=Sum('price'),
                avg_amount=Avg('price'),
                total_pending=Sum('pending_amount')
            )
            
            # Analytics por periodicidad
            analytics_by_periodicity = queryset.values(
                'periodicity__name'
            ).annotate(
                count=Count('id'),
                total_amount=Sum('price'),
                avg_amount=Avg('price'),
                overdue_count=Count(
                    'id',
                    filter=Q(morosidad_level__in=['mild_default', 'moderate_default', 'severe_default', 'critical_default'])
                )
            )
            
            # Analytics por subcategoría
            analytics_by_subcategory = queryset.values(
                'subcategory__name'
            ).annotate(
                count=Count('id'),
                total_amount=Sum('price'),
                avg_amount=Avg('price')
            )
            
            # Tendencias temporales
            date_from = timezone.now() - timedelta(days=days)
            temporal_analytics = queryset.filter(
                created_at__gte=date_from
            ).extra(
                select={'day': 'date(created_at)'}
            ).values('day').annotate(
                count=Count('id'),
                total_amount=Sum('price')
            ).order_by('day')
            
            return Response({
                'success': True,
                'data': {
                    'analytics_by_state': list(analytics_by_state),
                    'analytics_by_periodicity': list(analytics_by_periodicity),
                    'analytics_by_subcategory': list(analytics_by_subcategory),
                    'temporal_analytics': list(temporal_analytics),
                    'filters_applied': {
                        'days': days,
                        'periodicity': periodicity_filter,
                        'state': state_filter
                    }
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RiskAnalysisAdvancedView(APIView):
    """Vista para análisis de riesgo"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        """Obtener análisis detallado de riesgo"""
        try:
            from apps.fintech.models import Credit, Installment
            
            # Análisis por nivel de morosidad
            risk_by_morosidad = Credit.objects.filter(
                state='pending'
            ).values('morosidad_level').annotate(
                count=Count('id'),
                total_amount=Sum('price'),
                total_pending=Sum('pending_amount'),
                avg_delay=Avg('installments__days_overdue')
            )
            
            # Créditos en alto riesgo
            high_risk_credits = Credit.objects.filter(
                state='pending',
                morosidad_level__in=['severe_default', 'critical_default']
            ).select_related('user', 'subcategory').prefetch_related('installments')[:50]
            
            # Análisis de cuotas vencidas
            overdue_analysis = Installment.objects.filter(
                status='overdue'
            ).values('credit__morosidad_level').annotate(
                count=Count('id'),
                total_amount=Sum('amount'),
                avg_days_overdue=Avg('days_overdue')
            )
            
            # Proyección de pérdidas
            potential_losses = Credit.objects.filter(
                state='pending',
                morosidad_level__in=['severe_default', 'critical_default']
            ).aggregate(
                total_potential_loss=Sum('pending_amount')
            )['total_potential_loss'] or 0
            
            return Response({
                'success': True,
                'data': {
                    'risk_by_morosidad': list(risk_by_morosidad),
                    'high_risk_credits_count': high_risk_credits.count(),
                    'overdue_analysis': list(overdue_analysis),
                    'potential_losses': str(potential_losses),
                    'risk_alerts': get_alerts()
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =============================================================================
# NUEVAS VISTAS PARA INSIGHTS POR CRÉDITO
# =============================================================================

class CreditInsightsView(APIView):
    """Vista para insights detallados de un crédito específico"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, credit_id):
        """
        Obtener insights detallados de un crédito específico
        
        Args:
            credit_id: UUID del crédito
            
        Returns:
            Insights detallados del crédito incluyendo:
            - Información básica
            - Análisis de pagos
            - Evaluación de riesgo
            - Métricas de rendimiento
            - Desglose de cuotas
            - Análisis temporal
            - Análisis comparativo
            - Recomendaciones
        """
        try:
            from apps.insights.services.credit_insights_service import CreditInsightsService
            from apps.insights.serializers.credit_insights_serializers import CreditInsightsResponseSerializer
            
            # Validar que el usuario tenga acceso al crédito
            from apps.fintech.models import Credit
            try:
                credit = Credit.objects.get(uid=credit_id)
                
                # Verificar permisos: el usuario debe ser el dueño del crédito o admin
                if not request.user.is_staff and credit.user != request.user:
                    return Response({
                        'success': False,
                        'error': 'No tienes permisos para acceder a este crédito'
                    }, status=status.HTTP_403_FORBIDDEN)
                    
            except Credit.DoesNotExist:
                return Response({
                    'success': False,
                    'error': 'Crédito no encontrado'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Obtener insights detallados
            insights_data = CreditInsightsService.get_credit_detailed_insights(credit_id)
            
            if not insights_data:
                return Response({
                    'success': False,
                    'error': 'No se pudieron generar los insights del crédito'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Validar respuesta con serializer
            response_data = {
                'success': True,
                'data': insights_data
            }
            
            serializer = CreditInsightsResponseSerializer(data=response_data)
            if serializer.is_valid():
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'error': 'Error en la validación de datos',
                    'details': serializer.errors
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.error(f"Error in CreditInsightsView: {e}")
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CreditPerformanceView(APIView):
    """Vista para métricas de rendimiento de créditos"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        """
        Obtener métricas de rendimiento de créditos
        
        Parámetros de consulta:
        - period: Período de análisis (7d, 30d, 90d, 1y)
        - metric_type: Tipo de métrica (collection, risk, performance)
        
        Returns:
            Métricas de rendimiento de créditos
        """
        try:
            from apps.fintech.models import Credit, Installment
            from django.db.models import Q, Count, Sum, Avg, Case, When, F, DecimalField
            from datetime import timedelta
            
            # Parámetros
            period = request.query_params.get('period', '30d')
            metric_type = request.query_params.get('metric_type', 'all')
            
            # Calcular fechas según el período
            now = timezone.now()
            if period == '7d':
                start_date = now - timedelta(days=7)
            elif period == '30d':
                start_date = now - timedelta(days=30)
            elif period == '90d':
                start_date = now - timedelta(days=90)
            elif period == '1y':
                start_date = now - timedelta(days=365)
            else:
                start_date = now - timedelta(days=30)
            
            # Base queryset
            credits = Credit.objects.filter(created_at__gte=start_date)
            
            metrics = {}
            
            # Métricas de recaudación
            if metric_type in ['all', 'collection']:
                collection_metrics = credits.aggregate(
                    total_credits=Count('id'),
                    total_amount=Sum('price'),
                    total_collected=Sum('total_abonos'),
                    avg_collection_rate=Avg(
                        Case(
                            When(price__gt=0, then=F('total_abonos') / F('price') * 100),
                            default=0,
                            output_field=DecimalField()
                        )
                    )
                )
                
                # Créditos por estado de recaudación
                collection_status = credits.annotate(
                    collection_rate=Case(
                        When(price__gt=0, then=F('total_abonos') / F('price') * 100),
                        default=0,
                        output_field=DecimalField()
                    )
                ).aggregate(
                    fully_collected=Count('id', filter=Q(collection_rate__gte=100)),
                    partially_collected=Count('id', filter=Q(collection_rate__gte=50, collection_rate__lt=100)),
                    low_collection=Count('id', filter=Q(collection_rate__lt=50))
                )
                
                metrics['collection'] = {
                    **collection_metrics,
                    'collection_status': collection_status
                }
            
            # Métricas de riesgo
            if metric_type in ['all', 'risk']:
                risk_metrics = credits.aggregate(
                    total_in_default=Count('id', filter=Q(is_in_default=True)),
                    default_rate=Count('id', filter=Q(is_in_default=True)) * 100.0 / Count('id'),
                    avg_days_in_default=Avg(
                        Case(
                            When(is_in_default=True, then=F('first_date_payment')),
                            default=None
                        )
                    )
                )
                
                # Distribución por nivel de morosidad
                morosidad_distribution = credits.values('morosidad_level').annotate(
                    count=Count('id'),
                    total_amount=Sum('price')
                )
                
                metrics['risk'] = {
                    **risk_metrics,
                    'morosidad_distribution': list(morosidad_distribution)
                }
            
            # Métricas de rendimiento
            if metric_type in ['all', 'performance']:
                performance_metrics = credits.aggregate(
                    avg_credit_amount=Avg('price'),
                    avg_credit_days=Avg('credit_days'),
                    avg_interest_rate=Avg('interest'),
                    total_earnings=Sum('earnings')
                )
                
                # ROI promedio
                roi_metrics = credits.filter(cost__gt=0).aggregate(
                    avg_roi=Avg(
                        Case(
                            When(cost__gt=0, then=F('earnings') / F('cost') * 100),
                            default=0,
                            output_field=DecimalField()
                        )
                    )
                )
                
                metrics['performance'] = {
                    **performance_metrics,
                    **roi_metrics
                }
            
            return Response({
                'success': True,
                'data': {
                    'period': period,
                    'start_date': start_date,
                    'end_date': now,
                    'metrics': metrics
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in CreditPerformanceView: {e}")
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreditsTableView(APIView):
    """Vista para tabla de créditos del dashboard de riesgo"""
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request):
        """
        Obtener tabla de créditos con datos estructurados para dashboard de riesgo
        
        Parámetros de consulta:
        - date_from: Fecha de inicio (YYYY-MM-DD)
        - date_to: Fecha de fin (YYYY-MM-DD)
        - page: Número de página (default: 1)
        - page_size: Tamaño de página (default: 20, máximo: 100)
        - state: Filtrar por estado del crédito
        - morosidad_level: Filtrar por nivel de morosidad
        - risk_level: Filtrar por nivel de riesgo
        - seller_id: Filtrar por vendedor específico
        - sort_by: Campo de ordenamiento (default: 'created_at')
        - sort_order: Orden (asc, desc, default: 'desc')
        """
        try:
            from apps.insights.services.credits_table_service import CreditsTableService
            from datetime import datetime
            
            # Validar parámetros requeridos
            date_from_str = request.query_params.get('date_from')
            date_to_str = request.query_params.get('date_to')
            
            if not date_from_str or not date_to_str:
                return Response({
                    'success': False,
                    'error': 'date_from y date_to son parámetros requeridos (formato: YYYY-MM-DD)'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Parsear fechas
            try:
                date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
                date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({
                    'success': False,
                    'error': 'Formato de fecha inválido. Use YYYY-MM-DD'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar que date_from <= date_to
            if date_from > date_to:
                return Response({
                    'success': False,
                    'error': 'date_from debe ser menor o igual a date_to'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Obtener parámetros de paginación
            try:
                page = int(request.query_params.get('page', 1))
                page_size = int(request.query_params.get('page_size', 20))
                
                if page < 1:
                    page = 1
                if page_size < 1:
                    page_size = 20
                if page_size > 100:
                    page_size = 100
                    
            except ValueError:
                return Response({
                    'success': False,
                    'error': 'page y page_size deben ser números enteros'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Obtener filtros
            filters = {
                'state': request.query_params.get('state'),
                'morosidad_level': request.query_params.get('morosidad_level'),
                'risk_level': request.query_params.get('risk_level'),
                'seller_id': request.query_params.get('seller_id'),
                'sort_by': request.query_params.get('sort_by', 'created_at'),
                'sort_order': request.query_params.get('sort_order', 'desc')
            }
            
            # Validar seller_id si se proporciona
            if filters['seller_id']:
                try:
                    filters['seller_id'] = int(filters['seller_id'])
                except ValueError:
                    return Response({
                        'success': False,
                        'error': 'seller_id debe ser un número entero'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar sort_order
            if filters['sort_order'] not in ['asc', 'desc']:
                filters['sort_order'] = 'desc'
            
            # Obtener datos de la tabla
            result = CreditsTableService.get_credits_table_data(
                date_from=date_from,
                date_to=date_to,
                page=page,
                page_size=page_size,
                filters=filters
            )
            
            if not result:
                return Response({
                    'success': False,
                    'error': 'No se pudieron obtener los datos de la tabla'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({
                'success': True,
                'data': result,
                'parameters': {
                    'date_from': date_from_str,
                    'date_to': date_to_str,
                    'page': page,
                    'page_size': page_size,
                    **filters
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in CreditsTableView: {e}")
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreditStatusListView(APIView):
    """
    Vista para listar el estado de créditos con filtros dinámicos
    y KPIs calculados en tiempo real sobre el mismo queryset filtrado.

    Query params:
        - date_from (str, YYYY-MM-DD): Fecha inicio del periodo.
        - date_to   (str, YYYY-MM-DD): Fecha fin del periodo.
        - seller    (int, opcional):    ID del vendedor (Seller.pk).
        - page      (int, default 1):  Página actual.
        - page_size (int, default 20): Registros por página (máx 100).
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            from apps.insights.services.credit_status_service import CreditStatusService
            from datetime import datetime, timedelta

            # ── Parseo de fechas ──────────────────────────────────
            date_from_str = request.query_params.get('date_from')
            date_to_str = request.query_params.get('date_to')

            # Defaults: últimos 30 días si no se proporcionan
            today = timezone.now().date()
            if not date_from_str:
                date_from = today - timedelta(days=30)
            else:
                try:
                    date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
                except ValueError:
                    return Response({
                        'success': False,
                        'error': 'Formato de date_from inválido. Use YYYY-MM-DD'
                    }, status=status.HTTP_400_BAD_REQUEST)

            if not date_to_str:
                date_to = today
            else:
                try:
                    date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
                except ValueError:
                    return Response({
                        'success': False,
                        'error': 'Formato de date_to inválido. Use YYYY-MM-DD'
                    }, status=status.HTTP_400_BAD_REQUEST)

            if date_from > date_to:
                return Response({
                    'success': False,
                    'error': 'date_from debe ser menor o igual a date_to'
                }, status=status.HTTP_400_BAD_REQUEST)

            # ── Seller (opcional) ─────────────────────────────────
            seller_id = None
            seller_raw = request.query_params.get('seller')
            if seller_raw:
                try:
                    seller_id = int(seller_raw)
                except ValueError:
                    return Response({
                        'success': False,
                        'error': 'seller debe ser un número entero (ID del vendedor)'
                    }, status=status.HTTP_400_BAD_REQUEST)

            # ── Paginación ────────────────────────────────────────
            try:
                page = max(1, int(request.query_params.get('page', 1)))
                page_size = min(100, max(1, int(request.query_params.get('page_size', 20))))
            except ValueError:
                return Response({
                    'success': False,
                    'error': 'page y page_size deben ser números enteros'
                }, status=status.HTTP_400_BAD_REQUEST)

            # ── Obtener datos ─────────────────────────────────────
            result = CreditStatusService.get_credit_status_data(
                date_from=date_from,
                date_to=date_to,
                seller_id=seller_id,
                page=page,
                page_size=page_size,
            )

            if not result:
                return Response({
                    'success': False,
                    'error': 'No se pudieron obtener los datos del estado de créditos'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                'success': True,
                'data': result,
                'filters_applied': {
                    'date_from': date_from.isoformat(),
                    'date_to': date_to.isoformat(),
                    'seller': seller_id,
                    'page': page,
                    'page_size': page_size,
                },
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error in CreditStatusListView: {e}")
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)