#!/usr/bin/env python3
"""
Script para probar el acceso basado en roles implementado.
Ejecutar con: python3 manage.py shell < scripts/test_role_based_access.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.fintech.models import Credit, Currency, Periodicity, SubCategory, Account, Seller
from apps.fintech.services.credit_query_service import CreditQueryService

User = get_user_model()

def create_test_users():
    """Crear usuarios de prueba con diferentes roles"""
    print("🔧 Creando usuarios de prueba...")
    
    # 1. Super Admin
    super_admin, created = User.objects.get_or_create(
        username='superadmin_test',
        defaults={
            'email': 'superadmin@test.com',
            'first_name': 'Super',
            'last_name': 'Admin',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    # 2. Admin (no superuser)
    admin_user, created = User.objects.get_or_create(
        username='admin_test',
        defaults={
            'email': 'admin@test.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': False
        }
    )
    
    # 3. Seller
    seller_user, created = User.objects.get_or_create(
        username='seller_test',
        defaults={
            'email': 'seller@test.com',
            'first_name': 'Seller',
            'last_name': 'User',
            'is_staff': False,
            'is_superuser': False
        }
    )
    
    # Crear perfil de vendedor
    seller_profile, _ = Seller.objects.get_or_create(
        user=seller_user,
        defaults={
            'total_sales': Decimal('0.00'),
            'commissions': Decimal('0.00'),
            'returns': 0
        }
    )
    
    # 4. Client
    client_user, created = User.objects.get_or_create(
        username='client_test',
        defaults={
            'email': 'client@test.com',
            'first_name': 'Client',
            'last_name': 'User',
            'is_staff': False,
            'is_superuser': False
        }
    )
    
    print(f"✅ Usuarios creados:")
    print(f"   - Super Admin: {super_admin.username}")
    print(f"   - Admin: {admin_user.username}")
    print(f"   - Seller: {seller_user.username}")
    print(f"   - Client: {client_user.username}")
    
    return super_admin, admin_user, seller_user, client_user

def create_test_credits():
    """Crear créditos de prueba"""
    print("🔧 Creando créditos de prueba...")
    
    # Obtener datos necesarios
    currency, _ = Currency.objects.get_or_create(id_currency='USD', defaults={'currency': 'Dólar', 'exchange_rate': 1.0})
    periodicity, _ = Periodicity.objects.get_or_create(name='Mensual', defaults={'days': 30})
    subcategory, _ = SubCategory.objects.get_or_create(name='Préstamo Personal')
    payment_account, _ = Account.objects.get_or_create(name='Cuenta Principal', defaults={'account_number': '123456789', 'balance': Decimal('10000.00'), 'currency': currency})
    
    # Obtener usuarios
    super_admin, admin_user, seller_user, client_user = create_test_users()
    
    # Obtener perfil de vendedor
    seller_profile = Seller.objects.get(user=seller_user)
    
    # Crear créditos de prueba
    credits = []
    
    # Crédito 1: Vendedo por seller_user, cliente client_user
    credit1 = Credit.objects.create(
        user=client_user,
        seller=seller_profile,
        cost=Decimal('800.00'),
        price=Decimal('1000.00'),
        currency=currency,
        periodicity=periodicity,
        subcategory=subcategory,
        payment=payment_account,
        first_date_payment=datetime.now().date(),
        second_date_payment=(datetime.now() + timedelta(days=30)).date(),
        credit_days=30,
        description='Crédito de prueba 1 - Seller vende a Client'
    )
    credits.append(credit1)
    
    # Crédito 2: Vendedo por seller_user, cliente super_admin
    credit2 = Credit.objects.create(
        user=super_admin,
        seller=seller_profile,
        cost=Decimal('1200.00'),
        price=Decimal('1500.00'),
        currency=currency,
        periodicity=periodicity,
        subcategory=subcategory,
        payment=payment_account,
        first_date_payment=datetime.now().date(),
        second_date_payment=(datetime.now() + timedelta(days=30)).date(),
        credit_days=30,
        description='Crédito de prueba 2 - Seller vende a Super Admin'
    )
    credits.append(credit2)
    
    # Crédito 3: Cliente client_user (sin seller específico)
    credit3 = Credit.objects.create(
        user=client_user,
        seller=None,
        cost=Decimal('600.00'),
        price=Decimal('750.00'),
        currency=currency,
        periodicity=periodicity,
        subcategory=subcategory,
        payment=payment_account,
        first_date_payment=datetime.now().date(),
        second_date_payment=(datetime.now() + timedelta(days=30)).date(),
        credit_days=30,
        description='Crédito de prueba 3 - Client sin seller'
    )
    credits.append(credit3)
    
    print(f"✅ Créditos creados:")
    for i, credit in enumerate(credits, 1):
        print(f"   - Crédito {i}: {credit.uid} - Cliente: {credit.user.username}, Seller: {credit.seller.user.username if credit.seller else 'None'}")
    
    return credits

def test_role_based_access():
    """Probar acceso basado en roles"""
    print("\n🔍 Probando acceso basado en roles...")
    
    # Crear datos de prueba
    credits = create_test_credits()
    super_admin, admin_user, seller_user, client_user = create_test_users()
    
    # Probar cada tipo de usuario
    test_users = [
        ('Super Admin', super_admin),
        ('Admin', admin_user),
        ('Seller', seller_user),
        ('Client', client_user)
    ]
    
    for role_name, user in test_users:
        print(f"\n📊 Probando {role_name}: {user.username}")
        
        # Obtener créditos según rol
        user_credits = CreditQueryService.get_user_credits(user)
        
        print(f"   Créditos encontrados: {user_credits.count()}")
        
        # Mostrar detalles de cada crédito
        for credit in user_credits:
            seller_info = f"Seller: {credit.seller.user.username}" if credit.seller else "Sin seller"
            print(f"   - {credit.uid}: Cliente {credit.user.username}, {seller_info}")
        
        # Probar resumen
        summary = CreditQueryService.get_user_credits_summary(user)
        print(f"   Resumen: {summary}")

def test_date_range_filtering():
    """Probar filtrado por rango de fechas"""
    print("\n🔍 Probando filtrado por fechas...")
    
    super_admin, admin_user, seller_user, client_user = create_test_users()
    
    # Fechas de prueba
    start_date = datetime.now().date() - timedelta(days=7)
    end_date = datetime.now().date() + timedelta(days=7)
    
    for role_name, user in [('Super Admin', super_admin), ('Client', client_user)]:
        print(f"\n📊 {role_name} - Rango: {start_date} a {end_date}")
        
        credits = CreditQueryService.get_user_credits_by_date_range(user, start_date, end_date)
        print(f"   Créditos en rango: {credits.count()}")
        
        for credit in credits:
            print(f"   - {credit.uid}: {credit.created_at.date()}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de acceso basado en roles...")
    
    try:
        test_role_based_access()
        test_date_range_filtering()
        
        print("\n✅ Todas las pruebas completadas exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc() 