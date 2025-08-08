#!/usr/bin/env python3
"""
Script para probar la autenticación JWT y filtrado por usuario en las vistas del dashboard.
Ejecutar con: python3 manage.py shell < scripts/test_jwt_authentication.py
"""

import os
import sys
import django
import requests
import json
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from apps.fintech.models import Credit, Currency, Periodicity, SubCategory, Account
from decimal import Decimal

User = get_user_model()

def create_test_data():
    """Crear datos de prueba para el test"""
    print("🔧 Creando datos de prueba...")
    
    # Crear usuario de prueba
    user, created = User.objects.get_or_create(
        username='testuser_jwt',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    # Crear otro usuario para verificar filtrado
    other_user, created = User.objects.get_or_create(
        username='otheruser_jwt',
        defaults={
            'email': 'other@example.com',
            'first_name': 'Other',
            'last_name': 'User'
        }
    )
    
    # Crear datos necesarios
    currency, _ = Currency.objects.get_or_create(
        id_currency='USD',
        defaults={'currency': 'Dólar', 'exchange_rate': 1.0}
    )
    
    periodicity, _ = Periodicity.objects.get_or_create(
        name='Mensual',
        defaults={'days': 30}
    )
    
    subcategory, _ = SubCategory.objects.get_or_create(
        name='Préstamo Personal'
    )
    
    payment_account, _ = Account.objects.get_or_create(
        name='Cuenta Principal',
        defaults={
            'account_number': '123456789',
            'balance': Decimal('10000.00'),
            'currency': currency
        }
    )
    
    # Crear créditos para el usuario de prueba
    credit1 = Credit.objects.create(
        user=user,
        cost=Decimal('800.00'),
        price=Decimal('1000.00'),
        currency=currency,
        periodicity=periodicity,
        subcategory=subcategory,
        payment=payment_account,
        first_date_payment=datetime.now().date(),
        second_date_payment=(datetime.now() + timedelta(days=30)).date(),
        credit_days=30,
        description='Crédito de prueba 1'
    )
    
    credit2 = Credit.objects.create(
        user=user,
        cost=Decimal('1200.00'),
        price=Decimal('1500.00'),
        currency=currency,
        periodicity=periodicity,
        subcategory=subcategory,
        payment=payment_account,
        first_date_payment=datetime.now().date(),
        second_date_payment=(datetime.now() + timedelta(days=30)).date(),
        credit_days=30,
        description='Crédito de prueba 2'
    )
    
    # Crear crédito para otro usuario
    credit3 = Credit.objects.create(
        user=other_user,
        cost=Decimal('500.00'),
        price=Decimal('600.00'),
        currency=currency,
        periodicity=periodicity,
        subcategory=subcategory,
        payment=payment_account,
        first_date_payment=datetime.now().date(),
        second_date_payment=(datetime.now() + timedelta(days=30)).date(),
        credit_days=30,
        description='Crédito de otro usuario'
    )
    
    print(f"✅ Datos creados:")
    print(f"   - Usuario: {user.username} (ID: {user.id})")
    print(f"   - Otro usuario: {other_user.username} (ID: {other_user.id})")
    print(f"   - Créditos de {user.username}: {Credit.objects.filter(user=user).count()}")
    print(f"   - Créditos de {other_user.username}: {Credit.objects.filter(user=other_user).count()}")
    print(f"   - Total créditos: {Credit.objects.count()}")
    
    return user, other_user

def get_jwt_token(user):
    """Obtener token JWT para un usuario"""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

def test_api_without_token():
    """Probar API sin token (debe fallar)"""
    print("\n🔒 Probando API sin token...")
    
    url = "http://localhost:8000/dashboard/credits/"
    data = {
        'start_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
        'end_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("   ✅ Correcto: API rechaza petición sin token")
        else:
            print("   ❌ Error: API debería rechazar petición sin token")
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")

def test_api_with_token(user):
    """Probar API con token JWT"""
    print(f"\n🔑 Probando API con token JWT para {user.username}...")
    
    token = get_jwt_token(user)
    headers = {'Authorization': f'Bearer {token}'}
    
    url = "http://localhost:8000/dashboard/credits/"
    data = {
        'start_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
        'end_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Éxito: API acepta token")
            print(f"   📊 Resultados:")
            print(f"      - Total créditos: {result.get('count', 0)}")
            print(f"      - Página actual: {result.get('current_page', 'N/A')}")
            
            # Verificar que solo devuelve créditos del usuario autenticado
            user_credits = Credit.objects.filter(user=user).count()
            api_credits = result.get('count', 0)
            
            if api_credits == user_credits:
                print(f"      ✅ Correcto: API devuelve solo {api_credits} créditos del usuario")
            else:
                print(f"      ❌ Error: API devuelve {api_credits} créditos, debería ser {user_credits}")
                
        else:
            print(f"   ❌ Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")

def test_kpi_api(user):
    """Probar API de KPIs con token JWT"""
    print(f"\n📈 Probando API de KPIs con token JWT para {user.username}...")
    
    token = get_jwt_token(user)
    headers = {'Authorization': f'Bearer {token}'}
    
    url = "http://localhost:8000/dashboard/kpi/summary/"
    params = {
        'start_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
        'end_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Éxito: API de KPIs acepta token")
            print(f"   📊 KPIs del usuario:")
            print(f"      - Total créditos: {result.get('credit_count', 0)}")
            print(f"      - Monto total: ${result.get('total_credit_amount', 0)}")
            print(f"      - Abonos: ${result.get('abonos', 0)}")
            print(f"      - Tasa de morosidad: {result.get('morosidad_rate', 0)}%")
            
        else:
            print(f"   ❌ Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")

def test_filter_api(user):
    """Probar API de filtros con token JWT"""
    print(f"\n🔍 Probando API de filtros con token JWT para {user.username}...")
    
    token = get_jwt_token(user)
    headers = {'Authorization': f'Bearer {token}'}
    
    url = "http://localhost:8000/dashboard/credits/filter/"
    data = {
        'state': 'pending'
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Éxito: API de filtros acepta token")
            print(f"   📊 Resultados filtrados:")
            print(f"      - Total créditos: {result.get('count', 0)}")
            
            # Verificar que solo devuelve créditos del usuario autenticado
            user_pending_credits = Credit.objects.filter(user=user, state='pending').count()
            api_credits = result.get('count', 0)
            
            if api_credits == user_pending_credits:
                print(f"      ✅ Correcto: API devuelve solo {api_credits} créditos pendientes del usuario")
            else:
                print(f"      ❌ Error: API devuelve {api_credits} créditos, debería ser {user_pending_credits}")
                
        else:
            print(f"   ❌ Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")

def cleanup_test_data(user, other_user):
    """Limpiar datos de prueba"""
    print(f"\n🧹 Limpiando datos de prueba...")
    
    # Eliminar créditos de prueba
    Credit.objects.filter(user__in=[user, other_user]).delete()
    
    # Eliminar usuarios de prueba
    user.delete()
    other_user.delete()
    
    print("   ✅ Datos de prueba eliminados")

def main():
    """Función principal del test"""
    print("🚀 Iniciando test de autenticación JWT y filtrado por usuario")
    print("=" * 60)
    
    try:
        # Crear datos de prueba
        user, other_user = create_test_data()
        
        # Probar sin token
        test_api_without_token()
        
        # Probar con token del usuario principal
        test_api_with_token(user)
        
        # Probar con token del otro usuario
        test_api_with_token(other_user)
        
        # Probar API de KPIs
        test_kpi_api(user)
        
        # Probar API de filtros
        test_filter_api(user)
        
        print("\n" + "=" * 60)
        print("✅ Test completado")
        
    except Exception as e:
        print(f"\n❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Limpiar datos de prueba
        try:
            cleanup_test_data(user, other_user)
        except:
            pass

if __name__ == "__main__":
    main() 