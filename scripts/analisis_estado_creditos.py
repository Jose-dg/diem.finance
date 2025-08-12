#!/usr/bin/env python3
"""
Script para analizar el estado de los créditos desde mayo de 2025 hasta hoy.
Analiza clientes que solicitaron crédito y no han hecho abono o están atrasados.
"""

import os
import sys
import django
from datetime import datetime, date
from decimal import Decimal
from django.db.models import Q, Sum, Count, Case, When, Value, IntegerField
from django.utils import timezone

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.fintech.models import Credit, User, AccountMethodAmount, Transaction
from apps.fintech.managers import CreditManager


def analizar_estado_creditos():
    """
    Analiza el estado de los créditos desde mayo de 2025 hasta hoy.
    """
    print("=" * 80)
    print("ANÁLISIS DE ESTADO DE CRÉDITOS")
    print("Período: Mayo 2025 - Hoy")
    print("=" * 80)
    
    # Fecha de inicio: 1 de mayo de 2025
    fecha_inicio = date(2025, 5, 1)
    fecha_fin = timezone.now().date()
    
    print(f"Fecha de inicio: {fecha_inicio}")
    print(f"Fecha de fin: {fecha_fin}")
    print()
    
    # 1. Obtener todos los créditos en el período
    creditos_periodo = Credit.objects.filter(
        created_at__date__range=[fecha_inicio, fecha_fin]
    ).select_related('user', 'subcategory', 'currency')
    
    total_creditos = creditos_periodo.count()
    print(f"1. TOTAL DE CRÉDITOS SOLICITADOS: {total_creditos}")
    print()
    
    if total_creditos == 0:
        print("No se encontraron créditos en el período especificado.")
        return
    
    # 2. Análisis por estado de crédito
    print("2. ANÁLISIS POR ESTADO DE CRÉDITO:")
    print("-" * 50)
    
    estados = creditos_periodo.values('state').annotate(
        count=Count('id'),
        total_amount=Sum('price'),
        total_pending=Sum('pending_amount')
    ).order_by('state')
    
    for estado in estados:
        print(f"Estado '{estado['state']}':")
        print(f"  - Cantidad: {estado['count']}")
        print(f"  - Monto total: ${estado['total_amount']:,.2f}")
        print(f"  - Monto pendiente: ${estado['total_pending']:,.2f}")
        print()
    
    # 3. Clientes que solicitaron crédito y no han hecho abono
    print("3. CLIENTES SIN ABONOS:")
    print("-" * 50)
    
    creditos_sin_abonos = creditos_periodo.filter(
        total_abonos=0.00
    ).select_related('user')
    
    clientes_sin_abonos = creditos_sin_abonos.values('user__username', 'user__first_name', 'user__last_name').annotate(
        creditos_count=Count('id'),
        total_solicitado=Sum('price'),
        total_pendiente=Sum('pending_amount')
    ).order_by('-total_solicitado')
    
    print(f"Total de clientes sin abonos: {len(clientes_sin_abonos)}")
    print()
    
    for cliente in clientes_sin_abonos:
        nombre = f"{cliente['user__first_name']} {cliente['user__last_name']}".strip()
        if not nombre:
            nombre = cliente['user__username']
        
        print(f"Cliente: {nombre}")
        print(f"  - Créditos solicitados: {cliente['creditos_count']}")
        print(f"  - Monto total solicitado: ${cliente['total_solicitado']:,.2f}")
        print(f"  - Monto pendiente: ${cliente['total_pendiente']:,.2f}")
        print()
    
    # 4. Clientes con créditos atrasados
    print("4. CLIENTES CON CRÉDITOS ATRASADOS:")
    print("-" * 50)
    
    creditos_atrasados = creditos_periodo.filter(
        Q(is_in_default=True) | 
        Q(morosidad_level__in=['mild_default', 'moderate_default', 'severe_default', 'recurrent_default', 'critical_default'])
    ).select_related('user')
    
    clientes_atrasados = creditos_atrasados.values('user__username', 'user__first_name', 'user__last_name').annotate(
        creditos_count=Count('id'),
        total_solicitado=Sum('price'),
        total_pendiente=Sum('pending_amount'),
        total_abonado=Sum('total_abonos')
    ).order_by('-total_pendiente')
    
    print(f"Total de clientes con créditos atrasados: {len(clientes_atrasados)}")
    print()
    
    for cliente in clientes_atrasados:
        nombre = f"{cliente['user__first_name']} {cliente['user__last_name']}".strip()
        if not nombre:
            nombre = cliente['user__username']
        
        print(f"Cliente: {nombre}")
        print(f"  - Créditos atrasados: {cliente['creditos_count']}")
        print(f"  - Monto total solicitado: ${cliente['total_solicitado']:,.2f}")
        print(f"  - Monto abonado: ${cliente['total_abonado']:,.2f}")
        print(f"  - Monto pendiente: ${cliente['total_pendiente']:,.2f}")
        print()
    
    # 5. Análisis detallado por cliente
    print("5. ANÁLISIS DETALLADO POR CLIENTE:")
    print("-" * 50)
    
    # Obtener todos los clientes únicos que solicitaron crédito en el período
    clientes_unicos = creditos_periodo.values('user__username', 'user__first_name', 'user__last_name').annotate(
        total_creditos=Count('id'),
        creditos_sin_abono=Count('id', filter=Q(total_abonos=0.00)),
        creditos_atrasados=Count('id', filter=Q(is_in_default=True)),
        total_solicitado=Sum('price'),
        total_abonado=Sum('total_abonos'),
        total_pendiente=Sum('pending_amount')
    ).order_by('-total_solicitado')
    
    print(f"Total de clientes únicos: {len(clientes_unicos)}")
    print()
    
    for cliente in clientes_unicos:
        nombre = f"{cliente['user__first_name']} {cliente['user__last_name']}".strip()
        if not nombre:
            nombre = cliente['user__username']
        
        print(f"Cliente: {nombre}")
        print(f"  - Total de créditos: {cliente['total_creditos']}")
        print(f"  - Créditos sin abono: {cliente['creditos_sin_abono']}")
        print(f"  - Créditos atrasados: {cliente['creditos_atrasados']}")
        print(f"  - Monto total solicitado: ${cliente['total_solicitado']:,.2f}")
        print(f"  - Monto total abonado: ${cliente['total_abonado']:,.2f}")
        print(f"  - Monto total pendiente: ${cliente['total_pendiente']:,.2f}")
        
        # Calcular porcentaje de pago
        if cliente['total_solicitado'] > 0:
            porcentaje_pago = (cliente['total_abonado'] / cliente['total_solicitado']) * 100
            print(f"  - Porcentaje de pago: {porcentaje_pago:.1f}%")
        
        print()
    
    # 6. Resumen ejecutivo
    print("6. RESUMEN EJECUTIVO:")
    print("-" * 50)
    
    total_monto_solicitado = creditos_periodo.aggregate(total=Sum('price'))['total'] or Decimal('0.00')
    total_monto_abonado = creditos_periodo.aggregate(total=Sum('total_abonos'))['total'] or Decimal('0.00')
    total_monto_pendiente = creditos_periodo.aggregate(total=Sum('pending_amount'))['total'] or Decimal('0.00')
    
    print(f"Total de créditos solicitados: {total_creditos}")
    print(f"Total de clientes únicos: {len(clientes_unicos)}")
    print(f"Monto total solicitado: ${total_monto_solicitado:,.2f}")
    print(f"Monto total abonado: ${total_monto_abonado:,.2f}")
    print(f"Monto total pendiente: ${total_monto_pendiente:,.2f}")
    
    if total_monto_solicitado > 0:
        porcentaje_pago_general = (total_monto_abonado / total_monto_solicitado) * 100
        print(f"Porcentaje de pago general: {porcentaje_pago_general:.1f}%")
    
    print()
    print("=" * 80)
    print("ANÁLISIS COMPLETADO")
    print("=" * 80)


def generar_reporte_detallado():
    """
    Genera un reporte detallado en formato CSV
    """
    from django.db import connection
    import csv
    
    fecha_inicio = date(2025, 5, 1)
    fecha_fin = timezone.now().date()
    
    # Query para obtener datos detallados
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                u.username,
                u.first_name,
                u.last_name,
                u.email,
                COUNT(c.id) as total_creditos,
                SUM(CASE WHEN c.total_abonos = 0 THEN 1 ELSE 0 END) as creditos_sin_abono,
                SUM(CASE WHEN c.is_in_default = True THEN 1 ELSE 0 END) as creditos_atrasados,
                SUM(c.price) as total_solicitado,
                SUM(c.total_abonos) as total_abonado,
                SUM(c.pending_amount) as total_pendiente,
                AVG(c.price) as promedio_credito,
                MIN(c.created_at) as primer_credito,
                MAX(c.created_at) as ultimo_credito
            FROM fintech_credit c
            JOIN fintech_user u ON c.user_id = u.id
            WHERE c.created_at::date BETWEEN %s AND %s
            GROUP BY u.id, u.username, u.first_name, u.last_name, u.email
            ORDER BY total_solicitado DESC
        """, [fecha_inicio, fecha_fin])
        
        resultados = cursor.fetchall()
    
    # Generar archivo CSV
    archivo_csv = f"reporte_creditos_{fecha_inicio}_{fecha_fin}.csv"
    
    with open(archivo_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Encabezados
        writer.writerow([
            'Username', 'Nombre', 'Apellido', 'Email', 'Total Créditos',
            'Créditos Sin Abono', 'Créditos Atrasados', 'Total Solicitado',
            'Total Abonado', 'Total Pendiente', 'Promedio Crédito',
            'Primer Crédito', 'Último Crédito'
        ])
        
        # Datos
        for row in resultados:
            writer.writerow(row)
    
    print(f"Reporte detallado generado: {archivo_csv}")


if __name__ == "__main__":
    try:
        analizar_estado_creditos()
        print("\n¿Desea generar un reporte detallado en CSV? (s/n): ", end="")
        respuesta = input().lower().strip()
        
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            generar_reporte_detallado()
            
    except Exception as e:
        print(f"Error durante el análisis: {str(e)}")
        import traceback
        traceback.print_exc()
