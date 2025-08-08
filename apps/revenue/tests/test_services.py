from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from apps.fintech.models import Credit
from ..models import CreditEarnings, RevenueMetrics, EarningsSnapshot, RevenueAdjustment
from ..services.revenue_service import RevenueService
from ..services.earnings_service import EarningsService
from ..services.calculation_service import CalculationService

User = get_user_model()

class RevenueServiceTests(TestCase):
    def setUp(self):
        self.credit = Credit.objects.create(
            price=Decimal('1000.00'),
            cost=Decimal('800.00'),
            interest=Decimal('100.00')
        )

    def test_create_credit_earnings(self):
        """Prueba la creación de CreditEarnings"""
        earnings = RevenueService.create_credit_earnings(
            self.credit,
            Decimal('300.00')
        )
        
        self.assertEqual(earnings.theoretical, Decimal('300.00'))
        self.assertEqual(earnings.realized, Decimal('0.00'))
        self.assertEqual(earnings.pending, Decimal('300.00'))
        
        # Verificar que se creó el snapshot inicial
        self.assertEqual(earnings.snapshots.count(), 1)

    def test_update_realized_earnings(self):
        """Prueba la actualización de ganancias realizadas"""
        earnings = CreditEarnings.objects.create(
            credit=self.credit,
            theoretical=Decimal('300.00'),
            realized=Decimal('100.00'),
            pending=Decimal('200.00')
        )
        
        updated = RevenueService.update_realized_earnings(
            earnings,
            Decimal('50.00')
        )
        
        self.assertEqual(updated.realized, Decimal('150.00'))
        self.assertEqual(updated.pending, Decimal('150.00'))
        
        # Verificar que se creó un nuevo snapshot
        self.assertEqual(updated.snapshots.count(), 1)

    def test_calculate_period_metrics(self):
        """Prueba el cálculo de métricas por período"""
        start_date = timezone.now()
        end_date = start_date + timezone.timedelta(days=30)
        
        # Crear algunos CreditEarnings para el período
        CreditEarnings.objects.create(
            credit=self.credit,
            theoretical=Decimal('300.00'),
            realized=Decimal('150.00'),
            pending=Decimal('150.00')
        )
        
        metrics = RevenueService.calculate_period_metrics(
            start_date,
            end_date
        )
        
        self.assertEqual(metrics.total_theoretical, Decimal('300.00'))
        self.assertEqual(metrics.total_realized, Decimal('150.00'))
        self.assertEqual(metrics.total_pending, Decimal('150.00'))

class EarningsServiceTests(TestCase):
    def setUp(self):
        self.credit = Credit.objects.create(
            price=Decimal('1000.00'),
            cost=Decimal('800.00'),
            interest=Decimal('100.00')
        )
        
        self.earnings = CreditEarnings.objects.create(
            credit=self.credit,
            theoretical=Decimal('300.00'),
            realized=Decimal('100.00'),
            pending=Decimal('200.00')
        )

    def test_calculate_theoretical_earnings(self):
        """Prueba el cálculo de ganancias teóricas"""
        theoretical = EarningsService.calculate_theoretical_earnings(self.credit)
        
        # price (1000) - cost (800) + interest (100) = 300
        self.assertEqual(theoretical, Decimal('300.00'))

    def test_recalculate_earnings(self):
        """Prueba el recálculo de ganancias"""
        # Cambiar el precio del crédito
        self.credit.price = Decimal('1500.00')
        self.credit.save()
        
        updated = EarningsService.recalculate_earnings(self.earnings)
        
        # price (1500) - cost (800) + interest (100) = 800
        self.assertEqual(updated.theoretical, Decimal('800.00'))
        self.assertEqual(updated.snapshots.count(), 1)

    def test_validate_earnings_state(self):
        """Prueba la validación del estado de ganancias"""
        # Estado válido
        self.assertTrue(EarningsService.validate_earnings_state(self.earnings))
        
        # Estado inválido: realized > theoretical
        self.earnings.realized = Decimal('400.00')
        with self.assertRaises(ValidationError):
            EarningsService.validate_earnings_state(self.earnings)

class CalculationServiceTests(TestCase):
    def test_calculate_realization_rate(self):
        """Prueba el cálculo de tasa de realización"""
        rate = CalculationService.calculate_realization_rate(
            Decimal('1000.00'),
            Decimal('600.00')
        )
        
        self.assertEqual(rate, Decimal('60.00'))

    def test_calculate_period_growth(self):
        """Prueba el cálculo de crecimiento por período"""
        growth = CalculationService.calculate_period_growth(
            Decimal('1000.00'),
            Decimal('1200.00'),
            days=30
        )
        
        # ((1200/1000 - 1) * 100) * (365/30)
        self.assertAlmostEqual(float(growth), 243.33, places=2)

    def test_calculate_moving_average(self):
        """Prueba el cálculo de media móvil"""
        values = [
            Decimal('100.00'),
            Decimal('200.00'),
            Decimal('300.00'),
            Decimal('400.00'),
            Decimal('500.00')
        ]
        
        averages = CalculationService.calculate_moving_average(
            values,
            window_size=3
        )
        
        expected = [
            Decimal('200.00'),  # (100 + 200 + 300) / 3
            Decimal('300.00'),  # (200 + 300 + 400) / 3
            Decimal('400.00')   # (300 + 400 + 500) / 3
        ]
        
        self.assertEqual(averages, expected)

    def test_calculate_risk_metrics(self):
        """Prueba el cálculo de métricas de riesgo"""
        values = [
            Decimal('100.00'),
            Decimal('200.00'),
            Decimal('300.00'),
            Decimal('400.00'),
            Decimal('500.00')
        ]
        
        metrics = CalculationService.calculate_risk_metrics(values)
        
        self.assertEqual(metrics['mean'], Decimal('300.00'))
        self.assertEqual(metrics['min'], Decimal('100.00'))
        self.assertEqual(metrics['max'], Decimal('500.00')) 