#!/usr/bin/env python3
"""
Script para probar la nueva lógica de la API.
Ejecutar con: python3 manage.py shell < scripts/test_new_api_logic.py
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.fintech.models import Seller, Credit
from apps.fintech.services.credit_query_service import CreditQueryService

User = get_user_model()

print("🔍 Probando nueva lógica de API...")

# Obtener usuario
daniel_user = User.objects.get(username='danielojeda')
print(f"Usuario: {daniel_user.username}")

# Probar sin filtro de fecha (nueva lógica)
base_qs = CreditQueryService.get_user_credits(daniel_user).order_by('-created_at')
print(f"Créditos sin filtro de fecha: {base_qs.count()}")

for credit in base_qs:
    print(f"  - {credit.uid}: Creado {credit.created_at.date()}")

print("✅ Prueba completada!") 