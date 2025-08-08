#!/usr/bin/env python3
"""
Script para verificar sellers existentes y probar acceso a créditos.
Ejecutar con: python3 manage.py shell < scripts/check_sellers_and_credits.py
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

def check_existing_sellers():
    """Verificar sellers existentes en el sistema"""
    print("🔍 Verificando sellers existentes...")
    
    sellers = Seller.objects.all().select_related('user', 'role')
    
    if not sellers.exists():
        print("❌ No hay sellers registrados en el sistema")
        return []
    
    print(f"✅ Se encontraron {sellers.count()} sellers:")
    
    for seller in sellers:
        print(f"\n👤 Seller: {seller.user.username}")
        print(f"   - Email: {seller.user.email}")
        print(f"   - Nombre: {seller.user.first_name} {seller.user.last_name}")
        print(f"   - is_staff: {seller.user.is_staff}")
        print(f"   - is_superuser: {seller.user.is_superuser}")
        print(f"   - Role: {seller.role.name if seller.role else 'Sin rol'}")
        print(f"   - Total sales: {seller.total_sales}")
        print(f"   - Commissions: {seller.commissions}")
        print(f"   - Returns: {seller.returns}")
    
    return sellers

def check_credits_by_seller():
    """Verificar créditos asociados a cada seller"""
    print("\n🔍 Verificando créditos por seller...")
    
    sellers = Seller.objects.all().select_related('user')
    
    for seller in sellers:
        print(f"\n📊 Créditos vendidos por {seller.user.username}:")
        
        # Créditos donde este seller es el vendedor
        seller_credits = Credit.objects.filter(seller=seller)
        print(f"   Total créditos vendidos: {seller_credits.count()}")
        
        if seller_credits.exists():
            for credit in seller_credits[:5]:  # Mostrar solo primeros 5
                print(f"   - {credit.uid}: Cliente {credit.user.username}, Monto: {credit.price}")
        else:
            print("   - No tiene créditos vendidos")

def test_role_based_access_for_sellers():
    """Probar acceso basado en roles para sellers"""
    print("\n🔍 Probando acceso basado en roles para sellers...")
    
    sellers = Seller.objects.all().select_related('user')
    
    for seller in sellers:
        user = seller.user
        print(f"\n👤 Probando acceso para seller: {user.username}")
        
        # Verificar tipo de usuario
        user_type = "super_admin" if user.is_superuser else \
                   "admin" if user.is_staff else \
                   "seller" if hasattr(user, 'seller_profile') else "client"
        
        print(f"   Tipo de usuario: {user_type}")
        
        # Probar acceso usando CreditQueryService
        user_credits = CreditQueryService.get_user_credits(user)
        print(f"   Créditos accesibles según rol: {user_credits.count()}")
        
        # Mostrar algunos créditos
        for credit in user_credits[:3]:
            seller_info = f"Seller: {credit.seller.user.username}" if credit.seller else "Sin seller"
            print(f"   - {credit.uid}: Cliente {credit.user.username}, {seller_info}")

def test_specific_seller_access():
    """Probar acceso específico para un seller"""
    print("\n🔍 Probando acceso específico para sellers...")
    
    # Obtener el primer seller
    seller = Seller.objects.first()
    if not seller:
        print("❌ No hay sellers para probar")
        return
    
    user = seller.user
    print(f"👤 Probando acceso específico para: {user.username}")
    
    # Probar diferentes métodos del servicio
    print(f"\n📊 Resumen de créditos:")
    summary = CreditQueryService.get_user_credits_summary(user)
    for key, value in summary.items():
        print(f"   {key}: {value}")
    
    # Probar filtrado por fecha
    from datetime import datetime, timedelta
    start_date = datetime.now().date() - timedelta(days=365)  # Último año
    end_date = datetime.now().date()
    
    print(f"\n📅 Créditos en rango {start_date} a {end_date}:")
    date_filtered_credits = CreditQueryService.get_user_credits_by_date_range(user, start_date, end_date)
    print(f"   Total: {date_filtered_credits.count()}")
    
    for credit in date_filtered_credits[:3]:
        print(f"   - {credit.uid}: {credit.created_at.date()}")

def create_test_seller_if_needed():
    """Crear un seller de prueba si no hay ninguno"""
    print("\n🔧 Verificando si necesitamos crear seller de prueba...")
    
    if not Seller.objects.exists():
        print("⚠️ No hay sellers, creando uno de prueba...")
        
        # Crear usuario para seller
        seller_user, created = User.objects.get_or_create(
            username='test_seller',
            defaults={
                'email': 'seller@test.com',
                'first_name': 'Test',
                'last_name': 'Seller',
                'is_staff': False,
                'is_superuser': False
            }
        )
        
        # Crear seller
        seller, created = Seller.objects.get_or_create(
            user=seller_user,
            defaults={
                'total_sales': 0,
                'commissions': 0,
                'returns': 0
            }
        )
        
        print(f"✅ Seller de prueba creado: {seller.user.username}")
        return seller
    
    print("✅ Ya hay sellers existentes")
    return None

if __name__ == "__main__":
    print("🚀 Iniciando verificación de sellers y créditos...")
    
    try:
        # Crear seller de prueba si es necesario
        test_seller = create_test_seller_if_needed()
        
        # Verificar sellers existentes
        sellers = check_existing_sellers()
        
        # Verificar créditos por seller
        check_credits_by_seller()
        
        # Probar acceso basado en roles
        test_role_based_access_for_sellers()
        
        # Probar acceso específico
        test_specific_seller_access()
        
        print("\n✅ Verificación completada exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error durante la verificación: {str(e)}")
        import traceback
        traceback.print_exc() 