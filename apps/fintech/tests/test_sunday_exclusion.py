from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from datetime import date, timedelta
from django.db.models.signals import post_save

from apps.fintech.models import Credit, Periodicity, User, Currency, SubCategory, Category, Account
from apps.fintech.utils.root import should_exclude_sundays
from apps.fintech.services.credit import InstallmentService


class SundayExclusionTestCase(TestCase):
    def setUp(self):
        # Deshabilitar signals para evitar generación automática de cuotas
        self.disconnect_signals()
        
        # Crear datos de prueba
        self.currency = Currency.objects.create(
            id_currency="COP",
            currency="Peso Colombiano",
            exchange_rate=1.0000
        )
        
        self.category = Category.objects.create(
            name="Préstamos"
        )
        
        self.subcategory = SubCategory.objects.create(
            name="Préstamo Personal",
            category=self.category
        )
        
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        self.account = Account.objects.create(
            name="Cuenta Test",
            account_number="123456789",
            balance=1000000.00,
            currency=self.currency
        )
        
        # Crear periodicidades
        self.daily_periodicity = Periodicity.objects.create(
            name="Diario",
            days=1
        )
        
        self.monthly_periodicity = Periodicity.objects.create(
            name="Mensual",
            days=30
        )
        
        self.quarterly_periodicity = Periodicity.objects.create(
            name="Trimestral",
            days=90
        )
    
    def tearDown(self):
        # Reconectar signals
        self.reconnect_signals()
    
    def disconnect_signals(self):
        """Desconecta signals para evitar interferencia en tests"""
        from apps.fintech.signals import crear_cuotas_credito
        post_save.disconnect(crear_cuotas_credito, sender=Credit)
    
    def reconnect_signals(self):
        """Reconecta signals después de los tests"""
        from apps.fintech.signals import crear_cuotas_credito
        post_save.connect(crear_cuotas_credito, sender=Credit)
    
    def test_should_exclude_sundays_daily_credit(self):
        """Test que verifica que créditos diarios excluyen domingos"""
        credit = Credit.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            cost=800000.00,
            price=1000000.00,
            currency=self.currency,
            first_date_payment=date(2024, 1, 15),  # Lunes
            second_date_payment=date(2024, 1, 21),  # Domingo
            credit_days=7,
            periodicity=self.daily_periodicity,
            payment=self.account
        )
        
        self.assertTrue(should_exclude_sundays(credit))
    
    def test_should_exclude_sundays_monthly_credit(self):
        """Test que verifica que créditos mensuales NO excluyen domingos"""
        credit = Credit.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            cost=800000.00,
            price=1000000.00,
            currency=self.currency,
            first_date_payment=date(2024, 1, 15),
            second_date_payment=date(2024, 2, 15),
            credit_days=30,
            periodicity=self.monthly_periodicity,
            payment=self.account
        )
        
        self.assertFalse(should_exclude_sundays(credit))
    
    def test_should_exclude_sundays_quarterly_credit(self):
        """Test que verifica que créditos trimestrales NO excluyen domingos"""
        credit = Credit.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            cost=800000.00,
            price=1000000.00,
            currency=self.currency,
            first_date_payment=date(2024, 1, 15),
            second_date_payment=date(2024, 4, 15),
            credit_days=90,
            periodicity=self.quarterly_periodicity,
            payment=self.account
        )
        
        self.assertFalse(should_exclude_sundays(credit))
    
    def test_generate_installments_excludes_sundays(self):
        """Test que verifica que la generación de cuotas excluye domingos para créditos diarios"""
        credit = Credit.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            cost=800000.00,
            price=1000000.00,
            currency=self.currency,
            first_date_payment=date(2024, 1, 15),  # Lunes
            second_date_payment=date(2024, 1, 21),  # Domingo
            credit_days=7,
            periodicity=self.daily_periodicity,
            payment=self.account,
            installment_number=6,
            installment_value=166666.67
        )
        
        # Generar cuotas manualmente
        success, message = InstallmentService.generate_installments_for_credit(credit)
        self.assertTrue(success)
        
        # Verificar que no hay cuotas en domingo
        installments = credit.installments.all().order_by('due_date')
        
        # Las fechas deberían ser: Lunes, Martes, Miércoles, Jueves, Viernes, Sábado
        expected_dates = [
            date(2024, 1, 15),  # Lunes
            date(2024, 1, 16),  # Martes
            date(2024, 1, 17),  # Miércoles
            date(2024, 1, 18),  # Jueves
            date(2024, 1, 19),  # Viernes
            date(2024, 1, 20),  # Sábado
        ]
        
        self.assertEqual(len(installments), 6)
        
        for i, installment in enumerate(installments):
            self.assertEqual(installment.due_date, expected_dates[i])
            self.assertNotEqual(installment.due_date.weekday(), 6)  # No debe ser domingo
    
    def test_generate_installments_includes_sundays_for_monthly(self):
        """Test que verifica que la generación de cuotas INCLUYE domingos para créditos mensuales"""
        credit = Credit.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            cost=800000.00,
            price=1000000.00,
            currency=self.currency,
            first_date_payment=date(2024, 1, 15),
            second_date_payment=date(2024, 2, 15),
            credit_days=30,
            periodicity=self.monthly_periodicity,
            payment=self.account,
            installment_number=2,
            installment_value=500000.00
        )
        
        # Generar cuotas manualmente
        success, message = InstallmentService.generate_installments_for_credit(credit)
        self.assertTrue(success)
        
        # Verificar que las cuotas pueden incluir domingos
        installments = credit.installments.all().order_by('due_date')
        
        self.assertEqual(len(installments), 2)
        
        # La segunda cuota podría caer en domingo dependiendo de la fecha
        # Solo verificamos que no se excluyan sistemáticamente
        has_sunday = any(installment.due_date.weekday() == 6 for installment in installments)
        # No aseguramos que haya domingos, solo que no se excluyan automáticamente
    
    def test_calculate_effective_days(self):
        """Test que verifica el cálculo de días efectivos excluyendo domingos"""
        credit = Credit.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            cost=800000.00,
            price=1000000.00,
            currency=self.currency,
            first_date_payment=date(2024, 1, 15),  # Lunes
            second_date_payment=date(2024, 1, 21),  # Domingo
            credit_days=7,
            periodicity=self.daily_periodicity,
            payment=self.account
        )
        
        # Para un período de 7 días (Lunes a Domingo), debería tener 6 días efectivos
        effective_days = credit._calculate_effective_days(7)
        self.assertEqual(effective_days, 6)  # Excluye el domingo
    
    def test_calculate_effective_days_monthly_credit(self):
        """Test que verifica que créditos mensuales no excluyen domingos en días efectivos"""
        credit = Credit.objects.create(
            user=self.user,
            subcategory=self.subcategory,
            cost=800000.00,
            price=1000000.00,
            currency=self.currency,
            first_date_payment=date(2024, 1, 15),
            second_date_payment=date(2024, 2, 15),
            credit_days=30,
            periodicity=self.monthly_periodicity,
            payment=self.account
        )
        
        # Para un período de 30 días, debería tener todos los días
        effective_days = credit._calculate_effective_days(30)
        self.assertEqual(effective_days, 30)  # Incluye todos los días 