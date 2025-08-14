#!/usr/bin/env python3
"""
Script de prueba para verificar la eliminación de créditos
"""
import os
import sys
import django

# Configurar Django
import sys
sys.path.append('/Users/ojeda/Documents/Dev/fintech')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.fintech.models import Credit, Installment, CreditAdjustment, AccountMethodAmount, Transaction
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

def test_credit_deletion():
    """
    Prueba la eliminación de un crédito con todas sus relaciones
    """
    print("🧪 Iniciando prueba de eliminación de créditos...")
    
    # Buscar un crédito de prueba (que tenga cuotas)
    credit = Credit.objects.filter(installments__isnull=False).first()
    
    if not credit:
        print("❌ No se encontró ningún crédito con cuotas para probar")
        return False
    
    print(f"📋 Crédito seleccionado para prueba:")
    print(f"   - ID: {credit.id}")
    print(f"   - UID: {credit.uid}")
    print(f"   - Usuario: {credit.user.username}")
    print(f"   - Monto: ${credit.price}")
    
    # Contar registros relacionados antes de eliminar
    installments_count = credit.installments.count()
    adjustments_count = credit.adjustments.count()
    payments_count = credit.payments.count()
    
    print(f"📊 Registros relacionados:")
    print(f"   - Cuotas: {installments_count}")
    print(f"   - Ajustes: {adjustments_count}")
    print(f"   - Pagos: {payments_count}")
    
    # Verificar transacciones relacionadas
    transactions = []
    for payment in credit.payments.all():
        if payment.transaction:
            transactions.append(payment.transaction)
    
    print(f"   - Transacciones: {len(transactions)}")
    
    try:
        with transaction.atomic():
            print("\n🗑️  Eliminando crédito...")
            
            # Eliminar el crédito (esto debería eliminar automáticamente las relaciones)
            credit.delete()
            
            print("✅ Crédito eliminado exitosamente!")
            
            # Verificar que las relaciones se eliminaron
            remaining_installments = Installment.objects.filter(credit_id=credit.id).count()
            remaining_adjustments = CreditAdjustment.objects.filter(credit_id=credit.id).count()
            remaining_payments = AccountMethodAmount.objects.filter(credit_id=credit.id).count()
            
            print(f"\n📊 Verificación post-eliminación:")
            print(f"   - Cuotas restantes: {remaining_installments} (esperado: 0)")
            print(f"   - Ajustes restantes: {remaining_adjustments} (esperado: 0)")
            print(f"   - Pagos restantes: {remaining_payments} (esperado: 0)")
            
            # Verificar transacciones
            remaining_transactions = Transaction.objects.filter(
                account_method_amounts__credit_id=credit.id
            ).count()
            print(f"   - Transacciones restantes: {remaining_transactions} (esperado: 0)")
            
            # Verificar que todo se eliminó correctamente
            if (remaining_installments == 0 and 
                remaining_adjustments == 0 and 
                remaining_payments == 0 and 
                remaining_transactions == 0):
                print("\n🎉 ¡PRUEBA EXITOSA! Todas las relaciones se eliminaron correctamente.")
                return True
            else:
                print("\n❌ PRUEBA FALLIDA: Algunas relaciones no se eliminaron.")
                return False
                
    except Exception as e:
        print(f"\n❌ Error durante la eliminación: {str(e)}")
        return False

def test_admin_permissions():
    """
    Prueba los permisos de administrador
    """
    print("\n🔐 Probando permisos de administrador...")
    
    # Buscar un usuario administrador
    admin_user = User.objects.filter(is_staff=True).first()
    if not admin_user:
        print("❌ No se encontró ningún usuario administrador")
        return False
    
    print(f"👤 Usuario administrador: {admin_user.username}")
    print(f"   - is_staff: {admin_user.is_staff}")
    print(f"   - is_superuser: {admin_user.is_superuser}")
    
    # Simular verificación de permisos
    from apps.fintech.admin import InstallmentAdmin
    admin_instance = InstallmentAdmin(Installment, None)
    
    # Crear un mock request con el usuario
    class MockRequest:
        def __init__(self, user):
            self.user = user
    
    mock_request = MockRequest(admin_user)
    has_delete_permission = admin_instance.has_delete_permission(mock_request, None)
    print(f"   - Tiene permisos de eliminación: {has_delete_permission}")
    
    return has_delete_permission

def main():
    """
    Función principal
    """
    print("🚀 Iniciando pruebas de eliminación de créditos...")
    print("=" * 50)
    
    # Prueba 1: Permisos de administrador
    permissions_ok = test_admin_permissions()
    
    # Prueba 2: Eliminación de crédito
    deletion_ok = test_credit_deletion()
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE PRUEBAS:")
    print(f"   - Permisos de administrador: {'✅ OK' if permissions_ok else '❌ FALLÓ'}")
    print(f"   - Eliminación de crédito: {'✅ OK' if deletion_ok else '❌ FALLÓ'}")
    
    if permissions_ok and deletion_ok:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON! La solución está funcionando correctamente.")
        return True
    else:
        print("\n❌ Algunas pruebas fallaron. Revisar la implementación.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
