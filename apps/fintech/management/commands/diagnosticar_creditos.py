from django.core.management.base import BaseCommand
from decimal import Decimal
from django.db.models import Sum, Count
from apps.fintech.models import Credit, Transaction, AccountMethodAmount, CreditAdjustment
from apps.fintech.utils.root import recalculate_credit

class Command(BaseCommand):
    help = 'Diagnóstico completo de inconsistencias en saldos de créditos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Corregir automáticamente los créditos con problemas'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Número máximo de créditos a procesar'
        )

    def handle(self, *args, **options):
        fix_mode = options['fix']
        limit = options['limit']
        
        self.stdout.write("🔍 DIAGNÓSTICO COMPLETO DE CRÉDITOS")
        self.stdout.write("=" * 60)
        
        # Estadísticas generales
        total_credits = Credit.objects.count()
        active_credits = Credit.objects.filter(state='pending').count()
        
        self.stdout.write(f"📊 ESTADÍSTICAS GENERALES:")
        self.stdout.write(f"   Total créditos: {total_credits}")
        self.stdout.write(f"   Créditos activos: {active_credits}")
        self.stdout.write("")
        
        # Análisis de inconsistencias
        problematic_credits = []
        fixed_credits = []
        
        # Obtener créditos con posibles problemas
        credits_to_check = Credit.objects.filter(
            state__in=['pending', 'completed']
        ).select_related('user', 'periodicity')[:limit]
        
        self.stdout.write(f"🔍 ANALIZANDO {credits_to_check.count()} CRÉDITOS...")
        self.stdout.write("")
        
        for credit in credits_to_check:
            try:
                # Calcular total real de transacciones confirmadas
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
                
                # Verificar inconsistencias
                abonos_difference = abs(credit.total_abonos - real_payments)
                pending_difference = abs(credit.pending_amount - expected_pending)
                
                is_problematic = (
                    abonos_difference > Decimal('0.01') or 
                    pending_difference > Decimal('0.01')
                )
                
                if is_problematic:
                    problematic_credits.append({
                        'credit': credit,
                        'real_payments': real_payments,
                        'total_adjustments': total_adjustments,
                        'expected_pending': expected_pending,
                        'abonos_difference': abonos_difference,
                        'pending_difference': pending_difference
                    })
                    
                    self.stdout.write(f"⚠️  CRÉDITO PROBLEMÁTICO: {credit.uid}")
                    self.stdout.write(f"   Usuario: {credit.user}")
                    self.stdout.write(f"   Precio: ${credit.price:,.2f}")
                    self.stdout.write(f"   Total abonos en BD: ${credit.total_abonos:,.2f}")
                    self.stdout.write(f"   Pagos reales: ${real_payments:,.2f}")
                    self.stdout.write(f"   Diferencia abonos: ${abonos_difference:,.2f}")
                    self.stdout.write(f"   Saldo en BD: ${credit.pending_amount:,.2f}")
                    self.stdout.write(f"   Saldo esperado: ${expected_pending:,.2f}")
                    self.stdout.write(f"   Diferencia saldo: ${pending_difference:,.2f}")
                    
                    if fix_mode:
                        self.stdout.write(f"   🔄 CORRIGIENDO...")
                        try:
                            recalculate_credit(credit)
                            credit.refresh_from_db()
                            
                            # Verificar si se corrigió
                            new_real_payments = Transaction.objects.filter(
                                account_method_amounts__credit=credit,
                                transaction_type='income',
                                status='confirmed'
                            ).aggregate(
                                total=Sum('account_method_amounts__amount_paid')
                            )['total'] or Decimal('0.00')
                            
                            new_expected_pending = credit.price + total_adjustments - new_real_payments
                            new_difference = abs(credit.pending_amount - new_expected_pending)
                            
                            if new_difference <= Decimal('0.01'):
                                fixed_credits.append(credit.uid)
                                self.stdout.write(f"   ✅ CORREGIDO")
                            else:
                                self.stdout.write(f"   ❌ NO SE PUDO CORREGIR")
                                
                        except Exception as e:
                            self.stdout.write(f"   ❌ ERROR: {str(e)}")
                    
                    self.stdout.write("")
                    
            except Exception as e:
                self.stdout.write(f"❌ Error analizando crédito {credit.uid}: {str(e)}")
        
        # Resumen final
        self.stdout.write("📋 RESUMEN FINAL:")
        self.stdout.write(f"   Créditos analizados: {credits_to_check.count()}")
        self.stdout.write(f"   Créditos problemáticos: {len(problematic_credits)}")
        
        if fix_mode:
            self.stdout.write(f"   Créditos corregidos: {len(fixed_credits)}")
            
            if fixed_credits:
                self.stdout.write(f"   ✅ CRÉDITOS CORREGIDOS:")
                for credit_uid in fixed_credits:
                    self.stdout.write(f"      - {credit_uid}")
        
        # Recomendaciones
        self.stdout.write("")
        self.stdout.write("🎯 RECOMENDACIONES:")
        
        if len(problematic_credits) > 0:
            self.stdout.write(f"   1. Ejecutar con --fix para corregir automáticamente")
            self.stdout.write(f"   2. Revisar logs de transacciones para identificar causas")
            self.stdout.write(f"   3. Implementar validaciones en el proceso de pagos")
            self.stdout.write(f"   4. Programar recálculos periódicos")
        else:
            self.stdout.write(f"   ✅ No se encontraron inconsistencias en los créditos analizados")
        
        # Estadísticas de problemas
        if problematic_credits:
            total_difference = sum(p['abonos_difference'] for p in problematic_credits)
            self.stdout.write(f"")
            self.stdout.write(f"💰 IMPACTO FINANCIERO:")
            self.stdout.write(f"   Diferencia total en abonos: ${total_difference:,.2f}")
            
            # Categorizar problemas
            abonos_only = [p for p in problematic_credits if p['abonos_difference'] > Decimal('0.01') and p['pending_difference'] <= Decimal('0.01')]
            pending_only = [p for p in problematic_credits if p['pending_difference'] > Decimal('0.01') and p['abonos_difference'] <= Decimal('0.01')]
            both_problems = [p for p in problematic_credits if p['abonos_difference'] > Decimal('0.01') and p['pending_difference'] > Decimal('0.01')]
            
            self.stdout.write(f"   Problemas solo en abonos: {len(abonos_only)}")
            self.stdout.write(f"   Problemas solo en saldo: {len(pending_only)}")
            self.stdout.write(f"   Problemas en ambos: {len(both_problems)}") 