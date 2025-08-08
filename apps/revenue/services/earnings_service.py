from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..models import CreditEarnings

class EarningsService:
    """
    Servicio especializado para la gestión de ganancias de créditos.
    Se enfoca únicamente en ganancias, no en pagos ni saldos.
    """
    
    @staticmethod
    def calculate_theoretical_earnings(credit):
        """
        Calcula las ganancias teóricas totales para un crédito.
        Ganancia = (precio - costo) + intereses
        """
        price = credit.price or Decimal('0.00')
        cost = credit.cost or Decimal('0.00')
        interest = credit.interest or Decimal('0.00')
        
        # Ganancia base (margen)
        base_earnings = price - cost
        
        # Ganancias por intereses (calculadas sobre el precio)
        interest_earnings = (price * interest / 100) if interest > 0 else Decimal('0.00')
        
        total_earnings = base_earnings + interest_earnings
        return max(total_earnings, Decimal('0.00'))

    @staticmethod
    def calculate_earnings_rate(credit):
        """
        Calcula la tasa de ganancia sobre el precio total.
        """
        theoretical_earnings = EarningsService.calculate_theoretical_earnings(credit)
        price = credit.price or Decimal('0.00')
        
        if price > 0:
            return theoretical_earnings / price
        return Decimal('0.0000')

    @staticmethod
    def calculate_realized_earnings(credit):
        """
        Calcula las ganancias realizadas basadas en los pagos recibidos.
        Usa la tasa de ganancia para determinar qué porción de los pagos es ganancia.
        """
        # Obtener total de pagos confirmados
        total_paid = credit.total_abonos or Decimal('0.00')
        
        # Obtener o calcular la tasa de ganancia
        if hasattr(credit, 'earnings_detail'):
            earnings_rate = credit.earnings_detail.earnings_rate
        else:
            earnings_rate = EarningsService.calculate_earnings_rate(credit)
        
        # La ganancia realizada es la proporción de ganancia de lo ya pagado
        realized_earnings = total_paid * earnings_rate
        
        return realized_earnings.quantize(Decimal('0.01'))

    @staticmethod
    @transaction.atomic
    def create_or_update_earnings(credit):
        """
        Crea o actualiza el registro de ganancias para un crédito.
        """
        theoretical_earnings = EarningsService.calculate_theoretical_earnings(credit)
        earnings_rate = EarningsService.calculate_earnings_rate(credit)
        realized_earnings = EarningsService.calculate_realized_earnings(credit)
        
        # Crear o actualizar CreditEarnings
        earnings, created = CreditEarnings.objects.get_or_create(
            credit=credit,
            defaults={
                'theoretical_earnings': theoretical_earnings,
                'realized_earnings': realized_earnings,
                'earnings_rate': earnings_rate,
            }
        )
        
        if not created:
            # Actualizar valores existentes
            earnings.theoretical_earnings = theoretical_earnings
            earnings.realized_earnings = realized_earnings
            earnings.earnings_rate = earnings_rate
            earnings.full_clean()
            earnings.save()
        
        # Nota: Los snapshots se removieron para simplificar el modelo
        
        return earnings

    @staticmethod
    def get_earnings_summary(credit_earnings):
        """
        Obtiene un resumen del estado actual de las ganancias.
        """
        return {
            'credit_id': credit_earnings.credit.uid,
            'theoretical_earnings': credit_earnings.theoretical_earnings,
            'realized_earnings': credit_earnings.realized_earnings,
            'pending_earnings': credit_earnings.pending_earnings,
            'realization_percentage': credit_earnings.realization_percentage,
            'earnings_rate': credit_earnings.earnings_rate,
            'last_update': credit_earnings.updated_at,
            # Información del crédito
            'credit_price': credit_earnings.credit.price,
            'credit_cost': credit_earnings.credit.cost,
            'credit_total_paid': credit_earnings.credit.total_abonos,
            'credit_pending_amount': credit_earnings.credit.pending_amount,
        }

    @staticmethod
    def validate_earnings_consistency(credit_earnings):
        """
        Valida la consistencia del estado de las ganancias.
        """
        errors = []
        credit = credit_earnings.credit
        
        # Recalcular valores esperados
        expected_theoretical = EarningsService.calculate_theoretical_earnings(credit)
        expected_rate = EarningsService.calculate_earnings_rate(credit)
        expected_realized = EarningsService.calculate_realized_earnings(credit)
        
        # Validar ganancia teórica
        if abs(credit_earnings.theoretical_earnings - expected_theoretical) > Decimal('0.01'):
            errors.append(_('Ganancia teórica inconsistente. Esperado: %(expected).2f, Actual: %(actual).2f') % {
                'expected': expected_theoretical,
                'actual': credit_earnings.theoretical_earnings
            })
        
        # Validar tasa de ganancia
        if abs(credit_earnings.earnings_rate - expected_rate) > Decimal('0.0001'):
            errors.append(_('Tasa de ganancia inconsistente. Esperado: %(expected).4f, Actual: %(actual).4f') % {
                'expected': expected_rate,
                'actual': credit_earnings.earnings_rate
            })
        
        # Validar ganancia realizada
        if abs(credit_earnings.realized_earnings - expected_realized) > Decimal('0.01'):
            errors.append(_('Ganancia realizada inconsistente. Esperado: %(expected).2f, Actual: %(actual).2f') % {
                'expected': expected_realized,
                'actual': credit_earnings.realized_earnings
            })
        
        # Validaciones de negocio
        if credit_earnings.realized_earnings > credit_earnings.theoretical_earnings:
            errors.append(_('La ganancia realizada no puede superar la teórica'))
        
        if credit_earnings.theoretical_earnings < 0:
            errors.append(_('La ganancia teórica no puede ser negativa'))
            
        if errors:
            raise ValidationError({
                'consistency': errors
            })
        
        return True

    @staticmethod
    def get_earnings_trends(credit_earnings, days=30):
        """
        Analiza tendencias básicas en las ganancias.
        Nota: Sin snapshots, solo podemos analizar el estado actual vs histórico del crédito.
        """
        return {
            'current_theoretical': credit_earnings.theoretical_earnings,
            'current_realized': credit_earnings.realized_earnings,
            'current_pending': credit_earnings.pending_earnings,
            'realization_percentage': credit_earnings.realization_percentage,
            'last_update': credit_earnings.updated_at,
            'note': 'Análisis detallado requiere implementar snapshots en forecasting app'
        } 