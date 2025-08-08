#!/usr/bin/env python3
"""
Test simple para verificar JWT authentication
Ejecutar: python3 manage.py shell < scripts/test_jwt_simple.py
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
from rest_framework_simplejwt.tokens import RefreshToken
from apps.fintech.models import Credit, Currency, Periodicity, SubCategory, Account
from apps.fintech.services.kpi_service import KPIService

User = get_user_model()

def test_jwt_token_generation():
    """Probar generación de tokens JWT"""
    print("🔑 Probando generación de tokens JWT...")
    
    # Crear usuario de prueba
    user, created = User.objects.get_or_create(
        username='testuser_jwt',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    try:
        # Generar token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        print(f"   ✅ Token generado exitosamente")
        print(f"   Usuario: {user.username}")
        print(f"   Token: {access_token[:50]}...")
        
        return user, access_token
        
    except Exception as e:
        print(f"   ❌ Error generando token: {e}")
        return None, None

def test_kpi_service_with_user():
    """Probar KPIService con filtrado por usuario"""
    print("\n📈 Probando KPIService con filtrado por usuario...")
    
    user, token = test_jwt_token_generation()
    if not user:
        return
    
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
    
    # Crear crédito de prueba
    credit = Credit.objects.create(
        user=user,
        cost=Decimal('800.00'),
        price=Decimal('1000.00'),
        currency=currency,
        periodicity=periodicity,
        subcategory=subcategory,
        payment=payment_account,
        first_date_payment=datetime.now().date(),
        second_date_payment=(datetime.now() + timedelta(days=30)).date(),
        credit_days=30,
        description='Crédito de prueba'
    )
    
    try:
        # Probar KPIService sin filtro de usuario
        start_date = (datetime.now() - timedelta(days=30)).date()
        end_date = datetime.now().date()
        
        kpis_all = KPIService.get_credit_kpi_summary(start_date, end_date)
        print(f"   📊 KPIs sin filtro de usuario:")
        print(f"      - Total créditos: {kpis_all.get('credit_count', 0)}")
        print(f"      - Monto total: ${kpis_all.get('total_credit_amount', 0)}")
        
        # Probar KPIService con filtro de usuario
        kpis_user = KPIService.get_credit_kpi_summary(start_date, end_date, user=user)
        print(f"   📊 KPIs con filtro de usuario:")
        print(f"      - Total créditos: {kpis_user.get('credit_count', 0)}")
        print(f"      - Monto total: ${kpis_user.get('total_credit_amount', 0)}")
        
        # Verificar que el filtrado funciona
        if kpis_user.get('credit_count', 0) == 1:
            print("   ✅ Correcto: KPIService filtra correctamente por usuario")
        else:
            print("   ❌ Error: KPIService no filtra correctamente por usuario")
            
    except Exception as e:
        print(f"   ❌ Error probando KPIService: {e}")
    
    finally:
        # Limpiar datos de prueba
        credit.delete()
        user.delete()

def test_credit_filtering():
    """Probar filtrado de créditos por usuario"""
    print("\n🔍 Probando filtrado de créditos por usuario...")
    
    # Crear usuarios de prueba
    user1, _ = User.objects.get_or_create(
        username='user1_jwt',
        defaults={'email': 'user1@example.com'}
    )
    
    user2, _ = User.objects.get_or_create(
        username='user2_jwt',
        defaults={'email': 'user2@example.com'}
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
    
    # Crear créditos para cada usuario
    credit1 = Credit.objects.create(
        user=user1,
        cost=Decimal('800.00'),
        price=Decimal('1000.00'),
        currency=currency,
        periodicity=periodicity,
        subcategory=subcategory,
        payment=payment_account,
        first_date_payment=datetime.now().date(),
        second_date_payment=(datetime.now() + timedelta(days=30)).date(),
        credit_days=30,
        description='Crédito de user1'
    )
    
    credit2 = Credit.objects.create(
        user=user2,
        cost=Decimal('1200.00'),
        price=Decimal('1500.00'),
        currency=currency,
        periodicity=periodicity,
        subcategory=subcategory,
        payment=payment_account,
        first_date_payment=datetime.now().date(),
        second_date_payment=(datetime.now() + timedelta(days=30)).date(),
        credit_days=30,
        description='Crédito de user2'
    )
    
    try:
        # Verificar filtrado
        user1_credits = Credit.objects.filter(user=user1).count()
        user2_credits = Credit.objects.filter(user=user2).count()
        total_credits = Credit.objects.count()
        
        print(f"   📊 Estadísticas:")
        print(f"      - Créditos de {user1.username}: {user1_credits}")
        print(f"      - Créditos de {user2.username}: {user2_credits}")
        print(f"      - Total créditos: {total_credits}")
        
        if user1_credits == 1 and user2_credits == 1 and total_credits == 2:
            print("   ✅ Correcto: Filtrado de créditos funciona correctamente")
        else:
            print("   ❌ Error: Filtrado de créditos no funciona correctamente")
            
    except Exception as e:
        print(f"   ❌ Error probando filtrado: {e}")
    
    finally:
        # Limpiar datos de prueba
        credit1.delete()
        credit2.delete()
        user1.delete()
        user2.delete()

def main():
    """Función principal"""
    print("🚀 Test de JWT Authentication y Filtrado por Usuario")
    print("=" * 50)
    
    try:
        test_jwt_token_generation()
        test_kpi_service_with_user()
        test_credit_filtering()
        
        print("\n" + "=" * 50)
        print("✅ Test completado exitosamente")
        
    except Exception as e:
        print(f"\n❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 