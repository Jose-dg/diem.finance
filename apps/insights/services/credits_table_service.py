from django.db.models import Q, Count, Sum, Avg, Max, Min, F, Case, When, DecimalField
from django.db.models.functions import Coalesce, Extract, TruncDate
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Any
import logging

from apps.fintech.models import Credit, User, Installment, Transaction, AccountMethodAmount
from apps.insights.models import FinancialControlMetrics

logger = logging.getLogger(__name__)

class CreditsTableService:
    """Servicio para obtener datos de la tabla de créditos del dashboard de riesgo"""
    
    @staticmethod
    def get_credits_table_data(date_from: date, date_to: date, page: int = 1, 
                             page_size: int = 20, filters: Dict = None) -> Dict[str, Any]:
        """
        Obtiene datos estructurados para la tabla de créditos
        
        Args:
            date_from: Fecha de inicio del período
            date_to: Fecha de fin del período
            page: Número de página
            page_size: Tamaño de página
            filters: Filtros aplicados
            
        Returns:
            Dict con datos de créditos, resumen y paginación
        """
        try:
            if filters is None:
                filters = {}
            
            # Obtener queryset base con optimizaciones
            queryset = CreditsTableService._get_optimized_queryset()
            
            # Aplicar filtros de fecha
            queryset = queryset.filter(
                created_at__date__range=[date_from, date_to]
            )
            
            # Aplicar filtros adicionales
            queryset = CreditsTableService._apply_filters(queryset, filters)
            
            # Aplicar ordenamiento
            queryset = CreditsTableService._apply_ordering(queryset, filters)
            
            # Obtener total count antes de paginación
            total_count = queryset.count()
            
            # Aplicar paginación
            paginator = Paginator(queryset, page_size)
            page_obj = paginator.get_page(page)
            
            # Procesar créditos de la página actual
            credits_data = []
            for credit in page_obj:
                credit_data = CreditsTableService._process_credit_data(credit)
                credits_data.append(credit_data)
            
            # Obtener métricas agregadas
            summary = CreditsTableService._get_summary_metrics(queryset)
            
            # Obtener distribuciones
            distributions = CreditsTableService._get_distributions(queryset)
            
            return {
                'credits': credits_data,
                'summary': summary,
                'distributions': distributions,
                'pagination': {
                    'current_page': page,
                    'total_pages': paginator.num_pages,
                    'total_count': total_count,
                    'page_size': page_size,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
                    'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting credits table data: {e}")
            return {}
    
    @staticmethod
    def _get_optimized_queryset():
        """Obtiene queryset optimizado con select_related y prefetch_related"""
        return Credit.objects.select_related(
            'user', 'subcategory', 'periodicity', 'currency', 'payment'
        ).prefetch_related(
            'installments'
        )
    
    @staticmethod
    def _apply_filters(queryset, filters: Dict):
        """Aplica filtros al queryset"""
        if filters.get('state'):
            queryset = queryset.filter(state=filters['state'])
        
        if filters.get('morosidad_level'):
            queryset = queryset.filter(morosidad_level=filters['morosidad_level'])
        
        if filters.get('risk_level'):
            # Filtrar por nivel de riesgo calculado
            queryset = CreditsTableService._filter_by_risk_level(queryset, filters['risk_level'])
        
        if filters.get('seller_id'):
            queryset = queryset.filter(registered_by_id=filters['seller_id'])
        
        return queryset
    
    @staticmethod
    def _filter_by_risk_level(queryset, risk_level: str):
        """Filtra créditos por nivel de riesgo calculado"""
        if risk_level == 'low':
            return queryset.filter(
                Q(morosidad_level__in=['', 'no_default']) |
                Q(morosidad_level='mild_default', total_abonos__gt=0)
            )
        elif risk_level == 'medium':
            return queryset.filter(
                Q(morosidad_level='moderate_default') |
                Q(morosidad_level='mild_default', total_abonos=0)
            )
        elif risk_level == 'high':
            return queryset.filter(
                morosidad_level__in=['severe_default', 'critical_default', 'recurrent_default']
            )
        
        return queryset
    
    @staticmethod
    def _apply_ordering(queryset, filters: Dict):
        """Aplica ordenamiento al queryset"""
        sort_by = filters.get('sort_by', 'created_at')
        sort_order = filters.get('sort_order', 'desc')
        
        # Campos válidos para ordenamiento
        valid_sort_fields = [
            'created_at', 'updated_at', 'price', 'pending_amount', 
            'total_abonos', 'first_date_payment', 'credit_days'
        ]
        
        if sort_by not in valid_sort_fields:
            sort_by = 'created_at'
        
        # Aplicar ordenamiento
        if sort_order == 'asc':
            return queryset.order_by(sort_by)
        else:
            return queryset.order_by(f'-{sort_by}')
    
    @staticmethod
    def _process_credit_data(credit: Credit) -> Dict[str, Any]:
        """Procesa datos de un crédito individual"""
        try:
            # Calcular métricas básicas
            percentage_paid = 0
            if credit.price and credit.price > 0:
                percentage_paid = (credit.total_abonos / credit.price) * 100
            
            # Calcular días desde creación
            days_since_creation = (timezone.now().date() - credit.created_at.date()).days
            
            # Calcular días hasta completar
            days_until_completion = 0
            if credit.credit_days:
                days_until_completion = max(0, credit.credit_days - days_since_creation)
            
            # Obtener información de cuotas
            installments_info = CreditsTableService._get_installments_info(credit)
            
            # Calcular puntuación de riesgo
            risk_score = CreditsTableService._calculate_risk_score(credit)
            
            # Determinar nivel de riesgo
            risk_level = CreditsTableService._determine_risk_level(risk_score, credit)
            
            # Calcular puntuación de rentabilidad
            profitability_score = CreditsTableService._calculate_profitability_score(credit)
            
            # Determinar prioridad de recaudo
            collection_priority = CreditsTableService._determine_collection_priority(credit, risk_score)
            
            return {
                # Información básica del crédito
                'uid': str(credit.uid),
                'state': credit.state,
                'created_at': credit.created_at.isoformat(),
                'updated_at': credit.updated_at.isoformat(),
                'description': credit.description or '',
                
                # Información del usuario
                'user_id': credit.user.id,
                'user_full_name': f"{credit.user.first_name} {credit.user.last_name}".strip() or credit.user.username,
                'user_username': credit.user.username,
                'user_email': credit.user.email,
                
                # Información del vendedor
                'seller_id': credit.registered_by.id if credit.registered_by else None,
                'seller_name': f"{credit.registered_by.first_name} {credit.registered_by.last_name}".strip() if credit.registered_by else None,
                'registered_by_id': credit.registered_by.id if credit.registered_by else None,
                
                # Información financiera
                'cost': float(credit.cost) if credit.cost else 0.0,
                'price': float(credit.price) if credit.price else 0.0,
                'earnings': float(credit.earnings) if credit.earnings else 0.0,
                'interest': float(credit.interest) if credit.interest else 0.0,
                'currency': credit.currency.currency if credit.currency else 'COP',
                'total_abonos': float(credit.total_abonos) if credit.total_abonos else 0.0,
                'pending_amount': float(credit.pending_amount) if credit.pending_amount else 0.0,
                'percentage_paid': round(percentage_paid, 2),
                'installment_number': credit.installment_number or 0,
                'installment_value': float(credit.installment_value) if credit.installment_value else 0.0,
                
                # Información de fechas
                'first_date_payment': credit.first_date_payment.isoformat() if credit.first_date_payment else None,
                'second_date_payment': credit.second_date_payment.isoformat() if credit.second_date_payment else None,
                'credit_days': credit.credit_days or 0,
                'credit_days_calculated': credit.credit_days_calculated or 0,
                'next_due_date': CreditsTableService._get_next_due_date(credit),
                'expected_completion_date': CreditsTableService._get_expected_completion_date(credit),
                'days_since_creation': days_since_creation,
                'days_until_completion': days_until_completion,
                
                # Información de cuotas
                'total_installments_count': installments_info['total_count'],
                'paid_installments_count': installments_info['paid_count'],
                'overdue_installments_count': installments_info['overdue_count'],
                'average_payment_delay': installments_info['avg_delay'],
                
                # Información de riesgo
                'morosidad_level': credit.morosidad_level or 'no_default',
                'risk_score': risk_score,
                'is_high_risk': risk_level == 'high',
                'is_performing_well': percentage_paid >= 80 and risk_level == 'low',
                'collection_priority': collection_priority,
                'profitability_score': profitability_score,
                
                # Información de categorización
                'subcategory_id': credit.subcategory.id if credit.subcategory else None,
                'subcategory_name': credit.subcategory.name if credit.subcategory else None,
                'periodicity_id': credit.periodicity.id if credit.periodicity else None,
                'periodicity_name': credit.periodicity.name if credit.periodicity else None,
                'periodicity_days': credit.periodicity.days if credit.periodicity else 0
            }
            
        except Exception as e:
            logger.error(f"Error processing credit data for {credit.uid}: {e}")
            return {}
    
    @staticmethod
    def _get_installments_info(credit: Credit) -> Dict[str, Any]:
        """Obtiene información de cuotas del crédito"""
        try:
            installments = credit.installments.all()
            
            total_count = installments.count()
            paid_count = installments.filter(status='paid').count()
            overdue_count = installments.filter(status='overdue').count()
            
            # Calcular promedio de días de retraso
            avg_delay = 0
            if overdue_count > 0:
                overdue_installments = installments.filter(status='overdue')
                total_delay = sum(inst.days_overdue or 0 for inst in overdue_installments)
                avg_delay = total_delay / overdue_count if overdue_count > 0 else 0
            
            return {
                'total_count': total_count,
                'paid_count': paid_count,
                'overdue_count': overdue_count,
                'avg_delay': round(avg_delay, 1)
            }
            
        except Exception as e:
            logger.error(f"Error getting installments info: {e}")
            return {
                'total_count': 0,
                'paid_count': 0,
                'overdue_count': 0,
                'avg_delay': 0
            }
    
    @staticmethod
    def _calculate_risk_score(credit: Credit) -> int:
        """Calcula puntuación de riesgo (0-100)"""
        try:
            score = 0
            
            # Factor por nivel de morosidad
            morosidad_scores = {
                'no_default': 0,
                'mild_default': 25,
                'moderate_default': 50,
                'severe_default': 75,
                'critical_default': 90,
                'recurrent_default': 95
            }
            score += morosidad_scores.get(credit.morosidad_level, 0)
            
            # Factor por porcentaje de pago
            if credit.price and credit.price > 0:
                payment_percentage = (credit.total_abonos / credit.price) * 100
                if payment_percentage < 25:
                    score += 30
                elif payment_percentage < 50:
                    score += 20
                elif payment_percentage < 75:
                    score += 10
            
            # Factor por días de retraso
            if credit.first_date_payment:
                days_overdue = (timezone.now().date() - credit.first_date_payment).days
                if days_overdue > 60:
                    score += 20
                elif days_overdue > 30:
                    score += 15
                elif days_overdue > 15:
                    score += 10
            
            return min(score, 100)
            
        except Exception as e:
            logger.error(f"Error calculating risk score: {e}")
            return 0
    
    @staticmethod
    def _determine_risk_level(risk_score: int, credit: Credit) -> str:
        """Determina nivel de riesgo basado en puntuación y otros factores"""
        if risk_score >= 70:
            return 'high'
        elif risk_score >= 40:
            return 'medium'
        else:
            return 'low'
    
    @staticmethod
    def _calculate_profitability_score(credit: Credit) -> float:
        """Calcula puntuación de rentabilidad"""
        try:
            if not credit.cost or credit.cost <= 0:
                return 0.0
            
            # Calcular ROI
            roi = float(credit.earnings / credit.cost * 100) if credit.earnings else 0
            
            # Ajustar por riesgo
            risk_adjustment = 1.0
            if credit.morosidad_level in ['severe_default', 'critical_default']:
                risk_adjustment = 0.5
            elif credit.morosidad_level in ['moderate_default', 'recurrent_default']:
                risk_adjustment = 0.7
            elif credit.morosidad_level == 'mild_default':
                risk_adjustment = 0.9
            
            return round(roi * risk_adjustment, 1)
            
        except Exception as e:
            logger.error(f"Error calculating profitability score: {e}")
            return 0.0
    
    @staticmethod
    def _determine_collection_priority(credit: Credit, risk_score: int) -> str:
        """Determina prioridad de recaudo"""
        if risk_score >= 80 or credit.morosidad_level in ['critical_default', 'recurrent_default']:
            return 'critical'
        elif risk_score >= 60 or credit.morosidad_level in ['severe_default']:
            return 'high'
        elif risk_score >= 40 or credit.morosidad_level in ['moderate_default']:
            return 'medium'
        else:
            return 'low'
    
    @staticmethod
    def _get_next_due_date(credit: Credit) -> Optional[str]:
        """Obtiene próxima fecha de vencimiento"""
        try:
            next_installment = credit.installments.filter(
                status='pending'
            ).order_by('due_date').first()
            
            if next_installment:
                return next_installment.due_date.isoformat()
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting next due date: {e}")
            return None
    
    @staticmethod
    def _get_expected_completion_date(credit: Credit) -> Optional[str]:
        """Obtiene fecha esperada de completación"""
        try:
            if credit.first_date_payment and credit.credit_days:
                expected_date = credit.first_date_payment + timedelta(days=credit.credit_days)
                return expected_date.isoformat()
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting expected completion date: {e}")
            return None
    
    @staticmethod
    def _get_summary_metrics(queryset) -> Dict[str, Any]:
        """Obtiene métricas agregadas del queryset"""
        try:
            # Métricas básicas
            total_credits = queryset.count()
            
            # Agregaciones financieras
            financial_metrics = queryset.aggregate(
                total_amount=Coalesce(Sum('price'), 0, output_field=DecimalField()),
                total_pending=Coalesce(Sum('pending_amount'), 0, output_field=DecimalField()),
                total_paid=Coalesce(Sum('total_abonos'), 0, output_field=DecimalField()),
                avg_risk_score=Avg('id')  # Placeholder, se calculará después
            )
            
            # Calcular puntuación promedio de riesgo
            risk_scores = []
            high_risk_count = 0
            
            for credit in queryset:
                risk_score = CreditsTableService._calculate_risk_score(credit)
                risk_scores.append(risk_score)
                if risk_score >= 70:
                    high_risk_count += 1
            
            avg_risk_score = sum(risk_scores) / len(risk_scores) if risk_scores else 0
            
            # Calcular tasa de morosidad
            defaulted_credits = queryset.filter(
                Q(is_in_default=True) | 
                Q(morosidad_level__in=['mild_default', 'moderate_default', 'severe_default', 'critical_default', 'recurrent_default'])
            ).count()
            
            default_rate = (defaulted_credits / total_credits * 100) if total_credits > 0 else 0
            
            return {
                'total_credits': total_credits,
                'total_amount': float(financial_metrics['total_amount']),
                'total_pending': float(financial_metrics['total_pending']),
                'total_paid': float(financial_metrics['total_paid']),
                'average_risk_score': round(avg_risk_score, 1),
                'high_risk_credits_count': high_risk_count,
                'default_rate': round(default_rate, 1)
            }
            
        except Exception as e:
            logger.error(f"Error getting summary metrics: {e}")
            return {}
    
    @staticmethod
    def _get_distributions(queryset) -> Dict[str, Any]:
        """Obtiene distribuciones por diferentes categorías"""
        try:
            # Distribución por estado
            credits_by_state = queryset.values('state').annotate(
                count=Count('id')
            ).order_by('-count')
            
            # Distribución por nivel de morosidad
            credits_by_morosidad_level = queryset.values('morosidad_level').annotate(
                count=Count('id')
            ).order_by('-count')
            
            # Distribución por nivel de riesgo (calculado)
            risk_distribution = {'low': 0, 'medium': 0, 'high': 0}
            for credit in queryset:
                risk_score = CreditsTableService._calculate_risk_score(credit)
                risk_level = CreditsTableService._determine_risk_level(risk_score, credit)
                risk_distribution[risk_level] += 1
            
            # Distribución por vendedor (para filtros en frontend)
            # Agrupamos por ID y nombre del vendedor
            from django.db.models.functions import Concat
            from django.db.models import Value, CharField
            
            credits_by_seller = queryset.values(
                'registered_by__id',
                'registered_by__first_name', 
                'registered_by__last_name',
                'registered_by__username'
            ).annotate(
                count=Count('id')
            ).order_by('-count')
            
            # Formatear la respuesta de vendedores
            sellers_data = []
            for item in credits_by_seller:
                if item['registered_by__id']:
                    first_name = item['registered_by__first_name'] or ''
                    last_name = item['registered_by__last_name'] or ''
                    full_name = f"{first_name} {last_name}".strip()
                    
                    if not full_name:
                        full_name = item['registered_by__username'] or f"User {item['registered_by__id']}"
                        
                    sellers_data.append({
                        'id': item['registered_by__id'],
                        'name': full_name,
                        'count': item['count']
                    })
            
            return {
                'credits_by_state': list(credits_by_state),
                'credits_by_morosidad_level': list(credits_by_morosidad_level),
                'credits_by_risk_level': [
                    {'risk_level': level, 'count': count} 
                    for level, count in risk_distribution.items()
                ],
                'credits_by_seller': sellers_data
            }
            
        except Exception as e:
            logger.error(f"Error getting distributions: {e}")
            return {}
