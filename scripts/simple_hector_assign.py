#!/usr/bin/env python3
"""
Script simple para asignar todos los créditos a HectorAA.
Ejecutar con: python3 manage.py shell < scripts/simple_hector_assign.py
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.fintech.models import Seller, Credit

print("🚀 Asignando todos los créditos a HectorAA...")

# Obtener el seller de Hector
hector_seller = Seller.objects.get(user__username='HectorAA')
print(f"✅ Encontrado seller: {hector_seller.user.username}")

# Contar créditos actuales
total_credits = Credit.objects.count()
hector_credits_before = Credit.objects.filter(seller=hector_seller).count()
print(f"📊 Total créditos: {total_credits}")
print(f"📊 Créditos de Hector antes: {hector_credits_before}")

# Asignar todos los créditos a Hector
Credit.objects.all().update(seller=hector_seller)
print("✅ Todos los créditos asignados a HectorAA")

# Verificar resultado
hector_credits_after = Credit.objects.filter(seller=hector_seller).count()
print(f"📊 Créditos de Hector después: {hector_credits_after}")

if hector_credits_after == total_credits:
    print("🎉 ¡Éxito! HectorAA ahora tiene todos los créditos")
else:
    print("❌ Error en la asignación")

print("✅ Script completado!") 