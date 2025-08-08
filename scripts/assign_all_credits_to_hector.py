#!/usr/bin/env python3
"""
Script para asignar todos los créditos a HectorAA.
Ejecutar con: python3 manage.py shell < scripts/assign_all_credits_to_hector.py
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import transaction
from apps.fintech.models import Seller, Credit
from apps.fintech.services.credit_query_service import CreditQueryService

def show_current_state():
    """Mostrar estado actual de los sellers"""
    print("🔍 Estado actual de los sellers:")
    
    sellers = Seller.objects.all()
    for seller in sellers:
        credits_count = Credit.objects.filter(seller=seller).count()
        print(f"   - {seller.user.username}: {credits_count} créditos")
    
    print()

def assign_all_credits_to_hector():
    """Asignar todos los créditos a HectorAA"""
    print("🔄 Asignando todos los créditos a HectorAA...")
    
    try:
        # Obtener el seller de Hector
        hector_seller = Seller.objects.get(user__username='HectorAA')
        
        print(f"   - HectorAA: {hector_seller.user.username}")
        
        # Contar créditos actuales
        total_credits = Credit.objects.count()
        hector_credits_before = Credit.objects.filter(seller=hector_seller).count()
        other_credits = total_credits - hector_credits_before
        
        print(f"\n📊 Estado antes del cambio:")
        print(f"   - Total créditos en sistema: {total_credits}")
        print(f"   - HectorAA: {hector_credits_before} créditos")
        print(f"   - Otros sellers: {other_credits} créditos")
        
        # Asignar todos los créditos a Hector
        with transaction.atomic():
            # Obtener todos los créditos que NO son de Hector
            credits_to_move = Credit.objects.exclude(seller=hector_seller)
            credits_count = credits_to_move.count()
            
            print(f"\n🔄 Moviendo {credits_count} créditos a HectorAA...")
            
            # Asignar todos a Hector
            credits_to_move.update(seller=hector_seller)
        
        # Verificar resultado
        hector_credits_after = Credit.objects.filter(seller=hector_seller).count()
        other_credits_after = Credit.objects.exclude(seller=hector_seller).count()
        
        print(f"\n📊 Estado después del cambio:")
        print(f"   - HectorAA: {hector_credits_after} créditos")
        print(f"   - Otros sellers: {other_credits_after} créditos")
        
        # Verificar que el cambio fue correcto
        if hector_credits_after == total_credits and other_credits_after == 0:
            print("✅ Asignación exitosa! HectorAA ahora tiene todos los créditos")
        else:
            print("❌ Error en la asignación")
            
    except Seller.DoesNotExist as e:
        print(f"❌ Error: No se encontró el seller HectorAA")
    except Exception as e:
        print(f"❌ Error durante la asignación: {e}")

def test_access_after_change():
    """Probar acceso después del cambio"""
    print("\n🔍 Probando acceso después del cambio...")
    
    sellers = Seller.objects.all()
    for seller in sellers:
        user = seller.user
        accessible_credits = CreditQueryService.get_user_credits(user).count()
        actual_sales = Credit.objects.filter(seller=seller).count()
        
        print(f"\n👤 {user.username}:")
        print(f"   - Créditos accesibles según rol: {accessible_credits}")
        print(f"   - Créditos realmente vendidos: {actual_sales}")
        
        if accessible_credits == actual_sales:
            print(f"   ✅ CORRECTO")
        else:
            print(f"   ❌ ERROR")

def show_credits_without_seller():
    """Mostrar créditos sin seller asignado"""
    print("\n🔍 Verificando créditos sin seller...")
    
    credits_without_seller = Credit.objects.filter(seller__isnull=True)
    count = credits_without_seller.count()
    
    if count > 0:
        print(f"   - Créditos sin seller: {count}")
        for credit in credits_without_seller[:5]:  # Mostrar solo primeros 5
            print(f"   - {credit.uid}: Cliente {credit.user.username}")
    else:
        print("   - No hay créditos sin seller")

if __name__ == "__main__":
    print("🚀 Iniciando asignación de todos los créditos a HectorAA...")
    
    # Mostrar estado inicial
    show_current_state()
    
    # Verificar créditos sin seller
    show_credits_without_seller()
    
    # Realizar asignación
    assign_all_credits_to_hector()
    
    # Probar acceso después del cambio
    test_access_after_change()
    
    print("\n✅ Asignación completada!") 