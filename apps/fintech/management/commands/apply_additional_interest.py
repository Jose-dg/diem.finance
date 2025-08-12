from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import F
from apps.fintech.models import Credit
from apps.fintech.services.credit import CreditAdjustmentService


class Command(BaseCommand):
    help = 'Aplica interés adicional a créditos que no han cumplido con el pago pactado'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simula la aplicación sin hacer cambios reales',
        )
        parser.add_argument(
            '--credit-uid',
            type=str,
            help='UID específico del crédito a procesar',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Fuerza la aplicación incluso si ya existe el ajuste',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        credit_uid = options['credit_uid']
        force = options['force']

        if dry_run:
            self.stdout.write(
                self.style.WARNING('🔍 MODO SIMULACIÓN - No se harán cambios reales')
            )

        # Filtrar créditos
        if credit_uid:
            credits = Credit.objects.filter(uid=credit_uid)
            if not credits.exists():
                self.stdout.write(
                    self.style.ERROR(f'❌ Crédito con UID {credit_uid} no encontrado')
                )
                return
        else:
            # Créditos con pagos parciales que no han recibido interés adicional
            credits = Credit.objects.filter(
                total_abonos__lt=F('price'),
                state__in=['pending', 'completed']
            )
            
            if not force:
                # Excluir los que ya tienen interés adicional
                credits = credits.exclude(adjustments__type__code='C0001')

        total_credits = credits.count()
        self.stdout.write(f'📊 Procesando {total_credits} créditos...')

        applied_count = 0
        skipped_count = 0
        error_count = 0

        for credit in credits:
            try:
                # Verificar si ya tiene el ajuste
                existing_adjustment = credit.adjustments.filter(type__code='C0001').first()
                
                if existing_adjustment and not force:
                    self.stdout.write(
                        f'⏭️  Crédito {credit.uid}: Ya tiene interés adicional (${existing_adjustment.amount})'
                    )
                    skipped_count += 1
                    continue

                # Calcular interés adicional
                additional_interest = CreditAdjustmentService.calculate_additional_interest(credit)
                
                if additional_interest <= 0:
                    self.stdout.write(
                        f'ℹ️  Crédito {credit.uid}: No requiere interés adicional (price <= cost)'
                    )
                    skipped_count += 1
                    continue

                if not dry_run:
                    # Aplicar interés adicional
                    with transaction.atomic():
                        if existing_adjustment and force:
                            # Actualizar ajuste existente
                            existing_adjustment.amount = additional_interest
                            existing_adjustment.reason = f"Actualizado por comando. Price: {credit.price}, Cost: {credit.cost}"
                            existing_adjustment.save()
                            
                            # Actualizar pending_amount
                            current_pending = credit.pending_amount or 0
                            credit.pending_amount = current_pending + additional_interest
                            credit.save(update_fields=['pending_amount'])
                        else:
                            # Crear nuevo ajuste
                            CreditAdjustmentService.apply_additional_interest(
                                credit,
                                reason=f"Aplicado por comando. Price: {credit.price}, Cost: {credit.cost}"
                            )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Crédito {credit.uid}: Interés adicional ${additional_interest} '
                        f'(Price: ${credit.price}, Cost: ${credit.cost}, Pagado: ${credit.total_abonos})'
                    )
                )
                applied_count += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error procesando crédito {credit.uid}: {str(e)}')
                )
                error_count += 1

        # Resumen final
        self.stdout.write('\n' + '='*50)
        self.stdout.write('📋 RESUMEN FINAL:')
        self.stdout.write(f'✅ Aplicados: {applied_count}')
        self.stdout.write(f'⏭️  Omitidos: {skipped_count}')
        self.stdout.write(f'❌ Errores: {error_count}')
        self.stdout.write(f'📊 Total procesados: {total_credits}')
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('🔍 MODO SIMULACIÓN - Ejecuta sin --dry-run para aplicar cambios')
            ) 