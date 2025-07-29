#!/usr/bin/env python3
"""
Script para diagnosticar el error de tracker en el modelo Credit
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
from django.db import connection
from django.test import RequestFactory
from django.contrib.admin.sites import AdminSite
from apps.fintech.admin import TransactionAdmin

def check_credit_attributes():
    """Verifica los atributos del modelo Credit"""
    print("=== VERIFICACIÓN DE ATRIBUTOS DEL MODELO CREDIT ===")
    
    # Obtener un crédito de ejemplo
    credit = Credit.objects.first()
    if not credit:
        print("❌ No hay créditos disponibles")
        return
    
    print(f"🔍 Analizando crédito ID: {credit.id}")
    
    # Verificar atributos del modelo
    credit_attrs = dir(credit)
    print(f"📋 Atributos del modelo Credit: {len(credit_attrs)}")
    
    # Buscar si hay algún atributo relacionado con tracker
    tracker_attrs = [attr for attr in credit_attrs if 'tracker' in attr.lower()]
    if tracker_attrs:
        print(f"⚠️  Atributos relacionados con tracker: {tracker_attrs}")
    else:
        print("✅ No se encontraron atributos relacionados con tracker")
    
    # Verificar si hay algún método que intente acceder a tracker
    try:
        # Intentar acceder a tracker para ver el error exacto
        tracker_value = getattr(credit, 'tracker', None)
        print(f"ℹ️  Valor de tracker: {tracker_value}")
    except Exception as e:
        print(f"❌ Error al acceder a tracker: {e}")
    
    return credit

def check_admin_transaction():
    """Verifica el admin de Transaction"""
    print("\n=== VERIFICACIÓN DEL ADMIN DE TRANSACTION ===")
    
    try:
        # Crear un request factory
        factory = RequestFactory()
        request = factory.post('/admin/fintech/transaction/add/')
        
        # Crear admin site
        admin_site = AdminSite()
        
        # Verificar si hay algún problema con el admin
        transaction_admin = TransactionAdmin(Transaction, admin_site)
        print("✅ TransactionAdmin creado correctamente")
        
        # Verificar métodos del admin
        admin_methods = [method for method in dir(transaction_admin) if not method.startswith('_')]
        print(f"📋 Métodos del admin: {len(admin_methods)}")
        
    except Exception as e:
        print(f"❌ Error en admin: {e}")
        return False
    
    return True

def check_signals_registration():
    """Verifica el registro de signals"""
    print("\n=== VERIFICACIÓN DE SIGNALS ===")
    
    from django.db.models.signals import post_save
    
    try:
        # Verificar signals de manera más segura
        receivers = getattr(post_save, '_live_receivers', [])
        if hasattr(receivers, '__len__'):
            signal_count = len(receivers)
        else:
            signal_count = "No disponible"
        
        print(f"📊 Signals registrados: {signal_count}")
        
        # Verificar signals específicos de manera más segura
        credit_signals = []
        if hasattr(receivers, '__iter__'):
            for receiver in receivers:
                if hasattr(receiver, '__name__') and 'credit' in receiver.__name__.lower():
                    credit_signals.append(receiver.__name__)
        
        print(f"📋 Signals de crédito: {len(credit_signals)}")
        for signal in credit_signals:
            print(f"  - {signal}")
        
    except Exception as e:
        print(f"❌ Error al verificar signals: {e}")
        return False
    
    return True

def check_model_integrity():
    """Verifica la integridad del modelo"""
    print("\n=== VERIFICACIÓN DE INTEGRIDAD DEL MODELO ===")
    
    try:
        # Verificar si el modelo se puede instanciar
        credit = Credit()
        print("✅ Modelo Credit se puede instanciar")
        
        # Verificar campos del modelo
        fields = [field.name for field in Credit._meta.fields]
        print(f"📋 Campos del modelo: {len(fields)}")
        
        # Verificar si hay campos problemáticos
        problematic_fields = [field for field in fields if 'tracker' in field.lower()]
        if problematic_fields:
            print(f"⚠️  Campos problemáticos: {problematic_fields}")
        else:
            print("✅ No se encontraron campos problemáticos")
            
    except Exception as e:
        print(f"❌ Error en integridad del modelo: {e}")
        return False
    
    return True

def main():
    """Función principal de diagnóstico"""
    print("🔍 DIAGNÓSTICO DEL ERROR DE TRACKER")
    print("=" * 50)
    
    results = []
    
    # Ejecutar verificaciones
    results.append(("Atributos del modelo", check_credit_attributes() is not None))
    results.append(("Admin de Transaction", check_admin_transaction()))
    results.append(("Signals", check_signals_registration()))
    results.append(("Integridad del modelo", check_model_integrity()))
    
    # Resumen
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE DIAGNÓSTICO")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{len(results)} pruebas pasaron")
    
    if passed == len(results):
        print("🎉 No se encontraron problemas evidentes")
        print("💡 El error puede estar en código no visible o en una dependencia")
    else:
        print("⚠️  Se encontraron problemas que requieren atención")

if __name__ == "__main__":
    main() 