#!/usr/bin/env python3
"""
Script automático para intercambiar créditos entre sellers.
Ejecutar con: python3 manage.py shell < scripts/swap_seller_credits_auto.py
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

def swap_seller_credits():
    """Intercambiar créditos entre danielojeda y HectorAA"""
    print("🔄 Intercambiando créditos entre sellers...")
    
    try:
        # Obtener los sellers
        daniel_seller = Seller.objects.get(user__username='danielojeda')
        hector_seller = Seller.objects.get(user__username='HectorAA')
        
        print(f"   - danielojeda: {daniel_seller.user.username}")
        print(f"   - HectorAA: {hector_seller.user.username}")
        
        # Contar créditos actuales
        daniel_credits_before = Credit.objects.filter(seller=daniel_seller).count()
        hector_credits_before = Credit.objects.filter(seller=hector_seller).count()
        
        print(f"\n📊 Créditos antes del intercambio:")
        print(f"   - danielojeda: {daniel_credits_before} créditos")
        print(f"   - HectorAA: {hector_credits_before} créditos")
        
        # Realizar el intercambio en una transacción
        with transaction.atomic():
            # Obtener todos los créditos de daniel
            daniel_credits = list(Credit.objects.filter(seller=daniel_seller))
            hector_credits = list(Credit.objects.filter(seller=hector_seller))
            
            print(f"\n🔄 Intercambiando...")
            print(f"   - Moviendo {len(daniel_credits)} créditos de danielojeda a HectorAA")
            print(f"   - Moviendo {len(hector_credits)} créditos de HectorAA a danielojeda")
            
            # Intercambiar
            for credit in daniel_credits:
                credit.seller = hector_seller
                credit.save()
            
            for credit in hector_credits:
                credit.seller = daniel_seller
                credit.save()
        
        # Verificar resultado
        daniel_credits_after = Credit.objects.filter(seller=daniel_seller).count()
        hector_credits_after = Credit.objects.filter(seller=hector_seller).count()
        
        print(f"\n📊 Créditos después del intercambio:")
        print(f"   - danielojeda: {daniel_credits_after} créditos")
        print(f"   - HectorAA: {hector_credits_after} créditos")
        
        # Verificar que el intercambio fue correcto
        if daniel_credits_after == hector_credits_before and hector_credits_after == daniel_credits_before:
            print("✅ Intercambio exitoso!")
        else:
            print("❌ Error en el intercambio")
            
    except Seller.DoesNotExist as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Error durante el intercambio: {e}")

def test_access_after_swap():
    """Probar acceso después del intercambio"""
    print("\n🔍 Probando acceso después del intercambio...")
    
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

if __name__ == "__main__":
    print("🚀 Iniciando intercambio automático de créditos entre sellers...")
    
    # Mostrar estado inicial
    show_current_state()
    
    # Realizar intercambio automáticamente
    swap_seller_credits()
    
    # Probar acceso después del intercambio
    test_access_after_swap()
    
    print("\n✅ Intercambio completado!") 