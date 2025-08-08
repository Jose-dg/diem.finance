#!/usr/bin/env python3
"""
Script para probar la lógica corregida de roles.
Ejecutar con: python3 manage.py shell < scripts/test_fixed_roles.py
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.fintech.models import Seller, Credit
from apps.fintech.services.credit_query_service import CreditQueryService

print("🔍 Probando lógica corregida de roles...")

# Obtener sellers
sellers = Seller.objects.all()

for seller in sellers:
    user = seller.user
    print(f"\n👤 Probando seller: {user.username}")
    print(f"   - is_staff: {user.is_staff}")
    print(f"   - is_superuser: {user.is_superuser}")
    print(f"   - has seller_profile: {hasattr(user, 'seller_profile')}")
    
    # Créditos que realmente vendió
    actual_sales = Credit.objects.filter(seller=seller).count()
    print(f"   - Créditos realmente vendidos: {actual_sales}")
    
    # Créditos que puede ver según el servicio
    accessible_credits = CreditQueryService.get_user_credits(user).count()
    print(f"   - Créditos accesibles según rol: {accessible_credits}")
    
    # Verificar si coincide
    if actual_sales == accessible_credits:
        print(f"   ✅ CORRECTO: Ve solo sus ventas")
    else:
        print(f"   ❌ ERROR: Ve {accessible_credits} pero vendió {actual_sales}")

print("\n✅ Prueba completada!") 