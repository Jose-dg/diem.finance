from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth import get_user_model  
from django.db import transaction as db_transaction
from django.db import models, transaction as db_transaction
from django.utils import timezone
from decimal import ROUND_HALF_UP, Decimal
from django.conf import settings

import uuid
import math

from apps.fintech.managers import CreditManager, UserProfileManager, TransactionManager, InstallmentManager

class Country(models.Model):
    name = models.CharField(max_length=100)
    utc_offset = models.IntegerField() 

    def __str__(self):
        return f"{self.name}"

class ParamsLocation(models.Model):
    city_code = models.CharField(max_length=10, null=True, blank=True)
    city_name = models.CharField(max_length=50, null=True, blank=True)
    state_code = models.CharField(max_length=10, null=True, blank=True)
    state_name = models.CharField(max_length=50, null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    country_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.city_name}, {self.state_name}, {self.country_name}"

class PhoneNumber(models.Model):
    country_code = models.CharField(max_length=15)
    country_related = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.country_code} {self.country_related}"

class DocumentType(models.Model):
    code = models.CharField(max_length=2, unique=True)
    description = models.CharField(max_length=50)
    country_id = models.ForeignKey(Country, max_length=20, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.code} - {self.description}"

class Identifier(models.Model):
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    document_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.document_type.description} ({self.country}): {self.document_number}"

class Language(models.Model):
    name = models.CharField(max_length=100)
    region_of_use = models.CharField(max_length=100)  

    def __str__(self):
        return f"{self.name}"

class Label(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name}" 

class Address(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=50, choices=[('billing', 'Billing'), ('shipping', 'Shipping')])
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

class CategoryType(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    category_type = models.ForeignKey(CategoryType, on_delete=models.SET_NULL, null=True, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
class Currency(models.Model):
    TYPE_CHOICES = (
        ('FIAT', 'Moneda FIAT'),
        ('CRYPTO', 'Criptomoneda'),
        ('SECURITY', 'Título valor'),
    )

    asset_type = models.CharField(max_length=8, choices=TYPE_CHOICES, default='FIAT')
    id_currency = models.CharField(max_length=4, null=False, blank=False)
    # simbol 
    currency = models.CharField(max_length=15, null=False, blank=False)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=0)

    def __str__(self):
        return self.currency

class Account(models.Model):
    id_payment_method = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.ForeignKey(Currency, null=True, blank=True, on_delete=models.SET_NULL)
    
    # Campo Alegra para facturación electronica.
    eletronic_software_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

class Periodicity(models.Model):

    name = models.CharField(max_length=50)
    days = models.IntegerField()  # Número de días de la periodicidad

    def __str__(self):
        return f"{self.name}"

class AccountMethodAmount(models.Model):
    payment_method = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_code = models.CharField(max_length=100, null=False, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    currency = models.ForeignKey(Currency, null=True, blank=True, on_delete=models.SET_NULL)
    credit = models.ForeignKey('Credit', on_delete=models.CASCADE, related_name='payments')
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE, related_name='account_method_amounts')

    def __str__(self):
        return f"Payment method {self.payment_method.name} - Amount Paid: {self.amount_paid}"

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_staff_role = models.BooleanField(default=False)  

    def __str__(self):
        return self.name

class Seller(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='sellers')
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='seller_profile')
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    commissions = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    returns = models.IntegerField(default=0)

    def __str__(self):
        return f"Seller: {self.user}"
       
class User(AbstractUser):
    id_user = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    document = models.ForeignKey(Identifier, null=True, blank=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(ParamsLocation, null=True, blank=True, on_delete=models.SET_NULL)
    billing_address = models.CharField(max_length=255, default='')
    address_shipping = models.CharField(max_length=255, default='')
    phone_1 = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE, null=True, blank=True)
    label = models.ForeignKey(Label, null=True, blank=True, on_delete=models.CASCADE)
    reference_1 = models.CharField(max_length=255, null=True, blank=True)
    reference_2 = models.CharField(max_length=255, null=True, blank=True)
    electronic_id = models.CharField(max_length=50, blank=True, null=True)

    # Relación con Role
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)
    groups = models.ManyToManyField(
        Group,
        related_name='fintech_user_set',  # Cambia el related_name para evitar el conflicto
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=('groups'),
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='fintech_user_permissions_set',  # Cambia el related_name para evitar el conflicto
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )

    def __str__(self):
        return self.username

# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    
#     # Custom manager
#     objects = UserProfileManager()
    
#     monthly_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,help_text="Ingreso mensual del usuario.")
#     monthly_expenses = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,help_text="Gastos mensuales del usuario.")
#     monthly_savings = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,help_text="Ahorro mensual del usuario.")
#     monthly_investments = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,help_text="Inversiones mensuales del usuario.")
#     monthly_debt = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,help_text="Deuda mensual del usuario.")
#     monthly_credit_payments = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True,help_text="Pagos de crédito mensuales del usuario.")
    
#     income_source = models.CharField(max_length=255, null=True, blank=True,help_text="Fuente de ingresos del usuario.")
#     employment_type = models.CharField(max_length=20, choices=[
#             ('FULL_TIME', 'Tiempo Completo'),
#             ('PART_TIME', 'Medio Tiempo'),
#             ('CONTRACTOR', 'Contratista'),
#             ('SELF_EMPLOYED', 'Independiente'),
#             ('UNEMPLOYED', 'Desempleado'),
#             ('RETIRED', 'Jubilado'),
#         ], null=True, blank=True, help_text="Tipo de empleo del usuario.")
    
#     investment_experience = models.CharField(max_length=255, null=True, blank=True,help_text="Experiencia en inversiones del usuario.")
    
#     risk_tolerance = models.CharField(max_length=20, choices=[
#             ('VERY_LOW', 'Muy Bajo'),
#             ('LOW', 'Bajo'),
#             ('MODERATE', 'Moderado'),
#             ('HIGH', 'Alto'),
#             ('VERY_HIGH', 'Muy Alto'),
#         ], default='MODERATE', help_text="Tolerancia al riesgo del usuario."
#     )
    
#     # Verificación de información
#     info_verified = models.BooleanField(default=False,help_text="Verificación de información del usuario")

#     can_request_credit = models.BooleanField(default=True, help_text="Indica si el usuario puede solicitar créditos")
    
#     # Ratio deuda/ingreso calculado automáticamente
#     debt_to_income_ratio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Ratio deuda/ingreso calculado automáticamente")
#     restriction_reason = models.TextField(null=True, blank=True, help_text="Razón por la cual el usuario tiene restricciones")
#     financial_health_score = models.IntegerField(null=True, blank=True, help_text="Puntaje de salud financiera (0-100)")
    
#     # Timestamps
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = "Perfil de Usuario"
#         verbose_name_plural = "Perfiles de Usuario"

#     def __str__(self):
#         return f"{self.user.username} - Perfil"
    
#     def can_create_request(self, request_type):
#         """Valida si el usuario puede crear un tipo específico de solicitud"""
#         if not request_type:
#             return False, "Tipo de solicitud no especificado"
        
#         # Verificar si el tipo de solicitud requiere perfil completo
#         if request_type.requires_complete_profile and not self.is_profile_complete:
#             return False, "Debe completar su perfil financiero para este tipo de solicitud"
        
#         # Verificar restricciones específicas por tipo
#         if 'credit' in request_type.name.lower() or 'crédito' in request_type.name.lower():
#             if not self.can_request_credit:
#                 return False, self.restriction_reason or "No puede solicitar créditos en este momento"
        
#         if 'investment' in request_type.name.lower() or 'inversión' in request_type.name.lower():
#             if not self.can_request_investment:
#                 return False, self.restriction_reason or "No puede solicitar inversiones en este momento"
        
#         return True, "Solicitud permitida"

#     def calculate_debt_to_income_ratio(self):
#         """Calcula automáticamente el ratio deuda/ingreso"""
#         if self.monthly_income and self.monthly_debt:
#             if self.monthly_income > 0:
#                 ratio = (self.monthly_debt / self.monthly_income) * 100
#                 self.debt_to_income_ratio = round(ratio, 2)
#                 return self.debt_to_income_ratio
#         return None

#     def calculate_financial_health_score(self):
#         """Calcula el puntaje de salud financiera y lo almacena"""
#         if not self.monthly_income:
#             self.financial_health_score = None
#             return None
        
#         score = 0
        
#         # Tiene ahorros
#         if self.monthly_savings and self.monthly_savings > 0:
#             score += 25
        
#         # Tiene inversiones
#         if self.monthly_investments and self.monthly_investments > 0:
#             score += 25
        
#         # Ratio deuda/ingreso saludable (menos del 30%)
#         if self.debt_to_income_ratio and self.debt_to_income_ratio < 30:
#             score += 25
        
#         # Gastos controlados (menos del 80% de ingresos)
#         if self.monthly_expenses and self.monthly_income:
#             expense_ratio = (self.monthly_expenses / self.monthly_income) * 100
#             if expense_ratio < 80:
#                 score += 25
        
#         self.financial_health_score = score
#         return score

#     def save(self, *args, **kwargs):
#         """Override save para calcular automáticamente métricas"""
#         self.calculate_debt_to_income_ratio()
#         self.calculate_financial_health_score()
#         super().save(*args, **kwargs)

#     @property
#     def is_profile_complete(self):
#         """Verifica si el perfil tiene la información básica completa"""
#         required_fields = [
#             self.monthly_income,
#             self.monthly_expenses,
#             self.employment_type,
#             self.income_source
#         ]
#         return all(field is not None and field != '' for field in required_fields)

#     @property
#     def financial_health_category(self):
#         """Categoriza la salud financiera basada en el score"""
#         if self.financial_health_score is None:
#             return "Sin evaluar"
        
#         if self.financial_health_score >= 75:
#             return "Excelente"
#         elif self.financial_health_score >= 50:
#             return "Buena"
#         elif self.financial_health_score >= 25:
#             return "Regular"
#         else:
#             return "Necesita mejoras"

class Credit(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    ORDER_STATES = (
        ('checking', 'Checking'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('to_solve', 'To Solve'),
        ('preorder', 'Preorder')
    )
    
    # Custom manager
    objects = CreditManager()

    registered_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='credits_registered')
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True, related_name='credits_made') 
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='credits')

    state = models.CharField(max_length=15, choices=ORDER_STATES, default='pending')
    subcategory = models.ForeignKey('SubCategory', null=True, blank=True, on_delete=models.SET_NULL)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.ForeignKey('Currency', null=True, blank=False, on_delete=models.SET_NULL)
    earnings = models.DecimalField(max_digits=12, decimal_places=2, editable=False, null=True, blank=True, default=0.00)
    first_date_payment = models.DateField()
    second_date_payment = models.DateField()
    credit_days = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    interest = models.DecimalField(max_digits=5, decimal_places=2, editable=True, null=True, blank=True, default=0.00)
    periodicity = models.ForeignKey('Periodicity', on_delete=models.PROTECT)
    payment = models.ForeignKey('Account', on_delete=models.PROTECT, related_name='credit_payments')
    refinancing = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_abonos = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    pending_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    installment_number = models.IntegerField(null=True, blank=True)
    installment_value = models.DecimalField(max_digits=12, null=True, blank=True, decimal_places=2)
    is_in_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    morosidad_level = models.CharField(max_length=20, choices=[
        ('on_time', 'On Time'),
        ('mild_default', 'Mild Default'),
        ('moderate_default', 'Moderate Default'),
        ('severe_default', 'Severe Default'),
        ('recurrent_default', 'Recurrent Default'),
        ('critical_default', 'Critical Default')
    ], default='on_time')

    def __str__(self):
        return f"{self.uid} - {self.user} - {self.subcategory}: Credit:{self.price}, pending:{self.pending_amount}"

    def update_total_abonos(self, amount_paid_difference):
        """
        Actualiza el total de abonos realizados al crédito y recalcula el saldo pendiente.
        """
        self.total_abonos += Decimal(amount_paid_difference)
        self.update_pending_amount()

    def update_pending_amount(self):
        """
        Recalcula el saldo pendiente del crédito basado en el total de abonos.
        """
        self.pending_amount = self.price - self.total_abonos
        self.save()

    def save(self, *args, **kwargs):
        """
        Custom save method to initialize pending_amount and calculate interest, earnings,
        installment_number, and installment_value.
        """
        with db_transaction.atomic():
            is_new = self.pk is None
            cost = Decimal(self.cost)
            price = Decimal(self.price)
            credit_days = Decimal(self.credit_days)
            periodicity_days = Decimal(self.periodicity.days) if self.periodicity else Decimal(1)

            if is_new:
                self.pending_amount = self.price

            self.earnings = price - cost

            if cost and price and credit_days:
                self.interest = (Decimal(1) / (credit_days / Decimal(30))) * ((price - cost) / cost)

            if self.periodicity and self.credit_days:
                self.installment_number = math.ceil(self.credit_days / periodicity_days)
                if self.installment_number > 0:
                    self.installment_value = (price / Decimal(self.installment_number)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
                else:
                    self.installment_value = price

            super(Credit, self).save(*args, **kwargs)

class Transaction(models.Model):
    
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense')
    ]

    TRANSACTION_STATUSES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed'),
        ('reversed', 'Reversed')
    ]
    
    # Custom manager
    objects = TransactionManager()

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    category = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True, related_name='transactions')
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='transactions')
    agent = models.ForeignKey('Seller', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    status = models.CharField(max_length=50, choices=TRANSACTION_STATUSES, default='confirmed')
    
    source = models.CharField(max_length=50, choices=[
        ('web', 'Web App'),
        ('mobile', 'Mobile App'),
        ('admin', 'Admin Panel'),
        ('import', 'Imported Data'),
    ], default='admin')
    
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True, blank=True)
 
class Expense(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, related_name='expenses')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='expenses')
    registered_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='expenses')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='expense_made_by')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True) 

    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subcategory} - {self.amount}"

class Adjustment(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_positive = models.BooleanField(default=True)

    def __str__(self):
        sign = '+' if self.is_positive else '-'
        return f"{self.name} ({sign}{self.code})"
    
class CreditAdjustment(models.Model):
    credit = models.ForeignKey('Credit',on_delete=models.CASCADE,related_name='adjustments',null=True,blank=True)
    type = models.ForeignKey('Adjustment', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    added_on = models.DateField(default=timezone.now)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-added_on']

    def __str__(self):
        signo = '+' if self.type and self.type.is_positive else '-'
        return f"{self.type.name if self.type else 'Tipo desconocido'} {signo}${self.amount} al crédito {self.credit_id or 'sin asignar'} ({self.added_on})"

class Installment(models.Model):
    # Custom manager
    objects = InstallmentManager()
    
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name='installments', null=True, blank=True)
    number = models.PositiveIntegerField(null=True, blank=True, help_text="Número de cuota")
    due_date = models.DateField(null=True, blank=True, help_text="Fecha de vencimiento de la cuota")
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Monto de la cuota")
    paid = models.BooleanField(default=False, help_text="Indica si la cuota ha sido pagada")
    paid_on = models.DateField(null=True, blank=True, help_text="Fecha en la cual se realizó el pago")
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), null=True, blank=True, help_text="Monto aplicado a capital")
    interest_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), null=True, blank=True, help_text="Monto aplicado a intereses")
    late_fee = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), null=True, blank=True, help_text="Recargo por mora si aplica")
    
    # NUEVOS CAMPOS PARA ROBUSTEZ
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pendiente'),
        ('paid', 'Pagada'),
        ('overdue', 'Vencida'),
        ('cancelled', 'Cancelada'),
        ('partial', 'Pago Parcial')
    ], default='pending', help_text="Estado actual de la cuota")
    
    # NOTIFICACIONES
    notification_sent = models.BooleanField(default=False, help_text="Indica si se envió notificación")
    reminder_count = models.PositiveIntegerField(default=0, help_text="Número de recordatorios enviados")
    last_reminder_date = models.DateTimeField(null=True, blank=True, help_text="Fecha del último recordatorio")
    next_reminder_date = models.DateTimeField(null=True, blank=True, help_text="Fecha del próximo recordatorio")
    
    # PAGOS PARCIALES
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), help_text="Monto pagado hasta ahora")
    remaining_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), help_text="Monto restante por pagar")
    
    # MORA
    days_overdue = models.PositiveIntegerField(default=0, help_text="Días de mora")
    
    # PROGRAMACIÓN
    is_scheduled = models.BooleanField(default=False, help_text="Indica si está programada para pago automático")
    scheduled_payment_date = models.DateField(null=True, blank=True, help_text="Fecha programada para pago automático")
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('credit', 'number')
        ordering = ['due_date']

    def mark_as_paid(self, amount_paid=None):
        if amount_paid is None:
            amount_paid = self.amount
        
        self.amount_paid = amount_paid
        self.remaining_amount = self.amount - self.amount_paid
        
        if self.remaining_amount <= 0:
            self.status = 'paid'
            self.paid = True
        else:
            self.status = 'partial'
        
        self.paid_on = timezone.now().date()
        self.save()

    def is_overdue(self):
        return self.status == 'pending' and self.due_date and timezone.now().date() > self.due_date

    def get_total_amount_due(self):
        return self.remaining_amount + self.late_fee

    def __str__(self):
        return f"Cuota #{self.number or '?'} de {self.credit_id} - Vence: {self.due_date or 'sin fecha'} - Estado: {self.status}"