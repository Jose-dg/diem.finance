#!/usr/bin/env python3
"""
Script para probar compatibilidad con frontend.
Ejecutar con: python3 manage.py shell < scripts/test_frontend_compatibility.py
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.fintech.models import Seller, Credit
from apps.fintech.services.credit_query_service import CreditQueryService
from datetime import datetime

User = get_user_model()

print("🔍 Probando compatibilidad con frontend...")

# Obtener usuario
daniel_user = User.objects.get(username='danielojeda')
print(f"Usuario: {daniel_user.username}")

# Simular datos del frontend
frontend_data = {
    'start_date': '2025-05-01',
    'end_date': '2025-05-31',
    'status': None  # Opcional
}

print(f"Datos del frontend: {frontend_data}")

# Procesar fechas como lo haría la API
start_date = datetime.strptime(frontend_data['start_date'], '%Y-%m-%d').date()
end_date = datetime.strptime(frontend_data['end_date'], '%Y-%m-%d').date()

print(f"Fechas procesadas: {start_date} a {end_date}")

# Obtener créditos usando el servicio
base_qs = CreditQueryService.get_user_credits_by_date_range(
    daniel_user, 
    start_date, 
    end_date
).order_by('-created_at')

print(f"Créditos encontrados: {base_qs.count()}")

for credit in base_qs:
    print(f"  - {credit.uid}: Creado {credit.created_at.date()}")

# Probar con un rango más amplio que incluya el crédito de daniel
frontend_data_wide = {
    'start_date': '2025-06-01',
    'end_date': '2025-08-31'
}

print(f"\nProbando con rango amplio: {frontend_data_wide}")

start_date_wide = datetime.strptime(frontend_data_wide['start_date'], '%Y-%m-%d').date()
end_date_wide = datetime.strptime(frontend_data_wide['end_date'], '%Y-%m-%d').date()

base_qs_wide = CreditQueryService.get_user_credits_by_date_range(
    daniel_user, 
    start_date_wide, 
    end_date_wide
).order_by('-created_at')

print(f"Créditos encontrados (rango amplio): {base_qs_wide.count()}")

for credit in base_qs_wide:
    print(f"  - {credit.uid}: Creado {credit.created_at.date()}")

print("✅ Prueba completada!") 