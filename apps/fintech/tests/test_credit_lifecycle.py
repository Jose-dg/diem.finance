from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta

from apps.fintech.models import (
    Credit, Installment, Transaction, AccountMethodAmount,
    User, Currency, Periodicity, SubCategory, Account, Category, CategoryType
)
from apps.fintech.services.credit_service import CreditService
from apps.fintech.services.installment_service import InstallmentService
from apps.fintech.utils.root import recalculate_credit


class CreditLifecycleTestCase(TestCase):
    """Test completo del ciclo de vida de un crédito"""
    
    def setUp(self):
        """Configurar datos de prueba"""
        # Deshabilitar notificaciones para los tests
        try:
            from apps.notifications.signals import disable_notifications
            disable_notifications()
        except ImportError:
            pass  # Si no existe la aplicación de notificaciones, continuar
        
        # Crear usuario usando el modelo User de fintech
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Crear moneda
        self.currency = Currency.objects.create(
            id_currency='USD',
            currency='Dólar',
            exchange_rate=1.0
        )
        
        # Crear periodicidad
        self.periodicity = Periodicity.objects.create(
            name='Mensual',
            days=30
        )
        
        # Crear categoría y subcategoría
        self.category_type = CategoryType.objects.create(
            name='Financiero'
        )
        
        self.category = Category.objects.create(
            name='Préstamos',
            category_type=self.category_type
        )
        
        self.subcategory = SubCategory.objects.create(
            name='Préstamo Personal',
            category=self.category
        )
        
        # Crear cuenta de pago
        self.payment_account = Account.objects.create(
            name='Cuenta Principal',
            account_number='123456789',
            balance=Decimal('10000.00'),
            currency=self.currency
        )
        
        # Datos del crédito
        self.credit_data = {
            'user': self.user,
            'cost': Decimal('8000.00'),
            'price': Decimal('10000.00'),
            'currency': self.currency,
            'credit_days': 90,
            'periodicity': self.periodicity,
            'payment': self.payment_account,
            'first_date_payment': timezone.now().date(),
            'second_date_payment': timezone.now().date() + timedelta(days=90),
            'description': 'Préstamo de prueba'
        }
    
    def tearDown(self):
        """Limpiar después de cada test"""
        # Habilitar notificaciones nuevamente
        try:
            from apps.notifications.signals import enable_notifications
            enable_notifications()
        except ImportError:
            pass
    
    def test_credit_creation_calculations(self):
        """Test de creación de crédito y cálculos automáticos"""
        # Crear crédito
        credit = Credit.objects.create(**self.credit_data)
        
        # Verificar cálculos automáticos
        self.assertEqual(credit.pending_amount, credit.price)
        self.assertEqual(credit.earnings, credit.price - credit.cost)
        self.assertEqual(credit.installment_number, 3)  # 90 días / 30 días
        self.assertIsNotNone(credit.installment_value)
        
        # Verificar que se generaron las cuotas
        installments = credit.installments.all()
        self.assertEqual(installments.count(), 3)
        
        # Verificar fechas de cuotas
        for i, installment in enumerate(installments):
            expected_date = credit.first_date_payment + timedelta(days=30 * i)
            self.assertEqual(installment.due_date, expected_date)
    
    def test_payment_flow_on_time(self):
        """Test de flujo de pagos puntuales"""
        credit = Credit.objects.create(**self.credit_data)
        installment = credit.installments.first()
        
        # Realizar pago puntual
        payment_amount = installment.amount
        
        # Crear transacción de pago
        transaction = Transaction.objects.create(
            transaction_type='income',
            user=self.user,
            category=self.subcategory,
            description='Pago puntual',
            date=timezone.now()
        )
        
        # Crear método de pago
        payment_method = AccountMethodAmount.objects.create(
            payment_method=self.payment_account,
            payment_code=f'PAY_{transaction.uid}',
            amount=payment_amount,
            amount_paid=payment_amount,
            credit=credit,
            transaction=transaction
        )
        
        # Verificar actualizaciones
        credit.refresh_from_db()
        installment.refresh_from_db()
        
        self.assertEqual(credit.total_abonos, payment_amount)
        self.assertEqual(credit.pending_amount, credit.price - payment_amount)
        self.assertTrue(installment.paid)
        self.assertEqual(installment.status, 'paid')
    
    def test_payment_flow_late(self):
        """Test de flujo de pagos tardíos"""
        credit = Credit.objects.create(**self.credit_data)
        installment = credit.installments.first()
        
        # Simular pago tardío (15 días después)
        payment_amount = installment.amount
        late_payment_date = installment.due_date + timedelta(days=15)
        
        # Crear transacción de pago tardío
        transaction = Transaction.objects.create(
            transaction_type='income',
            user=self.user,
            category=self.subcategory,
            description='Pago tardío',
            date=timezone.now()
        )
        
        payment_method = AccountMethodAmount.objects.create(
            payment_method=self.payment_account,
            payment_code=f'PAY_{transaction.uid}',
            amount=payment_amount,
            amount_paid=payment_amount,
            credit=credit,
            transaction=transaction
        )
        
        # Verificar estado de mora
        credit.refresh_from_db()
        installment.refresh_from_db()
        
        self.assertEqual(installment.days_overdue, 15)
        self.assertEqual(installment.status, 'paid')
        self.assertGreater(installment.late_fee, 0)
    
    def test_payment_flow_partial(self):
        """Test de flujo de pagos parciales"""
        credit = Credit.objects.create(**self.credit_data)
        installment = credit.installments.first()
        
        # Realizar pago parcial (50% de la cuota)
        partial_amount = installment.amount * Decimal('0.5')
        
        transaction = Transaction.objects.create(
            transaction_type='income',
            user=self.user,
            category=self.subcategory,
            description='Pago parcial',
            date=timezone.now()
        )
        
        payment_method = AccountMethodAmount.objects.create(
            payment_method=self.payment_account,
            payment_code=f'PAY_{transaction.uid}',
            amount=partial_amount,
            amount_paid=partial_amount,
            credit=credit,
            transaction=transaction
        )
        
        # Verificar estado parcial
        credit.refresh_from_db()
        installment.refresh_from_db()
        
        self.assertEqual(installment.status, 'partial')
        self.assertEqual(installment.amount_paid, partial_amount)
        self.assertEqual(installment.remaining_amount, installment.amount - partial_amount)
    
    def test_morosidad_states(self):
        """Test de estados de morosidad"""
        credit = Credit.objects.create(**self.credit_data)
        installment = credit.installments.first()
        
        # Simular cuota vencida sin pago
        installment.status = 'overdue'
        installment.days_overdue = 30
        installment.save()
        
        # Recalcular estado del crédito
        recalculate_credit(credit)
        credit.refresh_from_db()
        
        # Verificar estado de mora
        self.assertTrue(credit.is_in_default)
        self.assertEqual(credit.morosidad_level, 'alta')
        
        # Simular mora crítica
        installment.days_overdue = 90
        installment.save()
        
        recalculate_credit(credit)
        credit.refresh_from_db()
        
        self.assertEqual(credit.morosidad_level, 'critica')
    
    def test_credit_complete_lifecycle(self):
        """Test integral del ciclo de vida completo"""
        # 1. Crear crédito
        credit = Credit.objects.create(**self.credit_data)
        self.assertEqual(credit.state, 'pending')
        self.assertEqual(credit.installments.count(), 3)
        
        # 2. Realizar pago puntual
        first_installment = credit.installments.first()
        payment_amount = first_installment.amount
        
        transaction = Transaction.objects.create(
            transaction_type='income',
            user=self.user,
            category=self.subcategory,
            description='Pago puntual',
            date=timezone.now()
        )
        
        AccountMethodAmount.objects.create(
            payment_method=self.payment_account,
            payment_code=f'PAY_{transaction.uid}',
            amount=payment_amount,
            amount_paid=payment_amount,
            credit=credit,
            transaction=transaction
        )
        
        credit.refresh_from_db()
        self.assertEqual(credit.total_abonos, payment_amount)
        
        # 3. Realizar pago tardío
        second_installment = credit.installments.all()[1]
        second_installment.status = 'overdue'
        second_installment.days_overdue = 15
        second_installment.save()
        
        late_transaction = Transaction.objects.create(
            transaction_type='income',
            user=self.user,
            category=self.subcategory,
            description='Pago tardío',
            date=timezone.now()
        )
        
        AccountMethodAmount.objects.create(
            payment_method=self.payment_account,
            payment_code=f'PAY_{late_transaction.uid}',
            amount=second_installment.amount,
            amount_paid=second_installment.amount,
            credit=credit,
            transaction=late_transaction
        )
        
        # 4. Verificar cambio de estado
        recalculate_credit(credit)
        credit.refresh_from_db()
        
        self.assertTrue(credit.is_in_default)
        self.assertEqual(credit.morosidad_level, 'alta')
        
        # 5. Completar crédito
        third_installment = credit.installments.last()
        final_transaction = Transaction.objects.create(
            transaction_type='income',
            user=self.user,
            category=self.subcategory,
            description='Pago final',
            date=timezone.now()
        )
        
        AccountMethodAmount.objects.create(
            payment_method=self.payment_account,
            payment_code=f'PAY_{final_transaction.uid}',
            amount=third_installment.amount,
            amount_paid=third_installment.amount,
            credit=credit,
            transaction=final_transaction
        )
        
        # 6. Verificar estado final
        credit.refresh_from_db()
        self.assertEqual(credit.total_abonos, credit.price)
        self.assertEqual(credit.pending_amount, Decimal('0.00'))
        
        # Marcar como completado
        credit.state = 'completed'
        credit.save()
        
        self.assertEqual(credit.state, 'completed')
        self.assertFalse(credit.is_in_default)
    
    def test_installment_calculations(self):
        """Test de cálculos de cuotas"""
        credit = Credit.objects.create(**self.credit_data)
        
        for installment in credit.installments.all():
            # Verificar que el monto total de cuotas sea igual al precio
            self.assertEqual(installment.amount, credit.installment_value)
            
            # Verificar que la suma de cuotas sea igual al precio
            total_installments = sum(i.amount for i in credit.installments.all())
            self.assertEqual(total_installments, credit.price)
    
    def test_credit_recalculation(self):
        """Test de recálculo de crédito"""
        credit = Credit.objects.create(**self.credit_data)
        
        # Realizar pago
        installment = credit.installments.first()
        payment_amount = installment.amount
        
        transaction = Transaction.objects.create(
            transaction_type='income',
            user=self.user,
            category=self.subcategory,
            description='Pago de prueba',
            date=timezone.now()
        )
        
        AccountMethodAmount.objects.create(
            payment_method=self.payment_account,
            payment_code=f'PAY_{transaction.uid}',
            amount=payment_amount,
            amount_paid=payment_amount,
            credit=credit,
            transaction=transaction
        )
        
        # Recalcular crédito
        recalculate_credit(credit)
        credit.refresh_from_db()
        
        # Verificar cálculos actualizados
        self.assertEqual(credit.total_abonos, payment_amount)
        self.assertEqual(credit.pending_amount, credit.price - payment_amount)
        self.assertIsNotNone(credit.earnings) 