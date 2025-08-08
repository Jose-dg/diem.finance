#!/usr/bin/env python3
"""
Script para verificar que el filtrado por usuario funciona correctamente
Ejecutar: python3 manage.py shell < scripts/verify_user_filtering.py
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
from apps.fintech.models import Credit, Currency, Periodicity, SubCategory, Account

User = get_user_model()

def verify_user_filtering():
    """Verificar que el filtrado por usuario funciona correctamente"""
    print("🔍 Verificando filtrado por usuario...")
    
    # Obtener todos los usuarios que tienen créditos
    users_with_credits = User.objects.filter(credits__isnull=False).distinct()
    
    print(f"📊 Usuarios con créditos: {users_with_credits.count()}")
    
    for user in users_with_credits:
        user_credits = Credit.objects.filter(user=user)
        total_credits = user_credits.count()
        pending_credits = user_credits.filter(state='pending').count()
        completed_credits = user_credits.filter(state='completed').count()
        
        print(f"\n👤 Usuario: {user.username} (ID: {user.id})")
        print(f"   - Total créditos: {total_credits}")
        print(f"   - Créditos pendientes: {pending_credits}")
        print(f"   - Créditos completados: {completed_credits}")
        
        # Mostrar algunos créditos de ejemplo
        if total_credits > 0:
            sample_credit = user_credits.first()
            print(f"   - Ejemplo crédito: {sample_credit.uid} - ${sample_credit.price} - {sample_credit.state}")
    
    # Verificar que el filtrado funciona correctamente
    print(f"\n✅ Verificación de filtrado:")
    
    # Contar total de créditos
    total_all_credits = Credit.objects.count()
    print(f"   - Total créditos en sistema: {total_all_credits}")
    
    # Contar créditos por usuario
    total_by_user = sum([Credit.objects.filter(user=user).count() for user in users_with_credits])
    print(f"   - Total créditos por filtrado de usuario: {total_by_user}")
    
    if total_all_credits == total_by_user:
        print("   ✅ Correcto: El filtrado por usuario funciona correctamente")
    else:
        print("   ❌ Error: Hay discrepancia en el filtrado por usuario")
        print(f"      Diferencia: {total_all_credits - total_by_user}")

def test_kpi_service_filtering():
    """Probar el filtrado en KPIService"""
    print(f"\n📈 Probando filtrado en KPIService...")
    
    # Obtener un usuario con créditos
    user_with_credits = User.objects.filter(credits__isnull=False).first()
    
    if not user_with_credits:
        print("   ⚠️ No hay usuarios con créditos para probar")
        return
    
    from apps.fintech.services.kpi_service import KPIService
    
    # Fechas de prueba
    start_date = (datetime.now() - timedelta(days=30)).date()
    end_date = datetime.now().date()
    
    try:
        # Probar sin filtro de usuario
        kpis_all = KPIService.get_credit_kpi_summary(start_date, end_date)
        print(f"   📊 KPIs sin filtro de usuario:")
        print(f"      - Total créditos: {kpis_all.get('credit_count', 0)}")
        print(f"      - Monto total: ${kpis_all.get('total_credit_amount', 0)}")
        
        # Probar con filtro de usuario
        kpis_user = KPIService.get_credit_kpi_summary(start_date, end_date, user=user_with_credits)
        print(f"   📊 KPIs con filtro de usuario ({user_with_credits.username}):")
        print(f"      - Total créditos: {kpis_user.get('credit_count', 0)}")
        print(f"      - Monto total: ${kpis_user.get('total_credit_amount', 0)}")
        
        # Verificar que el filtrado funciona
        user_credits_count = Credit.objects.filter(user=user_with_credits).count()
        kpi_credits_count = kpis_user.get('credit_count', 0)
        
        if kpi_credits_count == user_credits_count:
            print("   ✅ Correcto: KPIService filtra correctamente por usuario")
        else:
            print(f"   ❌ Error: KPIService no filtra correctamente")
            print(f"      Esperado: {user_credits_count}, Obtenido: {kpi_credits_count}")
            
    except Exception as e:
        print(f"   ❌ Error probando KPIService: {e}")

def check_credit_relationships():
    """Verificar las relaciones de créditos"""
    print(f"\n🔗 Verificando relaciones de créditos...")
    
    # Verificar que todos los créditos tienen usuario
    credits_without_user = Credit.objects.filter(user__isnull=True)
    if credits_without_user.exists():
        print(f"   ❌ Error: {credits_without_user.count()} créditos sin usuario")
        for credit in credits_without_user[:5]:  # Mostrar solo los primeros 5
            print(f"      - Crédito {credit.uid} sin usuario")
    else:
        print("   ✅ Correcto: Todos los créditos tienen usuario asignado")
    
    # Verificar que todos los créditos tienen registered_by
    credits_without_registered_by = Credit.objects.filter(registered_by__isnull=True)
    if credits_without_registered_by.exists():
        print(f"   ⚠️ Advertencia: {credits_without_registered_by.count()} créditos sin registered_by")
    else:
        print("   ✅ Correcto: Todos los créditos tienen registered_by")
    
    # Verificar consistencia entre user y registered_by
    inconsistent_credits = Credit.objects.filter(user__isnull=False, registered_by__isnull=False).exclude(user=registered_by)
    if inconsistent_credits.exists():
        print(f"   ⚠️ Advertencia: {inconsistent_credits.count()} créditos donde user != registered_by")
    else:
        print("   ✅ Correcto: user y registered_by son consistentes")

def main():
    """Función principal"""
    print("🚀 Verificación de Filtrado por Usuario")
    print("=" * 50)
    
    try:
        verify_user_filtering()
        test_kpi_service_filtering()
        check_credit_relationships()
        
        print("\n" + "=" * 50)
        print("✅ Verificación completada")
        
    except Exception as e:
        print(f"\n❌ Error durante la verificación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 