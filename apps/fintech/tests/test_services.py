from django.test import TestCase
from decimal import Decimal
from django.utils import timezone
from datetime import date, timedelta

from apps.fintech.models import Credit, SubCategory, Category, Currency, Periodicity, Account, User
from apps.fintech.services.credit_service import CreditService
from apps.fintech.services.kpi_service import KPIService


class CreditServiceTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        self.currency = Currency.objects.create(
            id_currency='USD',
            currency='US Dollar',
            asset_type='FIAT',
            exchange_rate=Decimal('1.0')
        )
        
        self.category = Category.objects.create(
            name='Test Category'
        )
        
        self.subcategory = SubCategory.objects.create(
            name='Test Subcategory',
            category=self.category
        )
        
        self.periodicity = Periodicity.objects.create(
            name='Monthly',
            days=30
        )
        
        self.account = Account.objects.create(
            name='Test Account',
            currency=self.currency
        )
        
        self.credit = Credit.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            cost=Decimal('1000.00'),
            price=Decimal('1200.00'),
            currency=self.currency,
            first_date_payment=date.today(),
            second_date_payment=date.today() + timedelta(days=30),
            credit_days=30,
            periodicity=self.periodicity,
            payment=self.account
        )

    def test_create_transaction_from_payment_success(self):
        """Test successful transaction creation"""
        success, result, status_code = CreditService.create_transaction_from_payment(
            credit_uid=self.credit.uid,
            amount=Decimal('100.00'),
            description='Test payment',
            user_id=self.user.id,
            subcategory_name='Test Subcategory',
            payment_type='cash'
        )
        
        self.assertTrue(success)
        self.assertEqual(status_code, 201)
        self.assertIsNotNone(result)

    def test_create_transaction_invalid_amount(self):
        """Test transaction creation with invalid amount"""
        success, result, status_code = CreditService.create_transaction_from_payment(
            credit_uid=self.credit.uid,
            amount=Decimal('0.00'),
            description='Test payment',
            user_id=self.user.id,
            subcategory_name='Test Subcategory',
            payment_type='cash'
        )
        
        self.assertFalse(success)
        self.assertEqual(status_code, 400)
        self.assertIn('mayor a 0', result)

    def test_create_transaction_invalid_subcategory(self):
        """Test transaction creation with invalid subcategory"""
        success, result, status_code = CreditService.create_transaction_from_payment(
            credit_uid=self.credit.uid,
            amount=Decimal('100.00'),
            description='Test payment',
            user_id=self.user.id,
            subcategory_name='Invalid Subcategory',
            payment_type='cash'
        )
        
        self.assertFalse(success)
        self.assertEqual(status_code, 400)
        self.assertIn('No se encontró', result)

    def test_get_credit_summary(self):
        """Test credit summary retrieval"""
        summary, error = CreditService.get_credit_summary(self.credit.uid)
        
        self.assertIsNotNone(summary)
        self.assertIsNone(error)
        self.assertEqual(summary['credit'], self.credit)
        self.assertEqual(summary['payment_count'], 0)


class KPIServiceTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.currency = Currency.objects.create(
            id_currency='USD',
            currency='US Dollar',
            exchange_rate=1.0
        )
        
        self.category = Category.objects.create(
            name='Test Category'
        )
        
        self.subcategory = SubCategory.objects.create(
            name='Test Subcategory',
            category=self.category
        )
        
        self.periodicity = Periodicity.objects.create(
            name='Monthly',
            days=30
        )
        
        self.account = Account.objects.create(
            name='Test Account',
            currency=self.currency
        )
        
        # Create test credits
        self.credit1 = Credit.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            cost=Decimal('1000.00'),
            price=Decimal('1200.00'),
            currency=self.currency,
            first_date_payment=date.today(),
            second_date_payment=date.today(),
            credit_days=30,
            periodicity=self.periodicity,
            payment=self.account,
            total_abonos=Decimal('600.00')
        )
        
        self.credit2 = Credit.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            cost=Decimal('2000.00'),
            price=Decimal('2400.00'),
            currency=self.currency,
            first_date_payment=date.today(),
            second_date_payment=date.today(),
            credit_days=60,
            periodicity=self.periodicity,
            payment=self.account,
            total_abonos=Decimal('0.00'),
            is_in_default=True
        )

    def test_get_credit_kpi_summary(self):
        """Test KPI summary calculation"""
        start_date = date.today() - timezone.timedelta(days=30)
        end_date = date.today()
        
        kpi_data = KPIService.get_credit_kpi_summary(start_date, end_date)
        
        self.assertIsNotNone(kpi_data)
        self.assertEqual(kpi_data['credit_count'], 2)
        self.assertEqual(kpi_data['total_credit_amount'], Decimal('3600.00'))
        self.assertEqual(kpi_data['morosos_count'], 1)
        self.assertEqual(kpi_data['morosidad_rate'], 50.0)

    def test_get_user_financial_metrics(self):
        """Test user financial metrics calculation"""
        metrics = KPIService.get_user_financial_metrics(self.user.id)
        
        self.assertIsNotNone(metrics)
        self.assertEqual(metrics['total_credits'], 2)
        self.assertEqual(metrics['total_credit_amount'], Decimal('3600.00'))
        self.assertEqual(metrics['total_paid'], Decimal('600.00'))
        self.assertEqual(metrics['defaulted_credits'], 1)

    def test_get_portfolio_health_metrics(self):
        """Test portfolio health metrics calculation"""
        metrics = KPIService.get_portfolio_health_metrics()
        
        self.assertIsNotNone(metrics)
        self.assertEqual(metrics['total_credits'], 2)
        self.assertEqual(metrics['defaulted_credits'], 1)
        self.assertEqual(metrics['default_rate'], 50.0) 