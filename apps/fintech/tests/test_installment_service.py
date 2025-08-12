from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from apps.fintech.models import Credit, Installment, User, Currency, Periodicity, Account
from apps.fintech.services.credit import InstallmentService


class InstallmentServiceTestCase(TestCase):
    """Tests para InstallmentService optimizado"""
    
    def setUp(self):
        """Configuración inicial"""
        # Crear usuario
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Crear moneda
        self.currency = Currency.objects.create(
            id_currency='USD',
            currency='US Dollar',
            asset_type='FIAT',
            exchange_rate=Decimal('1.00')
        )
        
        # Crear periodicidad
        self.periodicity = Periodicity.objects.create(
            name='Mensual',
            days=30
        )
        
        # Crear cuenta
        self.account = Account.objects.create(
            name='Test Account',
            balance=Decimal('0.00'),
            currency=self.currency
        )
        
        # Crear crédito
        self.credit = Credit.objects.create(
            user=self.user,
            cost=Decimal('8000.00'),
            price=Decimal('10000.00'),
            installment_number=12,
            installment_value=Decimal('833.33'),
            first_date_payment=timezone.now().date(),
            second_date_payment=timezone.now().date() + timedelta(days=365),
            credit_days=365,
            periodicity=self.periodicity,
            currency=self.currency,
            state='pending',
            payment=self.account
        )
    
    def test_generate_installments_for_credit(self):
        """Test generar cuotas para un crédito"""
        success, message = InstallmentService.generate_installments_for_credit(self.credit)
        
        self.assertTrue(success)
        # Verificar que se generaron las cuotas correctas
        # 365 días / 30 días = 12.17, redondeado hacia arriba = 13 cuotas
        self.assertEqual(self.credit.installments.count(), 13)
        
        # Verificar primera cuota
        first_installment = self.credit.installments.first()
        self.assertEqual(first_installment.number, 1)
        # El monto se calcula automáticamente: 10000 / 13 = 769.23
        self.assertEqual(first_installment.amount, Decimal('769.23'))
        self.assertEqual(first_installment.status, 'pending')
        self.assertIsNotNone(first_installment.next_reminder_date)
    
    def test_update_all_installment_statuses(self):
        """Test actualizar estados de cuotas"""
        # Crear cuotas
        InstallmentService.generate_installments_for_credit(self.credit)
        
        # Marcar algunas como vencidas
        overdue_installment = self.credit.installments.first()
        overdue_installment.due_date = timezone.now().date() - timedelta(days=5)
        overdue_installment.save()
        
        # Actualizar estados
        success, message = InstallmentService.update_all_installment_statuses()
        
        self.assertTrue(success)
        overdue_installment.refresh_from_db()
        self.assertEqual(overdue_installment.status, 'overdue')
        self.assertGreater(overdue_installment.days_overdue, 0)
    
    def test_get_pending_installments_summary(self):
        """Test obtener resumen de cuotas pendientes"""
        # Crear cuotas
        InstallmentService.generate_installments_for_credit(self.credit)
        
        # Obtener resumen
        success, summary = InstallmentService.get_pending_installments_summary()
        
        self.assertTrue(success)
        self.assertIn('total_pending', summary)
        self.assertIn('total_overdue', summary)
        self.assertIn('due_today', summary)
        self.assertIn('due_this_week', summary)
    
    def test_get_expected_collection(self):
        """Test calcular recaudo esperado"""
        # Crear cuotas
        InstallmentService.generate_installments_for_credit(self.credit)
        
        # Calcular recaudo esperado para este mes
        start_date = timezone.now().date().replace(day=1)
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        success, collection = InstallmentService.get_expected_collection(start_date, end_date)
        
        self.assertTrue(success)
        self.assertIn('total_expected', collection)
        self.assertIn('total_remaining', collection)
        self.assertIn('count_installments', collection)
    
    def test_bulk_update_remaining_amounts(self):
        """Test actualizar montos restantes en batch"""
        # Crear cuotas
        InstallmentService.generate_installments_for_credit(self.credit)
        
        # Hacer un pago parcial
        installment = self.credit.installments.first()
        installment.amount_paid = Decimal('400.00')
        installment.save()
        
        # Actualizar montos restantes
        success, message = InstallmentService.bulk_update_remaining_amounts()
        
        self.assertTrue(success)
        installment.refresh_from_db()
        # 769.23 - 400.00 = 369.23
        self.assertEqual(installment.remaining_amount, Decimal('369.23'))
    
    def test_schedule_payment_reminders(self):
        """Test programar recordatorios de pago"""
        # Crear cuotas
        InstallmentService.generate_installments_for_credit(self.credit)
        
        # Programar recordatorios
        success, message = InstallmentService.schedule_payment_reminders()
        
        self.assertTrue(success)
        self.assertIn("Se programaron", message)
    
    def test_send_overdue_notifications(self):
        """Test enviar notificaciones de cuotas vencidas"""
        # Crear cuotas
        InstallmentService.generate_installments_for_credit(self.credit)
        
        # Marcar como vencida
        installment = self.credit.installments.first()
        installment.due_date = timezone.now().date() - timedelta(days=5)
        installment.status = 'overdue'
        installment.save()
        
        # Enviar notificaciones
        success, message = InstallmentService.send_overdue_notifications()
        
        self.assertTrue(success)
        self.assertIn("Se enviaron", message)
        
        installment.refresh_from_db()
        self.assertTrue(installment.notification_sent)
        self.assertGreater(installment.reminder_count, 0)
    
    def test_calculate_credit_morosidad(self):
        """Test calcular morosidad de un crédito"""
        # Crear cuotas
        InstallmentService.generate_installments_for_credit(self.credit)
        
        # Marcar algunas como vencidas
        overdue_installments = self.credit.installments.all()[:3]
        for installment in overdue_installments:
            installment.status = 'overdue'
            installment.save()
        
        # Calcular morosidad
        morosidad_rate = InstallmentService.calculate_credit_morosidad(self.credit)
        
        self.assertEqual(morosidad_rate, 23.08)  # 3 de 13 cuotas = 23.08%
    
    def test_get_installment_analytics(self):
        """Test obtener analytics de cuotas"""
        # Crear cuotas
        InstallmentService.generate_installments_for_credit(self.credit)
        
        # Obtener analytics
        success, analytics = InstallmentService.get_installment_analytics()
        
        self.assertTrue(success)
        self.assertIn('summary', analytics)
        self.assertIn('overdue_summary', analytics)
        self.assertIn('due_today', analytics)
        self.assertIn('due_this_week', analytics)
        self.assertIn('high_risk', analytics) 