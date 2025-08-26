"""
Tests unitarios para las vistas del dashboard de insights
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from datetime import date, timedelta
from django.utils import timezone

from apps.fintech.models import (
    Credit, Installment, User, SubCategory, Currency, 
    Periodicity, Account, Seller, Role
)

User = get_user_model()

class DashboardViewsTestCase(APITestCase):
    """Tests para las vistas del dashboard"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Crear datos de prueba
        self.currency = Currency.objects.create(
            currency='COP',
            id_currency='COP'
        )
        
        self.subcategory = SubCategory.objects.create(
            name='Préstamo Personal'
        )
        
        self.periodicity = Periodicity.objects.create(
            name='Semanal',
            days=7
        )
        
        self.account = Account.objects.create(
            name='Cuenta Principal'
        )
        
        self.role = Role.objects.create(name='Vendedor')
        self.seller = Seller.objects.create(
            role=self.role,
            user=self.user
        )
        
        # Crear crédito de prueba
        self.credit = Credit.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            cost=Decimal('800000.00'),
            price=Decimal('1000000.00'),
            currency=self.currency,
            first_date_payment=date.today(),
            second_date_payment=date.today() + timedelta(days=70),
            credit_days=70,
            periodicity=self.periodicity,
            payment=self.account,
            seller=self.seller,
            state='pending'
        )
        
        # Crear cuotas de prueba
        for i in range(1, 11):
            due_date = date.today() + timedelta(days=i*7)
            status = 'paid' if i <= 3 else 'pending'
            paid_on = due_date if i <= 3 else None
            
            Installment.objects.create(
                credit=self.credit,
                number=i,
                due_date=due_date,
                amount=Decimal('100000.00'),
                status=status,
                paid_on=paid_on,
                amount_paid=Decimal('100000.00') if i <= 3 else Decimal('0.00'),
                remaining_amount=Decimal('0.00') if i <= 3 else Decimal('100000.00')
            )
        
        # Autenticar usuario
        self.client.force_authenticate(user=self.user)
    
    def test_credits_dashboard_endpoint(self):
        """Test para el endpoint de dashboard de créditos"""
        url = reverse('insights:credits_dashboard')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertIn('page_info', response.data)
        
        # Verificar estructura de datos
        if response.data['results']:
            credit_data = response.data['results'][0]
            self.assertIn('uid', credit_data)
            self.assertIn('client_info', credit_data)
            self.assertIn('credit_details', credit_data)
            self.assertIn('payment_info', credit_data)
            self.assertIn('installment_info', credit_data)
            self.assertIn('calculated_metrics', credit_data)
            self.assertIn('seller_info', credit_data)
    
    def test_credits_dashboard_pagination(self):
        """Test para paginación del dashboard de créditos"""
        url = reverse('insights:credits_dashboard')
        response = self.client.get(url, {'page': 1, 'page_size': 25})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('page_info', response.data)
        self.assertEqual(response.data['page_info']['current_page'], 1)
        self.assertEqual(response.data['page_info']['page_size'], 25)
    
    def test_credits_dashboard_ordering(self):
        """Test para ordenamiento del dashboard de créditos"""
        url = reverse('insights:credits_dashboard')
        response = self.client.get(url, {'ordering': '-price'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_installments_collection_endpoint(self):
        """Test para el endpoint de recaudo esperado"""
        url = reverse('insights:installments_collection')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        
        # Verificar estructura de datos
        if response.data['results']:
            installment_data = response.data['results'][0]
            self.assertIn('id', installment_data)
            self.assertIn('credit_info', installment_data)
            self.assertIn('installment_details', installment_data)
            self.assertIn('payment_tracking', installment_data)
            self.assertIn('periodicity_info', installment_data)
            self.assertIn('calculated_metrics', installment_data)
            self.assertIn('client_history', installment_data)
    
    def test_dashboard_summary_endpoint(self):
        """Test para el endpoint de resumen del dashboard"""
        url = reverse('insights:dashboard_summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)
        self.assertIn('data', response.data)
        
        data = response.data['data']
        self.assertIn('credits_summary', data)
        self.assertIn('installments_summary', data)
        self.assertIn('performance_metrics', data)
        self.assertIn('by_periodicity', data)
        self.assertIn('alerts', data)
    
    def test_credits_analytics_endpoint(self):
        """Test para el endpoint de analytics de créditos"""
        url = reverse('insights:credits_analytics_advanced')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)
        self.assertIn('data', response.data)
        
        data = response.data['data']
        self.assertIn('analytics_by_state', data)
        self.assertIn('analytics_by_periodicity', data)
        self.assertIn('analytics_by_subcategory', data)
        self.assertIn('temporal_analytics', data)
        self.assertIn('filters_applied', data)
    
    def test_risk_analysis_endpoint(self):
        """Test para el endpoint de análisis de riesgo"""
        url = reverse('insights:risk_analysis_advanced')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)
        self.assertIn('data', response.data)
        
        data = response.data['data']
        self.assertIn('risk_by_morosidad', data)
        self.assertIn('high_risk_credits_count', data)
        self.assertIn('overdue_analysis', data)
        self.assertIn('potential_losses', data)
        self.assertIn('risk_alerts', data)

class CreditModelTestCase(TestCase):
    """Tests para los métodos del modelo Credit"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.currency = Currency.objects.create(
            currency='COP',
            id_currency='COP'
        )
        
        self.subcategory = SubCategory.objects.create(
            name='Préstamo Personal'
        )
        
        self.periodicity = Periodicity.objects.create(
            name='Semanal',
            days=7
        )
        
        self.account = Account.objects.create(
            name='Cuenta Principal'
        )
        
        self.credit = Credit.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            cost=Decimal('800000.00'),
            price=Decimal('1000000.00'),
            currency=self.currency,
            first_date_payment=date.today(),
            second_date_payment=date.today() + timedelta(days=70),
            credit_days=70,
            periodicity=self.periodicity,
            payment=self.account,
            state='pending'
        )
    
    def test_percentage_paid_property(self):
        """Test para la propiedad percentage_paid"""
        # Sin abonos
        self.assertEqual(self.credit.percentage_paid, 0)
        
        # Con abonos
        self.credit.total_abonos = Decimal('300000.00')
        self.assertEqual(self.credit.percentage_paid, 30.0)
        
        # Con abonos completos
        self.credit.total_abonos = Decimal('1000000.00')
        self.assertEqual(self.credit.percentage_paid, 100.0)
    
    def test_days_since_creation_property(self):
        """Test para la propiedad days_since_creation"""
        days = self.credit.days_since_creation
        self.assertIsInstance(days, int)
        self.assertGreaterEqual(days, 0)
    
    def test_credit_days_calculated_property(self):
        """Test para la propiedad credit_days_calculated"""
        days = self.credit.credit_days_calculated
        self.assertEqual(days, 70)
    
    def test_interest_rate_calculated_property(self):
        """Test para la propiedad interest_rate_calculated"""
        # Sin interés configurado
        rate = self.credit.interest_rate_calculated
        expected_rate = float((self.credit.earnings / self.credit.cost) * 100)
        self.assertEqual(rate, expected_rate)
        
        # Con interés configurado
        self.credit.interest = Decimal('2.5')
        rate = self.credit.interest_rate_calculated
        self.assertEqual(rate, 2.5)
    
    def test_installment_count_properties(self):
        """Test para las propiedades de conteo de cuotas"""
        # Crear cuotas de prueba
        for i in range(1, 6):
            status = 'paid' if i <= 2 else 'pending'
            Installment.objects.create(
                credit=self.credit,
                number=i,
                amount=Decimal('100000.00'),
                status=status
            )
        
        self.assertEqual(self.credit.paid_installments_count, 2)
        self.assertEqual(self.credit.total_installments_count, 5)
        self.assertEqual(self.credit.overdue_installments_count, 0)

class InstallmentModelTestCase(TestCase):
    """Tests para los métodos del modelo Installment"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.currency = Currency.objects.create(
            currency='COP',
            id_currency='COP'
        )
        
        self.subcategory = SubCategory.objects.create(
            name='Préstamo Personal'
        )
        
        self.periodicity = Periodicity.objects.create(
            name='Semanal',
            days=7
        )
        
        self.account = Account.objects.create(
            name='Cuenta Principal'
        )
        
        self.credit = Credit.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            cost=Decimal('800000.00'),
            price=Decimal('1000000.00'),
            currency=self.currency,
            first_date_payment=date.today(),
            second_date_payment=date.today() + timedelta(days=70),
            credit_days=70,
            periodicity=self.periodicity,
            payment=self.account,
            state='pending'
        )
        
        self.installment = Installment.objects.create(
            credit=self.credit,
            number=1,
            due_date=date.today() + timedelta(days=7),
            amount=Decimal('100000.00'),
            status='pending',
            amount_paid=Decimal('50000.00'),
            remaining_amount=Decimal('50000.00')
        )
    
    def test_days_until_due_property(self):
        """Test para la propiedad days_until_due"""
        days = self.installment.days_until_due
        self.assertIsInstance(days, int)
        self.assertGreater(days, 0)
    
    def test_is_overdue_property(self):
        """Test para la propiedad is_overdue"""
        # Cuota futura
        self.assertFalse(self.installment.is_overdue)
        
        # Cuota vencida
        self.installment.due_date = date.today() - timedelta(days=1)
        self.installment.save()
        self.assertTrue(self.installment.is_overdue)
    
    def test_percentage_paid_property(self):
        """Test para la propiedad percentage_paid"""
        percentage = self.installment.percentage_paid
        self.assertEqual(percentage, 50.0)
    
    def test_collection_priority_property(self):
        """Test para la propiedad collection_priority"""
        # Cuota futura
        priority = self.installment.collection_priority
        self.assertEqual(priority, 'low')
        
        # Cuota vencida
        self.installment.due_date = date.today() - timedelta(days=1)
        self.installment.save()
        priority = self.installment.collection_priority
        self.assertEqual(priority, 'high')
    
    def test_risk_level_property(self):
        """Test para la propiedad risk_level"""
        risk_level = self.installment.risk_level
        self.assertIn(risk_level, ['low', 'medium', 'high'])

class CalculationsTestCase(TestCase):
    """Tests para las funciones de cálculo"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        from apps.insights.utils.calculations import (
            calculate_percentage_paid,
            calculate_days_since_creation,
            calculate_risk_score
        )
        
        self.calculate_percentage_paid = calculate_percentage_paid
        self.calculate_days_since_creation = calculate_days_since_creation
        self.calculate_risk_score = calculate_risk_score
    
    def test_calculate_percentage_paid(self):
        """Test para calcular porcentaje pagado"""
        # Casos normales
        self.assertEqual(self.calculate_percentage_paid(300000, 1000000), 30.0)
        self.assertEqual(self.calculate_percentage_paid(1000000, 1000000), 100.0)
        self.assertEqual(self.calculate_percentage_paid(0, 1000000), 0)
        
        # Casos edge
        self.assertEqual(self.calculate_percentage_paid(0, 0), 0)
        self.assertEqual(self.calculate_percentage_paid(100000, 0), 0)
    
    def test_calculate_days_since_creation(self):
        """Test para calcular días desde creación"""
        from django.utils import timezone
        
        # Crear fecha de hace 5 días
        past_date = timezone.now() - timedelta(days=5)
        days = self.calculate_days_since_creation(past_date)
        self.assertEqual(days, 5)
        
        # Fecha futura
        future_date = timezone.now() + timedelta(days=5)
        days = self.calculate_days_since_creation(future_date)
        self.assertLess(days, 0)
    
    def test_calculate_risk_score(self):
        """Test para calcular puntuación de riesgo"""
        # Mock credit y installments
        class MockCredit:
            def __init__(self):
                self.morosidad_level = 'on_time'
                self.total_abonos = Decimal('300000.00')
                self.price = Decimal('1000000.00')
                self.created_at = timezone.now() - timedelta(days=30)
        
        class MockInstallments:
            def filter(self, **kwargs):
                return self
            
            def count(self):
                return 0
        
        credit = MockCredit()
        installments = MockInstallments()
        
        score = self.calculate_risk_score(credit, installments)
        self.assertIsInstance(score, (int, float))
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
