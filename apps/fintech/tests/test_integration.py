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
from apps.fintech.services.transaction import TransactionService
from apps.fintech.utils.root import recalculate_credit

User = get_user_model()


class CreditIntegrationTestCase(TestCase):
    """Tests de integración para el sistema completo de créditos"""
    
    def setUp(self):
        """Configurar datos de prueba"""
        # Crear usuario
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
        
        # Crear subcategoría
        self.subcategory = SubCategory.objects.create(
            name='Préstamo Personal'
        )
        
        # Crear cuenta de pago
        self.payment_account = Account.objects.create(
            name='Cuenta Principal',
            account_number='123456789',
            balance=Decimal('10000.00'),
            currency=self.currency
        )
    
    def test_credit_complete_lifecycle(self):
        """Test integral del ciclo de vida completo de un crédito"""
        
        # 1. CREAR CRÉDITO
        credit_data = {
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
        
        credit = Credit.objects.create(**credit_data)
        
        # Verificar creación
        self.assertEqual(credit.state, 'pending')
        self.assertEqual(credit.pending_amount, credit.price)
        self.assertEqual(credit.installments.count(), 3)
        
        # 2. REALIZAR PAGO PUNTUAL
        first_installment = credit.installments.first()
        payment_amount = first_installment.amount
        
        success, result, status_code = TransactionService.create_payment_transaction(
            credit=credit,
            amount=payment_amount,
            method=self.payment_account
        )
        
        self.assertTrue(success)
        self.assertEqual(status_code, 201)
        
        # Verificar actualización
        credit.refresh_from_db()
        self.assertEqual(credit.total_abonos, payment_amount)
        self.assertEqual(credit.pending_amount, credit.price - payment_amount)
        
        # Verificar cuota pagada
        first_installment.refresh_from_db()
        self.assertTrue(first_installment.paid)
        self.assertEqual(first_installment.status, 'paid')
        
        # 3. REALIZAR PAGO TARDÍO
        second_installment = credit.installments.all()[1]
        
        # Simular cuota vencida
        second_installment.status = 'overdue'
        second_installment.days_overdue = 15
        second_installment.save()
        
        # Realizar pago tardío
        success, result, status_code = TransactionService.create_payment_transaction(
            credit=credit,
            amount=second_installment.amount,
            method=self.payment_account
        )
        
        self.assertTrue(success)
        
        # Verificar mora aplicada
        second_installment.refresh_from_db()
        self.assertGreater(second_installment.late_fee, 0)
        
        # 4. VERIFICAR CAMBIO DE ESTADO
        CreditService.update_credit_status(credit)
        credit.refresh_from_db()
        
        # Como hay cuotas vencidas, debe estar en mora
        self.assertTrue(credit.is_in_default)
        self.assertEqual(credit.morosidad_level, 'alta')
        
        # 5. COMPLETAR CRÉDITO
        third_installment = credit.installments.last()
        
        success, result, status_code = TransactionService.create_payment_transaction(
            credit=credit,
            amount=third_installment.amount,
            method=self.payment_account
        )
        
        self.assertTrue(success)
        
        # 6. VERIFICAR ESTADO FINAL
        credit.refresh_from_db()
        self.assertEqual(credit.total_abonos, credit.price)
        self.assertEqual(credit.pending_amount, Decimal('0.00'))
        
        # Marcar como completado
        credit.state = 'completed'
        credit.save()
        
        self.assertEqual(credit.state, 'completed')
        self.assertFalse(credit.is_in_default)
    
    def test_payment_flow_scenarios(self):
        """Test de diferentes escenarios de pago"""
        
        # Crear crédito
        credit = Credit.objects.create(
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
        
        # ESCENARIO 1: Pago puntual
        installment = credit.installments.first()
        success, result, status_code = TransactionService.create_payment_transaction(
            credit=credit,
            amount=installment.amount,
            method=self.payment_account
        )
        
        self.assertTrue(success)
        installment.refresh_from_db()
        self.assertEqual(installment.status, 'paid')
        
        # ESCENARIO 2: Pago parcial
        second_installment = credit.installments.all()[1]
        partial_amount = second_installment.amount * Decimal('0.5')
        
        success, result, status_code = TransactionService.create_payment_transaction(
            credit=credit,
            amount=partial_amount,
            method=self.payment_account
        )
        
        self.assertTrue(success)
        second_installment.refresh_from_db()
        self.assertEqual(second_installment.status, 'partial')
        self.assertEqual(second_installment.amount_paid, partial_amount)
        
        # ESCENARIO 3: Pago tardío con mora
        third_installment = credit.installments.last()
        third_installment.status = 'overdue'
        third_installment.days_overdue = 30
        third_installment.save()
        
        success, result, status_code = TransactionService.create_payment_transaction(
            credit=credit,
            amount=third_installment.amount,
            method=self.payment_account
        )
        
        self.assertTrue(success)
        third_installment.refresh_from_db()
        self.assertGreater(third_installment.late_fee, 0)
    
    def test_morosidad_states_transitions(self):
        """Test de transiciones de estados de morosidad"""
        
        # Crear crédito
        credit = Credit.objects.create(
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
        
        # ESTADO 1: Al día
        CreditService.update_credit_status(credit)
        credit.refresh_from_db()
        self.assertEqual(credit.morosidad_level, 'al_dia')
        self.assertFalse(credit.is_in_default)
        
        # ESTADO 2: Mora leve (30 días)
        installment = credit.installments.first()
        installment.status = 'overdue'
        installment.days_overdue = 30
        installment.save()
        
        CreditService.update_credit_status(credit)
        credit.refresh_from_db()
        self.assertEqual(credit.morosidad_level, 'leve')
        self.assertTrue(credit.is_in_default)
        
        # ESTADO 3: Mora moderada (60 días)
        installment.days_overdue = 60
        installment.save()
        
        CreditService.update_credit_status(credit)
        credit.refresh_from_db()
        self.assertEqual(credit.morosidad_level, 'moderada')
        
        # ESTADO 4: Mora alta (90 días)
        installment.days_overdue = 90
        installment.save()
        
        CreditService.update_credit_status(credit)
        credit.refresh_from_db()
        self.assertEqual(credit.morosidad_level, 'alta')
        
        # ESTADO 5: Mora crítica (120 días)
        installment.days_overdue = 120
        installment.save()
        
        CreditService.update_credit_status(credit)
        credit.refresh_from_db()
        self.assertEqual(credit.morosidad_level, 'critica')
    
    def test_transaction_reversal(self):
        """Test de reversión de transacciones"""
        
        # Crear crédito
        credit = Credit.objects.create(
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
        
        # Crear transacción
        success, result, status_code = TransactionService.create_payment_transaction(
            credit=credit,
            amount=Decimal('1000.00'),
            method=self.payment_account
        )
        
        self.assertTrue(success)
        
        # Obtener transacción creada
        transaction = result['transaction']
        
        # Verificar estado inicial
        credit.refresh_from_db()
        initial_total = credit.total_abonos
        
        # Reversar transacción
        success, result, status_code = TransactionService.reverse_transaction(transaction.id)
        
        self.assertTrue(success)
        self.assertEqual(status_code, 200)
        
        # Verificar reversión
        credit.refresh_from_db()
        self.assertEqual(credit.total_abonos, initial_total - Decimal('1000.00'))
        
        # Verificar transacción original
        transaction.refresh_from_db()
        self.assertEqual(transaction.status, 'reversed')
    
    def test_payment_reconciliation(self):
        """Test de conciliación de pagos"""
        
        # Crear crédito
        credit = Credit.objects.create(
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
        
        # Realizar varios pagos
        payments = [Decimal('3000.00'), Decimal('4000.00'), Decimal('3000.00')]
        
        for payment_amount in payments:
            success, result, status_code = TransactionService.create_payment_transaction(
                credit=credit,
                amount=payment_amount,
                method=self.payment_account
            )
            self.assertTrue(success)
        
        # Conciliar pagos
        success, reconciliation_data = TransactionService.reconcile_payments(credit)
        
        self.assertTrue(success)
        self.assertTrue(reconciliation_data['is_reconciled'])
        self.assertEqual(reconciliation_data['total_paid'], credit.price)
        self.assertEqual(reconciliation_data['payment_count'], 3)
    
    def test_credit_metrics_calculation(self):
        """Test de cálculo de métricas de crédito"""
        
        # Crear crédito
        credit = Credit.objects.create(
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
        
        # Realizar pagos parciales
        TransactionService.create_payment_transaction(
            credit=credit,
            amount=Decimal('3000.00'),
            method=self.payment_account
        )
        
        # Crear cuota vencida
        installment = credit.installments.first()
        installment.status = 'overdue'
        installment.days_overdue = 15
        installment.save()
        
        # Calcular métricas
        metrics = CreditService.get_credit_metrics(credit)
        
        self.assertIsNotNone(metrics)
        self.assertEqual(metrics['total_amount'], credit.price)
        self.assertEqual(metrics['total_paid'], Decimal('3000.00'))
        self.assertEqual(metrics['remaining_amount'], credit.price - Decimal('3000.00'))
        self.assertEqual(metrics['installment_count'], 3)
        self.assertEqual(metrics['overdue_installments'], 1)
        self.assertGreater(metrics['late_fees'], 0)
    
    def test_installment_service_integration(self):
        """Test de integración con InstallmentService"""
        
        # Crear crédito
        credit = Credit.objects.create(
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
        
        # Generar tabla de amortización
        schedule = InstallmentService.generate_payment_schedule(credit)
        
        self.assertEqual(len(schedule), 3)
        
        # Actualizar estados de cuotas
        success, message = InstallmentService.update_all_installment_statuses()
        self.assertTrue(success)
        
        # Calcular cuotas vencidas
        overdue_count = InstallmentService.calculate_overdue_installments(credit)
        self.assertEqual(overdue_count, 0)  # No hay cuotas vencidas inicialmente
        
        # Crear cuota vencida
        installment = credit.installments.first()
        installment.due_date = timezone.now().date() - timedelta(days=5)
        installment.status = 'pending'
        installment.save()
        
        # Recalcular
        success, message = InstallmentService.update_all_installment_statuses()
        self.assertTrue(success)
        
        overdue_count = InstallmentService.calculate_overdue_installments(credit)
        self.assertEqual(overdue_count, 1) 