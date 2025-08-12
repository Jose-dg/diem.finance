#!/usr/bin/env python3
"""
Script para analizar pagos y abonos de créditos desde mayo de 2025 hasta hoy.
Analiza en detalle los pagos realizados y los abonos pendientes.
"""

import os
import sys
import django
from datetime import datetime, date, timedelta
from decimal import Decimal
from django.db.models import Q, Sum, Count, Avg
from django.utils import timezone

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.fintech.models import Credit, User, AccountMethodAmount, Transaction


def analizar_pagos_y_abonos():
    """
    Analiza los pagos y abonos de créditos desde mayo de 2025 hasta hoy.
    """
    print("=" * 80)
    print("ANÁLISIS DE PAGOS Y ABONOS DE CRÉDITOS")
    print("Período: Mayo 2025 - Hoy")
    print("=" * 80)
    
    # Fecha de inicio: 1 de mayo de 2025
    fecha_inicio = date(2025, 5, 1)
    fecha_fin = timezone.now().date()
    
    print(f"Fecha de inicio: {fecha_inicio}")
    print(f"Fecha de fin: {fecha_fin}")
    print()
    
    # 1. Análisis general de pagos
    print("1. ANÁLISIS GENERAL DE PAGOS:")
    print("-" * 50)
    
    # Obtener todos los pagos (AccountMethodAmount) relacionados con créditos del período
    pagos_creditos = AccountMethodAmount.objects.filter(
        credit__created_at__date__range=[fecha_inicio, fecha_fin],
        transaction__transaction_type='income',
        transaction__status='confirmed'
    ).select_related('credit', 'credit__user', 'transaction')
    
    total_pagos = pagos_creditos.count()
    total_monto_pagado = pagos_creditos.aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
    
    print(f"Total de pagos realizados: {total_pagos}")
    print(f"Total monto pagado: ${total_monto_pagado:,.2f}")
    
    if total_pagos > 0:
        promedio_pago = total_monto_pagado / total_pagos
        print(f"Promedio por pago: ${promedio_pago:,.2f}")
    
    print()
    
    # 2. Análisis de pagos por mes
    print("2. ANÁLISIS DE PAGOS POR MES:")
    print("-" * 50)
    
    pagos_por_mes = pagos_creditos.extra(
        select={'mes': "EXTRACT(month FROM transaction.date)"}
    ).values('mes').annotate(
        count=Count('id'),
        total_pagado=Sum('amount_paid'),
        promedio_pago=Avg('amount_paid')
    ).order_by('mes')
    
    meses = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
        7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    
    for pago_mes in pagos_por_mes:
        mes_nombre = meses.get(pago_mes['mes'], f"Mes {pago_mes['mes']}")
        print(f"{mes_nombre}:")
        print(f"  - Pagos realizados: {pago_mes['count']}")
        print(f"  - Total pagado: ${pago_mes['total_pagado']:,.2f}")
        print(f"  - Promedio por pago: ${pago_mes['promedio_pago']:,.2f}")
        print()
    
    # 3. Clientes con mejor comportamiento de pago
    print("3. CLIENTES CON MEJOR COMPORTAMIENTO DE PAGO:")
    print("-" * 50)
    
    clientes_pagos = pagos_creditos.values(
        'credit__user__username', 
        'credit__user__first_name', 
        'credit__user__last_name'
    ).annotate(
        pagos_count=Count('id'),
        total_pagado=Sum('amount_paid'),
        promedio_pago=Avg('amount_paid')
    ).order_by('-total_pagado')[:10]  # Top 10
    
    for cliente in clientes_pagos:
        nombre = f"{cliente['credit__user__first_name']} {cliente['credit__user__last_name']}".strip()
        if not nombre:
            nombre = cliente['credit__user__username']
        
        print(f"Cliente: {nombre}")
        print(f"  - Pagos realizados: {cliente['pagos_count']}")
        print(f"  - Total pagado: ${cliente['total_pagado']:,.2f}")
        print(f"  - Promedio por pago: ${cliente['promedio_pago']:,.2f}")
        print()
    
    # 4. Análisis de créditos sin pagos
    print("4. CRÉDITOS SIN PAGOS:")
    print("-" * 50)
    
    creditos_sin_pagos = Credit.objects.filter(
        created_at__date__range=[fecha_inicio, fecha_fin],
        total_abonos=0.00
    ).select_related('user', 'subcategory')
    
    creditos_sin_pagos_por_cliente = creditos_sin_pagos.values(
        'user__username', 
        'user__first_name', 
        'user__last_name'
    ).annotate(
        creditos_count=Count('id'),
        total_solicitado=Sum('price'),
        dias_sin_pago=Count('id')  # Esto se puede mejorar calculando días reales
    ).order_by('-total_solicitado')
    
    print(f"Total de clientes con créditos sin pagos: {len(creditos_sin_pagos_por_cliente)}")
    print()
    
    for cliente in creditos_sin_pagos_por_cliente:
        nombre = f"{cliente['user__first_name']} {cliente['user__last_name']}".strip()
        if not nombre:
            nombre = cliente['user__username']
        
        print(f"Cliente: {nombre}")
        print(f"  - Créditos sin pagos: {cliente['creditos_count']}")
        print(f"  - Total solicitado: ${cliente['total_solicitado']:,.2f}")
        print()
    
    # 5. Análisis de morosidad por días
    print("5. ANÁLISIS DE MOROSIDAD POR DÍAS:")
    print("-" * 50)
    
    # Créditos que deberían haber tenido pagos pero no los tienen
    creditos_morosos = Credit.objects.filter(
        created_at__date__range=[fecha_inicio, fecha_fin],
        is_in_default=True
    ).select_related('user')
    
    # Calcular días de mora
    hoy = timezone.now().date()
    
    for credito in creditos_morosos[:10]:  # Mostrar solo los primeros 10
        dias_mora = (hoy - credito.first_date_payment).days
        nombre = f"{credito.user.first_name} {credito.user.last_name}".strip()
        if not nombre:
            nombre = credito.user.username
        
        print(f"Cliente: {nombre}")
        print(f"  - Crédito ID: {credito.id}")
        print(f"  - Monto solicitado: ${credito.price:,.2f}")
        print(f"  - Monto abonado: ${credito.total_abonos:,.2f}")
        print(f"  - Monto pendiente: ${credito.pending_amount:,.2f}")
        print(f"  - Fecha primer pago: {credito.first_date_payment}")
        print(f"  - Días de mora: {dias_mora}")
        print(f"  - Nivel de morosidad: {credito.morosidad_level}")
        print()
    
    # 6. Resumen de abonos pendientes
    print("6. RESUMEN DE ABONOS PENDIENTES:")
    print("-" * 50)
    
    creditos_periodo = Credit.objects.filter(
        created_at__date__range=[fecha_inicio, fecha_fin]
    )
    
    total_creditos = creditos_periodo.count()
    total_solicitado = creditos_periodo.aggregate(total=Sum('price'))['total'] or Decimal('0.00')
    total_abonado = creditos_periodo.aggregate(total=Sum('total_abonos'))['total'] or Decimal('0.00')
    total_pendiente = creditos_periodo.aggregate(total=Sum('pending_amount'))['total'] or Decimal('0.00')
    
    print(f"Total de créditos en el período: {total_creditos}")
    print(f"Total solicitado: ${total_solicitado:,.2f}")
    print(f"Total abonado: ${total_abonado:,.2f}")
    print(f"Total pendiente: ${total_pendiente:,.2f}")
    
    if total_solicitado > 0:
        porcentaje_pago = (total_abonado / total_solicitado) * 100
        porcentaje_pendiente = (total_pendiente / total_solicitado) * 100
        print(f"Porcentaje pagado: {porcentaje_pago:.1f}%")
        print(f"Porcentaje pendiente: {porcentaje_pendiente:.1f}%")
    
    print()
    print("=" * 80)
    print("ANÁLISIS DE PAGOS COMPLETADO")
    print("=" * 80)


def generar_reporte_pagos_csv():
    """
    Genera un reporte detallado de pagos en formato CSV
    """
    from django.db import connection
    import csv
    
    fecha_inicio = date(2025, 5, 1)
    fecha_fin = timezone.now().date()
    
    # Query para obtener datos detallados de pagos
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                u.username,
                u.first_name,
                u.last_name,
                u.email,
                c.id as credit_id,
                c.price as credit_amount,
                c.total_abonos,
                c.pending_amount,
                c.first_date_payment,
                c.second_date_payment,
                c.is_in_default,
                c.morosidad_level,
                c.state,
                COUNT(ama.id) as payments_count,
                SUM(ama.amount_paid) as total_paid,
                AVG(ama.amount_paid) as avg_payment,
                MIN(t.date) as first_payment_date,
                MAX(t.date) as last_payment_date
            FROM fintech_credit c
            JOIN fintech_user u ON c.user_id = u.id
            LEFT JOIN fintech_accountmethodamount ama ON c.id = ama.credit_id
            LEFT JOIN fintech_transaction t ON ama.transaction_id = t.id AND t.transaction_type = 'income' AND t.status = 'confirmed'
            WHERE c.created_at::date BETWEEN %s AND %s
            GROUP BY u.id, u.username, u.first_name, u.last_name, u.email, c.id, c.price, c.total_abonos, c.pending_amount, c.first_date_payment, c.second_date_payment, c.is_in_default, c.morosidad_level, c.state
            ORDER BY c.created_at DESC
        """, [fecha_inicio, fecha_fin])
        
        resultados = cursor.fetchall()
    
    # Generar archivo CSV
    archivo_csv = f"reporte_pagos_creditos_{fecha_inicio}_{fecha_fin}.csv"
    
    with open(archivo_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Encabezados
        writer.writerow([
            'Username', 'Nombre', 'Apellido', 'Email', 'ID Crédito',
            'Monto Crédito', 'Total Abonado', 'Monto Pendiente',
            'Fecha Primer Pago', 'Fecha Segundo Pago', 'En Mora',
            'Nivel Morosidad', 'Estado', 'Cantidad Pagos',
            'Total Pagado', 'Promedio Pago', 'Primer Pago', 'Último Pago'
        ])
        
        # Datos
        for row in resultados:
            writer.writerow(row)
    
    print(f"Reporte de pagos generado: {archivo_csv}")


if __name__ == "__main__":
    try:
        analizar_pagos_y_abonos()
        print("\n¿Desea generar un reporte detallado de pagos en CSV? (s/n): ", end="")
        respuesta = input().lower().strip()
        
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            generar_reporte_pagos_csv()
            
    except Exception as e:
        print(f"Error durante el análisis: {str(e)}")
        import traceback
        traceback.print_exc()
