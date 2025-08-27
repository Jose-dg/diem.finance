#!/usr/bin/env python3
"""
Script para debuggear el error en DashboardSummaryView
"""
import os
import sys
import django

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def test_dashboard_summary_view():
    """Prueba la vista DashboardSummaryView directamente"""
    print("🔍 Probando DashboardSummaryView directamente...")
    
    try:
        from apps.insights.views import DashboardSummaryView
        
        # Crear un usuario de prueba
        user = User.objects.first()
        if not user:
            print("❌ No hay usuarios en la base de datos")
            return
        
        print(f"✅ Usuario encontrado: {user.username}")
        
        # Crear request factory
        factory = RequestFactory()
        
        # Crear request
        request = factory.get('/insights/api/dashboard/summary/')
        request.user = user
        
        # Crear instancia de la vista
        view = DashboardSummaryView()
        view.request = request
        
        # Ejecutar la vista
        response = view.get(request)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Response Data: {response.data}")
        
        if response.status_code == 200:
            print("✅ DashboardSummaryView funciona correctamente")
            return True
        else:
            print(f"❌ Error en DashboardSummaryView: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_dashboard_summary():
    """Prueba el endpoint de dashboard summary"""
    print("🔍 Iniciando debug del DashboardSummaryView...")
    
    # Crear un usuario de prueba
    try:
        user = User.objects.first()
        if not user:
            print("❌ No hay usuarios en la base de datos")
            return
        
        print(f"✅ Usuario encontrado: {user.username}")
        
        # Crear token JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        print(f"✅ Token JWT creado: {access_token[:20]}...")
        
        # Crear cliente API
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # Probar el endpoint
        print("🔍 Probando endpoint /insights/api/dashboard/summary/...")
        response = client.get('/insights/api/dashboard/summary/')
        
        print(f"📊 Status Code: {response.status_code}")
        
        if hasattr(response, 'data'):
            print(f"📊 Response: {response.data}")
        else:
            print(f"📊 Response Content: {response.content}")
        
        if response.status_code == 200:
            print("✅ Endpoint funciona correctamente")
        else:
            print(f"❌ Error en endpoint: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        import traceback
        traceback.print_exc()

def test_imports():
    """Prueba las importaciones necesarias"""
    print("🔍 Probando importaciones...")
    
    try:
        from apps.insights.views import DashboardSummaryView
        print("✅ DashboardSummaryView importado correctamente")
    except Exception as e:
        print(f"❌ Error importando DashboardSummaryView: {e}")
    
    try:
        from apps.insights.utils.calculations import calculate_performance_metrics
        print("✅ calculate_performance_metrics importado correctamente")
    except Exception as e:
        print(f"❌ Error importando calculate_performance_metrics: {e}")
    
    try:
        from apps.insights.utils.dashboard_helpers import get_alerts, get_by_periodicity_metrics
        print("✅ dashboard_helpers importado correctamente")
    except Exception as e:
        print(f"❌ Error importando dashboard_helpers: {e}")
    
    try:
        from apps.insights.serializers.dashboard_serializers import DashboardSummarySerializer
        print("✅ DashboardSummarySerializer importado correctamente")
    except Exception as e:
        print(f"❌ Error importando DashboardSummarySerializer: {e}")

def test_functions():
    """Prueba las funciones individuales"""
    print("🔍 Probando funciones individuales...")
    
    try:
        from apps.insights.utils.calculations import calculate_performance_metrics
        metrics = calculate_performance_metrics()
        print(f"✅ calculate_performance_metrics ejecutada: {len(metrics)} métricas")
    except Exception as e:
        print(f"❌ Error en calculate_performance_metrics: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        from apps.insights.utils.dashboard_helpers import get_alerts
        alerts = get_alerts()
        print(f"✅ get_alerts ejecutada: {len(alerts)} alertas")
    except Exception as e:
        print(f"❌ Error en get_alerts: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        from apps.insights.utils.dashboard_helpers import get_by_periodicity_metrics
        periodicity = get_by_periodicity_metrics()
        print(f"✅ get_by_periodicity_metrics ejecutada: {len(periodicity)} periodicidades")
    except Exception as e:
        print(f"❌ Error en get_by_periodicity_metrics: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Iniciando debug completo...")
    test_imports()
    test_functions()
    test_dashboard_summary_view()
    print("🏁 Debug completado")
