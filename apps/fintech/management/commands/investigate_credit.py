from django.core.management.base import BaseCommand
from decimal import Decimal
from apps.fintech.models import Credit, Transaction, AccountMethodAmount, CreditAdjustment
from apps.fintech.utils.root import recalculate_credit

class Command(BaseCommand):
    help = 'Investiga el saldo de un crédito específico'

    def add_arguments(self, parser):
        parser.add_argument('credit_uid', type=str, help='UID del crédito a investigar')

    def handle(self, *args, **options):
        credit_uid = options['credit_uid']
        
        self.stdout.write(f"🔍 Investigando crédito: {credit_uid}")
        self.stdout.write("=" * 60)
        
        try:
            # Buscar el crédito
            credit = Credit.objects.get(uid=credit_uid)
            self.stdout.write(f"✅ Crédito encontrado")
            self.stdout.write(f"   Usuario: {credit.user}")
            self.stdout.write(f"   Estado: {credit.state}")
            self.stdout.write(f"   Precio: ${credit.price:,.2f}")
            self.stdout.write(f"   Costo: ${credit.cost:,.2f}")
            self.stdout.write(f"   Total abonos: ${credit.total_abonos:,.2f}")
            self.stdout.write(f"   Saldo pendiente: ${credit.pending_amount:,.2f}")
            self.stdout.write(f"   Interés: {credit.interest}%")
            self.stdout.write(f"   Días de crédito: {credit.credit_days}")
            self.stdout.write(f"   Periodicidad: {credit.periodicity}")
            self.stdout.write(f"   Fecha primer pago: {credit.first_date_payment}")
            self.stdout.write(f"   Fecha segundo pago: {credit.second_date_payment}")
            self.stdout.write(f"   En mora: {credit.is_in_default}")
            self.stdout.write(f"   Nivel morosidad: {credit.morosidad_level}")
            self.stdout.write("")
            
            # Verificar transacciones confirmadas
            confirmed_transactions = Transaction.objects.filter(
                account_method_amounts__credit=credit,
                transaction_type='income',
                status='confirmed'
            ).select_related('user').prefetch_related('account_method_amounts')
            
            self.stdout.write(f"📊 Transacciones confirmadas: {confirmed_transactions.count()}")
            total_from_transactions = Decimal('0.00')
            
            for tx in confirmed_transactions:
                for ama in tx.account_method_amounts.all():
                    if ama.credit == credit:
                        total_from_transactions += ama.amount_paid
                        self.stdout.write(f"   - {tx.date.strftime('%Y-%m-%d %H:%M')}: ${ama.amount_paid:,.2f} ({tx.description})")
            
            self.stdout.write(f"   Total de transacciones: ${total_from_transactions:,.2f}")
            self.stdout.write("")
            
            # Verificar ajustes
            adjustments = CreditAdjustment.objects.filter(credit=credit)
            self.stdout.write(f"🔧 Ajustes: {adjustments.count()}")
            total_adjustments = Decimal('0.00')
            
            for adj in adjustments:
                total_adjustments += adj.amount
                self.stdout.write(f"   - {adj.added_on}: ${adj.amount:,.2f} ({adj.reason or 'Sin razón'})")
            
            self.stdout.write(f"   Total ajustes: ${total_adjustments:,.2f}")
            self.stdout.write("")
            
            # Calcular saldo esperado
            expected_pending = credit.price + total_adjustments - total_from_transactions
            self.stdout.write(f"🧮 Cálculo manual del saldo:")
            self.stdout.write(f"   Precio: ${credit.price:,.2f}")
            self.stdout.write(f"   + Ajustes: ${total_adjustments:,.2f}")
            self.stdout.write(f"   - Pagos: ${total_from_transactions:,.2f}")
            self.stdout.write(f"   = Saldo esperado: ${expected_pending:,.2f}")
            self.stdout.write(f"   Saldo actual en BD: ${credit.pending_amount:,.2f}")
            
            difference = abs(expected_pending - credit.pending_amount)
            if difference > Decimal('0.01'):
                self.stdout.write(f"   ⚠️  DIFERENCIA DETECTADA: ${difference:,.2f}")
            else:
                self.stdout.write(f"   ✅ Saldo correcto")
            self.stdout.write("")
            
            # Verificar cuotas
            installments = credit.installments.all()
            self.stdout.write(f"📅 Cuotas: {installments.count()}")
            for inst in installments:
                status = "✅ Pagada" if inst.paid else "⏳ Pendiente"
                self.stdout.write(f"   Cuota {inst.number}: ${inst.amount:,.2f} - {status}")
            self.stdout.write("")
            
            # Recalcular el crédito
            self.stdout.write("🔄 Recalculando crédito...")
            recalculate_credit(credit)
            credit.refresh_from_db()
            
            self.stdout.write(f"📊 Después del recálculo:")
            self.stdout.write(f"   Total abonos: ${credit.total_abonos:,.2f}")
            self.stdout.write(f"   Saldo pendiente: ${credit.pending_amount:,.2f}")
            self.stdout.write(f"   En mora: {credit.is_in_default}")
            self.stdout.write(f"   Nivel morosidad: {credit.morosidad_level}")
            
            # Verificar si el recálculo corrigió el problema
            new_expected_pending = credit.price + total_adjustments - credit.total_abonos
            new_difference = abs(new_expected_pending - credit.pending_amount)
            
            if new_difference > Decimal('0.01'):
                self.stdout.write(f"   ⚠️  PROBLEMA PERSISTE: ${new_difference:,.2f}")
            else:
                self.stdout.write(f"   ✅ Problema corregido")
                
        except Credit.DoesNotExist:
            self.stdout.write(f"❌ Crédito no encontrado: {credit_uid}")
        except Exception as e:
            self.stdout.write(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc() 