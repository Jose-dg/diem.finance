#!/usr/bin/env python3
"""
Script para revisar el estado de los créditos y sus relaciones
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.fintech.models import Credit, User, Currency, Periodicity, SubCategory, Account

def check_credits_status():
    """Revisar el estado general de los créditos"""
    print("🔍 Revisando estado de créditos...")
    
    # Contar créditos totales
    total_credits = Credit.objects.count()
    print(f"📊 Total de créditos: {total_credits}")
    
    if total_credits == 0:
        print("   ⚠️  No hay créditos en la base de datos")
        return
    
    # Revisar créditos por estado
    states = Credit.objects.values_list('state', flat=True).distinct()
    print(f"📋 Estados de créditos: {list(states)}")
    
    for state in states:
        count = Credit.objects.filter(state=state).count()
        print(f"   - {state}: {count} créditos")
    
    # Revisar créditos por usuario
    users_with_credits = Credit.objects.values_list('user__username', flat=True).distinct()
    print(f"👥 Usuarios con créditos: {list(users_with_credits)}")
    
    for username in users_with_credits:
        count = Credit.objects.filter(user__username=username).count()
        print(f"   - {username}: {count} créditos")
    
    # Revisar créditos en mora
    defaulted_credits = Credit.objects.filter(is_in_default=True).count()
    print(f"🚨 Créditos en mora: {defaulted_credits}")
    
    # Revisar campos importantes
    print("\n🔧 Revisando campos importantes...")
    
    # Créditos sin usuario
    credits_without_user = Credit.objects.filter(user__isnull=True).count()
    print(f"   - Créditos sin usuario: {credits_without_user}")
    
    # Créditos sin precio
    credits_without_price = Credit.objects.filter(price__isnull=True).count()
    print(f"   - Créditos sin precio: {credits_without_price}")
    
    # Créditos con precio 0
    credits_zero_price = Credit.objects.filter(price=0).count()
    print(f"   - Créditos con precio 0: {credits_zero_price}")
    
    # Revisar relaciones
    print("\n🔗 Revisando relaciones...")
    
    # Créditos sin moneda
    credits_without_currency = Credit.objects.filter(currency__isnull=True).count()
    print(f"   - Créditos sin moneda: {credits_without_currency}")
    
    # Créditos sin periodicidad
    credits_without_periodicity = Credit.objects.filter(periodicity__isnull=True).count()
    print(f"   - Créditos sin periodicidad: {credits_without_periodicity}")
    
    # Créditos sin subcategoría
    credits_without_subcategory = Credit.objects.filter(subcategory__isnull=True).count()
    print(f"   - Créditos sin subcategoría: {credits_without_subcategory}")

def check_specific_credit(credit_id=None):
    """Revisar un crédito específico"""
    if credit_id:
        try:
            credit = Credit.objects.get(uid=credit_id)
            print(f"\n🔍 Revisando crédito específico: {credit_id}")
        except Credit.DoesNotExist:
            print(f"❌ Crédito {credit_id} no encontrado")
            return
    else:
        # Tomar el primer crédito disponible
        credit = Credit.objects.first()
        if not credit:
            print("❌ No hay créditos disponibles")
            return
        print(f"\n🔍 Revisando primer crédito disponible: {credit.uid}")
    
    print(f"   📋 Información del crédito:")
    print(f"      - UID: {credit.uid}")
    print(f"      - Usuario: {credit.user.username if credit.user else 'Sin usuario'}")
    print(f"      - Estado: {credit.state}")
    print(f"      - Precio: ${credit.price}")
    print(f"      - Costo: ${credit.cost}")
    print(f"      - Pendiente: ${credit.pending_amount}")
    print(f"      - Total abonos: ${credit.total_abonos}")
    print(f"      - En mora: {credit.is_in_default}")
    print(f"      - Nivel morosidad: {credit.morosidad_level}")
    print(f"      - Días crédito: {credit.credit_days}")
    print(f"      - Fecha creación: {credit.created_at}")
    print(f"      - Fecha actualización: {credit.updated_at}")
    
    # Revisar relaciones
    print(f"   🔗 Relaciones:")
    print(f"      - Moneda: {credit.currency.currency if credit.currency else 'Sin moneda'}")
    print(f"      - Periodicidad: {credit.periodicity.name if credit.periodicity else 'Sin periodicidad'}")
    print(f"      - Subcategoría: {credit.subcategory.name if credit.subcategory else 'Sin subcategoría'}")
    print(f"      - Cuenta pago: {credit.payment.name if credit.payment else 'Sin cuenta'}")
    
    # Revisar cuotas
    installments_count = credit.installments.count()
    print(f"      - Cuotas: {installments_count}")
    
    # Revisar pagos
    payments_count = credit.payments.count()
    print(f"      - Pagos: {payments_count}")

def check_user_credits(username=None):
    """Revisar créditos de un usuario específico"""
    if username:
        try:
            user = User.objects.get(username=username)
            print(f"\n👤 Revisando créditos de usuario: {username}")
        except User.DoesNotExist:
            print(f"❌ Usuario {username} no encontrado")
            return
    else:
        # Tomar el primer usuario con créditos
        user = User.objects.filter(credits__isnull=False).first()
        if not user:
            print("❌ No hay usuarios con créditos")
            return
        print(f"\n👤 Revisando créditos de primer usuario: {user.username}")
    
    credits = Credit.objects.filter(user=user)
    total_credits = credits.count()
    
    print(f"   📊 Estadísticas del usuario:")
    print(f"      - Total créditos: {total_credits}")
    
    if total_credits > 0:
        total_amount = credits.aggregate(total=sum('price'))['total'] or 0
        total_pending = credits.aggregate(total=sum('pending_amount'))['total'] or 0
        total_paid = credits.aggregate(total=sum('total_abonos'))['total'] or 0
        
        print(f"      - Monto total: ${total_amount}")
        print(f"      - Pendiente total: ${total_pending}")
        print(f"      - Pagado total: ${total_paid}")
        
        # Estados
        for state in ['pending', 'completed', 'checking', 'to_solve', 'preorder']:
            count = credits.filter(state=state).count()
            if count > 0:
                print(f"      - {state}: {count} créditos")
        
        # Créditos en mora
        defaulted = credits.filter(is_in_default=True).count()
        print(f"      - En mora: {defaulted} créditos")

def main():
    """Función principal"""
    print("🚀 Revisión de Estado de Créditos")
    print("=" * 40)
    
    try:
        check_credits_status()
        
        # Revisar un crédito específico si se proporciona
        import sys
        if len(sys.argv) > 1:
            credit_id = sys.argv[1]
            check_specific_credit(credit_id)
        else:
            check_specific_credit()
        
        # Revisar créditos de usuario si se proporciona
        if len(sys.argv) > 2:
            username = sys.argv[2]
            check_user_credits(username)
        else:
            check_user_credits()
        
        print("\n" + "=" * 40)
        print("✅ Revisión completada")
        
    except Exception as e:
        print(f"\n❌ Error durante la revisión: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 