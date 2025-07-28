from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from apps.fintech.models import (
    User, Credit, Currency, Periodicity, Account, 
    Adjustment, CreditAdjustment, SubCategory, Category, CategoryType
)
from apps.fintech.services.credit_adjustment_service import CreditAdjustmentService


class CreditAdjustmentServiceTest(TestCase):
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear usuario
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Crear categorías
        self.category_type = CategoryType.objects.create(
            name='Test Category Type'
        )
        self.category = Category.objects.create(
            name='Test Category',
            category_type=self.category_type
        )
        self.subcategory = SubCategory.objects.create(
            name='Test SubCategory',
            category=self.category
        )
        
        # Crear moneda
        self.currency = Currency.objects.create(
            id_currency='USD',
            currency='US Dollar',
            exchange_rate=1.0
        )
        
        # Crear periodicidad
        self.periodicity = Periodicity.objects.create(
            name='Monthly',
            days=30
        )
        
        # Crear cuenta
        self.account = Account.objects.create(
            name='Test Account',
            currency=self.currency
        )
        
        # Crear ajuste de interés adicional
        self.adjustment = Adjustment.objects.create(
            code='C0001',
            name='Interés Adicional',
            description='Interés por incumplimiento de pagos pactados',
            is_positive=True
        )
        
        # Crear crédito con price > cost
        self.credit = Credit.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            cost=Decimal('100.00'),
            price=Decimal('105.00'),  # 5 de interés adicional
            currency=self.currency,
            first_date_payment=timezone.now().date(),
            second_date_payment=timezone.now().date() + timezone.timedelta(days=30),
            credit_days=60,
            periodicity=self.periodicity,
            payment=self.account,
            total_abonos=Decimal('80.00')  # Pagó menos del price
        )
    
    def test_calculate_additional_interest(self):
        """Test para calcular interés adicional"""
        # Calcular interés adicional
        additional_interest = CreditAdjustmentService.calculate_additional_interest(self.credit)
        
        # Debería ser price - cost = 105 - 100 = 5
        self.assertEqual(additional_interest, Decimal('5.00'))
    
    def test_should_apply_additional_interest(self):
        """Test para determinar si se debe aplicar interés adicional"""
        # Con total_abonos < price, debería aplicar
        should_apply = CreditAdjustmentService.should_apply_additional_interest(self.credit)
        self.assertTrue(should_apply)
        
        # Si paga el monto completo, no debería aplicar
        self.credit.total_abonos = Decimal('105.00')
        self.credit.save()
        
        should_apply = CreditAdjustmentService.should_apply_additional_interest(self.credit)
        self.assertFalse(should_apply)
    
    def test_apply_additional_interest(self):
        """Test para aplicar interés adicional"""
        # Aplicar interés adicional
        amount_applied = CreditAdjustmentService.apply_additional_interest(
            self.credit,
            reason="Test application"
        )
        
        # Verificar que se aplicó el monto correcto
        self.assertEqual(amount_applied, Decimal('5.00'))
        
        # Verificar que se creó el CreditAdjustment
        credit_adjustment = CreditAdjustment.objects.filter(
            credit=self.credit,
            type=self.adjustment
        ).first()
        
        self.assertIsNotNone(credit_adjustment)
        self.assertEqual(credit_adjustment.amount, Decimal('5.00'))
        self.assertEqual(credit_adjustment.reason, "Test application")
        
        # Verificar que se actualizó pending_amount
        self.credit.refresh_from_db()
        self.assertEqual(self.credit.pending_amount, Decimal('25.00'))  # 20 pendiente + 5 interés
    
    def test_apply_additional_interest_no_duplicate(self):
        """Test para evitar duplicados de interés adicional"""
        # Aplicar primera vez
        CreditAdjustmentService.apply_additional_interest(self.credit)
        
        # Intentar aplicar segunda vez
        amount_applied = CreditAdjustmentService.apply_additional_interest(self.credit)
        
        # Debería retornar el monto existente, no crear nuevo
        self.assertEqual(amount_applied, Decimal('5.00'))
        
        # Verificar que solo hay un CreditAdjustment
        adjustments = CreditAdjustment.objects.filter(
            credit=self.credit,
            type=self.adjustment
        )
        self.assertEqual(adjustments.count(), 1)
    
    def test_calculate_additional_interest_zero_when_price_equals_cost(self):
        """Test cuando price = cost, no hay interés adicional"""
        # Crear crédito con price = cost
        credit_equal = Credit.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            cost=Decimal('100.00'),
            price=Decimal('100.00'),  # Igual al cost
            currency=self.currency,
            first_date_payment=timezone.now().date(),
            second_date_payment=timezone.now().date() + timezone.timedelta(days=30),
            credit_days=60,
            periodicity=self.periodicity,
            payment=self.account,
            total_abonos=Decimal('80.00')
        )
        
        additional_interest = CreditAdjustmentService.calculate_additional_interest(credit_equal)
        self.assertEqual(additional_interest, Decimal('0.00'))
    
    def test_calculate_additional_interest_zero_when_price_less_than_cost(self):
        """Test cuando price < cost, no hay interés adicional"""
        # Crear crédito con price < cost
        credit_less = Credit.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            cost=Decimal('100.00'),
            price=Decimal('95.00'),  # Menor al cost
            currency=self.currency,
            first_date_payment=timezone.now().date(),
            second_date_payment=timezone.now().date() + timezone.timedelta(days=30),
            credit_days=60,
            periodicity=self.periodicity,
            payment=self.account,
            total_abonos=Decimal('80.00')
        )
        
        additional_interest = CreditAdjustmentService.calculate_additional_interest(credit_less)
        self.assertEqual(additional_interest, Decimal('0.00'))
    
    def test_get_total_adjustments(self):
        """Test para obtener total de ajustes"""
        # Aplicar interés adicional
        CreditAdjustmentService.apply_additional_interest(self.credit)
        
        # Obtener total de ajustes
        total_adjustments = CreditAdjustmentService.get_total_adjustments(self.credit)
        
        # Debería ser 5.00 (positivo)
        self.assertEqual(total_adjustments, Decimal('5.00'))
    
    def test_get_adjustment_history(self):
        """Test para obtener historial de ajustes"""
        # Aplicar interés adicional
        CreditAdjustmentService.apply_additional_interest(self.credit)
        
        # Obtener historial
        history = CreditAdjustmentService.get_adjustment_history(self.credit)
        
        # Debería tener 1 ajuste
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().amount, Decimal('5.00'))
    
    def test_get_adjustment_type(self):
        """Test para obtener tipo de ajuste"""
        adjustment_type = CreditAdjustmentService.get_adjustment_type()
        self.assertEqual(adjustment_type.code, 'C0001')
        self.assertEqual(adjustment_type.name, 'Interés Adicional')
    
    def test_get_adjustment_type_not_found(self):
        """Test cuando no existe el tipo de ajuste"""
        # Eliminar el ajuste
        self.adjustment.delete()
        
        # Debería lanzar ValueError
        with self.assertRaises(ValueError):
            CreditAdjustmentService.get_adjustment_type() 