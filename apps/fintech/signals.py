from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from apps.fintech.utils.root import distribuir_pago_a_cuotas, generar_cuotas, recalculate_credit
from .models import CreditAdjustment, Transaction, AccountMethodAmount, Credit
from datetime import datetime
from django.utils import timezone
from apps.fintech.models import Installment, Credit
from apps.fintech.services.installment_calculator import InstallmentCalculator
from apps.fintech.services.credit_adjustment_service import CreditAdjustmentService


@receiver(pre_save, sender=AccountMethodAmount)
def adjust_credit_on_update(sender, instance, **kwargs):
    """
    Ajusta el total de abonos cuando se actualiza un AccountMethodAmount.
    """
    if instance.pk:
        previous = AccountMethodAmount.objects.get(pk=instance.pk)
        if previous.amount_paid != instance.amount_paid:
            difference = instance.amount_paid - previous.amount_paid
            instance.credit.update_total_abonos(difference)

@receiver(post_save, sender=AccountMethodAmount)
def update_credit_on_account_method_change(sender, instance, **kwargs):
    """
    Solo actualizamos el crédito si la transacción es de tipo 'income'
    """
    if instance.transaction.transaction_type == 'income':
        instance.credit.update_total_abonos(instance.amount_paid)

@receiver(post_delete, sender=AccountMethodAmount)
def adjust_credit_on_delete(sender, instance, **kwargs):
    """
    Ajusta el total de abonos cuando se elimina un AccountMethodAmount.
    """
    if instance.credit:
        instance.credit.update_total_abonos(-instance.amount_paid)

@receiver(post_save, sender=Credit)
def create_transaction_and_account_method(sender, instance, created, **kwargs):
    """
    Crea una transacción de tipo 'expense' cuando se crea un nuevo crédito y un registro asociado en AccountMethodAmount.
    """
    if created:
        # Crear la transacción de crédito
        transaction = Transaction.objects.create(
            transaction_type='expense',
            user=instance.user,
            category=instance.subcategory,
            date=instance.created_at,
            description=f"Crédito de ${instance.price}.00 registrado.",
        )

        # Formatear la fecha y hora para el payment_code
        current_datetime = datetime.now()
        payment_code = current_datetime.strftime("%d%m%Y%H%M")  # Formato DDMMYYYYHHMM

        # Crear AccountMethodAmount asociado a la transacción
        AccountMethodAmount.objects.create(
            payment_method=instance.payment,  # Método de pago relacionado al crédito
            payment_code=f"CP{payment_code}",  # Código único
            amount=instance.price,  # Monto total del crédito (lo que se entrega)
            amount_paid=instance.price,  # El monto entregado al cliente es igual al amount
            currency=instance.currency,
            credit=instance,
            transaction=transaction  
        )

@receiver(post_save, sender=Transaction)
def handle_transaction_save(sender, instance, **kwargs):
    """
    Recalcula el crédito relacionado con una transacción de ingreso confirmada.
    """
    if instance.transaction_type != 'income' or instance.status != 'confirmed':
        return

    try:
        # Buscar el primer AccountMethodAmount relacionado a esta transacción
        ama = AccountMethodAmount.objects.filter(transaction=instance).select_related('credit').first()

        if ama and ama.credit:
            recalculate_credit(ama.credit.uid)

    except Exception as e:
        # Recomendado para debug, puedes poner logging si lo prefieres
        print(f"[ERROR] No se pudo recalcular el crédito: {e}")

@receiver(post_save, sender=Transaction)
def check_additional_interest_after_payment(sender, instance, created, **kwargs):
    """
    Verifica si se debe aplicar interés adicional después de un pago
    """
    if not created or instance.transaction_type != 'income' or instance.status != 'confirmed':
        return
    
    try:
        # Buscar créditos relacionados con esta transacción
        credit_adjustments = instance.account_method_amounts.all()
        
        for credit_adjustment in credit_adjustments:
            credit = credit_adjustment.credit
            
            # Verificar si se debe aplicar interés adicional
            if CreditAdjustmentService.should_apply_additional_interest(credit):
                CreditAdjustmentService.apply_additional_interest(
                    credit,
                    reason=f"Pago parcial detectado. Total pagado: {credit.total_abonos}, Total pactado: {credit.price}"
                )
                
    except Exception as e:
        print(f"[ERROR] No se pudo verificar interés adicional: {e}")
        
@receiver(post_delete, sender=Transaction)
def handle_transaction_delete(sender, instance, **kwargs):
    """
    Recalcula el crédito completo si se elimina una transacción que afecta el saldo.
    """
    if instance.credit:
        recalculate_credit(instance.credit.uid)
    
@receiver(post_save, sender=CreditAdjustment)
def handle_credit_adjustment_save(sender, instance, created, **kwargs):
    """
    Cuando se crea o actualiza un CreditAdjustment, recalculamos el crédito asociado.
    """
    if instance.credit:
        recalculate_credit(instance.credit)

@receiver(post_delete, sender=CreditAdjustment)
def handle_credit_adjustment_delete(sender, instance, **kwargs):
    """
    Cuando se elimina un CreditAdjustment, recalculamos el crédito asociado.
    """
    if instance.credit:
        recalculate_credit(instance.credit)

@receiver(post_save, sender=Credit)
def crear_cuotas_credito(sender, instance, created, **kwargs):
    if created and not instance.installments.exists():
        generar_cuotas(instance)

@receiver(post_save, sender=AccountMethodAmount)
def distribuir_pago(sender, instance, created, **kwargs):
    if not created:
        return

    transaction = instance.transaction
    fecha_pago = getattr(transaction, 'created_at', None)

    if not fecha_pago:
        fecha_pago = timezone.now().date()
    else:
        fecha_pago = fecha_pago.date()

    distribuir_pago_a_cuotas(instance.credit, instance.amount_paid, fecha_pago)


@receiver(post_save, sender=Installment)
def update_installment_calculations(sender, instance, created, **kwargs):
    """Actualiza cálculos cuando hay cambios en cuotas"""
    
    if created:
        # Nueva cuota: limpiar cache y calcular
        InstallmentCalculator.clear_cache(instance.id)
        InstallmentCalculator.get_remaining_amount(instance)
        InstallmentCalculator.get_days_overdue(instance)
        
        # Actualizar estado del crédito
        if instance.credit:
            InstallmentCalculator.update_credit_status(instance.credit)
    
    elif instance.tracker.has_changed('amount_paid'):
        # Pago realizado: recalcular remaining_amount
        InstallmentCalculator.clear_cache(instance.id)
        InstallmentCalculator.get_remaining_amount(instance)
        
        # Actualizar estado del crédito
        if instance.credit:
            InstallmentCalculator.update_credit_status(instance.credit)
    
    elif instance.tracker.has_changed('status'):
        # Cambio de estado: recalcular campos de mora
        InstallmentCalculator.clear_cache(instance.id)
        InstallmentCalculator.get_days_overdue(instance)
        InstallmentCalculator.get_late_fee(instance)
        
        # Actualizar estado del crédito
        if instance.credit:
            InstallmentCalculator.update_credit_status(instance.credit)


@receiver(post_save, sender=Credit)
def update_credit_installments(sender, instance, created, **kwargs):
    """Actualiza cuotas cuando hay cambios en créditos"""
    
    if created:
        # Nuevo crédito: no hacer nada especial
        pass
    
    elif instance.tracker.has_changed('state'):
        # Cambio de estado del crédito: actualizar cuotas relacionadas
        for installment in instance.installments.all():
            InstallmentCalculator.clear_cache(installment.id)
            InstallmentCalculator.get_days_overdue(installment)
            InstallmentCalculator.get_late_fee(installment)


@receiver(post_delete, sender=Installment)
def cleanup_installment_cache(sender, instance, **kwargs):
    """Limpia cache cuando se elimina una cuota"""
    InstallmentCalculator.clear_cache(instance.id)
    
    # Actualizar estado del crédito
    if instance.credit:
        InstallmentCalculator.update_credit_status(instance.credit)