from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import logging
from datetime import timedelta, date
from typing import Dict, List, Optional, Tuple

from apps.fintech.models import Credit, Transaction, AccountMethodAmount
from apps.revenue.models import CreditEarnings
from ..models import CreditPrediction

logger = logging.getLogger(__name__)

class PredictionService:
    """
    Servicio para generar predicciones sobre créditos.
    """
    
    @staticmethod
    def predict_next_payment_date(credit: Credit) -> Optional[date]:
        """
        Predice la fecha del próximo pago basándose en el historial.
        """
        try:
            # Obtener pagos anteriores
            payments = AccountMethodAmount.objects.filter(
                credit=credit,
                transaction__transaction_type='income',
                transaction__status='confirmed'
            ).order_by('transaction__date')
            
            if not payments.exists():
                return None
            
            # Calcular intervalos entre pagos
            intervals = []
            payment_dates = [p.transaction.date for p in payments]
            
            for i in range(1, len(payment_dates)):
                interval = (payment_dates[i] - payment_dates[i-1]).days
                intervals.append(interval)
            
            if not intervals:
                return None
            
            # Calcular intervalo promedio
            avg_interval = sum(intervals) / len(intervals)
            
            # Último pago
            last_payment = payment_dates[-1]
            next_payment = last_payment + timedelta(days=avg_interval)
            
            return next_payment.date()
            
        except Exception as e:
            logger.error(f"Error predicting next payment date for credit {credit.uid}: {e}")
            return None
    
    @staticmethod
    def predict_completion_date(credit: Credit) -> Optional[date]:
        """
        Predice la fecha de completación del crédito.
        """
        try:
            if credit.pending_amount <= 0:
                return None
            
            # Calcular tasa de pago promedio
            payments = AccountMethodAmount.objects.filter(
                credit=credit,
                transaction__transaction_type='income',
                transaction__status='confirmed'
            )
            
            if not payments.exists():
                return None
            
            total_paid = sum(p.amount for p in payments)
            avg_daily_payment = total_paid / credit.credit_days if credit.credit_days > 0 else 0
            
            if avg_daily_payment <= 0:
                return None
            
            # Calcular días restantes
            days_remaining = credit.pending_amount / avg_daily_payment
            completion_date = timezone.now().date() + timedelta(days=int(days_remaining))
            
            return completion_date
            
        except Exception as e:
            logger.error(f"Error predicting completion date for credit {credit.uid}: {e}")
            return None
    
    @staticmethod
    def calculate_default_risk(credit: Credit) -> Tuple[Decimal, str]:
        """
        Calcula el riesgo de impago de un crédito.
        """
        try:
            risk_score = Decimal('0.00')
            risk_factors = {}
            
            # Factor 1: Mora actual
            if credit.morosidad_level > 0:
                mora_risk = min(credit.morosidad_level * 20, 50)  # Máximo 50 puntos por mora
                risk_score += Decimal(str(mora_risk))
                risk_factors['mora_actual'] = mora_risk
            
            # Factor 2: Porcentaje de pago
            if credit.price > 0:
                payment_percentage = (credit.total_abonos / credit.price) * 100
                if payment_percentage < 30:
                    risk_score += Decimal('30.00')
                    risk_factors['bajo_pago'] = 30
                elif payment_percentage < 60:
                    risk_score += Decimal('15.00')
                    risk_factors['pago_medio'] = 15
            
            # Factor 3: Días de crédito vs días transcurridos
            if credit.credit_days > 0:
                days_elapsed = (timezone.now().date() - credit.created_at.date()).days
                if days_elapsed > credit.credit_days:
                    risk_score += Decimal('25.00')
                    risk_factors['exceso_plazo'] = 25
            
            # Factor 4: Historial de pagos
            late_payments = Transaction.objects.filter(
                accountmethodamount__credit=credit,
                transaction_type='income',
                status='confirmed',
                date__gt=credit.created_at + timedelta(days=credit.credit_days)
            ).count()
            
            if late_payments > 0:
                risk_score += Decimal(str(min(late_payments * 10, 20)))
                risk_factors['pagos_tardios'] = late_payments * 10
            
            # Normalizar score a 0-100
            risk_score = min(risk_score, Decimal('100.00'))
            
            # Determinar nivel de confianza
            if risk_score < 30:
                confidence = 'high'
                confidence_pct = Decimal('85.00')
            elif risk_score < 60:
                confidence = 'medium'
                confidence_pct = Decimal('70.00')
            else:
                confidence = 'low'
                confidence_pct = Decimal('55.00')
            
            return risk_score, confidence, confidence_pct, risk_factors
            
        except Exception as e:
            logger.error(f"Error calculating default risk for credit {credit.uid}: {e}")
            return Decimal('50.00'), 'medium', Decimal('50.00'), {}
    
    @staticmethod
    def predict_next_payment_amount(credit: Credit) -> Optional[Decimal]:
        """
        Predice el monto del próximo pago.
        """
        try:
            payments = AccountMethodAmount.objects.filter(
                credit=credit,
                transaction__transaction_type='income',
                transaction__status='confirmed'
            ).order_by('transaction__date')
            
            if not payments.exists():
                return None
            
            # Calcular monto promedio de pagos
            amounts = [p.amount for p in payments]
            avg_amount = sum(amounts) / len(amounts)
            
            # Considerar el saldo pendiente
            if credit.pending_amount < avg_amount:
                return credit.pending_amount
            
            return Decimal(str(avg_amount))
            
        except Exception as e:
            logger.error(f"Error predicting next payment amount for credit {credit.uid}: {e}")
            return None
    
    @classmethod
    def create_credit_prediction(
        cls,
        credit: Credit,
        prediction_type: str,
        **kwargs
    ) -> CreditPrediction:
        """
        Crea una nueva predicción para un crédito.
        """
        try:
            with transaction.atomic():
                # Calcular predicción según el tipo
                if prediction_type == 'payment_date':
                    predicted_date = cls.predict_next_payment_date(credit)
                    if not predicted_date:
                        raise ValidationError(_('No se pudo predecir la fecha de pago'))
                    
                    prediction = CreditPrediction.objects.create(
                        credit=credit,
                        prediction_type=prediction_type,
                        predicted_date=predicted_date,
                        confidence_percentage=Decimal('75.00'),
                        expires_at=timezone.now() + timedelta(days=30),
                        **kwargs
                    )
                
                elif prediction_type == 'completion_date':
                    predicted_date = cls.predict_completion_date(credit)
                    if not predicted_date:
                        raise ValidationError(_('No se pudo predecir la fecha de completación'))
                    
                    prediction = CreditPrediction.objects.create(
                        credit=credit,
                        prediction_type=prediction_type,
                        predicted_date=predicted_date,
                        confidence_percentage=Decimal('70.00'),
                        expires_at=timezone.now() + timedelta(days=60),
                        **kwargs
                    )
                
                elif prediction_type == 'default_risk':
                    risk_score, confidence, confidence_pct, features = cls.calculate_default_risk(credit)
                    
                    prediction = CreditPrediction.objects.create(
                        credit=credit,
                        prediction_type=prediction_type,
                        risk_score=risk_score,
                        confidence_level=confidence,
                        confidence_percentage=confidence_pct,
                        features_used=features,
                        expires_at=timezone.now() + timedelta(days=7),
                        **kwargs
                    )
                
                elif prediction_type == 'payment_amount':
                    predicted_amount = cls.predict_next_payment_amount(credit)
                    if not predicted_amount:
                        raise ValidationError(_('No se pudo predecir el monto de pago'))
                    
                    prediction = CreditPrediction.objects.create(
                        credit=credit,
                        prediction_type=prediction_type,
                        predicted_amount=predicted_amount,
                        confidence_percentage=Decimal('80.00'),
                        expires_at=timezone.now() + timedelta(days=15),
                        **kwargs
                    )
                
                else:
                    raise ValidationError(_('Tipo de predicción no válido'))
                
                logger.info(f"Predicción creada: {prediction}")
                return prediction
                
        except Exception as e:
            logger.error(f"Error creating prediction for credit {credit.uid}: {e}")
            raise
    
    @staticmethod
    def get_active_predictions(credit: Credit = None) -> List[CreditPrediction]:
        """
        Obtiene predicciones activas (no expiradas).
        """
        queryset = CreditPrediction.objects.filter(
            expires_at__gt=timezone.now()
        )
        
        if credit:
            queryset = queryset.filter(credit=credit)
        
        return list(queryset.order_by('-created_at'))
    
    @staticmethod
    def cleanup_expired_predictions() -> int:
        """
        Limpia predicciones expiradas.
        """
        expired_count = CreditPrediction.objects.filter(
            expires_at__lte=timezone.now()
        ).count()
        
        CreditPrediction.objects.filter(
            expires_at__lte=timezone.now()
        ).delete()
        
        logger.info(f"Predicciones expiradas eliminadas: {expired_count}")
        return expired_count 