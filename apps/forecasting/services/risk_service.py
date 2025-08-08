from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import logging
from datetime import timedelta, date
from typing import Dict, List, Optional, Tuple

from apps.fintech.models import Credit, Transaction, AccountMethodAmount, User
from apps.revenue.models import CreditEarnings
from ..models import RiskAssessment

logger = logging.getLogger(__name__)

class RiskService:
    """
    Servicio para evaluación de riesgos en créditos y carteras.
    """
    
    @staticmethod
    def assess_credit_default_risk(credit: Credit) -> RiskAssessment:
        """
        Evalúa el riesgo de impago de un crédito específico.
        """
        try:
            with transaction.atomic():
                # Calcular factores de riesgo
                risk_factors = {}
                risk_score = Decimal('0.00')
                
                # Factor 1: Mora actual
                if credit.morosidad_level > 0:
                    mora_risk = min(credit.morosidad_level * 25, 60)
                    risk_score += Decimal(str(mora_risk))
                    risk_factors['mora_actual'] = {
                        'value': credit.morosidad_level,
                        'weight': mora_risk,
                        'description': _('Nivel de mora actual del crédito')
                    }
                
                # Factor 2: Porcentaje de pago
                if credit.price > 0:
                    payment_percentage = (credit.total_abonos / credit.price) * 100
                    if payment_percentage < 25:
                        risk_score += Decimal('30.00')
                        risk_factors['bajo_pago'] = {
                            'value': payment_percentage,
                            'weight': 30,
                            'description': _('Porcentaje de pago muy bajo')
                        }
                    elif payment_percentage < 50:
                        risk_score += Decimal('15.00')
                        risk_factors['pago_medio'] = {
                            'value': payment_percentage,
                            'weight': 15,
                            'description': _('Porcentaje de pago medio')
                        }
                
                # Factor 3: Días de crédito vs días transcurridos
                if credit.credit_days > 0:
                    days_elapsed = (timezone.now().date() - credit.created_at.date()).days
                    if days_elapsed > credit.credit_days:
                        risk_score += Decimal('20.00')
                        risk_factors['exceso_plazo'] = {
                            'value': days_elapsed - credit.credit_days,
                            'weight': 20,
                            'description': _('Exceso de días sobre el plazo original')
                        }
                
                # Factor 4: Historial de pagos tardíos
                late_payments = Transaction.objects.filter(
                    accountmethodamount__credit=credit,
                    transaction_type='income',
                    status='confirmed',
                    date__gt=credit.created_at + timedelta(days=credit.credit_days)
                ).count()
                
                if late_payments > 0:
                    late_risk = min(late_payments * 8, 25)
                    risk_score += Decimal(str(late_risk))
                    risk_factors['pagos_tardios'] = {
                        'value': late_payments,
                        'weight': late_risk,
                        'description': _('Cantidad de pagos realizados fuera de plazo')
                    }
                
                # Factor 5: Comportamiento del usuario
                user_credits = Credit.objects.filter(user=credit.user).exclude(id=credit.id)
                if user_credits.exists():
                    user_defaults = user_credits.filter(is_in_default=True).count()
                    if user_defaults > 0:
                        user_risk = min(user_defaults * 10, 20)
                        risk_score += Decimal(str(user_risk))
                        risk_factors['historial_usuario'] = {
                            'value': user_defaults,
                            'weight': user_risk,
                            'description': _('Créditos en default del usuario')
                        }
                
                # Normalizar score a 0-100
                risk_score = min(risk_score, Decimal('100.00'))
                
                # Determinar nivel de riesgo
                if risk_score < 30:
                    risk_level = 'low'
                    probability = Decimal('15.00')
                elif risk_score < 60:
                    risk_level = 'medium'
                    probability = Decimal('40.00')
                elif risk_score < 80:
                    risk_level = 'high'
                    probability = Decimal('65.00')
                else:
                    risk_level = 'critical'
                    probability = Decimal('85.00')
                
                # Calcular impacto potencial
                potential_impact = credit.pending_amount
                
                # Crear evaluación
                assessment = RiskAssessment.objects.create(
                    credit=credit,
                    risk_type='credit_default',
                    risk_level=risk_level,
                    risk_score=risk_score,
                    probability=probability,
                    potential_impact=potential_impact,
                    risk_factors=risk_factors,
                    mitigation_actions=[
                        _('Contactar al cliente para renegociar términos'),
                        _('Implementar plan de pagos estructurado'),
                        _('Considerar refinanciamiento si es viable')
                    ],
                    valid_until=timezone.now() + timedelta(days=30)
                )
                
                logger.info(f"Evaluación de riesgo de crédito creada: {assessment}")
                return assessment
                
        except Exception as e:
            logger.error(f"Error assessing credit default risk for {credit.uid}: {e}")
            raise
    
    @staticmethod
    def assess_portfolio_concentration_risk() -> RiskAssessment:
        """
        Evalúa el riesgo de concentración en la cartera.
        """
        try:
            with transaction.atomic():
                # Obtener estadísticas de la cartera
                total_credits = Credit.objects.count()
                total_amount = Credit.objects.aggregate(
                    total=models.Sum('price')
                )['total'] or Decimal('0.00')
                
                # Analizar concentración por usuario
                user_concentrations = {}
                for credit in Credit.objects.select_related('user'):
                    user_id = credit.user.id
                    if user_id not in user_concentrations:
                        user_concentrations[user_id] = {
                            'user': credit.user,
                            'credits': 0,
                            'amount': Decimal('0.00')
                        }
                    user_concentrations[user_id]['credits'] += 1
                    user_concentrations[user_id]['amount'] += credit.price
                
                # Encontrar usuarios con mayor concentración
                sorted_users = sorted(
                    user_concentrations.values(),
                    key=lambda x: x['amount'],
                    reverse=True
                )
                
                if not sorted_users:
                    raise ValidationError(_('No hay créditos en la cartera'))
                
                # Calcular concentración del top 5
                top_5_amount = sum(user['amount'] for user in sorted_users[:5])
                concentration_percentage = (top_5_amount / total_amount) * 100 if total_amount > 0 else 0
                
                # Determinar nivel de riesgo
                if concentration_percentage > 50:
                    risk_level = 'critical'
                    risk_score = Decimal('90.00')
                    probability = Decimal('70.00')
                elif concentration_percentage > 30:
                    risk_level = 'high'
                    risk_score = Decimal('70.00')
                    probability = Decimal('50.00')
                elif concentration_percentage > 15:
                    risk_level = 'medium'
                    risk_score = Decimal('40.00')
                    probability = Decimal('30.00')
                else:
                    risk_level = 'low'
                    risk_score = Decimal('20.00')
                    probability = Decimal('10.00')
                
                # Crear evaluación
                assessment = RiskAssessment.objects.create(
                    risk_type='portfolio_concentration',
                    risk_level=risk_level,
                    risk_score=risk_score,
                    probability=probability,
                    potential_impact=total_amount * (concentration_percentage / 100),
                    risk_factors={
                        'concentration_percentage': concentration_percentage,
                        'top_5_users': [
                            {
                                'user': user['user'].username,
                                'credits': user['credits'],
                                'amount': float(user['amount']),
                                'percentage': float((user['amount'] / total_amount) * 100)
                            }
                            for user in sorted_users[:5]
                        ],
                        'total_portfolio': float(total_amount),
                        'total_credits': total_credits
                    },
                    mitigation_actions=[
                        _('Diversificar la cartera con nuevos clientes'),
                        _('Limitar exposición por cliente'),
                        _('Implementar políticas de concentración')
                    ],
                    valid_until=timezone.now() + timedelta(days=90)
                )
                
                logger.info(f"Evaluación de riesgo de concentración creada: {assessment}")
                return assessment
                
        except Exception as e:
            logger.error(f"Error assessing portfolio concentration risk: {e}")
            raise
    
    @staticmethod
    def assess_liquidity_risk() -> RiskAssessment:
        """
        Evalúa el riesgo de liquidez de la cartera.
        """
        try:
            with transaction.atomic():
                # Calcular flujos de efectivo esperados
                upcoming_payments = AccountMethodAmount.objects.filter(
                    transaction__transaction_type='income',
                    transaction__status='pending'
                ).aggregate(
                    total=models.Sum('amount')
                )['total'] or Decimal('0.00')
                
                # Calcular obligaciones pendientes
                pending_credits = Credit.objects.filter(
                    pending_amount__gt=0
                ).aggregate(
                    total=models.Sum('pending_amount')
                )['total'] or Decimal('0.00')
                
                # Calcular ratio de liquidez
                liquidity_ratio = upcoming_payments / pending_credits if pending_credits > 0 else 0
                
                # Determinar nivel de riesgo
                if liquidity_ratio < 0.5:
                    risk_level = 'critical'
                    risk_score = Decimal('85.00')
                    probability = Decimal('75.00')
                elif liquidity_ratio < 0.8:
                    risk_level = 'high'
                    risk_score = Decimal('65.00')
                    probability = Decimal('55.00')
                elif liquidity_ratio < 1.2:
                    risk_level = 'medium'
                    risk_score = Decimal('40.00')
                    probability = Decimal('35.00')
                else:
                    risk_level = 'low'
                    risk_score = Decimal('20.00')
                    probability = Decimal('15.00')
                
                # Crear evaluación
                assessment = RiskAssessment.objects.create(
                    risk_type='liquidity_risk',
                    risk_level=risk_level,
                    risk_score=risk_score,
                    probability=probability,
                    potential_impact=pending_credits - upcoming_payments,
                    risk_factors={
                        'liquidity_ratio': float(liquidity_ratio),
                        'upcoming_payments': float(upcoming_payments),
                        'pending_credits': float(pending_credits),
                        'cash_flow_gap': float(pending_credits - upcoming_payments)
                    },
                    mitigation_actions=[
                        _('Acelerar cobranza de pagos pendientes'),
                        _('Revisar políticas de otorgamiento'),
                        _('Considerar fuentes alternativas de financiamiento')
                    ],
                    valid_until=timezone.now() + timedelta(days=30)
                )
                
                logger.info(f"Evaluación de riesgo de liquidez creada: {assessment}")
                return assessment
                
        except Exception as e:
            logger.error(f"Error assessing liquidity risk: {e}")
            raise
    
    @staticmethod
    def assess_user_risk(user: User) -> RiskAssessment:
        """
        Evalúa el riesgo general de un usuario.
        """
        try:
            with transaction.atomic():
                # Obtener créditos del usuario
                user_credits = Credit.objects.filter(user=user)
                
                if not user_credits.exists():
                    raise ValidationError(_('El usuario no tiene créditos'))
                
                # Calcular métricas de riesgo
                total_credits = user_credits.count()
                total_amount = sum(credit.price for credit in user_credits)
                pending_amount = sum(credit.pending_amount for credit in user_credits)
                default_credits = user_credits.filter(is_in_default=True).count()
                
                # Calcular score de riesgo
                risk_score = Decimal('0.00')
                risk_factors = {}
                
                # Factor 1: Porcentaje de créditos en default
                if total_credits > 0:
                    default_percentage = (default_credits / total_credits) * 100
                    if default_percentage > 50:
                        risk_score += Decimal('40.00')
                        risk_factors['alto_default'] = {
                            'value': default_percentage,
                            'weight': 40,
                            'description': _('Alto porcentaje de créditos en default')
                        }
                    elif default_percentage > 25:
                        risk_score += Decimal('25.00')
                        risk_factors['default_medio'] = {
                            'value': default_percentage,
                            'weight': 25,
                            'description': _('Porcentaje medio de créditos en default')
                        }
                
                # Factor 2: Cantidad de créditos activos
                active_credits = user_credits.filter(pending_amount__gt=0).count()
                if active_credits > 3:
                    risk_score += Decimal('20.00')
                    risk_factors['muchos_creditos'] = {
                        'value': active_credits,
                        'weight': 20,
                        'description': _('Muchos créditos activos simultáneamente')
                    }
                
                # Factor 3: Ratio de pago
                if total_amount > 0:
                    payment_ratio = ((total_amount - pending_amount) / total_amount) * 100
                    if payment_ratio < 50:
                        risk_score += Decimal('30.00')
                        risk_factors['bajo_pago'] = {
                            'value': payment_ratio,
                            'weight': 30,
                            'description': _('Bajo ratio de pago general')
                        }
                
                # Normalizar score
                risk_score = min(risk_score, Decimal('100.00'))
                
                # Determinar nivel de riesgo
                if risk_score < 30:
                    risk_level = 'low'
                    probability = Decimal('20.00')
                elif risk_score < 60:
                    risk_level = 'medium'
                    probability = Decimal('45.00')
                elif risk_score < 80:
                    risk_level = 'high'
                    probability = Decimal('70.00')
                else:
                    risk_level = 'critical'
                    probability = Decimal('85.00')
                
                # Crear evaluación
                assessment = RiskAssessment.objects.create(
                    user=user,
                    risk_type='credit_default',
                    risk_level=risk_level,
                    risk_score=risk_score,
                    probability=probability,
                    potential_impact=pending_amount,
                    risk_factors=risk_factors,
                    mitigation_actions=[
                        _('Revisar capacidad de pago del cliente'),
                        _('Considerar límites de crédito'),
                        _('Implementar monitoreo más frecuente')
                    ],
                    valid_until=timezone.now() + timedelta(days=60)
                )
                
                logger.info(f"Evaluación de riesgo de usuario creada: {assessment}")
                return assessment
                
        except Exception as e:
            logger.error(f"Error assessing user risk for {user.username}: {e}")
            raise
    
    @staticmethod
    def get_active_assessments(risk_type: str = None) -> List[RiskAssessment]:
        """
        Obtiene evaluaciones de riesgo activas (no expiradas).
        """
        queryset = RiskAssessment.objects.filter(
            valid_until__gt=timezone.now()
        )
        
        if risk_type:
            queryset = queryset.filter(risk_type=risk_type)
        
        return list(queryset.order_by('-risk_score', '-assessment_date'))
    
    @staticmethod
    def cleanup_expired_assessments() -> int:
        """
        Limpia evaluaciones de riesgo expiradas.
        """
        expired_count = RiskAssessment.objects.filter(
            valid_until__lte=timezone.now()
        ).count()
        
        RiskAssessment.objects.filter(
            valid_until__lte=timezone.now()
        ).delete()
        
        logger.info(f"Evaluaciones de riesgo expiradas eliminadas: {expired_count}")
        return expired_count 