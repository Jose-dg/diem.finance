#!/usr/bin/env python3
"""
Script para probar la conexión a Redis y verificar la configuración de Celery
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings
import redis
from celery import current_app

def test_redis_connection():
    """Probar conexión a Redis"""
    
    print("🔍 TESTING REDIS CONNECTION")
    print("=" * 50)
    
    # 1. Verificar variables de entorno
    print("\n1️⃣ Verificando variables de entorno...")
    redis_url = os.environ.get('REDIS_URL')
    render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    
    print(f"   - REDIS_URL: {'✅ Configurada' if redis_url else '❌ No configurada'}")
    print(f"   - RENDER_EXTERNAL_HOSTNAME: {'✅ Configurada' if render_hostname else '❌ No configurada'}")
    
    if redis_url:
        print(f"   - URL de Redis: {redis_url}")
    
    # 2. Verificar configuración de Celery
    print("\n2️⃣ Verificando configuración de Celery...")
    print(f"   - CELERY_BROKER_URL: {settings.CELERY_BROKER_URL}")
    print(f"   - CELERY_RESULT_BACKEND: {settings.CELERY_RESULT_BACKEND}")
    print(f"   - CELERY_TASK_ALWAYS_EAGER: {settings.CELERY_TASK_ALWAYS_EAGER}")
    
    # 3. Probar conexión directa a Redis
    print("\n3️⃣ Probando conexión directa a Redis...")
    try:
        if redis_url:
            r = redis.from_url(redis_url)
            r.ping()
            print("✅ Conexión a Redis exitosa")
            
            # Probar operaciones básicas
            r.set('test_key', 'test_value')
            value = r.get('test_key')
            r.delete('test_key')
            print("✅ Operaciones básicas de Redis funcionan")
        else:
            print("⚠️ No hay REDIS_URL configurada")
    except Exception as e:
        print(f"❌ Error conectando a Redis: {e}")
    
    # 4. Probar configuración de Celery
    print("\n4️⃣ Probando configuración de Celery...")
    try:
        # Verificar que Celery puede conectarse
        app = current_app
        print(f"✅ Aplicación Celery: {app}")
        
        # Verificar brokers disponibles
        brokers = app.conf.broker_url
        print(f"✅ Broker URL: {brokers}")
        
    except Exception as e:
        print(f"❌ Error en configuración de Celery: {e}")
    
    # 5. Verificar si estamos en producción
    print("\n5️⃣ Verificando entorno...")
    if render_hostname:
        print(f"✅ Entorno de producción detectado: {render_hostname}")
        print("   - Usando REDIS_URL para conexión")
    else:
        print("✅ Entorno de desarrollo detectado")
        print("   - Usando localhost:6379 para conexión")
    
    print("\n🎉 Test de conexión completado")

def test_credit_creation_with_redis():
    """Probar creación de crédito con Redis disponible"""
    
    print("\n🧪 TESTING CREDIT CREATION WITH REDIS")
    print("=" * 50)
    
    try:
        from apps.fintech.models import (
            Credit, User, CategoryType, Category, SubCategory, 
            Currency, Periodicity, Account
        )
        from decimal import Decimal
        
        # Obtener datos necesarios
        user = User.objects.filter(is_superuser=False).first()
        if not user:
            user = User.objects.first()
        
        # Buscar una categoría que tenga subcategorías
        category = None
        for cat in Category.objects.all():
            if cat.subcategories.exists():
                category = cat
                break
        
        if not category:
            print("❌ No hay categorías con subcategorías")
            return
        
        subcategory = category.subcategories.first()
        currency = Currency.objects.first()
        periodicity = Periodicity.objects.first()
        account = Account.objects.first()
        
        if not all([subcategory, currency, periodicity, account]):
            print("❌ Faltan datos necesarios")
            return
        
        print(f"✅ Datos disponibles:")
        print(f"   - Usuario: {user.username}")
        print(f"   - Subcategoría: {subcategory.name}")
        print(f"   - Moneda: {currency.currency}")
        print(f"   - Periodicidad: {periodicity.name}")
        print(f"   - Cuenta: {account.name}")
        
        # Crear crédito
        print("\n📝 Creando crédito...")
        credit = Credit(
            user=user,
            subcategory=subcategory,
            currency=currency,
            periodicity=periodicity,
            payment=account,
            price=Decimal('1000.00'),
            cost=Decimal('800.00'),
            credit_days=30,
            first_date_payment='2025-01-27',
            second_date_payment='2025-02-26'
        )
        
        credit.save()
        print(f"✅ Crédito creado exitosamente: ID {credit.id}")
        print(f"   - Precio: ${credit.price}")
        print(f"   - Costo: ${credit.cost}")
        print(f"   - Earnings: ${credit.earnings}")
        print(f"   - Pendiente: ${credit.pending_amount}")
        
        # Verificar si se creó CreditEarnings
        from apps.revenue.models import CreditEarnings
        earnings = CreditEarnings.objects.filter(credit=credit)
        print(f"\n💰 CreditEarnings creados: {earnings.count()}")
        for earning in earnings:
            print(f"   - ID: {earning.id}, Teórica: ${earning.theoretical_earnings}")
        
        # Limpiar datos de prueba
        print("\n🧹 Limpiando datos de prueba...")
        credit.delete()
        print("✅ Datos limpiados")
        
        print("\n🎉 Test de creación de crédito completado exitosamente")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_redis_connection()
    test_credit_creation_with_redis()
