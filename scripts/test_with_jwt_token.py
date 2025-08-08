#!/usr/bin/env python3
"""
Script para probar la API con token JWT real
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
from apps.fintech.models import Credit, Currency, Periodicity, SubCategory, Account, Seller
from decimal import Decimal

User = get_user_model()

def create_test_user_and_token():
    """Crear usuario de prueba y obtener token JWT"""
    print("🔧 Creando usuario de prueba y token JWT...")
    
    # Crear usuario admin para probar
    admin_user, created = User.objects.get_or_create(
        username='testadmin_jwt',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Test',
            'last_name': 'Admin',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    # Crear seller para el admin
    seller, _ = Seller.objects.get_or_create(
        user=admin_user,
        defaults={
            'total_sales': Decimal('0.00'),
            'commissions': Decimal('0.00'),
            'returns': 0
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
    
    # Crear crédito de prueba
    credit = Credit.objects.create(
        user=admin_user,
        seller=seller,
        cost=Decimal('800.00'),
        price=Decimal('1000.00'),
        currency=currency,
        periodicity=periodicity,
        subcategory=subcategory,
        payment=payment_account,
        first_date_payment=datetime.now().date(),
        second_date_payment=(datetime.now() + timedelta(days=30)).date(),
        credit_days=30,
        description='Crédito de prueba para test JWT'
    )
    
    # Generar token JWT
    refresh = RefreshToken.for_user(admin_user)
    access_token = str(refresh.access_token)
    
    print(f"✅ Usuario creado: {admin_user.username}")
    print(f"✅ Token JWT generado: {access_token[:50]}...")
    print(f"✅ Crédito de prueba creado: {credit.uid}")
    
    return admin_user, access_token, credit

def test_api_with_jwt_token():
    """Probar API con token JWT real"""
    print("\n🔍 Probando API con token JWT...")
    
    admin_user, access_token, credit = create_test_user_and_token()
    
    base_url = "http://localhost:8000"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # 1. Probar endpoint de créditos
    print("\n1️⃣ Probando endpoint de créditos...")
    try:
        response = requests.post(
            f"{base_url}/dashboard/credits/",
            json={
                'start_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'end_date': datetime.now().strftime('%Y-%m-%d')
            },
            headers=headers
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Éxito: API acepta token JWT")
            print(f"   📊 Resultados:")
            print(f"      - Total créditos: {data.get('count', 0)}")
            print(f"      - Página actual: {data.get('current_page', 'N/A')}")
            print(f"      - Resultados por página: {len(data.get('results', []))}")
            
            # Verificar que devuelve créditos del admin
            if data.get('count', 0) > 0:
                print(f"   ✅ Correcto: API devuelve créditos del admin")
            else:
                print(f"   ⚠️ Advertencia: No se encontraron créditos")
                
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
    
    # 2. Probar endpoint de filtros
    print("\n2️⃣ Probando endpoint de filtros...")
    try:
        response = requests.post(
            f"{base_url}/dashboard/credits/filter/",
            json={'state': 'pending'},
            headers=headers
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Éxito: API de filtros acepta token JWT")
            print(f"   📊 Resultados filtrados:")
            print(f"      - Total créditos: {data.get('count', 0)}")
            
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
    
    # 3. Probar endpoint de KPIs
    print("\n3️⃣ Probando endpoint de KPIs...")
    try:
        response = requests.get(
            f"{base_url}/dashboard/kpi/summary/",
            params={
                'start_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'end_date': datetime.now().strftime('%Y-%m-%d')
            },
            headers=headers
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Éxito: API de KPIs acepta token JWT")
            print(f"   📊 KPIs:")
            print(f"      - Total créditos: {data.get('credit_count', 0)}")
            print(f"      - Monto total: ${data.get('total_credit_amount', 0)}")
            
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
    
    # Limpiar datos de prueba
    print(f"\n🧹 Limpiando datos de prueba...")
    credit.delete()
    admin_user.delete()
    print("   ✅ Datos de prueba eliminados")

def main():
    """Función principal"""
    print("🚀 Test de API con JWT Token")
    print("=" * 50)
    
    try:
        test_api_with_jwt_token()
        
        print("\n" + "=" * 50)
        print("✅ Test completado exitosamente")
        
    except Exception as e:
        print(f"\n❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 