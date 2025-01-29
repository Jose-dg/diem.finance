from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import AccountMethodAmount, DocumentType, Label, Seller, User, Address, CategoryType, Category, SubCategory, Account, Transaction, Credit, Expense, PhoneNumber, Country, ParamsLocation, Identifier, Language, Currency, Periodicity, Role
from django import forms
from .models import Transaction, Credit

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
    
class AddressInline(admin.TabularInline):
    model = Address
    extra = 1  # Número de direcciones extra para añadir por defecto

@admin.register(Address)
class AddressAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'address_type', 'address', 'city', 'country')
    search_fields = ('user__username', 'address', 'city', 'country__name')

class UserAdminWithAddress(UserAdmin):
    inlines = [AddressInline]

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_staff_role')  # Muestra el nombre del rol y el grupo asociado
    search_fields = ('name', 'is_staff_role')  # Permite búsqueda por nombre del rol y del grupo

@admin.register(DocumentType)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')

@admin.register(CategoryType)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', )

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at', 'updated_at')
    search_fields = ('name', 'category')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'category_type', 'created_at', 'updated_at')
    search_fields = ('name', 'category_type')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_number', 'currency', 'balance')
    search_fields = ('name', 'account_number', 'currency')

@admin.register(Label)
class LabelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'position')
    search_fields = ('name', 'position')
  
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'subcategory', 'amount', 'account', 'date', 'registered_by')
    search_fields = ('account__name', 'registered_by__username')

@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('country_code',)
    search_fields = ('country_code',) 

@admin.register(Country)
class CountryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'utc_offset')
    search_fields = ('name',)

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

class AccountMethodAmountInline(admin.TabularInline):
    model = AccountMethodAmount
    extra = 1
    autocomplete_fields = ['credit'] 

    def get_queryset(self, request):
        """
        Muestra solo los créditos en estado 'pending' del usuario seleccionado en la transacción.
        """
        qs = super().get_queryset(request)
        user_id = request.GET.get("user")  # Obtener usuario desde la URL

        if user_id:  # Si se seleccionó un usuario, filtrar créditos
            return qs.filter(credit__user_id=user_id, credit__state='pending')

        return qs.none()  # Si no hay usuario, no mostrar nada

 
class TransactionAdminForm(forms.ModelForm):
    class Meta:
        list_display = ('transaction_type', 'category', 'get_currency', 'get_client', 'date')
        model = Transaction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 🔹 Solo filtrar si 'user' existe en el formulario
        if 'user' in self.fields:
            self.fields['user'].queryset = User.objects.all()

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    form = TransactionAdminForm
    list_display = ('transaction_type', 'category', 'get_currency', 'get_client', 'date', 'display_payment_method', 'display_amount_paid')
    search_fields = ('transaction_type', 'category__name', 'user__username')
    inlines = [AccountMethodAmountInline]
    autocomplete_fields = ['user']  # Permitir búsqueda rápida de usuario

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filtra los créditos activos ('pending') del usuario seleccionado en la transacción.
        """
        if db_field.name == "credit":
            user_id = request.GET.get("user")  # Obtener el usuario desde la URL del admin
            if user_id:
                kwargs["queryset"] = Credit.objects.filter(user_id=user_id, state='pending')  # Solo créditos activos del usuario
            else:
                kwargs["queryset"] = Credit.objects.none()  # Si no hay usuario seleccionado, el queryset es vacío
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = ('admin/js/filter_credits.js',)  # Cargar el script para actualización dinámica

    def get_currency(self, obj):
        inline = obj.account_method_amounts.first()
        return inline.currency if inline else "No Currency"
    get_currency.short_description = 'Currency'

    def get_client(self, obj):
        return obj.user.username if obj.user else "No Client"
    get_client.short_description = 'Client'

    def display_payment_method(self, obj):
        inline = obj.account_method_amounts.first()
        return inline.payment_method.name if inline else "No Payment Method"
    display_payment_method.short_description = 'Payment Method'

    def display_amount_paid(self, obj):
        inline = obj.account_method_amounts.first()
        return inline.amount_paid if inline else "No Amount Paid"
    display_amount_paid.short_description = 'Amount Paid'

@admin.register(Credit)
class CreditAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'uid', 'state', 'created_at', 'description', 'morosidad_level', 'user', 'cost', 'price', 
        'credit_days', 'earnings', 'interest', 'periodicity', 'total_abonos','pending_amount', 
        'installment_number', 'installment_value'
    )
    search_fields = ('uid', 'user__username')

    exclude = ('interest', 'refinancing', 'total_abonos', 'pending_amount', 'installment_number', 'installment_value', 'is_in_default', 'morosidad_level')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.registered_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(ParamsLocation)
class ParamsLocationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('city_name', 'state_name', 'country_name', 'city_code', 'state_code', 'country_code')
    search_fields = ('city_name', 'state_name', 'country_name', 'city_code', 'state_code', 'country_code')

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_sales', 'commissions', 'returns')
    search_fields = ('user__username',)

    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'Seller Username'