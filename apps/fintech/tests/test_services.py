from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta

from apps.fintech.models import (
    Credit, Installment, Transaction, AccountMethodAmount,
    User, Currency, Periodicity, SubCategory, Account
)
from apps.fintech.services.credit import CreditService, InstallmentService


class CreditServiceTestCase(TestCase):
    """Tests para CreditService"""
    
    def setUp(self):
        """Configurar datos de prueba"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.currency = Currency.objects.create(
            id_currency='USD',
            currency='Dólar',
            exchange_rate=1.0
        )
        
        self.periodicity = Periodicity.objects.create(
            name='Mensual',
            days=30
        )
        
        self.subcategory = SubCategory.objects.create(
            name='Préstamo Personal'
        )
        
        self.payment_account = Account.objects.create(
            name='Cuenta Principal',
            account_number='123456789',
            balance=Decimal('10000.00'),
            currency=self.currency
        )
        
        self.credit = Credit.objects.create(
            user=self.user,
            cost=Decimal('8000.00'),
            price=Decimal('10000.00'),
            currency=self.currency,
            credit_days=90,
            periodicity=self.periodicity,
            payment=self.payment_account,
            first_date_payment=timezone.now().date(),
            second_date_payment=timezone.now().date() + timedelta(days=90),
            description='Préstamo de prueba'
        )
    
    def test_create_transaction_from_payment(self):
        """Test de creación de transacción desde pago"""
        amount = Decimal('1000.00')
        description = 'Pago de prueba'
        
        success, result, status = CreditService.create_transaction_from_payment(
            credit_uid=self.credit.uid,
            amount=amount,
            description=description,
            user_id=self.user.id,
            subcategory_name='Préstamo Personal',
            payment_type='Efectivo'
        )
        
        self.assertTrue(success)
        self.assertEqual(status, 201)
        
        # Verificar que se creó la transacción
        transaction = Transaction.objects.filter(description=description).first()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.transaction_type, 'income')
        
        # Verificar que se creó el método de pago
        payment_method = AccountMethodAmount.objects.filter(
            credit=self.credit,
            transaction=transaction
        ).first()
        self.assertIsNotNone(payment_method)
        self.assertEqual(payment_method.amount_paid, amount)
        
        # Verificar actualización del crédito
        self.credit.refresh_from_db()
        self.assertEqual(self.credit.total_abonos, amount)

    def test_create_transaction_invalid_amount(self):
        """Test de creación de transacción con monto inválido"""
        success, message, status = CreditService.create_transaction_from_payment(
            credit_uid=self.credit.uid,
            amount=Decimal('0.00'),
            description='Pago inválido',
            user_id=self.user.id,
            subcategory_name='Préstamo Personal',
            payment_type='Efectivo'
        )
        
        self.assertFalse(success)
        self.assertEqual(status, 400)
        self.assertIn('monto debe ser mayor a 0', message)
    
    def test_get_credit_summary(self):
        """Test de obtención de resumen de crédito"""
        # Crear algunos pagos
        transaction1 = Transaction.objects.create(
            transaction_type='income',
            user=self.user,
            category=self.subcategory,
            description='Pago 1'
        )
        
        AccountMethodAmount.objects.create(
            payment_method=self.payment_account,
            payment_code='PAY_1',
            amount=Decimal('1000.00'),
            amount_paid=Decimal('1000.00'),
            credit=self.credit,
            transaction=transaction1
        )
        
        transaction2 = Transaction.objects.create(
            transaction_type='income',
            user=self.user,
            category=self.subcategory,
            description='Pago 2'
        )
        
        AccountMethodAmount.objects.create(
            payment_method=self.payment_account,
            payment_code='PAY_2',
            amount=Decimal('500.00'),
            amount_paid=Decimal('500.00'),
            credit=self.credit,
            transaction=transaction2
        )
        
        summary = CreditService.get_credit_summary(self.credit.uid)
        
        self.assertIsNotNone(summary)
        self.assertEqual(summary['total_paid'], Decimal('1500.00'))
        self.assertEqual(summary['remaining_amount'], Decimal('8500.00'))
        self.assertEqual(summary['payment_count'], 2)
    
    def test_update_credit_status(self):
        """Test de actualización de estado de crédito"""
        success, message = CreditService.update_credit_status(self.credit.uid)
        
        self.assertTrue(success)
        self.assertIn('actualizado exitosamente', message)
    
    def test_calculate_late_fees(self):
        """Test de cálculo de mora"""
        # Crear cuota vencida
        installment = self.credit.installments.first()
        installment.status = 'overdue'
        installment.days_overdue = 30
        installment.remaining_amount = Decimal('1000.00')
        installment.save()
        
        # Calcular mora
        late_fee = CreditService.calculate_late_fees(self.credit)
        
        # 5% por mes de mora
        expected_fee = Decimal('1000.00') * Decimal('0.05') * Decimal('1')
        self.assertEqual(late_fee, expected_fee)


class InstallmentServiceTestCase(TestCase):
    """Tests para InstallmentService"""
    
    def setUp(self):
        """Configurar datos de prueba"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.currency = Currency.objects.create(
            id_currency='USD',
            currency='Dólar',
            exchange_rate=1.0
        )
        
        self.periodicity = Periodicity.objects.create(
            name='Mensual',
            days=30
        )
        
        self.subcategory = SubCategory.objects.create(
            name='Préstamo Personal'
        )
        
        self.payment_account = Account.objects.create(
            name='Cuenta Principal',
            account_number='123456789',
            balance=Decimal('10000.00'),
            currency=self.currency
        )
        
        self.credit = Credit.objects.create(
            user=self.user,
            cost=Decimal('8000.00'),
            price=Decimal('10000.00'),
            currency=self.currency,
            credit_days=90,
            periodicity=self.periodicity,
            payment=self.payment_account,
            first_date_payment=timezone.now().date(),
            second_date_payment=timezone.now().date() + timedelta(days=90),
            description='Préstamo de prueba'
        )
    
    def test_generate_payment_schedule(self):
        """Test de generación de tabla de amortización"""
        schedule = InstallmentService.generate_payment_schedule(self.credit)
        
        self.assertEqual(len(schedule), 3)  # 3 cuotas
        
        for i, installment_data in enumerate(schedule):
            self.assertIn('number', installment_data)
            self.assertIn('due_date', installment_data)
            self.assertIn('amount', installment_data)
            self.assertEqual(installment_data['number'], i + 1)
    
    def test_process_installment_payment(self):
        """Test de procesamiento de pago de cuota"""
        installment = self.credit.installments.first()
        payment_amount = installment.amount
        
        success = InstallmentService.process_installment_payment(
            installment, payment_amount
        )
        
        self.assertTrue(success)
        
        installment.refresh_from_db()
        self.assertTrue(installment.paid)
        self.assertEqual(installment.status, 'paid')
        self.assertEqual(installment.amount_paid, payment_amount)
    
    def test_calculate_overdue_installments(self):
        """Test de cálculo de cuotas vencidas"""
        # Crear cuota vencida
        installment = self.credit.installments.first()
        installment.status = 'overdue'
        installment.days_overdue = 15
        installment.save()
        
        overdue_count = InstallmentService.calculate_overdue_installments(self.credit)
        
        self.assertEqual(overdue_count, 1)
    
    def test_apply_late_fees(self):
        """Test de aplicación de recargos por mora"""
        installment = self.credit.installments.first()
        installment.status = 'overdue'
        installment.days_overdue = 30
        installment.remaining_amount = Decimal('1000.00')
        installment.save()
        
        late_fee = InstallmentService.apply_late_fees(installment)
        
        # 5% por mes de mora
        expected_fee = Decimal('1000.00') * Decimal('0.05') * Decimal('1')
        self.assertEqual(late_fee, expected_fee)
        
        installment.refresh_from_db()
        self.assertEqual(installment.late_fee, expected_fee)
    
    def test_update_installment_statuses(self):
        """Test de actualización de estados de cuotas"""
        # Crear cuota vencida
        installment = self.credit.installments.first()
        installment.due_date = timezone.now().date() - timedelta(days=5)
        installment.status = 'pending'
        installment.save()
        
        success, message = InstallmentService.update_all_installment_statuses()
        
        self.assertTrue(success)
        
        installment.refresh_from_db()
        self.assertEqual(installment.status, 'overdue')
        self.assertEqual(installment.days_overdue, 5)
    
    def test_send_payment_reminders(self):
        """Test de envío de recordatorios de pago"""
        # Crear cuota que vence pronto
        installment = self.credit.installments.first()
        installment.due_date = timezone.now().date() + timedelta(days=2)
        installment.notification_sent = False
        installment.save()
        
        success, message = InstallmentService.schedule_payment_reminders()
        
        self.assertTrue(success)
        self.assertIn('recordatorios', message)
    
    def test_send_overdue_notifications(self):
        """Test de envío de notificaciones de cuotas vencidas"""
        # Crear cuota vencida
        installment = self.credit.installments.first()
        installment.status = 'overdue'
        installment.notification_sent = False
        installment.save()
        
        success, message = InstallmentService.send_overdue_notifications()
        
        self.assertTrue(success)
        self.assertIn('notificaciones', message) 