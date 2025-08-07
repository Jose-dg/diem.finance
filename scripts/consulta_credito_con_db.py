#!/usr/bin/env python3
import os
import sys
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Temporalmente cambiar la configuración de la base de datos
from django.conf import settings
from django.db import connections

# Intentar conectar a la base de datos actual
try:
    # Probar conexión a la base de datos actual
    from django.db import connection
    connection.ensure_connection()
    print("✅ Conexión exitosa a la base de datos actual")
    
    from apps.fintech.models import Credit, Transaction, AccountMethodAmount, CreditAdjustment
    
    def consulta_credito_con_db(credit_uid):
        """
        Consulta el crédito usando la base de datos actual
        """
        print(f"🔍 Consultando crédito: {credit_uid}")
        print("=" * 50)
        
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
                print(f"   ⚠️  PROBLEMA: Diferencia de ${difference:,.2f}")
                print(f"   El saldo en la BD no coincide con los cálculos")
            else:
                print(f"   ✅ Saldo correcto")
            
            print()
            print(f"📋 RESUMEN:")
            print(f"   - Total abonos en BD: ${credit.total_abonos:,.2f}")
            print(f"   - Total pagos reales: ${total_from_transactions:,.2f}")
            print(f"   - Diferencia en abonos: ${abs(credit.total_abonos - total_from_transactions):,.2f}")
            
            if credit.total_abonos != total_from_transactions:
                print(f"   ⚠️  Los abonos registrados no coinciden con las transacciones reales")
            
        except Credit.DoesNotExist:
            print(f"❌ Crédito no encontrado: {credit_uid}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # Ejecutar la consulta
    credit_uid = "4b78cc0f-ca11-49a3-98ad-39536fd5eb20"
    consulta_credito_con_db(credit_uid)
    
except Exception as e:
    print(f"❌ No se pudo conectar a la base de datos: {str(e)}")
    print("💡 SUGERENCIAS:")
    print("   1. Verificar que DATABASE_URL esté configurada")
    print("   2. Verificar conectividad a la base de datos")
    print("   3. Usar una base de datos local para pruebas") 