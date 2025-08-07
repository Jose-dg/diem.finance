#!/usr/bin/env python
import os
import sys
import django
from decimal import Decimal
from django.db import transaction
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.fintech.models import Credit, Transaction, AccountMethodAmount, CreditAdjustment
from apps.fintech.utils.root import recalculate_credit

def investigate_credit_balance(credit_uid):
    """
    Investiga el saldo de un crédito específico y muestra información detallada
    """
    print(f"🔍 Investigando crédito: {credit_uid}")
    print("=" * 60)
    
    try:
        # Buscar el crédito
        credit = Credit.objects.get(uid=credit_uid)
        print(f"✅ Crédito encontrado")
        print(f"   Usuario: {credit.user}")
        print(f"   Estado: {credit.state}")
        print(f"   Precio: ${credit.price:,.2f}")
        print(f"   Costo: ${credit.cost:,.2f}")
        print(f"   Total abonos: ${credit.total_abonos:,.2f}")
        print(f"   Saldo pendiente: ${credit.pending_amount:,.2f}")
        print(f"   Interés: {credit.interest}%")
        print(f"   Días de crédito: {credit.credit_days}")
        print(f"   Periodicidad: {credit.periodicity}")
        print(f"   Fecha primer pago: {credit.first_date_payment}")
        print(f"   Fecha segundo pago: {credit.second_date_payment}")
        print(f"   En mora: {credit.is_in_default}")
        print(f"   Nivel morosidad: {credit.morosidad_level}")
        print()
        
        # Verificar transacciones confirmadas
        confirmed_transactions = Transaction.objects.filter(
            account_method_amounts__credit=credit,
            transaction_type='income',
            status='confirmed'
        ).select_related('user').prefetch_related('account_method_amounts')
        
        print(f"📊 Transacciones confirmadas: {confirmed_transactions.count()}")
        total_from_transactions = Decimal('0.00')
        
        for tx in confirmed_transactions:
            for ama in tx.account_method_amounts.all():
                if ama.credit == credit:
                    total_from_transactions += ama.amount_paid
                    print(f"   - {tx.date.strftime('%Y-%m-%d %H:%M')}: ${ama.amount_paid:,.2f} ({tx.description})")
        
        print(f"   Total de transacciones: ${total_from_transactions:,.2f}")
        print()
        
        # Verificar ajustes
        adjustments = CreditAdjustment.objects.filter(credit=credit)
        print(f"🔧 Ajustes: {adjustments.count()}")
        total_adjustments = Decimal('0.00')
        
        for adj in adjustments:
            total_adjustments += adj.amount
            print(f"   - {adj.added_on}: ${adj.amount:,.2f} ({adj.reason or 'Sin razón'})")
        
        print(f"   Total ajustes: ${total_adjustments:,.2f}")
        print()
        
        # Calcular saldo esperado
        expected_pending = credit.price + total_adjustments - total_from_transactions
        print(f"🧮 Cálculo manual del saldo:")
        print(f"   Precio: ${credit.price:,.2f}")
        print(f"   + Ajustes: ${total_adjustments:,.2f}")
        print(f"   - Pagos: ${total_from_transactions:,.2f}")
        print(f"   = Saldo esperado: ${expected_pending:,.2f}")
        print(f"   Saldo actual en BD: ${credit.pending_amount:,.2f}")
        
        difference = abs(expected_pending - credit.pending_amount)
        if difference > Decimal('0.01'):
            print(f"   ⚠️  DIFERENCIA DETECTADA: ${difference:,.2f}")
        else:
            print(f"   ✅ Saldo correcto")
        print()
        
        # Verificar cuotas
        installments = credit.installments.all()
        print(f"📅 Cuotas: {installments.count()}")
        for inst in installments:
            status = "✅ Pagada" if inst.paid else "⏳ Pendiente"
            print(f"   Cuota {inst.number}: ${inst.amount:,.2f} - {status}")
        print()
        
        # Recalcular el crédito
        print("🔄 Recalculando crédito...")
        recalculate_credit(credit)
        credit.refresh_from_db()
        
        print(f"📊 Después del recálculo:")
        print(f"   Total abonos: ${credit.total_abonos:,.2f}")
        print(f"   Saldo pendiente: ${credit.pending_amount:,.2f}")
        print(f"   En mora: {credit.is_in_default}")
        print(f"   Nivel morosidad: {credit.morosidad_level}")
        
        # Verificar si el recálculo corrigió el problema
        new_expected_pending = credit.price + total_adjustments - credit.total_abonos
        new_difference = abs(new_expected_pending - credit.pending_amount)
        
        if new_difference > Decimal('0.01'):
            print(f"   ⚠️  PROBLEMA PERSISTE: ${new_difference:,.2f}")
        else:
            print(f"   ✅ Problema corregido")
            
    except Credit.DoesNotExist:
        print(f"❌ Crédito no encontrado: {credit_uid}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    credit_uid = "4b78cc0f-ca11-49a3-98ad-39536fd5eb20"
    investigate_credit_balance(credit_uid) 