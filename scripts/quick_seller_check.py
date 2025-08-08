#!/usr/bin/env python3
"""
Script rápido para verificar sellers y créditos.
Ejecutar con: python3 manage.py shell < scripts/quick_seller_check.py
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.fintech.models import Seller, Credit
from apps.fintech.services.credit_query_service import CreditQueryService

print("🔍 Verificando sellers existentes...")

# Contar sellers
sellers_count = Seller.objects.count()
print(f"Total sellers: {sellers_count}")

if sellers_count > 0:
    # Mostrar primeros 5 sellers
    sellers = Seller.objects.all()[:5]
    for seller in sellers:
        print(f"\n👤 Seller: {seller.user.username}")
        print(f"   - Email: {seller.user.email}")
        print(f"   - is_staff: {seller.user.is_staff}")
        print(f"   - is_superuser: {seller.user.is_superuser}")
        
        # Créditos vendidos por este seller
        credits_count = Credit.objects.filter(seller=seller).count()
        print(f"   - Créditos vendidos: {credits_count}")
        
        # Probar acceso usando el servicio
        user_credits = CreditQueryService.get_user_credits(seller.user)
        print(f"   - Créditos accesibles según rol: {user_credits.count()}")
else:
    print("❌ No hay sellers registrados")

print("\n🔍 Verificando créditos totales...")
total_credits = Credit.objects.count()
print(f"Total créditos en sistema: {total_credits}")

if total_credits > 0:
    # Mostrar algunos créditos con sus sellers
    credits = Credit.objects.select_related('seller__user', 'user')[:5]
    for credit in credits:
        seller_name = credit.seller.user.username if credit.seller else "Sin seller"
        print(f"   - {credit.uid}: Cliente {credit.user.username}, Seller: {seller_name}")

print("✅ Verificación completada!") 