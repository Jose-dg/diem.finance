#!/usr/bin/env python3
"""
Script para debuggear el acceso a la API.
Ejecutar con: python3 manage.py shell < scripts/debug_api_access.py
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.fintech.models import Seller, Credit
from apps.fintech.services.credit_query_service import CreditQueryService
from datetime import datetime, timedelta

User = get_user_model()

def debug_danielojeda_access():
    """Debuggear el acceso de danielojeda"""
    print("🔍 Debuggeando acceso de danielojeda...")
    
    # Obtener el usuario danielojeda
    try:
        daniel_user = User.objects.get(username='danielojeda')
        print(f"✅ Usuario encontrado: {daniel_user.username}")
        print(f"   - is_staff: {daniel_user.is_staff}")
        print(f"   - is_superuser: {daniel_user.is_superuser}")
        print(f"   - has seller_profile: {hasattr(daniel_user, 'seller_profile')}")
        
        # Verificar seller profile
        if hasattr(daniel_user, 'seller_profile'):
            seller = daniel_user.seller_profile
            print(f"   - Seller ID: {seller.id}")
            print(f"   - Seller user: {seller.user.username}")
        else:
            print("   ❌ No tiene seller_profile")
            return
        
        # Verificar créditos directamente en la base de datos
        direct_credits = Credit.objects.filter(seller=seller)
        print(f"\n📊 Créditos directos en BD:")
        print(f"   - Total créditos con seller={seller.id}: {direct_credits.count()}")
        
        for credit in direct_credits:
            print(f"   - {credit.uid}: Cliente {credit.user.username}, Creado: {credit.created_at}")
        
        # Verificar créditos usando el servicio
        service_credits = CreditQueryService.get_user_credits(daniel_user)
        print(f"\n📊 Créditos usando CreditQueryService:")
        print(f"   - Total créditos accesibles: {service_credits.count()}")
        
        for credit in service_credits:
            print(f"   - {credit.uid}: Cliente {credit.user.username}, Creado: {credit.created_at}")
        
        # Verificar filtrado por fecha (como hace la API)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)  # Último año
        
        date_filtered_credits = CreditQueryService.get_user_credits_by_date_range(
            daniel_user, start_date, end_date
        )
        print(f"\n📊 Créditos filtrados por fecha ({start_date} a {end_date}):")
        print(f"   - Total créditos en rango: {date_filtered_credits.count()}")
        
        for credit in date_filtered_credits:
            print(f"   - {credit.uid}: Cliente {credit.user.username}, Creado: {credit.created_at}")
        
        # Verificar si hay diferencias
        if direct_credits.count() != service_credits.count():
            print(f"\n⚠️ DIFERENCIA DETECTADA:")
            print(f"   - Créditos directos: {direct_credits.count()}")
            print(f"   - Créditos del servicio: {service_credits.count()}")
        
        if service_credits.count() != date_filtered_credits.count():
            print(f"\n⚠️ DIFERENCIA POR FECHA:")
            print(f"   - Créditos del servicio: {service_credits.count()}")
            print(f"   - Créditos filtrados por fecha: {date_filtered_credits.count()}")
            
    except User.DoesNotExist:
        print("❌ Usuario danielojeda no encontrado")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def debug_hector_access():
    """Debuggear el acceso de HectorAA para comparar"""
    print("\n🔍 Debuggeando acceso de HectorAA...")
    
    try:
        hector_user = User.objects.get(username='HectorAA')
        print(f"✅ Usuario encontrado: {hector_user.username}")
        
        # Verificar créditos usando el servicio
        service_credits = CreditQueryService.get_user_credits(hector_user)
        print(f"📊 Créditos usando CreditQueryService: {service_credits.count()}")
        
        # Verificar filtrado por fecha
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)
        
        date_filtered_credits = CreditQueryService.get_user_credits_by_date_range(
            hector_user, start_date, end_date
        )
        print(f"📊 Créditos filtrados por fecha: {date_filtered_credits.count()}")
        
    except User.DoesNotExist:
        print("❌ Usuario HectorAA no encontrado")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Iniciando debug de acceso a la API...")
    
    debug_danielojeda_access()
    debug_hector_access()
    
    print("\n✅ Debug completado!") 