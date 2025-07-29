#!/usr/bin/env python3
"""
Script de diagnóstico para identificar problemas con el modelo CreditAdjustment
"""

import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta
from django.db.models import Sum

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.fintech.models import Credit, CreditAdjustment, Adjustment, Transaction, AccountMethodAmount
from apps.fintech.services.credit_adjustment_service import CreditAdjustmentService
from django.db import transaction
from django.utils import timezone

def check_adjustment_data():
    """Verifica la integridad de los datos de ajustes"""
    print("=== VERIFICACIÓN DE DATOS DE AJUSTES ===")
    
    # Verificar si existe el tipo de ajuste requerido
    try:
        adjustment_type = CreditAdjustmentService.get_adjustment_type()
        print(f"✅ Tipo de ajuste encontrado: {adjustment_type.name} ({adjustment_type.code})")
    except ValueError as e:
        print(f"❌ Error con tipo de ajuste: {e}")
        return False
    
    # Verificar créditos con ajustes
    credits_with_adjustments = Credit.objects.filter(adjustments__isnull=False).distinct()
    print(f"📊 Créditos con ajustes: {credits_with_adjustments.count()}")
    
    # Verificar ajustes huérfanos
    orphan_adjustments = CreditAdjustment.objects.filter(credit__isnull=True)
    print(f"⚠️  Ajustes sin crédito asociado: {orphan_adjustments.count()}")
    
    return True

def check_credit_calculations():
    """Verifica los cálculos de créditos"""
    print("\n=== VERIFICACIÓN DE CÁLCULOS DE CRÉDITOS ===")
    
    # Verificar créditos con problemas de cálculo
    problematic_credits = []
    
    for credit in Credit.objects.all()[:10]:  # Solo los primeros 10 para diagnóstico
        try:
            # Verificar cálculos básicos
            expected_earnings = credit.price - credit.cost
            if credit.earnings != expected_earnings:
                problematic_credits.append({
                    'credit_id': credit.id,
                    'issue': f'Earnings incorrecto: {credit.earnings} vs {expected_earnings}'
                })
            
            # Verificar pending_amount
            total_payments = Transaction.objects.filter(
                account_method_amounts__credit=credit,
                transaction_type='income',
                status='confirmed'
            ).aggregate(total=Sum('account_method_amounts__amount_paid'))['total'] or Decimal('0.00')
            
            total_adjustments = credit.adjustments.aggregate(
                total=Sum('amount')
            )['total'] or Decimal('0.00')
            
            expected_pending = (credit.price + total_adjustments) - total_payments
            if abs(credit.pending_amount - expected_pending) > Decimal('0.01'):
                problematic_credits.append({
                    'credit_id': credit.id,
                    'issue': f'Pending amount incorrecto: {credit.pending_amount} vs {expected_pending}'
                })
                
        except Exception as e:
            problematic_credits.append({
                'credit_id': credit.id,
                'issue': f'Error en cálculos: {str(e)}'
            })
    
    if problematic_credits:
        print(f"❌ Créditos con problemas: {len(problematic_credits)}")
        for problem in problematic_credits[:5]:  # Mostrar solo los primeros 5
            print(f"  - Crédito {problem['credit_id']}: {problem['issue']}")
    else:
        print("✅ No se encontraron problemas en los cálculos")
    
    return len(problematic_credits) == 0

def test_credit_adjustment_service():
    """Prueba el servicio CreditAdjustmentService"""
    print("\n=== PRUEBA DEL SERVICIO CREDIT ADJUSTMENT ===")
    
    # Buscar un crédito para probar
    test_credit = Credit.objects.first()
    if not test_credit:
        print("❌ No hay créditos disponibles para probar")
        return False
    
    print(f"🔍 Probando con crédito ID: {test_credit.id}")
    
    try:
        # Probar cálculo de interés adicional
        additional_interest = CreditAdjustmentService.calculate_additional_interest(test_credit)
        print(f"💰 Interés adicional calculado: {additional_interest}")
        
        # Probar si se debe aplicar
        should_apply = CreditAdjustmentService.should_apply_additional_interest(test_credit)
        print(f"📋 Debe aplicar interés: {should_apply}")
        
        # Probar aplicación (solo si no existe ya)
        existing_adjustment = CreditAdjustment.objects.filter(
            credit=test_credit,
            type__code=CreditAdjustmentService.ADDITIONAL_INTEREST_CODE
        ).first()
        
        if not existing_adjustment and should_apply:
            with transaction.atomic():
                amount_applied = CreditAdjustmentService.apply_additional_interest(
                    test_credit,
                    reason="Prueba de diagnóstico"
                )
                print(f"✅ Interés aplicado: {amount_applied}")
        else:
            print(f"ℹ️  Ajuste ya existe o no se debe aplicar")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en servicio: {str(e)}")
        return False

def check_database_locks():
    """Verifica si hay bloqueos de base de datos"""
    print("\n=== VERIFICACIÓN DE BLOQUEOS DE BASE DE DATOS ===")
    
    try:
        # Intentar acceder a los modelos
        credit_count = Credit.objects.count()
        adjustment_count = CreditAdjustment.objects.count()
        transaction_count = Transaction.objects.count()
        
        print(f"📊 Registros en base de datos:")
        print(f"  - Créditos: {credit_count}")
        print(f"  - Ajustes: {adjustment_count}")
        print(f"  - Transacciones: {transaction_count}")
        
        # Verificar consultas lentas
        start_time = timezone.now()
        Credit.objects.select_related('user', 'periodicity').prefetch_related('adjustments').all()
        query_time = (timezone.now() - start_time).total_seconds()
        
        print(f"⏱️  Tiempo de consulta: {query_time:.3f} segundos")
        
        if query_time > 5:
            print("⚠️  Consulta lenta detectada")
            return False
        else:
            print("✅ Consultas funcionando correctamente")
            return True
            
    except Exception as e:
        print(f"❌ Error de base de datos: {str(e)}")
        return False

def main():
    """Función principal de diagnóstico"""
    print("🔍 DIAGNÓSTICO DEL MODELO CREDIT ADJUSTMENT")
    print("=" * 50)
    
    results = []
    
    # Ejecutar verificaciones
    results.append(("Datos de ajustes", check_adjustment_data()))
    results.append(("Cálculos de créditos", check_credit_calculations()))
    results.append(("Servicio CreditAdjustment", test_credit_adjustment_service()))
    results.append(("Bloqueos de BD", check_database_locks()))
    
    # Resumen
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE DIAGNÓSTICO")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{len(results)} pruebas pasaron")
    
    if passed == len(results):
        print("🎉 El modelo CreditAdjustment está funcionando correctamente")
    else:
        print("⚠️  Se encontraron problemas que requieren atención")
        
        # Recomendaciones
        print("\n💡 RECOMENDACIONES:")
        if not results[0][1]:  # Datos de ajustes
            print("- Verificar que existe el Adjustment con código C0001")
        if not results[1][1]:  # Cálculos
            print("- Ejecutar recálculo de créditos problemáticos")
        if not results[2][1]:  # Servicio
            print("- Revisar logs de errores del servicio")
        if not results[3][1]:  # BD
            print("- Verificar conexión y rendimiento de base de datos")

if __name__ == "__main__":
    main() 