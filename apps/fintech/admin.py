from django.contrib import admin
from django.contrib import messages

from .models import (
    AccountMethodAmount, 
    Adjustment, CreditAdjustment, 
    DocumentType, 
    Installment, 
    Label, 
    Seller, 
    User, 
    Address, 
    CategoryType, 
    Category, 
    SubCategory, 
    Account, 
    Transaction, 
    Credit, 
    Expense, 
    PhoneNumber, 
    Country, ParamsLocation, 
    Identifier, 
    Language, 
    Currency, 
    Periodicity, 
    Role
    )
from django import forms
from django.core.exceptions import ValidationError
from .models import Transaction, Credit
from django.db.models import Q
from apps.fintech.services.utils import InstallmentCalculator


def change_credit_state_to_solve(modeladmin, request, queryset):
    """
    Acción personalizada para cambiar el estado de créditos seleccionados de 'pending' a 'to_solve'
    """
    # Filtrar solo los créditos que están en estado 'pending'
    pending_credits = queryset.filter(state='pending')
    
    if not pending_credits.exists():
        messages.warning(request, 'No hay créditos en estado "pending" seleccionados.')
        return
    
    # Actualizar el estado a 'to_solve'
    updated_count = pending_credits.update(state='to_solve')
    
    if updated_count > 0:
        messages.success(request, f'Se cambió el estado de {updated_count} crédito(s) de "pending" a "to_solve".')
    else:
        messages.warning(request, 'No se pudo actualizar ningún crédito.')

change_credit_state_to_solve.short_description = "Cambiar estado a 'To Solve' (solo créditos pending)"

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
class AddressAdmin(admin.ModelAdmin):
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
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'description')
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
class LabelAdmin(admin.ModelAdmin):
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
class CountryAdmin(admin.ModelAdmin):
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

class TransactionAdminForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si estamos editando una transacción existente, aseguramos que se filtre el usuario
        if self.instance and self.instance.pk:
            self.fields['user'].queryset = User.objects.filter(pk=self.instance.user.pk)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    form = TransactionAdminForm
    list_display = ( 'transaction_type',  'category',  'get_currency',  'get_client',  'date',  'display_payment_method',  'display_amount_paid', 'agent',  'status', 'source')
    search_fields = ('transaction_type', 'category__name', 'user__username', 'agent__user__username')
    autocomplete_fields = ['user', 'agent']
    inlines = [AccountMethodAmountInline]

    def save_model(self, request, obj, form, change):
        """
        Asigna un valor por defecto a `source` si no se ha establecido.
        """
        if not obj.source:  # 🔹 Si `source` está vacío, asignarlo
            obj.source = 'admin'
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        """
        Pasar el objeto actual a request para que los inlines lo usen en `formfield_for_foreignkey()`.
        """
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)

    def get_currency(self, obj):
        """
        Retorna la moneda de la primera cuenta de método de pago asociada a la transacción.
        """
        inline = obj.account_method_amounts.first()
        return inline.currency if inline else "No Currency"
    get_currency.short_description = 'Currency'

    def get_client(self, obj):
        """
        Retorna el nombre de usuario del cliente asociado a la transacción.
        """
        return obj.user.username if obj.user else "No Client"
    get_client.short_description = 'Client'

    def display_payment_method(self, obj):
        """
        Retorna el método de pago de la primera cuenta de método de pago asociada a la transacción.
        """
        inline = obj.account_method_amounts.first()
        return inline.payment_method.name if inline else "No Payment Method"
    display_payment_method.short_description = 'Payment Method'

    def display_amount_paid(self, obj):
        """
        Retorna el monto pagado de la primera cuenta de método de pago asociada a la transacción.
        """
        inline = obj.account_method_amounts.first()
        return inline.amount_paid if inline else "No Amount Paid"
    display_amount_paid.short_description = 'Amount Paid'

    class Media:
        js = ('admin/js/filter_credits.js',)

# Inline para ingresar cuotas manualmente al crear/editar un crédito
class InstallmentInline(admin.TabularInline):
    model = Installment
    extra = 1  # Mostrar 1 fila vacía por defecto para agregar cuotas
    fields = ('number', 'due_date', 'amount', 'status')
    
    # Campos de solo lectura (opcionales, por ahora ninguno)
    readonly_fields = []
    
    # Configuración de visualización
    can_delete = True
    show_change_link = False
    
    # Ayuda al usuario
    verbose_name = "Cuota"
    verbose_name_plural = "Cuotas del Crédito"

@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = (
        'uid', 'state', 'created_at', 'description', 'morosidad_level', 'user', 'cost', 'price', 
        'credit_days', 'earnings', 'interest', 'periodicity', 'total_abonos','pending_amount', 
        'installment_number', 'installment_value'
    )
    search_fields = ('uid', 'user__username')
    actions = [change_credit_state_to_solve]
    
    # Agregar el inline de cuotas
    inlines = [InstallmentInline]

    exclude = ('interest', 'refinancing', 'total_abonos', 'pending_amount', 'installment_number', 'installment_value', 'is_in_default', 'morosidad_level')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Forzar la evaluación del SimpleLazyObject para obtener la instancia real de User
            obj.registered_by = request.user._wrapped if hasattr(request.user, '_wrapped') else request.user
        super().save_model(request, obj, form, change)
    
    def save_related(self, request, form, formsets, change):
        """
        Se ejecuta después de guardar el crédito y los inlines.
        Aquí validamos las cuotas ingresadas manualmente.
        """
        # Primero guardar los formsets (cuotas)
        super().save_related(request, form, formsets, change)
        
        credit = form.instance
        installments = credit.installments.all()
        installment_count = installments.count()
        
        # Si no hay cuotas, no validar (permitir guardar el crédito sin cuotas inicialmente)
        if installment_count == 0:
            return
        
        # Validación 1: Suma de montos de cuotas debe ser igual al precio del crédito
        total_installments = sum(inst.amount for inst in installments if inst.amount)
        if total_installments != credit.price:
            raise ValidationError(
                f"La suma de las cuotas ({total_installments}) debe ser igual al precio del crédito ({credit.price}). "
                f"Diferencia: {abs(total_installments - credit.price)}"
            )
        
        # Validación 2: Fechas de cuotas deben estar dentro del rango del crédito
        # Calcular la fecha máxima basándose en credit_days
        from datetime import timedelta
        max_date = credit.first_date_payment + timedelta(days=credit.credit_days)
        
        for inst in installments:
            if inst.due_date:
                if inst.due_date < credit.first_date_payment:
                    raise ValidationError(
                        f"La fecha de la cuota #{inst.number} ({inst.due_date}) es anterior a la primera fecha de pago del crédito ({credit.first_date_payment})"
                    )
                if inst.due_date > max_date:
                    raise ValidationError(
                        f"La fecha de la cuota #{inst.number} ({inst.due_date}) excede los días de crédito. "
                        f"Fecha máxima permitida: {max_date} (first_date_payment + {credit.credit_days} días)"
                    )

        
        # Validación 3: Reglas especiales para las primeras dos cuotas
        if installment_count >= 2:
            # Ordenar cuotas por número
            sorted_installments = sorted(installments, key=lambda x: x.number if x.number else 0)
            
            # La primera cuota debe tener la fecha first_date_payment
            if sorted_installments[0].due_date != credit.first_date_payment:
                raise ValidationError(
                    f"La primera cuota (#{sorted_installments[0].number}) debe tener la fecha {credit.first_date_payment}, "
                    f"pero tiene la fecha {sorted_installments[0].due_date}"
                )
            
            # La segunda cuota debe tener la fecha second_date_payment
            if sorted_installments[1].due_date != credit.second_date_payment:
                raise ValidationError(
                    f"La segunda cuota (#{sorted_installments[1].number}) debe tener la fecha {credit.second_date_payment}, "
                    f"pero tiene la fecha {sorted_installments[1].due_date}"
                )
        
        # Actualizar cálculos automáticos basándose en las cuotas ingresadas
        credit.update_installment_calculations()
        
        # Mostrar mensaje de éxito
        messages.success(
            request, 
            f"Crédito guardado exitosamente con {installment_count} cuota(s). "
            f"Valor promedio de cuota: {credit.installment_value}"
        )

@admin.register(ParamsLocation)
class ParamsLocationAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'state_name', 'country_name', 'city_code', 'state_code', 'country_code')
    search_fields = ('city_name', 'state_name', 'country_name', 'city_code', 'state_code', 'country_code')

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_sales', 'commissions', 'returns')
    search_fields = ('user__username',)

    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'Seller Username'

@admin.register(Adjustment)
class AdjustmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_positive', 'description')
    search_fields = ('code', 'name')
    list_filter = ('is_positive',)
    ordering = ('code',)

@admin.register(CreditAdjustment)
class CreditAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('credit', 'type', 'amount', 'added_on', 'reason', 'created_at')
    search_fields = ('credit__id', 'type__name', 'reason')
    list_filter = ('type__is_positive', 'added_on', 'created_at')
    date_hierarchy = 'added_on'
    ordering = ('-added_on',)
    

@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    # Campos básicos con cálculos optimizados
    list_display = (
        'credit_uid', 'number', 'due_date', 'amount', 'status', 'paid',
        'remaining_amount_calc', 'days_overdue_calc', 'late_fee_calc'
    )
    
    # Filtros simples
    list_filter = (
        'status', 'paid', 'due_date'
    )
    
    # Búsqueda básica
    search_fields = ('credit__uid', 'number')
    
    # Ordenamiento
    ordering = ('-due_date',)
    
    # Paginación ultra-reducida
    list_per_page = 10  # Muy pocos registros por página
    list_max_show_all = 25  # Máximo para "mostrar todo"
    
    # Solo lectura para campos del sistema
    readonly_fields = (
        'created_at', 'updated_at'
    )
    
    def credit_uid(self, obj):
        """UID compacto del crédito"""
        if obj.credit and obj.credit.uid:
            return str(obj.credit.uid)[:8] + '...'
        return 'N/A'
    credit_uid.short_description = 'Credit UID'
    credit_uid.admin_order_field = 'credit__uid'
    
    def remaining_amount_calc(self, obj):
        """Monto restante calculado con cache"""
        return InstallmentCalculator.get_remaining_amount(obj)
    remaining_amount_calc.short_description = 'Remaining Amount'
    
    def days_overdue_calc(self, obj):
        """Días de mora calculados con cache"""
        return InstallmentCalculator.get_days_overdue(obj)
    days_overdue_calc.short_description = 'Days Overdue'
    
    def late_fee_calc(self, obj):
        """Recargo por mora calculado con cache"""
        return InstallmentCalculator.get_late_fee(obj)
    late_fee_calc.short_description = 'Late Fee'
    
    def get_queryset(self, request):
        """Consulta optimizada sin campos calculados"""
        qs = super().get_queryset(request).select_related('credit').only(
            'id', 'number', 'due_date', 'amount', 'status', 'paid',
            'credit__uid', 'credit__user__username'
        )
        
        # Solo filtrar por defecto si no hay filtros aplicados
        if not request.GET.get('status') and not request.GET.get('paid'):
            qs = qs.filter(status='pending')
        
        return qs
    
    # Permitir eliminación de cuotas solo para administradores
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff





# from django.db import migrations

# def create_initial_request_data(apps, schema_editor):
#     RequestType = apps.get_model('user_requests', 'RequestType')
#     RequestStatus = apps.get_model('user_requests', 'RequestStatus')
#     RequestSource = apps.get_model('user_requests', 'RequestSource')

#     # RequestType
#     types = [
#         ("credit", "Solicitud de Crédito", "Cliente solicita un crédito o préstamo."),
#         ("investment", "Solicitud de Inversión", "Cliente desea invertir dinero."),
#         ("extend_term", "Ampliación de Plazo", "Solicita más tiempo para pagar el crédito."),
#         ("refinance", "Refinanciación", "Desea renegociar o consolidar el crédito."),
#         ("early_discount", "Pronto Pago", "Solicita descuento por pago anticipado."),
#         ("expand_investment", "Ampliar Inversión", "Desea aumentar el monto invertido."),
#         ("withdraw", "Retiro", "Desea retirar fondos de su inversión."),
#         ("reinvest", "Reinversión", "Desea reinvertir capital o rendimientos.")
#     ]
#     for code, name, desc in types:
#         RequestType.objects.get_or_create(code=code, defaults={"name": name, "description": desc})

#     # RequestStatus
#     statuses = [
#         ("pending", "Pendiente", "Aún no ha sido procesada."),
#         ("approved", "Aprobada", "La solicitud fue aceptada."),
#         ("rejected", "Rechazada", "La solicitud fue rechazada."),
#         ("cancelled", "Cancelada", "Cancelada por el cliente o el sistema."),
#         ("completed", "Completada", "La solicitud fue ejecutada.")
#     ]
#     for code, name, desc in statuses:
#         RequestStatus.objects.get_or_create(code=code, defaults={"name": name, "description": desc})

#     # RequestSource
#     sources = [
#         ("web", "Aplicación Web", "Solicitud enviada desde el sitio web."),
#         ("mobile", "App Móvil", "Solicitud enviada desde la app móvil."),
#         ("admin", "Panel Administrativo", "Registrada manualmente por staff."),
#         ("verbal", "Verbal", "Registrada por un asesor tras solicitud verbal."),
#         ("chatbot", "Chatbot", "Solicitud vía asistente virtual."),
#         ("api", "API", "Enviada desde una integración externa.")
#     ]
#     for code, name, desc in sources:
#         RequestSource.objects.get_or_create(code=code, defaults={"name": name, "description": desc})

# def reverse_func(apps, schema_editor):
#     RequestType = apps.get_model('user_requests', 'RequestType')
#     RequestStatus = apps.get_model('user_requests', 'RequestStatus')
#     RequestSource = apps.get_model('user_requests', 'RequestSource')
#     RequestType.objects.all().delete()
#     RequestStatus.objects.all().delete()
#     RequestSource.objects.all().delete()

# class Migration(migrations.Migration):

#     dependencies = [
#         # Reemplaza con tu última migración
#         ('user_requests', '000X_previous_migration'),
#     ]

#     operations = [
#         migrations.RunPython(create_initial_request_data, reverse_func),
#     ]
