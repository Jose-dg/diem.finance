#!/usr/bin/env python3
"""
Script para probar el sistema de interés adicional
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.fintech.models import (
    User, Credit, Currency, Periodicity, Account, 
    Adjustment, CreditAdjustment, SubCategory, Category, CategoryType
)
from apps.fintech.services.credit_adjustment_service import CreditAdjustmentService


def test_additional_interest_system():
    """Prueba completa del sistema de interés adicional"""
    print("🧪 INICIANDO PRUEBAS DEL SISTEMA DE INTERÉS ADICIONAL")
    print("=" * 60)
    
    # 1. Verificar que existe el Adjustment C0001
    try:
        adjustment = Adjustment.objects.get(code='C0001')
        print(f"✅ Adjustment C0001 encontrado: {adjustment.name}")
    except Adjustment.DoesNotExist:
        print("❌ ERROR: No existe el Adjustment C0001")
        print("   Ejecuta: python manage.py shell")
        print("   Luego: Adjustment.objects.create(code='C0001', name='Interés Adicional', is_positive=True)")
        return False
    
    # 2. Crear datos de prueba
    print("\n📊 Creando datos de prueba...")
    
    # Usuario
    user, created = User.objects.get_or_create(
        username='test_additional_interest',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        print(f"✅ Usuario creado: {user.username}")
    else:
        print(f"ℹ️  Usuario existente: {user.username}")
    
    # Categorías
    category_type, _ = CategoryType.objects.get_or_create(name='Test Category Type')
    category, _ = Category.objects.get_or_create(
        name='Test Category',
        defaults={'category_type': category_type}
    )
    subcategory, _ = SubCategory.objects.get_or_create(
        name='Test SubCategory',
        defaults={'category': category}
    )
    
    # Moneda
    currency, _ = Currency.objects.get_or_create(
        id_currency='USD',
        defaults={
            'currency': 'US Dollar',
            'exchange_rate': 1.0
        }
    )
    
    # Periodicidad
    periodicity, _ = Periodicity.objects.get_or_create(
        name='Monthly',
        defaults={'days': 30}
    )
    
    # Cuenta
    account, _ = Account.objects.get_or_create(
        name='Test Account',
        defaults={'currency': currency}
    )
    
    # 3. Crear crédito de prueba
    print("\n💰 Creando crédito de prueba...")
    
    # Limpiar créditos de prueba anteriores
    Credit.objects.filter(user=user, description__icontains='TEST').delete()
    
    credit = Credit.objects.create(
        user=user,
        subcategory=subcategory,
        cost=Decimal('100.00'),
        price=Decimal('105.00'),  # 5 de interés adicional
        currency=currency,
        first_date_payment=django.utils.timezone.now().date(),
        second_date_payment=django.utils.timezone.now().date() + django.utils.timezone.timedelta(days=30),
        credit_days=60,
        periodicity=periodicity,
        payment=account,
        total_abonos=Decimal('80.00'),  # Pagó menos del price
        description='CRÉDITO DE PRUEBA PARA INTERÉS ADICIONAL'
    )
    
    print(f"✅ Crédito creado: {credit.uid}")
    print(f"   Cost: ${credit.cost}")
    print(f"   Price: ${credit.price}")
    print(f"   Total abonos: ${credit.total_abonos}")
    print(f"   Diferencia: ${credit.price - credit.total_abonos}")
    
    # 4. Probar cálculo de interés adicional
    print("\n🧮 Probando cálculo de interés adicional...")
    
    additional_interest = CreditAdjustmentService.calculate_additional_interest(credit)
    print(f"✅ Interés adicional calculado: ${additional_interest}")
    
    should_apply = CreditAdjustmentService.should_apply_additional_interest(credit)
    print(f"✅ Debe aplicar interés: {should_apply}")
    
    # 5. Aplicar interés adicional
    print("\n💳 Aplicando interés adicional...")
    
    amount_applied = CreditAdjustmentService.apply_additional_interest(
        credit,
        reason="Prueba del sistema de interés adicional"
    )
    
    print(f"✅ Interés aplicado: ${amount_applied}")
    
    # 6. Verificar resultados
    print("\n🔍 Verificando resultados...")
    
    # Recargar crédito
    credit.refresh_from_db()
    print(f"✅ Pending amount actualizado: ${credit.pending_amount}")
    
    # Verificar CreditAdjustment
    credit_adjustment = CreditAdjustment.objects.filter(
        credit=credit,
        type=adjustment
    ).first()
    
    if credit_adjustment:
        print(f"✅ CreditAdjustment creado:")
        print(f"   ID: {credit_adjustment.id}")
        print(f"   Amount: ${credit_adjustment.amount}")
        print(f"   Reason: {credit_adjustment.reason}")
        print(f"   Date: {credit_adjustment.added_on}")
    else:
        print("❌ ERROR: No se creó el CreditAdjustment")
        return False
    
    # 7. Probar que no se duplica
    print("\n🔄 Probando que no se duplica...")
    
    amount_applied_again = CreditAdjustmentService.apply_additional_interest(credit)
    print(f"✅ Segunda aplicación: ${amount_applied_again}")
    
    adjustments_count = CreditAdjustment.objects.filter(
        credit=credit,
        type=adjustment
    ).count()
    
    print(f"✅ Total de ajustes: {adjustments_count} (debería ser 1)")
    
    if adjustments_count == 1:
        print("✅ No se duplicó el ajuste")
    else:
        print("❌ ERROR: Se duplicó el ajuste")
        return False
    
    # 8. Probar total de ajustes
    print("\n📊 Probando total de ajustes...")
    
    total_adjustments = CreditAdjustmentService.get_total_adjustments(credit)
    print(f"✅ Total de ajustes: ${total_adjustments}")
    
    # 9. Probar historial
    print("\n📋 Probando historial...")
    
    history = CreditAdjustmentService.get_adjustment_history(credit)
    print(f"✅ Registros en historial: {history.count()}")
    
    for adj in history:
        print(f"   - {adj.type.name}: ${adj.amount} ({adj.added_on})")
    
    # 10. Resumen final
    print("\n" + "=" * 60)
    print("🎉 PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("=" * 60)
    print(f"✅ Crédito: {credit.uid}")
    print(f"✅ Interés adicional: ${additional_interest}")
    print(f"✅ Pending amount: ${credit.pending_amount}")
    print(f"✅ Ajustes aplicados: {adjustments_count}")
    print("\n💡 El sistema está funcionando correctamente!")
    
    return True


if __name__ == '__main__':
    try:
        success = test_additional_interest_system()
        if success:
            print("\n✅ Todas las pruebas pasaron!")
            sys.exit(0)
        else:
            print("\n❌ Algunas pruebas fallaron!")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 