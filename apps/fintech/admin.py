from django.contrib import admin
from .models import AccountMethodAmount, DocumentType, Label, User, Address, CategoryType, Category, SubCategory, Account, Transaction, Credit, Expense, PhoneNumber, Country, ParamsLocation, Identifier, Language, Currency, Periodicity, Role
from django.utils.functional import SimpleLazyObject
from django.contrib.auth import get_user_model

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_document', 'get_country', 'get_city', 'get_phone_1')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'document__document_number')

    def get_document(self, obj):
        return obj.document.document_number if obj.document else None
    get_document.short_description = 'Document Number'

    def get_country(self, obj):
        return obj.country.name if obj.country else None
    get_country.short_description = 'Country'

    def get_city(self, obj):
        return obj.city.city_name if obj.city else None
    get_city.short_description = 'City'

    def get_phone_1(self, obj):
        return obj.phone_1.phone_number if obj.phone_1 else None
    get_phone_1.short_description = 'Phone 1'
    
# Inline para manejar las direcciones directamente en el admin de usuarios
class AddressInline(admin.TabularInline):
    model = Address
    extra = 1  # Número de direcciones extra para añadir por defecto

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_type', 'address', 'city', 'country')
    search_fields = ('user__username', 'address', 'city', 'country__name')

# Agregar el Inline de direcciones al admin de usuarios
class UserAdminWithAddress(UserAdmin):
    inlines = [AddressInline]


# Admin para el modelo Role
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')  # Muestra el nombre del rol y el grupo asociado
    search_fields = ('name', 'group__name')  # Permite búsqueda por nombre del rol y del grupo

# Registrar otros modelos como ya lo tienes
@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = (
        'uid', 'state', 'morosidad_level', 'client', 'cost', 'price', 
        'credit_days', 'earnings', 'interest', 'periodicity', 'total_abonos','pending_amount', 
        'installment_number', 'installment_value'
    )
    search_fields = ('uid', 'client__username')

    exclude = ('interest', 'refinancing', 'total_abonos', 'pending_amount', 'installment_number', 'installment_value', 'is_in_default', 'morosidad_level')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_by":
            kwargs["queryset"] = get_user_model().objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.registered_by = request.user
        super().save_model(request, obj, form, change)

# Registrar otros modelos sin cambios significativos
@admin.register(DocumentType)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')

@admin.register(CategoryType)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', )

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at', 'updated_at')
    search_fields = ('name', 'category')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'created_at', 'updated_at')
    search_fields = ('name', 'category_type')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_number', 'currency', 'balance')
    search_fields = ('name', 'account_number', 'currency')

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    search_fields = ('name', 'position')
   
class AccountMethodAmountInline(admin.TabularInline):
    model = AccountMethodAmount
    extra = 1

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('uid', 'transaction_type', 'display_currency', 'display_client', 'date')
    search_fields = ('transaction_type', 'description')

    def display_currency(self, obj):
        return obj.credit.currency if obj.credit else None

    def display_client(self, obj):
        return obj.credit.client if obj.credit else None

    display_currency.short_description = 'Currency'
    display_client.short_description = 'Client'

admin.site.register(Transaction, TransactionAdmin)
    
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'account', 'date', 'registered_by')
    search_fields = ('category__name', 'account__name', 'registered_by__username')

@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('country_code',)
    search_fields = ('country_code',) 

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'utc_offset')
    search_fields = ('name',)

@admin.register(ParamsLocation)
class CityAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'state_name', 'country_name')
    search_fields = ('city_name', 'state_name', 'country_name')

@admin.register(Identifier)
class IdAdmin(admin.ModelAdmin):
    list_display = ('document_type', 'document_number', 'country')
    search_fields = ('document_number', 'country__name')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'region_of_use')
    search_fields = ('name', 'region_of_use')

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('currency', 'asset_type', 'exchange_rate')
    search_fields = ('currency', 'asset_type')

@admin.register(Periodicity)
class PeriodicityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
