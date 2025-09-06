from django.core.management.base import BaseCommand
from django.db.models import Sum
from decimal import Decimal
from apps.fintech.models import Credit, AccountMethodAmount, CreditAdjustment
from apps.fintech.utils.root import recalculate_credit
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Corrige todos los saldos de créditos inconsistentes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostrar qué se corregiría sin hacer cambios'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Número máximo de créditos a procesar'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        limit = options['limit']
        
        self.stdout.write("🔧 CORRIGIENDO SALDOS DE CRÉDITOS...")
        self.stdout.write("=" * 60)
        
        if dry_run:
            self.stdout.write("🔍 MODO DRY-RUN: Solo mostrando qué se corregiría")
            self.stdout.write("")
        
        # Obtener créditos a procesar
        credits_query = Credit.objects.filter(
            state__in=['pending', 'completed']
        ).select_related('user', 'periodicity')
        
        if limit:
            credits_query = credits_query[:limit]
        
        credits = list(credits_query)
        total_credits = len(credits)
        
        self.stdout.write(f"📊 PROCESANDO {total_credits} CRÉDITOS...")
        self.stdout.write("")
        
        fixed_count = 0
        error_count = 0
        total_difference_corrected = Decimal('0.00')
        
        for i, credit in enumerate(credits, 1):
            try:
                # Calcular total real de pagos confirmados
                real_payments = AccountMethodAmount.objects.filter(
                    credit=credit,
                    transaction__status='confirmed',
                    transaction__transaction_type='income'
                ).aggregate(
                    total=Sum('amount_paid')
                )['total'] or Decimal('0.00')
                
                # Calcular total de ajustes
                total_adjustments = credit.adjustments.aggregate(
                    total=Sum('amount')
                )['total'] or Decimal('0.00')
                
                # Calcular saldo esperado
                expected_pending = credit.price + total_adjustments - real_payments
                
                # Verificar inconsistencias
                abonos_difference = abs(credit.total_abonos - real_payments)
                pending_difference = abs(credit.pending_amount - expected_pending)
                
                is_problematic = (
                    abonos_difference > Decimal('0.01') or 
                    pending_difference > Decimal('0.01')
                )
                
                if is_problematic:
                    self.stdout.write(f"⚠️  CRÉDITO {i}/{total_credits}: {credit.uid}")
                    self.stdout.write(f"   Usuario: {credit.user}")
                    self.stdout.write(f"   Precio: ${credit.price:,.2f}")
                    self.stdout.write(f"   Total abonos en BD: ${credit.total_abonos:,.2f}")
                    self.stdout.write(f"   Pagos reales: ${real_payments:,.2f}")
                    self.stdout.write(f"   Diferencia abonos: ${abonos_difference:,.2f}")
                    self.stdout.write(f"   Saldo en BD: ${credit.pending_amount:,.2f}")
                    self.stdout.write(f"   Saldo esperado: ${expected_pending:,.2f}")
                    self.stdout.write(f"   Diferencia saldo: ${pending_difference:,.2f}")
                    
                    if not dry_run:
                        self.stdout.write(f"   🔄 CORRIGIENDO...")
                        
                        # Corregir usando recalculate_credit que es más robusto
                        recalculate_credit(credit)
                        credit.refresh_from_db()
                        
                        # Verificar si se corrigió
                        new_real_payments = AccountMethodAmount.objects.filter(
                            credit=credit,
                            transaction__status='confirmed',
                            transaction__transaction_type='income'
                        ).aggregate(
                            total=Sum('amount_paid')
                        )['total'] or Decimal('0.00')
                        
                        new_expected_pending = credit.price + total_adjustments - new_real_payments
                        new_difference = abs(credit.pending_amount - new_expected_pending)
                        
                        if new_difference <= Decimal('0.01'):
                            fixed_count += 1
                            total_difference_corrected += abonos_difference + pending_difference
                            self.stdout.write(f"   ✅ CORREGIDO")
                        else:
                            self.stdout.write(f"   ❌ NO SE PUDO CORREGIR COMPLETAMENTE")
                    else:
                        self.stdout.write(f"   🔍 SE CORREGIRÍA")
                        fixed_count += 1
                        total_difference_corrected += abonos_difference + pending_difference
                    
                    self.stdout.write("")
                
                # Mostrar progreso cada 100 créditos
                if i % 100 == 0:
                    self.stdout.write(f"📊 Progreso: {i}/{total_credits} créditos procesados...")
                    
            except Exception as e:
                error_count += 1
                self.stdout.write(f"❌ Error procesando crédito {credit.uid}: {str(e)}")
                logger.error(f"Error corrigiendo crédito {credit.uid}: {str(e)}")
        
        # Resumen final
        self.stdout.write("📋 RESUMEN FINAL:")
        self.stdout.write(f"   Créditos procesados: {total_credits}")
        self.stdout.write(f"   Créditos {'que se corregirían' if dry_run else 'corregidos'}: {fixed_count}")
        self.stdout.write(f"   Errores: {error_count}")
        
        if fixed_count > 0:
            self.stdout.write(f"   Diferencia total {'que se corregiría' if dry_run else 'corregida'}: ${total_difference_corrected:,.2f}")
        
        if dry_run and fixed_count > 0:
            self.stdout.write("")
            self.stdout.write("💡 Para aplicar las correcciones, ejecuta el comando sin --dry-run")
        
        if error_count > 0:
            self.stdout.write("")
            self.stdout.write("⚠️  Se encontraron errores. Revisa los logs para más detalles.")
        
        self.stdout.write("")
        self.stdout.write("✅ Proceso completado.")
