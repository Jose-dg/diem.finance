#!/usr/bin/env python
"""
Script para validar que la refactorización funciona correctamente
"""
import sys
import os
import django
from django.test.utils import get_runner
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def run_tests():
    """Ejecuta los tests específicos"""
    print("🧪 Ejecutando tests...")
    
    # Configurar test runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    # Ejecutar tests específicos
    test_modules = [
        'apps.fintech.tests.test_services',
        'apps.fintech.tests.test_installment_service',
    ]
    
    failures = test_runner.run_tests(test_modules)
    
    if failures:
        print(f"❌ {failures} test(s) fallaron")
        return False
    else:
        print("✅ Todos los tests pasaron")
        return True

def validate_imports():
    """Valida que todos los imports funcionen correctamente"""
    print("📦 Validando imports...")
    
    try:
        # Importar servicios
        from apps.fintech.services.credit_service import CreditService
        from apps.fintech.services.kpi_service import KPIService
        from apps.fintech.services.client_service import ClientService
        from apps.fintech.services.installment_service import InstallmentService
        
        # Importar managers
        from apps.fintech.managers import CreditManager, UserProfileManager, TransactionManager
        
        # Importar vistas refactorizadas
        from apps.fintech.views import (
            TransactionViewSet, ClientCreditsView
        )
        
        print("✅ Todos los imports funcionan correctamente")
        return True
        
    except ImportError as e:
        print(f"❌ Error de import: {e}")
        return False

def validate_models():
    """Valida que los modelos tengan los managers correctos"""
    print("🏗️ Validando modelos...")
    
    try:
        from apps.fintech.models import Credit, UserProfile, Transaction
        
        # Verificar que los managers estén asignados
        assert hasattr(Credit.objects, 'active_credits'), "CreditManager no está asignado a Credit"
        assert hasattr(UserProfile.objects, 'complete_profiles'), "UserProfileManager no está asignado a UserProfile"
        assert hasattr(Transaction.objects, 'income_transactions'), "TransactionManager no está asignado a Transaction"
        
        print("✅ Todos los modelos tienen sus managers correctos")
        return True
        
    except Exception as e:
        print(f"❌ Error en modelos: {e}")
        return False

def validate_service_methods():
    """Valida que los servicios tengan los métodos esperados"""
    print("🔧 Validando métodos de servicios...")
    
    try:
        from apps.fintech.services.credit_service import CreditService
        from apps.fintech.services.kpi_service import KPIService
        from apps.fintech.services.client_service import ClientService
        from apps.fintech.services.installment_service import InstallmentService
        
        # Verificar métodos de CreditService
        assert hasattr(CreditService, 'create_transaction_from_payment'), "Método create_transaction_from_payment no encontrado"
        assert hasattr(CreditService, 'get_credit_summary'), "Método get_credit_summary no encontrado"
        
        # Verificar métodos de KPIService
        assert hasattr(KPIService, 'get_credit_kpi_summary'), "Método get_credit_kpi_summary no encontrado"
        assert hasattr(KPIService, 'get_user_financial_metrics'), "Método get_user_financial_metrics no encontrado"
        assert hasattr(KPIService, 'get_portfolio_health_metrics'), "Método get_portfolio_health_metrics no encontrado"
        
        # Verificar métodos de ClientService
        assert hasattr(ClientService, 'search_clients_by_criteria'), "Método search_clients_by_criteria no encontrado"
        assert hasattr(ClientService, 'normalize_document_number'), "Método normalize_document_number no encontrado"
        
        # Verificar métodos de InstallmentService
        assert hasattr(InstallmentService, 'generate_installments_for_credit'), "Método generate_installments_for_credit no encontrado"
        assert hasattr(InstallmentService, 'update_all_installment_statuses'), "Método update_all_installment_statuses no encontrado"
        assert hasattr(InstallmentService, 'get_pending_installments_summary'), "Método get_pending_installments_summary no encontrado"
        assert hasattr(InstallmentService, 'get_expected_collection'), "Método get_expected_collection no encontrado"
        
        print("✅ Todos los métodos de servicios están presentes")
        return True
        
    except Exception as e:
        print(f"❌ Error en métodos de servicios: {e}")
        return False

def main():
    """Función principal de validación"""
    print("🚀 Iniciando validación de refactorización...")
    print("=" * 50)
    
    validations = [
        ("Imports", validate_imports),
        ("Modelos", validate_models),
        ("Métodos de Servicios", validate_service_methods),
        ("Tests", run_tests),
    ]
    
    results = []
    for name, validation_func in validations:
        print(f"\n📋 Validando {name}...")
        try:
            result = validation_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error durante validación de {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 Resumen de Validación:")
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"  {name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} validaciones pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las validaciones pasaron! La refactorización está funcionando correctamente.")
        return 0
    else:
        print("⚠️ Algunas validaciones fallaron. Revisa los errores arriba.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 