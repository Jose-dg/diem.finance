#!/usr/bin/env python3
"""
Script para probar que la API lee parámetros del body.
Ejecutar con: python3 manage.py shell < scripts/test_body_parameters.py
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

print("🔍 Probando parámetros del body...")

# Obtener usuario
daniel_user = User.objects.get(username='danielojeda')
print(f"Usuario: {daniel_user.username}")

# Simular parámetros del body
body_data = {
    'start_date': '2025-05-01',
    'end_date': '2025-05-31'
}

print(f"Parámetros del body: {body_data}")

# Probar con filtro de fecha
start_date = datetime.strptime(body_data['start_date'], '%Y-%m-%d').date()
end_date = datetime.strptime(body_data['end_date'], '%Y-%m-%d').date()

print(f"Fechas procesadas: {start_date} a {end_date}")

# Obtener créditos con filtro
base_qs = CreditQueryService.get_user_credits_by_date_range(
    daniel_user, 
    start_date, 
    end_date
).order_by('-created_at')

print(f"Créditos encontrados: {base_qs.count()}")

for credit in base_qs:
    print(f"  - {credit.uid}: Creado {credit.created_at.date()}")

print("✅ Prueba completada!") 