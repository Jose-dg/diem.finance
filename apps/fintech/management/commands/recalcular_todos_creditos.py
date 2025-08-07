from django.core.management.base import BaseCommand
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.fintech.models import Credit
from apps.fintech.utils.root import recalculate_credit
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Recalcula todos los créditos en lotes de 300 con logging detallado'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=300,
            help='Tamaño del lote (default: 300)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Solo mostrar qué se haría sin ejecutar cambios'
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Número máximo de créditos a procesar'
        )

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        dry_run = options['dry_run']
        limit = options['limit']
        
        self.stdout.write("🔄 RECÁLCULO MASIVO DE CRÉDITOS")
        self.stdout.write("=" * 50)
        
        if dry_run:
            self.stdout.write("🔍 MODO DRY-RUN: Solo simulación, no se harán cambios")
        
        # Obtener todos los créditos activos
        credits_query = Credit.objects.filter(
            state__in=['pending', 'completed']
        ).select_related('user', 'periodicity')
        
        if limit:
            credits_query = credits_query[:limit]
        
        total_credits = credits_query.count()
        
        self.stdout.write(f"📊 ESTADÍSTICAS:")
        self.stdout.write(f"   Total créditos a procesar: {total_credits}")
        self.stdout.write(f"   Tamaño de lote: {batch_size}")
        self.stdout.write(f"   Modo: {'DRY-RUN' if dry_run else 'EJECUCIÓN REAL'}")
        self.stdout.write("")
        
        # Procesar por lotes
        processed = 0
        success_count = 0
        error_count = 0
        start_time = timezone.now()
        
        for i in range(0, total_credits, batch_size):
            batch_start = i + 1
            batch_end = min(i + batch_size, total_credits)
            
            self.stdout.write(f"📦 PROCESANDO LOTE {i//batch_size + 1}: créditos {batch_start}-{batch_end}")
            
            batch_credits = credits_query[i:i + batch_size]
            
            for credit in batch_credits:
                try:
                    processed += 1
                    
                    # Obtener datos antes del recálculo
                    old_total_abonos = credit.total_abonos
                    old_pending_amount = credit.pending_amount
                    old_is_in_default = credit.is_in_default
                    old_morosidad_level = credit.morosidad_level
                    
                    if not dry_run:
                        # Ejecutar recálculo
                        recalculate_credit(credit)
                        credit.refresh_from_db()
                    
                    # Verificar cambios
                    changes = []
                    if old_total_abonos != credit.total_abonos:
                        changes.append(f"total_abonos: ${old_total_abonos:,.2f} → ${credit.total_abonos:,.2f}")
                    if old_pending_amount != credit.pending_amount:
                        changes.append(f"pending_amount: ${old_pending_amount:,.2f} → ${credit.pending_amount:,.2f}")
                    if old_is_in_default != credit.is_in_default:
                        changes.append(f"is_in_default: {old_is_in_default} → {credit.is_in_default}")
                    if old_morosidad_level != credit.morosidad_level:
                        changes.append(f"morosidad_level: {old_morosidad_level} → {credit.morosidad_level}")
                    
                    if changes:
                        self.stdout.write(f"   ✅ {credit.uid} ({credit.user}): {', '.join(changes)}")
                        success_count += 1
                    else:
                        self.stdout.write(f"   ⚪ {credit.uid} ({credit.user}): Sin cambios")
                        
                except Exception as e:
                    error_count += 1
                    self.stdout.write(f"   ❌ {credit.uid} ({credit.user}): Error - {str(e)}")
                    logger.error(f"Error recalculando crédito {credit.uid}: {str(e)}")
            
            # Progreso del lote
            self.stdout.write(f"   📊 Lote completado: {processed}/{total_credits} créditos procesados")
            self.stdout.write("")
        
        # Resumen final
        end_time = timezone.now()
        duration = end_time - start_time
        
        self.stdout.write("📋 RESUMEN FINAL:")
        self.stdout.write(f"   ✅ Créditos procesados exitosamente: {success_count}")
        self.stdout.write(f"   ❌ Créditos con errores: {error_count}")
        self.stdout.write(f"   ⚪ Créditos sin cambios: {processed - success_count - error_count}")
        self.stdout.write(f"   ⏱️  Tiempo total: {duration}")
        self.stdout.write(f"   📈 Tasa de éxito: {(success_count/processed*100):.1f}%" if processed > 0 else "   📈 Tasa de éxito: 0%")
        
        if dry_run:
            self.stdout.write("")
            self.stdout.write("🔍 MODO DRY-RUN COMPLETADO")
            self.stdout.write("   Para ejecutar los cambios reales, ejecuta sin --dry-run")
        else:
            self.stdout.write("")
            self.stdout.write("✅ RECÁLCULO MASIVO COMPLETADO")
            self.stdout.write("   Todos los créditos han sido recalculados y corregidos") 