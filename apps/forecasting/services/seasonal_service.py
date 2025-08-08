from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import logging
from datetime import timedelta, date
from typing import Dict, List, Optional, Tuple
import calendar
from collections import defaultdict

from apps.fintech.models import Credit, Transaction, AccountMethodAmount
from apps.revenue.models import CreditEarnings
from ..models import SeasonalPattern

logger = logging.getLogger(__name__)

class SeasonalService:
    """
    Servicio para identificar patrones estacionales en los datos.
    """
    
    @staticmethod
    def identify_monthly_patterns(
        start_date: date,
        end_date: date,
        data_type: str = 'payments'
    ) -> SeasonalPattern:
        """
        Identifica patrones mensuales en los datos.
        """
        try:
            with transaction.atomic():
                # Obtener datos según el tipo
                if data_type == 'payments':
                    data = AccountMethodAmount.objects.filter(
                        transaction__transaction_type='income',
                        transaction__status='confirmed',
                        transaction__date__range=[start_date, end_date]
                    ).select_related('transaction')
                    
                    # Agrupar por mes
                    monthly_data = defaultdict(list)
                    for item in data:
                        month_key = (item.transaction.date.year, item.transaction.date.month)
                        monthly_data[month_key].append(item.amount)
                    
                    # Calcular totales mensuales
                    monthly_totals = {
                        month: sum(amounts) for month, amounts in monthly_data.items()
                    }
                    
                elif data_type == 'credits':
                    data = Credit.objects.filter(
                        created_at__date__range=[start_date, end_date]
                    )
                    
                    # Agrupar por mes
                    monthly_data = defaultdict(list)
                    for item in data:
                        month_key = (item.created_at.year, item.created_at.month)
                        monthly_data[month_key].append(item.price)
                    
                    # Calcular totales mensuales
                    monthly_totals = {
                        month: sum(amounts) for month, amounts in monthly_data.items()
                    }
                
                else:
                    raise ValidationError(_('Tipo de datos no válido'))
                
                if not monthly_totals:
                    raise ValidationError(_('No hay datos suficientes para identificar patrones'))
                
                # Encontrar picos y valles
                sorted_months = sorted(monthly_totals.items(), key=lambda x: x[1], reverse=True)
                peak_periods = [f"{year}-{month:02d}" for (year, month), _ in sorted_months[:3]]
                low_periods = [f"{year}-{month:02d}" for (year, month), _ in sorted_months[-3:]]
                
                # Calcular amplitud
                values = list(monthly_totals.values())
                amplitude = max(values) - min(values) if values else 0
                
                # Calcular confianza basada en la consistencia
                if len(values) >= 6:  # Al menos 6 meses de datos
                    confidence = min(85.0, 50.0 + (len(values) * 5.0))
                else:
                    confidence = 50.0
                
                # Crear patrón
                pattern = SeasonalPattern.objects.create(
                    pattern_name=f"Patrón Mensual - {data_type.title()}",
                    pattern_type='monthly',
                    description=f"Patrón mensual identificado en {data_type} entre {start_date} y {end_date}",
                    peak_periods=peak_periods,
                    low_periods=low_periods,
                    amplitude=Decimal(str(amplitude)),
                    confidence_score=Decimal(str(confidence)),
                    identified_from=start_date,
                    identified_to=end_date,
                    next_expected_peak=SeasonalService._predict_next_peak(peak_periods),
                    next_expected_low=SeasonalService._predict_next_low(low_periods)
                )
                
                logger.info(f"Patrón mensual identificado: {pattern}")
                return pattern
                
        except Exception as e:
            logger.error(f"Error identifying monthly patterns: {e}")
            raise
    
    @staticmethod
    def identify_quarterly_patterns(
        start_date: date,
        end_date: date,
        data_type: str = 'payments'
    ) -> SeasonalPattern:
        """
        Identifica patrones trimestrales en los datos.
        """
        try:
            with transaction.atomic():
                # Obtener datos según el tipo
                if data_type == 'payments':
                    data = AccountMethodAmount.objects.filter(
                        transaction__transaction_type='income',
                        transaction__status='confirmed',
                        transaction__date__range=[start_date, end_date]
                    ).select_related('transaction')
                    
                    # Agrupar por trimestre
                    quarterly_data = defaultdict(list)
                    for item in data:
                        quarter = (item.transaction.date.year, (item.transaction.date.month - 1) // 3 + 1)
                        quarterly_data[quarter].append(item.amount)
                    
                    # Calcular totales trimestrales
                    quarterly_totals = {
                        quarter: sum(amounts) for quarter, amounts in quarterly_data.items()
                    }
                    
                elif data_type == 'credits':
                    data = Credit.objects.filter(
                        created_at__date__range=[start_date, end_date]
                    )
                    
                    # Agrupar por trimestre
                    quarterly_data = defaultdict(list)
                    for item in data:
                        quarter = (item.created_at.year, (item.created_at.month - 1) // 3 + 1)
                        quarterly_data[quarter].append(item.price)
                    
                    # Calcular totales trimestrales
                    quarterly_totals = {
                        quarter: sum(amounts) for quarter, amounts in quarterly_data.items()
                    }
                
                else:
                    raise ValidationError(_('Tipo de datos no válido'))
                
                if not quarterly_totals:
                    raise ValidationError(_('No hay datos suficientes para identificar patrones'))
                
                # Encontrar picos y valles
                sorted_quarters = sorted(quarterly_totals.items(), key=lambda x: x[1], reverse=True)
                peak_periods = [f"{year}-Q{quarter}" for (year, quarter), _ in sorted_quarters[:2]]
                low_periods = [f"{year}-Q{quarter}" for (year, quarter), _ in sorted_quarters[-2:]]
                
                # Calcular amplitud
                values = list(quarterly_totals.values())
                amplitude = max(values) - min(values) if values else 0
                
                # Calcular confianza
                if len(values) >= 4:  # Al menos 4 trimestres
                    confidence = min(80.0, 40.0 + (len(values) * 10.0))
                else:
                    confidence = 40.0
                
                # Crear patrón
                pattern = SeasonalPattern.objects.create(
                    pattern_name=f"Patrón Trimestral - {data_type.title()}",
                    pattern_type='quarterly',
                    description=f"Patrón trimestral identificado en {data_type} entre {start_date} y {end_date}",
                    peak_periods=peak_periods,
                    low_periods=low_periods,
                    amplitude=Decimal(str(amplitude)),
                    confidence_score=Decimal(str(confidence)),
                    identified_from=start_date,
                    identified_to=end_date,
                    next_expected_peak=SeasonalService._predict_next_quarterly_peak(peak_periods),
                    next_expected_low=SeasonalService._predict_next_quarterly_low(low_periods)
                )
                
                logger.info(f"Patrón trimestral identificado: {pattern}")
                return pattern
                
        except Exception as e:
            logger.error(f"Error identifying quarterly patterns: {e}")
            raise
    
    @staticmethod
    def identify_weekly_patterns(
        start_date: date,
        end_date: date,
        data_type: str = 'payments'
    ) -> SeasonalPattern:
        """
        Identifica patrones semanales en los datos.
        """
        try:
            with transaction.atomic():
                # Obtener datos según el tipo
                if data_type == 'payments':
                    data = AccountMethodAmount.objects.filter(
                        transaction__transaction_type='income',
                        transaction__status='confirmed',
                        transaction__date__range=[start_date, end_date]
                    ).select_related('transaction')
                    
                    # Agrupar por día de la semana
                    weekly_data = defaultdict(list)
                    for item in data:
                        day_of_week = item.transaction.date.weekday()
                        weekly_data[day_of_week].append(item.amount)
                    
                    # Calcular totales por día
                    daily_totals = {
                        day: sum(amounts) for day, amounts in weekly_data.items()
                    }
                    
                elif data_type == 'credits':
                    data = Credit.objects.filter(
                        created_at__date__range=[start_date, end_date]
                    )
                    
                    # Agrupar por día de la semana
                    weekly_data = defaultdict(list)
                    for item in data:
                        day_of_week = item.created_at.weekday()
                        weekly_data[day_of_week].append(item.price)
                    
                    # Calcular totales por día
                    daily_totals = {
                        day: sum(amounts) for day, amounts in weekly_data.items()
                    }
                
                else:
                    raise ValidationError(_('Tipo de datos no válido'))
                
                if not daily_totals:
                    raise ValidationError(_('No hay datos suficientes para identificar patrones'))
                
                # Encontrar picos y valles
                sorted_days = sorted(daily_totals.items(), key=lambda x: x[1], reverse=True)
                peak_periods = [calendar.day_name[day] for day, _ in sorted_days[:3]]
                low_periods = [calendar.day_name[day] for day, _ in sorted_days[-3:]]
                
                # Calcular amplitud
                values = list(daily_totals.values())
                amplitude = max(values) - min(values) if values else 0
                
                # Calcular confianza
                if len(values) >= 7:  # Todos los días de la semana
                    confidence = min(90.0, 60.0 + (len(values) * 4.0))
                else:
                    confidence = 60.0
                
                # Crear patrón
                pattern = SeasonalPattern.objects.create(
                    pattern_name=f"Patrón Semanal - {data_type.title()}",
                    pattern_type='weekly',
                    description=f"Patrón semanal identificado en {data_type} entre {start_date} y {end_date}",
                    peak_periods=peak_periods,
                    low_periods=low_periods,
                    amplitude=Decimal(str(amplitude)),
                    confidence_score=Decimal(str(confidence)),
                    identified_from=start_date,
                    identified_to=end_date
                )
                
                logger.info(f"Patrón semanal identificado: {pattern}")
                return pattern
                
        except Exception as e:
            logger.error(f"Error identifying weekly patterns: {e}")
            raise
    
    @staticmethod
    def _predict_next_peak(peak_periods: List[str]) -> Optional[date]:
        """
        Predice el próximo pico basándose en los períodos pico históricos.
        """
        if not peak_periods:
            return None
        
        # Analizar el último pico
        last_peak = peak_periods[0]  # Asumimos que están ordenados
        try:
            year, month = map(int, last_peak.split('-'))
            next_peak = date(year, month, 1) + timedelta(days=365)  # Un año después
            return next_peak
        except:
            return None
    
    @staticmethod
    def _predict_next_low(low_periods: List[str]) -> Optional[date]:
        """
        Predice el próximo valle basándose en los períodos bajos históricos.
        """
        if not low_periods:
            return None
        
        # Analizar el último valle
        last_low = low_periods[0]  # Asumimos que están ordenados
        try:
            year, month = map(int, last_low.split('-'))
            next_low = date(year, month, 1) + timedelta(days=365)  # Un año después
            return next_low
        except:
            return None
    
    @staticmethod
    def _predict_next_quarterly_peak(peak_periods: List[str]) -> Optional[date]:
        """
        Predice el próximo pico trimestral.
        """
        if not peak_periods:
            return None
        
        # Analizar el último pico trimestral
        last_peak = peak_periods[0]
        try:
            year, quarter = last_peak.split('-Q')
            year, quarter = int(year), int(quarter)
            next_quarter = quarter + 1 if quarter < 4 else 1
            next_year = year + 1 if quarter == 4 else year
            next_month = (next_quarter - 1) * 3 + 1
            return date(next_year, next_month, 1)
        except:
            return None
    
    @staticmethod
    def _predict_next_quarterly_low(low_periods: List[str]) -> Optional[date]:
        """
        Predice el próximo valle trimestral.
        """
        if not low_periods:
            return None
        
        # Analizar el último valle trimestral
        last_low = low_periods[0]
        try:
            year, quarter = last_low.split('-Q')
            year, quarter = int(year), int(quarter)
            next_quarter = quarter + 1 if quarter < 4 else 1
            next_year = year + 1 if quarter == 4 else year
            next_month = (next_quarter - 1) * 3 + 1
            return date(next_year, next_month, 1)
        except:
            return None
    
    @staticmethod
    def get_active_patterns(pattern_type: str = None) -> List[SeasonalPattern]:
        """
        Obtiene patrones activos (con alta confianza).
        """
        queryset = SeasonalPattern.objects.filter(
            confidence_score__gte=70
        )
        
        if pattern_type:
            queryset = queryset.filter(pattern_type=pattern_type)
        
        return list(queryset.order_by('-confidence_score'))
    
    @staticmethod
    def cleanup_old_patterns(months_old: int = 12) -> int:
        """
        Limpia patrones antiguos.
        """
        cutoff_date = timezone.now().date() - timedelta(days=months_old * 30)
        
        old_patterns = SeasonalPattern.objects.filter(
            identified_to__lt=cutoff_date,
            confidence_score__lt=50
        ).count()
        
        SeasonalPattern.objects.filter(
            identified_to__lt=cutoff_date,
            confidence_score__lt=50
        ).delete()
        
        logger.info(f"Patrones antiguos eliminados: {old_patterns}")
        return old_patterns 