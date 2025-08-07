from django.core.management.base import BaseCommand
from decimal import Decimal
from apps.fintech.models import Credit, Transaction, AccountMethodAmount, CreditAdjustment

class Command(BaseCommand):
    help = 'Consulta simple del saldo de un crédito'

    def add_arguments(self, parser):
        parser.add_argument('credit_uid', type=str, help='UID del crédito a consultar')

    def handle(self, *args, **options):
        credit_uid = options['credit_uid']
        
        self.stdout.write(f"🔍 Consultando crédito: {credit_uid}")
        self.stdout.write("=" * 50)
        
        try:
            # Buscar el crédito
            credit = Credit.objects.get(uid=credit_uid)
            
            self.stdout.write(f"✅ CRÉDITO ENCONTRADO")
            self.stdout.write(f"   Usuario: {credit.user}")
            self.stdout.write(f"   Estado: {credit.state}")
            self.stdout.write(f"   Precio original: ${credit.price:,.2f}")
            self.stdout.write(f"   Costo: ${credit.cost:,.2f}")
            self.stdout.write(f"   Total abonos registrados: ${credit.total_abonos:,.2f}")
            self.stdout.write(f"   Saldo pendiente actual: ${credit.pending_amount:,.2f}")
            self.stdout.write(f"   Interés: {credit.interest}%")
            self.stdout.write(f"   Días de crédito: {credit.credit_days}")
            self.stdout.write(f"   En mora: {credit.is_in_default}")
            self.stdout.write(f"   Nivel morosidad: {credit.morosidad_level}")
            self.stdout.write("")
            
            # Verificar transacciones confirmadas
            confirmed_transactions = Transaction.objects.filter(
                account_method_amounts__credit=credit,
                transaction_type='income',
                status='confirmed'
            )
            
            self.stdout.write(f"📊 TRANSACCIONES CONFIRMADAS: {confirmed_transactions.count()}")
            total_from_transactions = Decimal('0.00')
            
            for tx in confirmed_transactions:
                for ama in tx.account_method_amounts.all():
                    if ama.credit == credit:
                        total_from_transactions += ama.amount_paid
                        self.stdout.write(f"   - {tx.date.strftime('%Y-%m-%d')}: ${ama.amount_paid:,.2f}")
            
            self.stdout.write(f"   Total de transacciones: ${total_from_transactions:,.2f}")
            self.stdout.write("")
            
            # Verificar ajustes
            adjustments = CreditAdjustment.objects.filter(credit=credit)
            self.stdout.write(f"🔧 AJUSTES: {adjustments.count()}")
            total_adjustments = Decimal('0.00')
            
            for adj in adjustments:
                total_adjustments += adj.amount
                self.stdout.write(f"   - {adj.added_on}: ${adj.amount:,.2f}")
            
            self.stdout.write(f"   Total ajustes: ${total_adjustments:,.2f}")
            self.stdout.write("")
            
            # Cálculo manual del saldo esperado
            expected_pending = credit.price + total_adjustments - total_from_transactions
            self.stdout.write(f"🧮 CÁLCULO MANUAL:")
            self.stdout.write(f"   Precio: ${credit.price:,.2f}")
            self.stdout.write(f"   + Ajustes: ${total_adjustments:,.2f}")
            self.stdout.write(f"   - Pagos reales: ${total_from_transactions:,.2f}")
            self.stdout.write(f"   = Saldo esperado: ${expected_pending:,.2f}")
            self.stdout.write(f"   Saldo en BD: ${credit.pending_amount:,.2f}")
            
            # Verificar diferencia
            difference = abs(expected_pending - credit.pending_amount)
            if difference > Decimal('0.01'):
                self.stdout.write(f"   ⚠️  PROBLEMA: Diferencia de ${difference:,.2f}")
                self.stdout.write(f"   El saldo en la BD no coincide con los cálculos")
            else:
                self.stdout.write(f"   ✅ Saldo correcto")
            
            self.stdout.write("")
            self.stdout.write(f"📋 RESUMEN:")
            self.stdout.write(f"   - Total abonos en BD: ${credit.total_abonos:,.2f}")
            self.stdout.write(f"   - Total pagos reales: ${total_from_transactions:,.2f}")
            self.stdout.write(f"   - Diferencia en abonos: ${abs(credit.total_abonos - total_from_transactions):,.2f}")
            
            if credit.total_abonos != total_from_transactions:
                self.stdout.write(f"   ⚠️  Los abonos registrados no coinciden con las transacciones reales")
            
        except Credit.DoesNotExist:
            self.stdout.write(f"❌ Crédito no encontrado: {credit_uid}")
        except Exception as e:
            self.stdout.write(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc() 