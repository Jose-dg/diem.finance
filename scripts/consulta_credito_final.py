#!/usr/bin/env python3
import os
import sys
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.fintech.models import Credit, Transaction, AccountMethodAmount, CreditAdjustment
from apps.fintech.utils.root import recalculate_credit

def consulta_credito_final(credit_uid):
    """
    Consulta final del crédito con recálculo automático
    """
    print(f"🔍 CONSULTA FINAL DEL CRÉDITO: {credit_uid}")
    print("=" * 60)
    
    try:
        # Buscar el crédito
        credit = Credit.objects.get(uid=credit_uid)
        
        print(f"✅ CRÉDITO ENCONTRADO")
        print(f"   Usuario: {credit.user}")
        print(f"   Estado: {credit.state}")
        print(f"   Precio original: ${credit.price:,.2f}")
        print(f"   Costo: ${credit.cost:,.2f}")
        print(f"   Total abonos registrados: ${credit.total_abonos:,.2f}")
        print(f"   Saldo pendiente actual: ${credit.pending_amount:,.2f}")
        print(f"   Interés: {credit.interest}%")
        print(f"   Días de crédito: {credit.credit_days}")
        print(f"   En mora: {credit.is_in_default}")
        print(f"   Nivel morosidad: {credit.morosidad_level}")
        print()
        
        # Verificar transacciones confirmadas
        confirmed_transactions = Transaction.objects.filter(
            account_method_amounts__credit=credit,
            transaction_type='income',
            status='confirmed'
        )
        
        print(f"📊 TRANSACCIONES CONFIRMADAS: {confirmed_transactions.count()}")
        total_from_transactions = Decimal('0.00')
        
        for tx in confirmed_transactions:
            for ama in tx.account_method_amounts.all():
                if ama.credit == credit:
                    total_from_transactions += ama.amount_paid
                    print(f"   - {tx.date.strftime('%Y-%m-%d')}: ${ama.amount_paid:,.2f}")
        
        print(f"   Total de transacciones: ${total_from_transactions:,.2f}")
        print()
        
        # Verificar ajustes
        adjustments = CreditAdjustment.objects.filter(credit=credit)
        print(f"🔧 AJUSTES: {adjustments.count()}")
        total_adjustments = Decimal('0.00')
        
        for adj in adjustments:
            total_adjustments += adj.amount
            print(f"   - {adj.added_on}: ${adj.amount:,.2f}")
        
        print(f"   Total ajustes: ${total_adjustments:,.2f}")
        print()
        
        # Cálculo manual del saldo esperado
        expected_pending = credit.price + total_adjustments - total_from_transactions
        print(f"🧮 CÁLCULO MANUAL:")
        print(f"   Precio: ${credit.price:,.2f}")
        print(f"   + Ajustes: ${total_adjustments:,.2f}")
        print(f"   - Pagos reales: ${total_from_transactions:,.2f}")
        print(f"   = Saldo esperado: ${expected_pending:,.2f}")
        print(f"   Saldo en BD: ${credit.pending_amount:,.2f}")
        
        # Verificar diferencia
        difference = abs(expected_pending - credit.pending_amount)
        if difference > Decimal('0.01'):
            print(f"   ⚠️  PROBLEMA DETECTADO: Diferencia de ${difference:,.2f}")
            print(f"   El saldo en la BD no coincide con los cálculos")
            
            # Intentar recálculo automático
            print(f"\n🔄 INTENTANDO RECÁLCULO AUTOMÁTICO...")
            try:
                recalculate_credit(credit)
                credit.refresh_from_db()
                
                print(f"📊 DESPUÉS DEL RECÁLCULO:")
                print(f"   Total abonos: ${credit.total_abonos:,.2f}")
                print(f"   Saldo pendiente: ${credit.pending_amount:,.2f}")
                print(f"   En mora: {credit.is_in_default}")
                print(f"   Nivel morosidad: {credit.morosidad_level}")
                
                # Verificar si el recálculo corrigió el problema
                new_expected_pending = credit.price + total_adjustments - credit.total_abonos
                new_difference = abs(new_expected_pending - credit.pending_amount)
                
                if new_difference > Decimal('0.01'):
                    print(f"   ⚠️  PROBLEMA PERSISTE: ${new_difference:,.2f}")
                    print(f"   Se requiere intervención manual")
                else:
                    print(f"   ✅ PROBLEMA CORREGIDO")
                    
            except Exception as e:
                print(f"   ❌ Error en recálculo: {str(e)}")
        else:
            print(f"   ✅ Saldo correcto")
        
        print()
        print(f"📋 RESUMEN FINAL:")
        print(f"   - Total abonos en BD: ${credit.total_abonos:,.2f}")
        print(f"   - Total pagos reales: ${total_from_transactions:,.2f}")
        print(f"   - Diferencia en abonos: ${abs(credit.total_abonos - total_from_transactions):,.2f}")
        
        if credit.total_abonos != total_from_transactions:
            print(f"   ⚠️  Los abonos registrados no coinciden con las transacciones reales")
            print(f"   CAUSA PROBABLE: total_abonos no se actualizó correctamente")
        
        print()
        print(f"🎯 RECOMENDACIONES:")
        if difference > Decimal('0.01'):
            print(f"   1. Ejecutar recalculate_credit() manualmente")
            print(f"   2. Verificar que no haya transacciones duplicadas")
            print(f"   3. Revisar logs de actualización de abonos")
        else:
            print(f"   ✅ El saldo del crédito está correcto")
            
    except Credit.DoesNotExist:
        print(f"❌ Crédito no encontrado: {credit_uid}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    credit_uid = "4b78cc0f-ca11-49a3-98ad-39536fd5eb20"
    consulta_credito_final(credit_uid) 