"""
Servicio para cálculos de créditos
Mueve la lógica compleja fuera del modelo Credit
"""
from decimal import Decimal, ROUND_HALF_UP
import math
from datetime import timedelta
from django.utils import timezone


class CreditCalculationService:
    """Servicio para cálculos de créditos optimizado"""
    
    @staticmethod
    def calculate_earnings(cost, price):
        """Calcula las ganancias del crédito"""
        if not cost or not price:
            return Decimal('0.00')
        return Decimal(str(price)) - Decimal(str(cost))
    
    @staticmethod
    def calculate_interest_rate(cost, price, credit_days, effective_days=None):
        """
        Calcula la tasa de interés del crédito
        """
        if not cost or not price or not credit_days:
            return Decimal('0.00')
        
        cost_decimal = Decimal(str(cost))
        price_decimal = Decimal(str(price))
        credit_days_decimal = Decimal(str(credit_days))
        
        if cost_decimal <= 0:
            return Decimal('0.00')
        
        # Usar días efectivos si se proporcionan, sino usar días normales
        days_to_use = effective_days if effective_days is not None else credit_days_decimal
        
        # Fórmula: (1 / (días_efectivos / 30)) * ((precio - costo) / costo)
        interest_rate = (Decimal('1') / (days_to_use / Decimal('30'))) * ((price_decimal - cost_decimal) / cost_decimal)
        
        return interest_rate.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_installment_number(credit_days, periodicity_days):
        """
        Calcula el número de cuotas basado en días de crédito y periodicidad
        """
        if not credit_days or not periodicity_days:
            return 1
        
        credit_days_decimal = Decimal(str(credit_days))
        periodicity_days_decimal = Decimal(str(periodicity_days))
        
        if periodicity_days_decimal <= 0:
            return 1
        
        return math.ceil(credit_days_decimal / periodicity_days_decimal)
    
    @staticmethod
    def calculate_installment_value(price, installment_number):
        """
        Calcula el valor de cada cuota
        """
        if not price or not installment_number or installment_number <= 0:
            return Decimal(str(price)) if price else Decimal('0.00')
        
        price_decimal = Decimal(str(price))
        installment_number_decimal = Decimal(str(installment_number))
        
        return (price_decimal / installment_number_decimal).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_effective_days(first_date, second_date, exclude_sundays=False):
        """
        Calcula los días efectivos para intereses, excluyendo domingos si aplica
        """
        if not first_date or not second_date:
            return 0
        
        # Convertir fechas a objetos date si son strings
        if isinstance(first_date, str):
            current_date = timezone.datetime.strptime(first_date, '%Y-%m-%d').date()
        else:
            current_date = first_date.date() if hasattr(first_date, 'date') else first_date
            
        if isinstance(second_date, str):
            end_date = timezone.datetime.strptime(second_date, '%Y-%m-%d').date()
        else:
            end_date = second_date.date() if hasattr(second_date, 'date') else second_date
        
        if not exclude_sundays:
            return (end_date - current_date).days + 1
        
        # Para créditos con periodicidad < 30 días, excluir domingos
        effective_days = 0
        
        while current_date <= end_date:
            if current_date.weekday() != 6:  # No es domingo
                effective_days += 1
            current_date += timedelta(days=1)
        
        return effective_days
    
    @staticmethod
    def should_exclude_sundays(credit_days, periodicity_days):
        """
        Determina si se deben excluir los domingos del cálculo
        """
        # Excluir domingos solo para créditos con periodicidad < 30 días
        return periodicity_days and periodicity_days < 30
    
    @classmethod
    def calculate_all_credit_values(cls, cost, price, credit_days, periodicity_days, 
                                  first_date_payment, second_date_payment):
        """
        Calcula todos los valores del crédito de una vez
        """
        # Valores básicos
        earnings = cls.calculate_earnings(cost, price)
        installment_number = cls.calculate_installment_number(credit_days, periodicity_days)
        installment_value = cls.calculate_installment_value(price, installment_number)
        
        # Calcular días efectivos
        exclude_sundays = cls.should_exclude_sundays(credit_days, periodicity_days)
        effective_days = cls.calculate_effective_days(
            first_date_payment, second_date_payment, exclude_sundays
        )
        
        # Calcular tasa de interés
        interest_rate = cls.calculate_interest_rate(cost, price, credit_days, effective_days)
        
        return {
            'earnings': earnings,
            'interest': interest_rate,
            'installment_number': installment_number,
            'installment_value': installment_value,
            'effective_days': effective_days
        }
    
    @staticmethod
    def validate_credit_data(cost, price, credit_days, periodicity_days, 
                           first_date_payment, second_date_payment):
        """
        Valida los datos del crédito antes de los cálculos
        """
        errors = []
        
        if not cost or cost <= 0:
            errors.append("El costo debe ser mayor a 0")
        
        if not price or price <= 0:
            errors.append("El precio debe ser mayor a 0")
        
        if price and cost and price <= cost:
            errors.append("El precio debe ser mayor al costo")
        
        if not credit_days or credit_days <= 0:
            errors.append("Los días de crédito deben ser mayores a 0")
        
        if not periodicity_days or periodicity_days <= 0:
            errors.append("Los días de periodicidad deben ser mayores a 0")
        
        if first_date_payment and second_date_payment:
            if first_date_payment >= second_date_payment:
                errors.append("La fecha de inicio debe ser anterior a la fecha de fin")
        
        return errors
