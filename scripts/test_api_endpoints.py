#!/usr/bin/env python3
"""
Script simple para probar los endpoints de la API
"""

import requests
import json
from datetime import datetime, timedelta

def test_api_endpoints():
    """Probar los endpoints de la API"""
    base_url = "http://localhost:8000"
    
    print("🚀 Probando endpoints de la API")
    print("=" * 50)
    
    # 1. Probar endpoint sin autenticación (debe fallar)
    print("\n1️⃣ Probando endpoint sin autenticación...")
    try:
        response = requests.post(f"{base_url}/dashboard/credits/", json={
            'start_date': '2024-01-01',
            'end_date': '2024-12-31'
        })
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Correcto: API rechaza petición sin autenticación")
        else:
            print(f"   ❌ Error: Debería ser 401, es {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
    
    # 2. Probar endpoint con URL malformada
    print("\n2️⃣ Probando URL malformada...")
    try:
        response = requests.post(f"{base_url}/dashboard/credits/?page=1" + "}", json={
            'start_date': '2024-01-01',
            'end_date': '2024-12-31'
        })
        print(f"   Status: {response.status_code}")
        if response.status_code == 404:
            print("   ✅ Correcto: API rechaza URL malformada")
        else:
            print(f"   ⚠️ Status inesperado: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
    
    # 3. Probar endpoint con URL correcta
    print("\n3️⃣ Probando URL correcta...")
    try:
        response = requests.post(f"{base_url}/dashboard/credits/", json={
            'start_date': '2024-01-01',
            'end_date': '2024-12-31'
        })
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Correcto: API rechaza petición sin token JWT")
        else:
            print(f"   ⚠️ Status inesperado: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
    
    # 4. Verificar que el servidor está corriendo
    print("\n4️⃣ Verificando que el servidor está corriendo...")
    try:
        response = requests.get(f"{base_url}/admin/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Servidor está corriendo correctamente")
        else:
            print(f"   ⚠️ Servidor responde con status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("   💡 Asegúrate de que el servidor esté corriendo con: python3 manage.py runserver")
    
    print("\n" + "=" * 50)
    print("✅ Test completado")

if __name__ == "__main__":
    test_api_endpoints() 