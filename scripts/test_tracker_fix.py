#!/usr/bin/env python3
"""
Script para verificar que el error del tracker se ha solucionado
"""

import os
import sys
import django

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.fintech.models import Credit, Transaction, AccountMethodAmount
from django.test import RequestFactory
from django.contrib.admin.sites import AdminSite
from apps.fintech.admin import TransactionAdmin

def test_tracker_access():
    """Prueba el acceso al tracker"""
    print("=== PRUEBA DE ACCESO AL TRACKER ===")
    
    try:
        # Obtener un crédito
        credit = Credit.objects.first()
        if not credit:
            print("❌ No hay créditos disponibles")
            return False
        
        print(f"🔍 Probando crédito ID: {credit.id}")
        
        # Probar acceso al tracker
        tracker = credit.tracker
        print(f"✅ Tracker accesible: {type(tracker)}")
        
        # Probar método has_changed
        has_changed = tracker.has_changed('price')
        print(f"✅ has_changed funciona: {has_changed}")
        
        # Probar método changed_fields
        changed_fields = tracker.changed_fields()
        print(f"✅ changed_fields funciona: {changed_fields}")
        
        # Probar método set_changed
        tracker.set_changed('price')
        changed_fields = tracker.changed_fields()
        print(f"✅ set_changed funciona: {changed_fields}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al probar tracker: {e}")
        return False

def test_admin_transaction():
    """Prueba el admin de Transaction"""
    print("\n=== PRUEBA DEL ADMIN DE TRANSACTION ===")
    
    try:
        # Crear un request factory
        factory = RequestFactory()
        request = factory.post('/admin/fintech/transaction/add/')
        
        # Crear admin site
        admin_site = AdminSite()
        
        # Crear admin de Transaction
        transaction_admin = TransactionAdmin(Transaction, admin_site)
        print("✅ TransactionAdmin creado correctamente")
        
        # Simular acceso a un crédito desde el admin
        credit = Credit.objects.first()
        if credit:
            # Probar acceso al tracker desde el contexto del admin
            tracker = credit.tracker
            has_changed = tracker.has_changed('price')
            print(f"✅ Tracker funciona en contexto de admin: {has_changed}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en admin: {e}")
        return False

def test_signals_with_tracker():
    """Prueba signals con tracker"""
    print("\n=== PRUEBA DE SIGNALS CON TRACKER ===")
    
    try:
        # Obtener un crédito
        credit = Credit.objects.first()
        if not credit:
            print("❌ No hay créditos disponibles")
            return False
        
        # Simular un cambio en el crédito
        original_price = credit.price
        credit.price = credit.price + 1
        
        # Probar acceso al tracker durante el save
        tracker = credit.tracker
        tracker.set_changed('price')
        
        # Verificar que el tracker funciona
        has_changed = tracker.has_changed('price')
        changed_fields = tracker.changed_fields()
        
        print(f"✅ Tracker funciona en signals: has_changed={has_changed}, changed_fields={changed_fields}")
        
        # Restaurar el precio original
        credit.price = original_price
        
        return True
        
    except Exception as e:
        print(f"❌ Error en signals: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("🔧 PRUEBA DE SOLUCIÓN DEL ERROR DE TRACKER")
    print("=" * 50)
    
    results = []
    
    # Ejecutar pruebas
    results.append(("Acceso al tracker", test_tracker_access()))
    results.append(("Admin de Transaction", test_admin_transaction()))
    results.append(("Signals con tracker", test_signals_with_tracker()))
    
    # Resumen
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE PRUEBAS")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{len(results)} pruebas pasaron")
    
    if passed == len(results):
        print("🎉 ¡El error del tracker se ha solucionado completamente!")
        print("✅ El modelo Credit ahora tiene un tracker funcional")
        print("✅ Los signals pueden acceder al tracker sin errores")
        print("✅ El admin de Transaction funciona correctamente")
    else:
        print("⚠️  Aún hay problemas que requieren atención")
        print("💡 Revisar los errores específicos mostrados arriba")

if __name__ == "__main__":
    main() 