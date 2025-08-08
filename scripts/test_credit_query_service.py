#!/usr/bin/env python3
"""
Script para probar el CreditQueryService
Ejecutar: python3 manage.py shell < scripts/test_credit_query_service.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.fintech.models import Credit, Currency, Periodicity, SubCategory, Account, Seller
from apps.fintech.services.credit_query_service import CreditQueryService

User = get_user_model()

def create_test_data():
    """Crear datos de prueba"""
    print("🔧 Creando datos de prueba...")
    
    # Crear usuario cliente
    client_user, _ = User.objects.get_or_create(
        username='testclient',
        defaults={
            'email': 'client@example.com',
            'first_name': 'Test',
            'last_name': 'Client'
        }
    )
    
    # Crear usuario admin
    admin_user, _ = User.objects.get_or_create(
        username='testadmin',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Test',
            'last_name': 'Admin',
            'is_staff': True
        }
    )
    
    # Crear seller para el admin
    seller, _ = Seller.objects.get_or_create(
        user=admin_user,
        defaults={
            'total_sales': Decimal('0.00'),
            'commissions': Decimal('0.00'),
            'returns': 0
        }
    )
    
    # Crear datos necesarios
    currency, _ = Currency.objects.get_or_create(
        id_currency='USD',
        defaults={'currency': 'Dólar', 'exchange_rate': 1.0}
    )
    
    periodicity, _ = Periodicity.objects.get_or_create(
        name='Mensual',
        defaults={'days': 30}
    )
    
    subcategory, _ = SubCategory.objects.get_or_create(
        name='Préstamo Personal'
    )
    
    payment_account, _ = Account.objects.get_or_create(
        name='Cuenta Principal',
        defaults={
            'account_number': '123456789',
            'balance': Decimal('10000.00'),
            'currency': currency
        }
    )
    
    # Crear crédito para cliente
    client_credit = Credit.objects.create(
        user=client_user,
        seller=seller,  # Vendido por el admin
        cost=Decimal('800.00'),
        price=Decimal('1000.00'),
        currency=currency,
        periodicity=periodicity,
        subcategory=subcategory,
        payment=payment_account,
        first_date_payment=datetime.now().date(),
        second_date_payment=(datetime.now() + timedelta(days=30)).date(),
        credit_days=30,
        description='Crédito de cliente'
    )
    
    # Crear crédito para admin (como cliente)
    admin_credit = Credit.objects.create(
        user=admin_user,
        seller=seller,
        cost=Decimal('1200.00'),
        price=Decimal('1500.00'),
        currency=currency,
        periodicity=periodicity,
        subcategory=subcategory,
        payment=payment_account,
        first_date_payment=datetime.now().date(),
        second_date_payment=(datetime.now() + timedelta(days=30)).date(),
        credit_days=30,
        description='Crédito de admin como cliente'
    )
    
    print(f"✅ Datos creados:")
    print(f"   - Cliente: {client_user.username} (is_staff: {client_user.is_staff})")
    print(f"   - Admin: {admin_user.username} (is_staff: {admin_user.is_staff})")
    print(f"   - Créditos del cliente: {Credit.objects.filter(user=client_user).count()}")
    print(f"   - Créditos vendidos por admin: {Credit.objects.filter(seller__user=admin_user).count()}")
    
    return client_user, admin_user

def test_credit_query_service():
    """Probar CreditQueryService"""
    print("\n🔍 Probando CreditQueryService...")
    
    client_user, admin_user = create_test_data()
    
    try:
        # Probar con cliente
        print(f"\n👤 Probando con cliente ({client_user.username}):")
        client_credits = CreditQueryService.get_user_credits(client_user)
        print(f"   - Créditos encontrados: {client_credits.count()}")
        print(f"   - Tipo esperado: cliente")
        print(f"   - Tipo detectado: {'admin' if (client_user.is_staff or client_user.is_superuser) else 'client'}")
        
        # Probar con admin
        print(f"\n🔧 Probando con admin ({admin_user.username}):")
        admin_credits = CreditQueryService.get_user_credits(admin_user)
        print(f"   - Créditos encontrados: {admin_credits.count()}")
        print(f"   - Tipo esperado: admin")
        print(f"   - Tipo detectado: {'admin' if (admin_user.is_staff or admin_user.is_superuser) else 'client'}")
        
        # Verificar que el filtrado funciona correctamente
        expected_client_credits = Credit.objects.filter(user=client_user).count()
        expected_admin_credits = Credit.objects.filter(seller__user=admin_user).count()
        
        if client_credits.count() == expected_client_credits:
            print("   ✅ Correcto: Cliente ve sus propios créditos")
        else:
            print(f"   ❌ Error: Cliente debería ver {expected_client_credits} créditos, ve {client_credits.count()}")
        
        if admin_credits.count() == expected_admin_credits:
            print("   ✅ Correcto: Admin ve créditos que vendió")
        else:
            print(f"   ❌ Error: Admin debería ver {expected_admin_credits} créditos, ve {admin_credits.count()}")
        
        # Probar métodos adicionales
        print(f"\n📊 Probando métodos adicionales:")
        
        # Resumen de cliente
        client_summary = CreditQueryService.get_user_credits_summary(client_user)
        print(f"   - Resumen cliente: {client_summary}")
        
        # Resumen de admin
        admin_summary = CreditQueryService.get_user_credits_summary(admin_user)
        print(f"   - Resumen admin: {admin_summary}")
        
    except Exception as e:
        print(f"   ❌ Error probando servicio: {e}")
        import traceback
        traceback.print_exc()

def cleanup_test_data(client_user, admin_user):
    """Limpiar datos de prueba"""
    print(f"\n🧹 Limpiando datos de prueba...")
    
    # Eliminar créditos
    Credit.objects.filter(user__in=[client_user, admin_user]).delete()
    
    # Eliminar seller
    if hasattr(admin_user, 'seller_profile'):
        admin_user.seller_profile.delete()
    
    # Eliminar usuarios
    client_user.delete()
    admin_user.delete()
    
    print("   ✅ Datos de prueba eliminados")

def main():
    """Función principal"""
    print("🚀 Test de CreditQueryService")
    print("=" * 50)
    
    try:
        test_credit_query_service()
        
        print("\n" + "=" * 50)
        print("✅ Test completado")
        
    except Exception as e:
        print(f"\n❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 