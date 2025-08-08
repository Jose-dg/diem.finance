from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.fintech.models import Credit, User, Account, Periodicity
from apps.revenue.models import CreditEarnings, EarningsMetrics, EarningsAdjustment


class RevenueModelFactory:
    @staticmethod
    def create_minimal_credit(**overrides) -> Credit:
        user = overrides.pop('user', None) or User.objects.create_user(username='user_test')
        periodicity = overrides.pop('periodicity', None) or Periodicity.objects.create(name='Mensual', days=30)
        account = overrides.pop('payment', None) or Account.objects.create(name='Cuenta Test')
        today = timezone.now().date()
        defaults = dict(
            registered_by=None,
            user=user,
            cost=Decimal('800.00'),
            price=Decimal('1000.00'),
            currency=None,
            first_date_payment=today,
            second_date_payment=today,
            credit_days=30,
            interest=Decimal('10.00'),
            periodicity=periodicity,
            payment=account,
            total_abonos=Decimal('0.00'),
        )
        defaults.update(overrides)
        return Credit.objects.create(**defaults)


class CreditEarningsTests(TestCase):
    def setUp(self):
        self.credit = RevenueModelFactory.create_minimal_credit()
        self.earnings = CreditEarnings.objects.create(
            credit=self.credit,
            theoretical_earnings=Decimal('300.00'),
            realized_earnings=Decimal('100.00'),
            earnings_rate=Decimal('0.3000'),
        )

    def test_pending_earnings_property(self):
        self.earnings.theoretical_earnings = Decimal('500.00')
        self.earnings.realized_earnings = Decimal('300.00')
        self.earnings.full_clean()
        self.earnings.save()
        self.assertEqual(self.earnings.pending_earnings, Decimal('200.00'))

    def test_realization_percentage(self):
        # 100 / 300 * 100 = 33.333...
        pct = self.earnings.realization_percentage
        self.assertTrue(Decimal('33.33') <= pct <= Decimal('33.34'))

    def test_realized_cannot_exceed_theoretical(self):
        self.earnings.realized_earnings = Decimal('400.00')  # > 300.00
        with self.assertRaises(ValidationError):
            self.earnings.full_clean()

    def test_theoretical_cannot_be_negative(self):
        self.earnings.theoretical_earnings = Decimal('-1.00')
        with self.assertRaises(ValidationError):
            self.earnings.full_clean()

    def test_earnings_rate_bounds(self):
        self.earnings.earnings_rate = Decimal('1.1000')  # > 1.0
        with self.assertRaises(ValidationError):
            self.earnings.full_clean()


class EarningsMetricsTests(TestCase):
    def setUp(self):
        self.start_date = timezone.now()
        self.end_date = self.start_date + timezone.timedelta(days=30)
        self.metrics = EarningsMetrics.objects.create(
            period_start=self.start_date,
            period_end=self.end_date,
            total_theoretical_earnings=Decimal('1000.00'),
            total_realized_earnings=Decimal('600.00'),
            credits_count=10,
            avg_realization_rate=Decimal('60.00'),
        )

    def test_pending_earnings_property(self):
        self.assertEqual(self.metrics.pending_earnings, Decimal('400.00'))

    def test_period_validation(self):
        self.metrics.period_end = self.start_date
        with self.assertRaises(ValidationError):
            self.metrics.full_clean()


class EarningsAdjustmentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='adjuster')
        self.credit = RevenueModelFactory.create_minimal_credit(user=self.user)
        self.earnings = CreditEarnings.objects.create(
            credit=self.credit,
            theoretical_earnings=Decimal('300.00'),
            realized_earnings=Decimal('100.00'),
            earnings_rate=Decimal('0.3000'),
        )

    def test_adjustment_creation(self):
        adjustment = EarningsAdjustment.objects.create(
            credit_earnings=self.earnings,
            amount=Decimal('50.00'),
            adjustment_type='manual',
            reason='Test adjustment',
            created_by=self.user,
        )
        self.assertEqual(adjustment.amount, Decimal('50.00'))
        self.assertEqual(adjustment.adjustment_type, 'manual')
        self.assertEqual(adjustment.created_by, self.user) 