from django.db import models
from django.utils import timezone
from django.conf import settings
import uuid


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
        return f"{self.country_code} {self.phone_number}"


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
    currency = models.CharField(max_length=15, null=False, blank=False)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=0)

    def __str__(self):
        return self.currency


class Periodicity(models.Model):

    name = models.CharField(max_length=50)
    days = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


__all__ = [
    'Country', 'ParamsLocation', 'PhoneNumber', 'DocumentType', 'Identifier', 'Language',
    'Label', 'CategoryType', 'Category', 'SubCategory', 'Currency', 'Periodicity'
]
