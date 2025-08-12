from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.fintech.models import (
    Credit, Transaction, AccountMethodAmount, CreditAdjustment,
    SubCategory, Currency, Periodicity, Account
)
from apps.fintech.services.credit import CreditBalanceService
from apps.fintech.utils.root import recalculate_credit

User = get_user_model()

class CreditBalanceServiceTestCase(TestCase):
    """
    Tests para el servicio de gestión de saldos de créditos
    """
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear datos de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.currency = Currency.objects.create(
            id_currency='COP',
            currency='Peso Colombiano',
            exchange_rate=1.0
        )
        
        self.periodicity = Periodicity.objects.create(
            name='Diario',
            days=1
        )
        
        self.account = Account.objects.create(
            name='Cuenta de Prueba',
            currency=self.currency
        )
        
        self.subcategory = SubCategory.objects.create(
            name='Préstamo Personal',
            category_id=1  # Asumiendo que existe
        )
        
        # Crear crédito de prueba
        self.credit = Credit.objects.create(
            user=self.user,
            price=Decimal('1000.00'),
            cost=Decimal('800.00'),
            currency=self.currency,
            periodicity=self.periodicity,
            payment=self.account,
            subcategory=self.subcategory,
            first_date_payment=timezone.now().date(),
            second_date_payment=timezone.now().date() + timezone.timedelta(days=30),
            credit_days=30,
            pending_amount=Decimal('1000.00'),
            total_abonos=Decimal('0.00')
        )
    
    def test_calculate_real_payments(self):
        """Test para calcular pagos reales"""
        # Crear transacciones de prueba
        transaction1 = Transaction.objects.create(
            transaction_type='income',
            user=self.user,
            category=self.subcategory,
            description='Pago 1',
            date=timezone.now(),
            status='confirmed'
        )
        
        AccountMethodAmount.objects.create(
            payment_method=self.account,
            payment_code='PAY_001',
            amount=Decimal('100.00'),
            amount_paid=Decimal('100.00'),
            credit=self.credit,
            transaction=transaction1
        )
        
        transaction2 = Transaction.objects.create(
            transaction_type='income',
            user=self.user,
            category=self.subcategory,
            description='Pago 2',
            date=timezone.now(),
            status='confirmed'
        )
        
        AccountMethodAmount.objects.create(
            payment_method=self.account,
            payment_code='PAY_002',
            amount=Decimal('200.00'),
            amount_paid=Decimal('200.00'),
            credit=self.credit,
            transaction=transaction2
        )
        
        # Calcular pagos reales
        real_payments = CreditBalanceService.calculate_real_payments(self.credit)
        
        # Verificar resultado
        self.assertEqual(real_payments, Decimal('300.00'))
    
    def test_calculate_total_adjustments(self):
        """Test para calcular ajustes totales"""
        # Crear ajustes de prueba
        CreditAdjustment.objects.create(
            credit=self.credit,
            amount=Decimal('50.00'),
            reason='Ajuste de prueba 1'
        )
        
        CreditAdjustment.objects.create(
            credit=self.credit,
            amount=Decimal('25.00'),
            reason='Ajuste de prueba 2'
        )
        
        # Calcular ajustes totales
        total_adjustments = CreditBalanceService.calculate_total_adjustments(self.credit)
        
        # Verificar resultado
        self.assertEqual(total_adjustments, Decimal('75.00'))
    
    def test_calculate_expected_pending(self):
        """Test para calcular saldo pendiente esperado"""
        # Crear pagos y ajustes
        transaction = Transaction.objects.create(
            transaction_type='income',
            user=self.user,
            category=self.subcategory,
            description='Pago de prueba',
            date=timezone.now(),
            status='confirmed'
        )
        
        AccountMethodAmount.objects.create(
            payment_method=self.account,
            payment_code='PAY_001',
            amount=Decimal('300.00'),
            amount_paid=Decimal('300.00'),
            credit=self.credit,
            transaction=transaction
        )
        
        CreditAdjustment.objects.create(
            credit=self.credit,
            amount=Decimal('50.00'),
            reason='Ajuste de prueba'
        )
        
        # Calcular saldo esperado
        expected_pending = CreditBalanceService.calculate_expected_pending(self.credit)
        
        # Verificar resultado: 1000 + 50 - 300 = 750
        self.assertEqual(expected_pending, Decimal('750.00'))
    
    def test_validate_credit_balance_consistent(self):
        """Test para validar saldo consistente"""
        # Crear pago que coincida con total_abonos
        transaction = Transaction.objects.create(
            transaction_type='income',
            user=self.user,
            category=self.subcategory,
            description='Pago de prueba',
            date=timezone.now(),
            status='confirmed'
        )
        
        AccountMethodAmount.objects.create(
            payment_method=self.account,
            payment_code='PAY_001',
            amount=Decimal('300.00'),
            amount_paid=Decimal('300.00'),
            credit=self.credit,
            transaction=transaction
        )
        
        # Actualizar crédito para que sea consistente
        self.credit.total_abonos = Decimal('300.00')
        self.credit.pending_amount = Decimal('700.00')
        self.credit.save()
        
        # Validar saldo
        validation = CreditBalanceService.validate_credit_balance(self.credit)
        
        # Verificar que es consistente
        self.assertTrue(validation['is_consistent'])
        self.assertEqual(validation['abonos_difference'], Decimal('0.00'))
        self.assertEqual(validation['pending_difference'], Decimal('0.00'))
    
    def test_validate_credit_balance_inconsistent(self):
        """Test para validar saldo inconsistente"""
        # Crear pago real
        transaction = Transaction.objects.create(
            transaction_type='income',
            user=self.user,
            category=self.subcategory,
            description='Pago de prueba',
            date=timezone.now(),
            status='confirmed'
        )
        
        AccountMethodAmount.objects.create(
            payment_method=self.account,
            payment_code='PAY_001',
            amount=Decimal('300.00'),
            amount_paid=Decimal('300.00'),
            credit=self.credit,
            transaction=transaction
        )
        
        # Dejar crédito con datos inconsistentes
        self.credit.total_abonos = Decimal('200.00')  # Menos de lo real
        self.credit.pending_amount = Decimal('800.00')  # Más de lo real
        self.credit.save()
        
        # Validar saldo
        validation = CreditBalanceService.validate_credit_balance(self.credit)
        
        # Verificar que es inconsistente
        self.assertFalse(validation['is_consistent'])
        self.assertGreater(validation['abonos_difference'], Decimal('0.01'))
        self.assertGreater(validation['pending_difference'], Decimal('0.01'))
    
    def test_fix_credit_balance(self):
        """Test para corregir saldo de crédito"""
        # Crear pago real
        transaction = Transaction.objects.create(
            transaction_type='income',
            user=self.user,
            category=self.subcategory,
            description='Pago de prueba',
            date=timezone.now(),
            status='confirmed'
        )
        
        AccountMethodAmount.objects.create(
            payment_method=self.account,
            payment_code='PAY_001',
            amount=Decimal('300.00'),
            amount_paid=Decimal('300.00'),
            credit=self.credit,
            transaction=transaction
        )
        
        # Dejar crédito con datos inconsistentes
        self.credit.total_abonos = Decimal('200.00')
        self.credit.pending_amount = Decimal('800.00')
        self.credit.save()
        
        # Corregir saldo
        result = CreditBalanceService.fix_credit_balance(self.credit)
        
        # Verificar que se corrigió exitosamente
        self.assertTrue(result['success'])
        self.assertIn('changes', result)
        
        # Verificar que los cambios se aplicaron
        self.credit.refresh_from_db()
        self.assertEqual(self.credit.total_abonos, Decimal('300.00'))
        self.assertEqual(self.credit.pending_amount, Decimal('700.00'))
    
    def test_process_payment_safely(self):
        """Test para procesar pago de manera segura"""
        # Procesar pago
        result = CreditBalanceService.process_payment_safely(
            self.credit,
            Decimal('300.00')
        )
        
        # Verificar que fue exitoso
        self.assertTrue(result['success'])
        self.assertIn('transaction', result)
        self.assertIn('payment_method', result)
        self.assertIn('remaining_amount', result)
        self.assertIn('validation', result)
        
        # Verificar que el saldo se actualizó correctamente
        self.credit.refresh_from_db()
        self.assertEqual(self.credit.pending_amount, Decimal('700.00'))
        self.assertEqual(self.credit.total_abonos, Decimal('300.00'))
    
    def test_process_payment_exceeds_balance(self):
        """Test para pago que excede el saldo"""
        # Intentar pago mayor al saldo pendiente
        result = CreditBalanceService.process_payment_safely(
            self.credit,
            Decimal('1500.00')  # Mayor que el saldo de 1000
        )
        
        # Verificar que falló
        self.assertFalse(result['success'])
        self.assertIn('error', result)
        self.assertIn('excede', result['error'])
    
    def test_get_credit_summary(self):
        """Test para obtener resumen de crédito"""
        # Crear algunos datos de prueba
        transaction = Transaction.objects.create(
            transaction_type='income',
            user=self.user,
            category=self.subcategory,
            description='Pago de prueba',
            date=timezone.now(),
            status='confirmed'
        )
        
        AccountMethodAmount.objects.create(
            payment_method=self.account,
            payment_code='PAY_001',
            amount=Decimal('300.00'),
            amount_paid=Decimal('300.00'),
            credit=self.credit,
            transaction=transaction
        )
        
        CreditAdjustment.objects.create(
            credit=self.credit,
            amount=Decimal('50.00'),
            reason='Ajuste de prueba'
        )
        
        # Obtener resumen
        summary = CreditBalanceService.get_credit_summary(self.credit)
        
        # Verificar estructura del resumen
        self.assertIn('credit_uid', summary)
        self.assertIn('user', summary)
        self.assertIn('price', summary)
        self.assertIn('validation', summary)
        self.assertIn('transactions_count', summary)
        self.assertIn('adjustments_count', summary)
        
        # Verificar valores
        self.assertEqual(summary['price'], 1000.0)
        self.assertEqual(summary['transactions_count'], 1)
        self.assertEqual(summary['adjustments_count'], 1)
    
    def test_batch_validate_credits(self):
        """Test para validación por lotes"""
        # Crear crédito adicional
        credit2 = Credit.objects.create(
            user=self.user,
            price=Decimal('500.00'),
            cost=Decimal('400.00'),
            currency=self.currency,
            periodicity=self.periodicity,
            payment=self.account,
            subcategory=self.subcategory,
            first_date_payment=timezone.now().date(),
            second_date_payment=timezone.now().date() + timezone.timedelta(days=30),
            credit_days=30,
            pending_amount=Decimal('500.00'),
            total_abonos=Decimal('0.00')
        )
        
        # Validar lote
        results = CreditBalanceService.batch_validate_credits([self.credit, credit2])
        
        # Verificar resultados
        self.assertEqual(results['total_credits'], 2)
        self.assertIn('consistent_credits', results)
        self.assertIn('inconsistent_credits', results)
        self.assertIn('errors', results)
        self.assertIn('details', results)
        self.assertEqual(len(results['details']), 2) 