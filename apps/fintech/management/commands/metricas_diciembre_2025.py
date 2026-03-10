from django.core.management.base import BaseCommand
from django.db.models import Sum, Count, Q
from apps.fintech.models import Credit
from datetime import datetime
from decimal import Decimal


class Command(BaseCommand):
    help = 'Muestra las métricas de créditos del mes de diciembre 2025'

    def handle(self, *args, **options):
        # Definir el rango de fechas para diciembre 2025
        start_date = datetime(2025, 12, 1, 0, 0, 0)
        end_date = datetime(2025, 12, 31, 23, 59, 59)

        self.stdout.write(self.style.SUCCESS('\n' + '='*80))
        self.stdout.write(self.style.SUCCESS('RESUMEN EJECUTIVO - MÉTRICAS DE CRÉDITOS'))
        self.stdout.write(self.style.SUCCESS(f'Período: Diciembre 2025'))
        self.stdout.write(self.style.SUCCESS('='*80 + '\n'))

        # Obtener todos los créditos creados en diciembre 2025
        creditos_diciembre = Credit.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date
        )

        # 1. Número total de créditos otorgados
        total_creditos = creditos_diciembre.count()

        # 2. Monto total de los créditos desembolsados (price es el monto total del crédito)
        monto_total = creditos_diciembre.aggregate(
            total=Sum('price')
        )['total'] or Decimal('0.00')

        # 3. Ganancia total generada (earnings = intereses cobrados)
        # earnings es el campo que almacena las ganancias/intereses del crédito
        ganancia_total = creditos_diciembre.aggregate(
            total=Sum('earnings')
        )['total'] or Decimal('0.00')

        # Calcular estadísticas adicionales
        monto_costo = creditos_diciembre.aggregate(
            total=Sum('cost')
        )['total'] or Decimal('0.00')

        # Formato de moneda COP
        def format_cop(amount):
            """Formatea un monto en pesos colombianos"""
            if amount is None:
                amount = Decimal('0.00')
            return f"${amount:,.2f} COP"

        # Mostrar resultados
        self.stdout.write(self.style.HTTP_INFO('📊 INDICADORES PRINCIPALES\n'))
        
        self.stdout.write(self.style.WARNING('1️⃣  NÚMERO TOTAL DE CRÉDITOS OTORGADOS'))
        self.stdout.write(f'   {total_creditos:,} créditos\n')

        self.stdout.write(self.style.WARNING('2️⃣  MONTO TOTAL DE CRÉDITOS DESEMBOLSADOS'))
        self.stdout.write(f'   {format_cop(monto_total)}\n')

        self.stdout.write(self.style.WARNING('3️⃣  GANANCIA TOTAL GENERADA (Intereses)'))
        self.stdout.write(f'   {format_cop(ganancia_total)}\n')

        # Información adicional
        self.stdout.write(self.style.HTTP_INFO('\n📈 INFORMACIÓN ADICIONAL\n'))
        
        self.stdout.write(f'💰 Costo total (capital prestado):')
        self.stdout.write(f'   {format_cop(monto_costo)}\n')

        if monto_costo > 0:
            margen = ((ganancia_total / monto_costo) * 100)
            self.stdout.write(f'📊 Margen de ganancia:')
            self.stdout.write(f'   {margen:.2f}%\n')

        if total_creditos > 0:
            promedio_credito = monto_total / total_creditos
            promedio_ganancia = ganancia_total / total_creditos
            
            self.stdout.write(f'📏 Promedio por crédito:')
            self.stdout.write(f'   Monto: {format_cop(promedio_credito)}')
            self.stdout.write(f'   Ganancia: {format_cop(promedio_ganancia)}\n')

        # Desglose por estado
        self.stdout.write(self.style.HTTP_INFO('\n📋 DESGLOSE POR ESTADO\n'))
        
        estados = creditos_diciembre.values('state').annotate(
            cantidad=Count('id'),
            monto=Sum('price'),
            ganancias=Sum('earnings')
        ).order_by('-cantidad')

        for estado in estados:
            estado_nombre = dict(Credit.ORDER_STATES).get(estado['state'], estado['state'])
            self.stdout.write(f"   {estado_nombre}:")
            self.stdout.write(f"      • Cantidad: {estado['cantidad']:,}")
            self.stdout.write(f"      • Monto: {format_cop(estado['monto'] or 0)}")
            self.stdout.write(f"      • Ganancias: {format_cop(estado['ganancias'] or 0)}")

        # Desglose por moneda
        self.stdout.write(self.style.HTTP_INFO('\n💱 DESGLOSE POR MONEDA\n'))
        
        monedas = creditos_diciembre.values('currency__currency').annotate(
            cantidad=Count('id'),
            monto=Sum('price'),
            ganancias=Sum('earnings')
        ).order_by('-cantidad')

        for moneda in monedas:
            nombre_moneda = moneda['currency__currency'] or 'Sin moneda'
            self.stdout.write(f"   {nombre_moneda}:")
            self.stdout.write(f"      • Cantidad: {moneda['cantidad']:,}")
            self.stdout.write(f"      • Monto: {format_cop(moneda['monto'] or 0)}")
            self.stdout.write(f"      • Ganancias: {format_cop(moneda['ganancias'] or 0)}")

        self.stdout.write(self.style.SUCCESS('\n' + '='*80))
        self.stdout.write(self.style.SUCCESS('Consulta completada exitosamente'))
        self.stdout.write(self.style.SUCCESS('='*80 + '\n'))
