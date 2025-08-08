#!/usr/bin/env python3
"""
Script simple para debuggear danielojeda.
Ejecutar con: python3 manage.py shell < scripts/simple_debug.py
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

print("🔍 Debuggeando danielojeda...")

# Obtener usuario
daniel_user = User.objects.get(username='danielojeda')
print(f"Usuario: {daniel_user.username}")
print(f"is_staff: {daniel_user.is_staff}")
print(f"is_superuser: {daniel_user.is_superuser}")
print(f"has seller_profile: {hasattr(daniel_user, 'seller_profile')}")

# Verificar seller
if hasattr(daniel_user, 'seller_profile'):
    seller = daniel_user.seller_profile
    print(f"Seller ID: {seller.id}")
    
    # Créditos directos
    direct_credits = Credit.objects.filter(seller=seller)
    print(f"Créditos directos: {direct_credits.count()}")
    
    # Créditos del servicio
    service_credits = CreditQueryService.get_user_credits(daniel_user)
    print(f"Créditos del servicio: {service_credits.count()}")
    
    if direct_credits.count() != service_credits.count():
        print("⚠️ DIFERENCIA DETECTADA!")
    else:
        print("✅ Los números coinciden")

print("✅ Debug completado!") 