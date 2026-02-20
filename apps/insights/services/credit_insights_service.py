from django.db.models import Q, Count, Sum, Avg, Max, Min, F, Case, When, DecimalField
from django.db.models.functions import TruncDate, TruncMonth, Extract, Coalesce
from django.utils import timezone
from django.core.cache import cache
from datetime import timedelta, datetime, date
from decimal import Decimal
from typing import Dict, List, Optional, Any
import logging

from apps.fintech.models import Credit, Installment, Transaction, User, SubCategory, Periodicity
from apps.insights.models import FinancialControlMetrics

logger = logging.getLogger(__name__)

class CreditInsightsService:
    """Servicio para generar insights detallados por crédito individual"""
    
    CACHE_TIMEOUT = 60 * 15  # 15 minutos
    
    @staticmethod
    def get_credit_detailed_insights(credit_id: str) -> Dict[str, Any]:
        """
        Obtiene insights detallados para un crédito específico con caché
        """
        cache_key = f'credit_insights_{credit_id}'
        cached_data = cache.get(cache_key)
        if cached_data:
            cached_data['is_cached'] = True
            return cached_data

        try:
            credit = Credit.objects.select_related(
                'user', 'subcategory', 'periodicity', 'currency', 'payment'
            ).prefetch_related('installments', 'transactions').get(uid=credit_id)
            
            data = {
                'credit_basic_info': CreditInsightsService._get_credit_basic_info(credit),
                'payment_analysis': CreditInsightsService._get_payment_analysis(credit),
                'risk_assessment': CreditInsightsService._get_risk_assessment(credit),
                'performance_metrics': CreditInsightsService._get_performance_metrics(credit),
                'installment_breakdown': CreditInsightsService._get_installment_breakdown(credit),
                'timeline_analysis': CreditInsightsService._get_timeline_analysis(credit),
                'comparative_analysis': CreditInsightsService._get_comparative_analysis(credit),
                'recommendations': CreditInsightsService._get_credit_recommendations(credit),
                'timestamp': timezone.now().isoformat(),
                'is_cached': False
            }
            
            cache.set(cache_key, data, CreditInsightsService.CACHE_TIMEOUT)
            return data
            
        except Credit.DoesNotExist:
            logger.error(f"Credit with ID {credit_id} not found")
            return {}
        except Exception as e:
            logger.error(f"Error getting credit insights: {e}")
            return {}
    
    @staticmethod
    def _get_credit_basic_info(credit: Credit) -> Dict[str, Any]:
        """Información básica del crédito"""
        return {
            'uid': str(credit.uid),
            'user': {
                'id': credit.user.id_user,
                'username': credit.user.username,
                'email': credit.user.email
            },
            'subcategory': {
                'name': credit.subcategory.name if credit.subcategory else None,
                'category': credit.subcategory.category.name if credit.subcategory and credit.subcategory.category else None
            },
            'amounts': {
                'price': float(credit.price),
                'cost': float(credit.cost),
                'earnings': float(credit.earnings or 0),
                'pending_amount': float(credit.pending_amount or 0),
                'total_abonos': float(credit.total_abonos),
                'refinancing': float(credit.refinancing or 0)
            },
            'terms': {
                'credit_days': credit.credit_days,
                'interest_rate': float(credit.interest or 0),
                'installment_number': credit.installment_number,
                'installment_value': float(credit.installment_value or 0),
                'periodicity': credit.periodicity.name if credit.periodicity else None
            },
            'dates': {
                'created_at': credit.created_at,
                'first_date_payment': credit.first_date_payment,
                'second_date_payment': credit.second_date_payment,
                'updated_at': credit.updated_at
            },
            'status': {
                'state': credit.state,
                'is_in_default': credit.is_in_default,
                'morosidad_level': credit.morosidad_level
            }
        }
    
    @staticmethod
    def _get_payment_analysis(credit: Credit) -> Dict[str, Any]:
        """Análisis detallado de pagos"""
        installments = credit.installments.all()
        
        # Estadísticas de cuotas
        total_installments = installments.count()
        paid_installments = installments.filter(paid=True).count()
        overdue_installments = installments.filter(
            Q(paid=False) & Q(due_date__lt=timezone.now().date())
        ).count()
        pending_installments = installments.filter(paid=False).count()
        
        # Análisis de pagos puntuales vs tardíos
        on_time_payments = installments.filter(
            paid=True,
            paid_on__lte=F('due_date')
        ).count()
        
        late_payments = installments.filter(
            paid=True,
            paid_on__gt=F('due_date')
        ).count()
        
        # Promedio de días de retraso
        late_installments = installments.filter(
            paid=True,
            paid_on__gt=F('due_date')
        )
        
        avg_delay_days = 0
        if late_installments.exists():
            total_delay = sum([
                (installment.paid_on - installment.due_date).days 
                for installment in late_installments 
                if installment.paid_on and installment.due_date
            ])
            avg_delay_days = total_delay / late_installments.count()
        
        # Montos
        total_paid = installments.filter(paid=True).aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')
        
        total_pending = installments.filter(paid=False).aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')
        
        return {
            'installment_summary': {
                'total_installments': total_installments,
                'paid_installments': paid_installments,
                'overdue_installments': overdue_installments,
                'pending_installments': pending_installments,
                'payment_rate': (paid_installments / total_installments * 100) if total_installments > 0 else 0
            },
            'payment_behavior': {
                'on_time_payments': on_time_payments,
                'late_payments': late_payments,
                'punctuality_rate': (on_time_payments / paid_installments * 100) if paid_installments > 0 else 0,
                'avg_delay_days': round(avg_delay_days, 2)
            },
            'amounts': {
                'total_paid': float(total_paid),
                'total_pending': float(total_pending),
                'payment_progress': float((total_paid / (total_paid + total_pending) * 100)) if (total_paid + total_pending) > 0 else 0
            }
        }
    
    @staticmethod
    def _get_risk_assessment(credit: Credit) -> Dict[str, Any]:
        """Evaluación de riesgo del crédito"""
        installments = credit.installments.all()
        
        # Días en mora
        days_in_default = 0
        if credit.is_in_default and credit.first_date_payment:
            days_in_default = (timezone.now().date() - credit.first_date_payment).days
        
        # Cuotas vencidas
        overdue_installments = installments.filter(
            Q(paid=False) & Q(due_date__lt=timezone.now().date())
        )
        
        overdue_amount = overdue_installments.aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')
        
        # Historial de morosidad
        morosidad_history = installments.filter(
            paid=True,
            paid_on__gt=F('due_date')
        ).count()
        
        # Score de riesgo (0-100, donde 100 es máximo riesgo)
        risk_score = CreditInsightsService._calculate_credit_risk_score(
            credit, days_in_default, overdue_installments.count(), morosidad_history
        )
        
        return {
            'risk_score': risk_score,
            'risk_level': CreditInsightsService._get_risk_level(risk_score),
            'days_in_default': days_in_default,
            'overdue_installments_count': overdue_installments.count(),
            'overdue_amount': float(overdue_amount),
            'morosidad_history': morosidad_history,
            'risk_factors': CreditInsightsService._identify_risk_factors(credit, risk_score)
        }
    
    @staticmethod
    def _get_performance_metrics(credit: Credit) -> Dict[str, Any]:
        """Métricas de rendimiento del crédito"""
        installments = credit.installments.all()
        
        # ROI del crédito
        roi = 0
        if credit.cost > 0:
            roi = ((credit.earnings or 0) / credit.cost) * 100
        
        # Tiempo promedio entre pagos
        paid_installments = installments.filter(paid=True).order_by('paid_on')
        avg_payment_interval = 0
        
        if paid_installments.count() > 1:
            intervals = []
            for i in range(1, len(paid_installments)):
                prev_payment = paid_installments[i-1].paid_on
                curr_payment = paid_installments[i].paid_on
                if prev_payment and curr_payment:
                    intervals.append((curr_payment - prev_payment).days)
            
            if intervals:
                avg_payment_interval = sum(intervals) / len(intervals)
        
        # Eficiencia de cobro
        expected_payments = credit.installment_number or 0
        actual_payments = installments.filter(paid=True).count()
        collection_efficiency = (actual_payments / expected_payments * 100) if expected_payments > 0 else 0
        
        return {
            'roi': round(roi, 2),
            'collection_efficiency': round(collection_efficiency, 2),
            'avg_payment_interval_days': round(avg_payment_interval, 2),
            'expected_vs_actual_payments': {
                'expected': expected_payments,
                'actual': actual_payments,
                'variance': actual_payments - expected_payments
            }
        }
    
    @staticmethod
    def _get_installment_breakdown(credit: Credit) -> List[Dict[str, Any]]:
        """Desglose detallado de cuotas"""
        installments = credit.installments.all().order_by('number')
        
        breakdown = []
        for installment in installments:
            days_overdue = 0
            if not installment.paid and installment.due_date:
                days_overdue = max(0, (timezone.now().date() - installment.due_date).days)
            
            breakdown.append({
                'number': installment.number,
                'due_date': installment.due_date,
                'amount': float(installment.amount or 0),
                'paid': installment.paid,
                'paid_on': installment.paid_on,
                'status': installment.status,
                'days_overdue': days_overdue,
                'principal_amount': float(installment.principal_amount or 0),
                'interest_amount': float(installment.interest_amount or 0),
                'late_fee': float(installment.late_fee or 0),
                'amount_paid': float(installment.amount_paid or 0)
            })
        
        return breakdown
    
    @staticmethod
    def _get_timeline_analysis(credit: Credit) -> Dict[str, Any]:
        """Análisis temporal del crédito"""
        installments = credit.installments.all().order_by('due_date')
        
        # Progreso temporal
        total_days = 0
        if credit.second_date_payment and credit.first_date_payment:
            total_days = (credit.second_date_payment - credit.first_date_payment).days
        
        elapsed_days = 0
        if credit.first_date_payment:
            elapsed_days = (timezone.now().date() - credit.first_date_payment).days
            
        progress_percentage = min(100, (elapsed_days / total_days * 100)) if total_days > 0 else 0
        
        # Tendencias de pago por mes
        monthly_payments = installments.filter(paid=True).extra(
            select={'month': "DATE_TRUNC('month', paid_on)"}
        ).values('month').annotate(
            count=Count('id'),
            total_amount=Sum('amount')
        ).order_by('month')
        
        return {
            'credit_lifecycle': {
                'total_days': total_days,
                'elapsed_days': elapsed_days,
                'progress_percentage': round(progress_percentage, 2),
                'remaining_days': max(0, total_days - elapsed_days)
            },
            'monthly_payment_trends': list(monthly_payments)
        }
    
    @staticmethod
    def _get_comparative_analysis(credit: Credit) -> Dict[str, Any]:
        """Análisis comparativo usando métricas del usuario y de la categoría"""
        # Métricas individuales del usuario pre-calculadas
        user_metrics = FinancialControlMetrics.objects.filter(user=credit.user).first()
        
        # Créditos de la misma subcategoría
        category_credits = Credit.objects.filter(
            subcategory=credit.subcategory
        ).exclude(uid=credit.uid) if credit.subcategory else Credit.objects.none()
        
        user_comparison = {}
        if user_metrics:
            current_payment_rate = (credit.total_abonos / credit.price * 100) if credit.price > 0 else 0
            user_comparison = {
                'user_avg_risk_score': float(user_metrics.risk_score),
                'user_total_overdue': float(user_metrics.total_overdue_amount),
                'current_payment_rate': float(current_payment_rate),
                'risk_level': user_metrics.risk_level
            }
        
        # Comparación con créditos de la categoría
        category_comparison = {}
        if category_credits.exists():
            avg_stats = category_credits.aggregate(
                avg_price=Avg('price'),
                avg_pending=Avg('pending_amount'),
                default_count=Count('id', filter=Q(is_in_default=True)),
                total_count=Count('id')
            )
            
            category_avg_default_rate = (avg_stats['default_count'] / avg_stats['total_count'] * 100) if avg_stats['total_count'] > 0 else 0
            
            category_comparison = {
                'category_avg_default_rate': round(category_avg_default_rate, 2),
                'category_avg_price': float(avg_stats['avg_price'] or 0),
                'current_is_in_default': credit.is_in_default,
                'performance_vs_category': 'better' if not credit.is_in_default and category_avg_default_rate > 10 else 'worse'
            }
        
        return {
            'user_comparison': user_comparison,
            'category_comparison': category_comparison
        }
    
    @staticmethod
    def _get_credit_recommendations(credit: Credit) -> List[Dict[str, Any]]:
        """Recomendaciones específicas para el crédito"""
        recommendations = []
        
        # Recomendaciones basadas en morosidad
        if credit.is_in_default:
            recommendations.append({
                'type': 'urgent',
                'title': 'Acción inmediata requerida',
                'description': 'El crédito está en mora. Se recomienda contactar al cliente inmediatamente.',
                'action': 'contact_client'
            })
        
        # Recomendaciones basadas en cuotas vencidas
        overdue_installments = credit.installments.filter(
            Q(paid=False) & Q(due_date__lt=timezone.now().date())
        )
        
        if overdue_installments.count() > 2:
            recommendations.append({
                'type': 'high',
                'title': 'Múltiples cuotas vencidas',
                'description': f'{overdue_installments.count()} cuotas vencidas. Evaluar plan de pagos.',
                'action': 'payment_plan'
            })
        
        # Recomendaciones basadas en historial de pagos
        late_payments = credit.installments.filter(
            paid=True,
            paid_on__gt=F('due_date')
        ).count()
        
        if late_payments > 0:
            recommendations.append({
                'type': 'medium',
                'title': 'Historial de pagos tardíos',
                'description': f'{late_payments} pagos tardíos detectados. Monitorear de cerca.',
                'action': 'monitor'
            })
        
        # Recomendaciones positivas
        if not credit.is_in_default and credit.total_abonos > 0:
            payment_rate = (credit.total_abonos / credit.price * 100) if credit.price > 0 else 0
            if payment_rate > 80:
                recommendations.append({
                    'type': 'positive',
                    'title': 'Excelente cumplimiento',
                    'description': 'Cliente con excelente historial de pagos. Considerar para futuros créditos.',
                    'action': 'reward'
                })
        
        return recommendations
    
    @staticmethod
    def _calculate_credit_risk_score(credit: Credit, days_in_default: int, overdue_count: int, late_payment_history: int) -> int:
        """Calcula el score de riesgo del crédito (0-100)"""
        score = 0
        
        # Días en mora (0-40 puntos)
        if days_in_default > 0:
            score += min(40, days_in_default * 2)
        
        # Cuotas vencidas (0-30 puntos)
        score += min(30, overdue_count * 5)
        
        # Historial de pagos tardíos (0-20 puntos)
        score += min(20, late_payment_history * 3)
        
        # Nivel de morosidad (0-10 puntos)
        morosidad_scores = {
            'on_time': 0,
            'mild_default': 2,
            'moderate_default': 5,
            'severe_default': 8,
            'recurrent_default': 10,
            'critical_default': 10
        }
        score += morosidad_scores.get(credit.morosidad_level, 0)
        
        return min(100, score)
    
    @staticmethod
    def _get_risk_level(risk_score: int) -> str:
        """Determina el nivel de riesgo basado en el score"""
        if risk_score <= 20:
            return 'low'
        elif risk_score <= 50:
            return 'medium'
        elif risk_score <= 80:
            return 'high'
        else:
            return 'critical'
    
    @staticmethod
    def _identify_risk_factors(credit: Credit, risk_score: int) -> List[str]:
        """Identifica los factores de riesgo específicos"""
        factors = []
        
        if credit.is_in_default:
            factors.append('Crédito en mora')
        
        if credit.morosidad_level != 'on_time':
            factors.append(f'Nivel de morosidad: {credit.morosidad_level}')
        
        overdue_installments = credit.installments.filter(
            Q(paid=False) & Q(due_date__lt=timezone.now().date())
        )
        
        if overdue_installments.exists():
            factors.append(f'{overdue_installments.count()} cuotas vencidas')
        
        late_payments = credit.installments.filter(
            paid=True,
            paid_on__gt=F('due_date')
        ).count()
        
        if late_payments > 0:
            factors.append(f'{late_payments} pagos tardíos en historial')
        
        if risk_score > 80:
            factors.append('Score de riesgo crítico')
        
        return factors
    
    @staticmethod
    def get_credits_comparative_analysis(filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Análisis comparativo de múltiples créditos con caché
        """
        import hashlib
        import json
        
        # Generar una clave de caché basada en los filtros
        filters_str = json.dumps(filters or {}, sort_keys=True)
        filters_hash = hashlib.md5(filters_str.encode()).hexdigest()
        cache_key = f'credits_comparative_{filters_hash}'
        
        cached_data = cache.get(cache_key)
        if cached_data:
            cached_data['is_cached'] = True
            return cached_data

        try:
            queryset = Credit.objects.select_related('user', 'subcategory', 'periodicity')
            
            # Aplicar filtros
            if filters:
                if filters.get('start_date'):
                    queryset = queryset.filter(created_at__gte=filters['start_date'])
                if filters.get('end_date'):
                    queryset = queryset.filter(created_at__lte=filters['end_date'])
                if filters.get('subcategory_id'):
                    queryset = queryset.filter(subcategory_id=filters['subcategory_id'])
                if filters.get('user_id'):
                    queryset = queryset.filter(user_id=filters['user_id'])
            
            # Métricas generales
            total_credits = queryset.count()
            total_amount = queryset.aggregate(total=Sum('price'))['total'] or Decimal('0.00')
            total_pending = queryset.aggregate(total=Sum('pending_amount'))['total'] or Decimal('0.00')
            default_rate = (queryset.filter(is_in_default=True).count() / total_credits * 100) if total_credits > 0 else 0
            
            # Análisis por categoría
            category_analysis = queryset.values('subcategory__name').annotate(
                count=Count('id'),
                total_amount=Sum('price'),
                default_count=Count('id', filter=Q(is_in_default=True)),
                avg_amount=Avg('price')
            ).order_by('-total_amount')
            
            # Análisis por estado
            state_analysis = queryset.values('state').annotate(
                count=Count('id'),
                total_amount=Sum('price')
            )
            
            # Análisis por nivel de morosidad
            morosidad_analysis = queryset.values('morosidad_level').annotate(
                count=Count('id'),
                total_amount=Sum('price')
            )
            
            # Top créditos por monto
            top_credits = queryset.order_by('-price')[:10].values(
                'uid', 'user__username', 'subcategory__name', 'price', 'pending_amount', 'is_in_default'
            )
            
            data = {
                'summary': {
                    'total_credits': total_credits,
                    'total_amount': float(total_amount),
                    'total_pending': float(total_pending),
                    'default_rate': round(default_rate, 2),
                    'collection_rate': round((1 - (total_pending / total_amount)) * 100, 2) if total_amount > 0 else 0
                },
                'category_analysis': list(category_analysis),
                'state_analysis': list(state_analysis),
                'morosidad_analysis': list(morosidad_analysis),
                'top_credits': list(top_credits),
                'timestamp': timezone.now().isoformat(),
                'is_cached': False
            }
            
            cache.set(cache_key, data, CreditInsightsService.CACHE_TIMEOUT)
            return data
            
        except Exception as e:
            logger.error(f"Error in comparative analysis: {e}")
            return {}
