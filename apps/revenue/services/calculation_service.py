from decimal import Decimal
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CalculationService:
    """
    Servicio para cálculos financieros complejos.
    """
    
    @staticmethod
    def calculate_realization_rate(theoretical, realized):
        """
        Calcula la tasa de realización de ganancias.
        """
        if not isinstance(theoretical, Decimal):
            theoretical = Decimal(str(theoretical))
        if not isinstance(realized, Decimal):
            realized = Decimal(str(realized))
            
        if theoretical <= 0:
            return Decimal('0.00')
            
        rate = (realized / theoretical) * 100
        return rate.quantize(Decimal('0.01'))

    @staticmethod
    def calculate_period_growth(start_value, end_value, days):
        """
        Calcula la tasa de crecimiento para un período.
        """
        if not isinstance(start_value, Decimal):
            start_value = Decimal(str(start_value))
        if not isinstance(end_value, Decimal):
            end_value = Decimal(str(end_value))
            
        if start_value <= 0:
            return None
            
        # Calcular crecimiento total
        total_growth = ((end_value / start_value) - 1) * 100
        
        # Anualizar la tasa
        annual_rate = total_growth * (365 / days)
        
        return annual_rate.quantize(Decimal('0.01'))

    @staticmethod
    def calculate_moving_average(values, window_size=7):
        """
        Calcula la media móvil de una serie de valores.
        """
        if not values or len(values) < window_size:
            return []
            
        result = []
        for i in range(len(values) - window_size + 1):
            window = values[i:i + window_size]
            average = sum(window) / window_size
            result.append(average.quantize(Decimal('0.01')))
            
        return result

    @staticmethod
    def calculate_projected_earnings(current_earnings, trend_rate, days):
        """
        Proyecta ganancias futuras basadas en tendencia actual.
        """
        if not isinstance(current_earnings, Decimal):
            current_earnings = Decimal(str(current_earnings))
        if not isinstance(trend_rate, Decimal):
            trend_rate = Decimal(str(trend_rate))
            
        daily_rate = trend_rate / 365
        growth_factor = (1 + (daily_rate / 100)) ** days
        
        projected = current_earnings * growth_factor
        return projected.quantize(Decimal('0.01'))

    @staticmethod
    def calculate_risk_metrics(earnings_data):
        """
        Calcula métricas de riesgo basadas en histórico de ganancias.
        """
        if not earnings_data:
            return None
            
        # Convertir valores a Decimal si es necesario
        values = [Decimal(str(x)) if not isinstance(x, Decimal) else x 
                 for x in earnings_data]
        
        # Calcular estadísticas básicas
        mean = sum(values) / len(values)
        squared_diff_sum = sum((x - mean) ** 2 for x in values)
        variance = squared_diff_sum / len(values)
        std_dev = variance.sqrt()
        
        # Calcular coeficiente de variación
        cv = (std_dev / mean * 100) if mean > 0 else Decimal('0.00')
        
        return {
            'mean': mean.quantize(Decimal('0.01')),
            'std_dev': std_dev.quantize(Decimal('0.01')),
            'cv': cv.quantize(Decimal('0.01')),
            'min': min(values).quantize(Decimal('0.01')),
            'max': max(values).quantize(Decimal('0.01'))
        }

    @staticmethod
    def calculate_efficiency_metrics(theoretical, realized, time_elapsed_days):
        """
        Calcula métricas de eficiencia en la realización de ganancias.
        """
        if not isinstance(theoretical, Decimal):
            theoretical = Decimal(str(theoretical))
        if not isinstance(realized, Decimal):
            realized = Decimal(str(realized))
            
        if theoretical <= 0:
            return None
            
        realization_rate = CalculationService.calculate_realization_rate(
            theoretical, realized
        )
        
        daily_rate = (realized / time_elapsed_days).quantize(Decimal('0.01'))
        remaining = theoretical - realized
        
        if daily_rate > 0:
            days_to_complete = (remaining / daily_rate).quantize(Decimal('0'))
        else:
            days_to_complete = None
            
        return {
            'realization_rate': realization_rate,
            'daily_rate': daily_rate,
            'days_to_complete': days_to_complete,
            'remaining_amount': remaining.quantize(Decimal('0.01'))
        } 