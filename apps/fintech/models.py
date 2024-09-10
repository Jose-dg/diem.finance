from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid
from django.contrib.auth import get_user_model  
from decimal import ROUND_HALF_UP, Decimal
from datetime import datetime
import math
from django.db import transaction as db_transaction

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
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    is_staff_role = models.BooleanField(default=False)  

    def __str__(self):
        return self.name
        
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


class Credit(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Estados de orden, también puede quedarse como choices
    ORDER_STATES = (
        ('checking', 'Checking'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('to_solve', 'To Solve'),
        ('preorder', 'Preorder')
    )

    # Aquí ahora referenciamos el modelo User en lugar de get_user_model()
    registered_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='credits_registered')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credits')

    state = models.CharField(max_length=15, choices=ORDER_STATES, default='pending')
    subcategory = models.ForeignKey(SubCategory, null=True, blank=True, on_delete=models.SET_NULL)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.ForeignKey(Currency, null=True, blank=False, on_delete=models.SET_NULL)
    earnings = models.DecimalField(max_digits=12, decimal_places=2, editable=False, null=True, blank=True, default=0.00)
    first_date_payment = models.DateField()
    second_date_payment = models.DateField()
    credit_days = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    interest = models.DecimalField(max_digits=5, decimal_places=2, editable=True, null=True, blank=True, default=0.00)
    periodicity = models.ForeignKey(Periodicity, null=True, blank=True, on_delete=models.SET_NULL)
    payment = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL, related_name='credit_payments')
    refinancing = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_abonos = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    pending_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    installment_number = models.IntegerField(null=True, blank=True)
    installment_value = models.DecimalField(max_digits=12, null=True, blank=True, decimal_places=2)
    is_in_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Manejo de morosidad
    morosidad_level = models.CharField(max_length=20, choices=[
        ('on_time', 'On Time'),
        ('mild_default', 'Mild Default'),
        ('moderate_default', 'Moderate Default'),
        ('severe_default', 'Severe Default'),
        ('recurrent_default', 'Recurrent Default'),
        ('critical_default', 'Critical Default')
    ], default='on_time')

    def __str__(self):
        return f"{self.user} - {self.subcategory}: Credit:{self.price}, pending:{self.pending_amount}"

    def save(self, *args, **kwargs):
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
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='transactions')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='transactions')
    credit = models.ForeignKey(Credit, on_delete=models.SET_NULL, null=True, related_name='transactions')
    date = models.DateTimeField(default=datetime.now)
    description = models.TextField(null=True, blank=True)
 
    def save(self, *args, **kwargs):
        with db_transaction.atomic():
            super(Transaction, self).save(*args, **kwargs)  # Guarda la transacción primero

            # Si la transacción es un abono (income) y está asociada a un crédito
            if self.transaction_type == 'income' and self.credit:
                inline_abono = self.account_method_amounts.first()  # Obtenemos el inline recién agregado
                if inline_abono:
                    self.credit.update_pending_amount(inline_abono.amount_paid)  # Actualiza el saldo pendiente en el crédito
                    self.credit.save()  # Guarda el crédito actualizado


class Expense(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='expenses')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='expenses')
    registered_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='expenses')
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"