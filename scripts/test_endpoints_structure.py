#!/usr/bin/env python3
"""
Test para verificar que los endpoints están correctamente estructurados
"""
import os
import sys
import django

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def test_endpoint_imports():
    """Prueba que todos los endpoints se pueden importar correctamente"""
    print("🔍 Probando importaciones de endpoints...")
    
    endpoints_to_test = [
        ('CreditDashboardViewSet', 'apps.insights.views'),
        ('InstallmentCollectionViewSet', 'apps.insights.views'),
        ('DashboardSummaryView', 'apps.insights.views'),
        ('CreditAnalyticsAdvancedView', 'apps.insights.views'),
        ('RiskAnalysisAdvancedView', 'apps.insights.views'),
    ]
    
    all_passed = True
    
    for endpoint_name, module_path in endpoints_to_test:
        try:
            module = __import__(module_path, fromlist=[endpoint_name])
            endpoint_class = getattr(module, endpoint_name)
            print(f"✅ {endpoint_name} importado correctamente")
        except Exception as e:
            print(f"❌ Error importando {endpoint_name}: {e}")
            all_passed = False
    
    return all_passed

def test_url_patterns():
    """Prueba que las URLs están correctamente configuradas"""
    print("\n🔍 Probando configuración de URLs...")
    
    try:
        from apps.insights.urls import urlpatterns
        
        expected_urls = [
            'api/credits/dashboard/',
            'api/installments/expected-collection/',
            'api/dashboard/summary/',
            'api/credits/analytics/',
            'api/risk/analysis/',
        ]
        
        url_paths = [str(pattern.pattern) for pattern in urlpatterns]
        
        all_urls_found = True
        for expected_url in expected_urls:
            if expected_url in url_paths:
                print(f"✅ URL encontrada: {expected_url}")
            else:
                print(f"❌ URL no encontrada: {expected_url}")
                all_urls_found = False
        
        return all_urls_found
        
    except Exception as e:
        print(f"❌ Error verificando URLs: {e}")
        return False

def test_serializers():
    """Prueba que los serializers están correctamente configurados"""
    print("\n🔍 Probando serializers...")
    
    serializers_to_test = [
        'CreditDashboardSerializer',
        'InstallmentCollectionSerializer', 
        'DashboardSummarySerializer'
    ]
    
    all_passed = True
    
    try:
        from apps.insights.serializers.dashboard_serializers import (
            CreditDashboardSerializer,
            InstallmentCollectionSerializer,
            DashboardSummarySerializer
        )
        
        serializers_imported = [
            CreditDashboardSerializer,
            InstallmentCollectionSerializer,
            DashboardSummarySerializer
        ]
        
        for serializer_class in serializers_imported:
            print(f"✅ {serializer_class.__name__} importado correctamente")
        
        return True
                
    except Exception as e:
        print(f"❌ Error importando serializers: {e}")
        all_passed = False
    
    return all_passed

def test_utility_functions():
    """Prueba que las funciones de utilidad están disponibles"""
    print("\n🔍 Probando funciones de utilidad...")
    
    functions_to_test = [
        ('calculate_performance_metrics', 'apps.insights.utils.calculations'),
        ('get_alerts', 'apps.insights.utils.dashboard_helpers'),
        ('get_by_periodicity_metrics', 'apps.insights.utils.dashboard_helpers'),
    ]
    
    all_passed = True
    
    for func_name, module_path in functions_to_test:
        try:
            module = __import__(module_path, fromlist=[func_name])
            func = getattr(module, func_name)
            print(f"✅ {func_name} importado correctamente")
        except Exception as e:
            print(f"❌ Error importando {func_name}: {e}")
            all_passed = False
    
    return all_passed

def test_view_structure():
    """Prueba la estructura básica de las vistas"""
    print("\n🔍 Probando estructura de vistas...")
    
    try:
        from apps.insights.views import DashboardSummaryView
        
        # Verificar que la vista tiene los métodos necesarios
        view = DashboardSummaryView()
        
        # Verificar que tiene permission_classes
        if hasattr(view, 'permission_classes'):
            print("✅ DashboardSummaryView tiene permission_classes")
        else:
            print("❌ DashboardSummaryView no tiene permission_classes")
            return False
        
        # Verificar que tiene método get
        if hasattr(view, 'get'):
            print("✅ DashboardSummaryView tiene método get")
        else:
            print("❌ DashboardSummaryView no tiene método get")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando estructura de vista: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("🚀 Iniciando tests de estructura de endpoints...")
    
    tests = [
        ("Importaciones de endpoints", test_endpoint_imports),
        ("Configuración de URLs", test_url_patterns),
        ("Serializers", test_serializers),
        ("Funciones de utilidad", test_utility_functions),
        ("Estructura de vistas", test_view_structure),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"📋 {test_name}")
        print('='*50)
        result = test_func()
        results.append((test_name, result))
    
    # Resumen final
    print(f"\n{'='*50}")
    print("📊 RESUMEN DE TESTS")
    print('='*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} tests pasaron")
    
    if passed == total:
        print("🎉 ¡Todos los tests pasaron! Los endpoints están correctamente estructurados.")
        print("✅ Puedes proceder con el backend.")
        return True
    else:
        print("⚠️ Algunos tests fallaron. Revisa los errores antes de proceder.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
