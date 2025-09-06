from django.core.management.base import BaseCommand
from django.db.models import Sum, Count
from decimal import Decimal
from apps.fintech.models import Credit, Transaction, AccountMethodAmount, CreditAdjustment, User
from apps.fintech.utils.root import recalculate_credit
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Diagnostica casos específicos de saldos incorrectos reportados por usuarios'

    def add_arguments(self, parser):
        parser.add_argument(
            '--usuario',
            type=str,
            help='Nombre de usuario específico a diagnosticar'
        )
        parser.add_argument(
            '--todos',
            action='store_true',
            help='Diagnosticar todos los casos reportados'
        )

    def handle(self, *args, **options):
        usuario = options.get('usuario')
        todos = options.get('todos')
        
        self.stdout.write("🔍 DIAGNÓSTICO DE CASOS ESPECÍFICOS")
        self.stdout.write("=" * 60)
        
        # Casos reportados
        casos_reportados = [
            {
                'nombre': 'Andres Magallon',
                'problema': 'Crédito cancelado en totalidad pero aparece saldo de 65',
                'buscar': ['Andres', 'Magallon']
            },
            {
                'nombre': 'Elidia Mendoza', 
                'problema': '22 pagos de 10 pero valor verde 170',
                'buscar': ['Elidia', 'Mendoza']
            },
            {
                'nombre': 'Melqueceded Rodriguez',
                'problema': 'Crédito 240, 4 cuotas de 60 cada una, saldo pendiente 60',
                'buscar': ['Melqueceded', 'Rodriguez']
            },
            {
                'nombre': 'Yamaris Medina',
                'problema': 'Crédito 150, 3 abonos de 50 cada uno, saldo pendiente 50',
                'buscar': ['Yamaris', 'Medina']
            }
        ]
        
        if usuario:
            # Buscar caso específico
            caso = next((c for c in casos_reportados if usuario.lower() in c['nombre'].lower()), None)
            if caso:
                self.diagnosticar_caso(caso)
            else:
                self.stdout.write(f"❌ Usuario '{usuario}' no encontrado en casos reportados")
        elif todos:
            # Diagnosticar todos los casos
            for caso in casos_reportados:
                self.diagnosticar_caso(caso)
                self.stdout.write("")
        else:
            self.stdout.write("❌ Debes especificar --usuario <nombre> o --todos")
            self.stdout.write("Casos disponibles:")
            for caso in casos_reportados:
                self.stdout.write(f"  - {caso['nombre']}: {caso['problema']}")

    def diagnosticar_caso(self, caso):
        self.stdout.write(f"🔍 DIAGNOSTICANDO: {caso['nombre']}")
        self.stdout.write(f"📋 Problema reportado: {caso['problema']}")
        self.stdout.write("-" * 50)
        
        # Buscar usuario
        usuarios = User.objects.filter(
            first_name__icontains=caso['buscar'][0],
            last_name__icontains=caso['buscar'][1]
        )
        
        if not usuarios.exists():
            self.stdout.write(f"❌ Usuario no encontrado: {caso['nombre']}")
            return
        
        for user in usuarios:
            self.stdout.write(f"👤 Usuario encontrado: {user.username} ({user.first_name} {user.last_name})")
            
            # Buscar créditos del usuario
            credits = Credit.objects.filter(user=user).order_by('-created_at')
            
            if not credits.exists():
                self.stdout.write(f"❌ No se encontraron créditos para {user.username}")
                continue
            
            self.stdout.write(f"📊 Total de créditos: {credits.count()}")
            self.stdout.write("")
            
            for i, credit in enumerate(credits, 1):
                self.stdout.write(f"💳 CRÉDITO #{i}: {credit.uid}")
                self.stdout.write(f"   Precio original: ${credit.price:,.2f}")
                self.stdout.write(f"   Total abonos (BD): ${credit.total_abonos:,.2f}")
                self.stdout.write(f"   Saldo pendiente (BD): ${credit.pending_amount:,.2f}")
                self.stdout.write(f"   Estado: {credit.state}")
                self.stdout.write(f"   En mora: {credit.is_in_default}")
                self.stdout.write(f"   Nivel morosidad: {credit.morosidad_level}")
                self.stdout.write(f"   Fecha creación: {credit.created_at}")
                
                # Calcular total real de pagos confirmados
                real_payments = Transaction.objects.filter(
                    account_method_amounts__credit=credit,
                    transaction_type='income',
                    status='confirmed'
                ).aggregate(
                    total=Sum('account_method_amounts__amount_paid')
                )['total'] or Decimal('0.00')
                
                # Calcular total de ajustes
                total_adjustments = credit.adjustments.aggregate(
                    total=Sum('amount')
                )['total'] or Decimal('0.00')
                
                # Calcular saldo esperado
                expected_pending = credit.price + total_adjustments - real_payments
                
                self.stdout.write(f"   💰 ANÁLISIS DETALLADO:")
                self.stdout.write(f"      Pagos reales confirmados: ${real_payments:,.2f}")
                self.stdout.write(f"      Total ajustes: ${total_adjustments:,.2f}")
                self.stdout.write(f"      Saldo esperado: ${expected_pending:,.2f}")
                
                # Verificar inconsistencias
                abonos_difference = abs(credit.total_abonos - real_payments)
                pending_difference = abs(credit.pending_amount - expected_pending)
                
                if abonos_difference > Decimal('0.01') or pending_difference > Decimal('0.01'):
                    self.stdout.write(f"   ⚠️  INCONSISTENCIAS DETECTADAS:")
                    self.stdout.write(f"      Diferencia en abonos: ${abonos_difference:,.2f}")
                    self.stdout.write(f"      Diferencia en saldo: ${pending_difference:,.2f}")
                else:
                    self.stdout.write(f"   ✅ Saldos consistentes")
                
                # Mostrar transacciones detalladas
                self.stdout.write(f"   📋 TRANSACCIONES DETALLADAS:")
                transactions = Transaction.objects.filter(
                    account_method_amounts__credit=credit,
                    transaction_type='income'
                ).order_by('date')
                
                if transactions.exists():
                    for j, transaction in enumerate(transactions, 1):
                        ama = transaction.account_method_amounts.filter(credit=credit).first()
                        if ama:
                            self.stdout.write(f"      {j}. Fecha: {transaction.date.strftime('%Y-%m-%d')}")
                            self.stdout.write(f"         Monto: ${ama.amount_paid:,.2f}")
                            self.stdout.write(f"         Estado: {transaction.status}")
                            self.stdout.write(f"         Descripción: {transaction.description or 'Sin descripción'}")
                else:
                    self.stdout.write(f"      No se encontraron transacciones de pago")
                
                # Mostrar cuotas
                self.stdout.write(f"   📅 CUOTAS:")
                installments = credit.installments.all().order_by('number')
                if installments.exists():
                    for installment in installments:
                        status_icon = "✅" if installment.status == 'paid' else "⏳" if installment.status == 'pending' else "❌"
                        self.stdout.write(f"      {status_icon} Cuota #{installment.number}: ${installment.amount:,.2f} - {installment.status}")
                        if installment.paid_on:
                            self.stdout.write(f"         Pagada el: {installment.paid_on}")
                else:
                    self.stdout.write(f"      No se encontraron cuotas generadas")
                
                self.stdout.write("")
                
                # Recomendaciones específicas
                if abonos_difference > Decimal('0.01') or pending_difference > Decimal('0.01'):
                    self.stdout.write(f"   🔧 RECOMENDACIONES:")
                    self.stdout.write(f"      1. Ejecutar recálculo: python3 manage.py fix_credit_balances")
                    self.stdout.write(f"      2. Verificar transacciones duplicadas o incorrectas")
                    self.stdout.write(f"      3. Revisar ajustes aplicados al crédito")
                
                self.stdout.write("-" * 50)
