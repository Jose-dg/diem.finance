#!/usr/bin/env python3
"""
Script simple para probar el acceso basado en roles.
Ejecutar con: python3 manage.py shell < scripts/test_simple_roles.py
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.fintech.services.credit_query_service import CreditQueryService

User = get_user_model()

def test_basic_roles():
    print("🔍 Probando roles básicos...")
    
    # Obtener usuarios existentes
    users = User.objects.all()[:5]  # Primeros 5 usuarios
    
    for user in users:
        print(f"\n👤 Usuario: {user.username}")
        print(f"   is_superuser: {user.is_superuser}")
        print(f"   is_staff: {user.is_staff}")
        print(f"   has seller_profile: {hasattr(user, 'seller_profile')}")
        
        # Probar acceso
        credits = CreditQueryService.get_user_credits(user)
        print(f"   Créditos encontrados: {credits.count()}")
        
        # Mostrar algunos créditos
        for credit in credits[:3]:  # Solo primeros 3
            seller_info = f"Seller: {credit.seller.user.username}" if credit.seller else "Sin seller"
            print(f"   - {credit.uid}: Cliente {credit.user.username}, {seller_info}")

if __name__ == "__main__":
    print("🚀 Iniciando prueba simple de roles...")
    test_basic_roles()
    print("✅ Prueba completada!") 