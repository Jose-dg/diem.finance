#!/usr/bin/env python3
"""
Script para simular exactamente lo que hace la API.
Ejecutar con: python3 manage.py shell < scripts/debug_api_simulation.py
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.fintech.models import Seller, Credit
from apps.fintech.services.credit_query_service import CreditQueryService
from datetime import datetime, timedelta

User = get_user_model()

print("🔍 Simulando API para danielojeda...")

# Obtener usuario
daniel_user = User.objects.get(username='danielojeda')
print(f"Usuario: {daniel_user.username}")

# Simular lo que hace la API (fechas por defecto - últimos 30 días)
end_aware = datetime.now()
start_aware = end_aware - timedelta(days=30)

print(f"Fechas por defecto de la API:")
print(f"  - start_date: {start_aware.date()}")
print(f"  - end_date: {end_aware.date()}")

# Obtener créditos usando el mismo método que la API
base_qs = CreditQueryService.get_user_credits_by_date_range(
    daniel_user, 
    start_aware.date(), 
    end_aware.date()
).order_by('-created_at')

print(f"\nCréditos encontrados: {base_qs.count()}")

# Mostrar detalles del crédito si existe
for credit in base_qs:
    print(f"  - {credit.uid}: Creado {credit.created_at.date()}")

# Verificar si el crédito existe pero fuera del rango
all_credits = CreditQueryService.get_user_credits(daniel_user)
print(f"\nTotal créditos sin filtro de fecha: {all_credits.count()}")

for credit in all_credits:
    print(f"  - {credit.uid}: Creado {credit.created_at.date()}")

# Verificar si el problema es el rango de fechas
if all_credits.count() > base_qs.count():
    print(f"\n⚠️ PROBLEMA DETECTADO: El filtro de fecha está excluyendo créditos!")
    print(f"  - Con filtro de fecha: {base_qs.count()}")
    print(f"  - Sin filtro de fecha: {all_credits.count()}")

print("✅ Simulación completada!") 