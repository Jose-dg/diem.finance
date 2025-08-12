#!/usr/bin/env python3
"""
Script principal para análisis completo de créditos desde mayo de 2025 hasta hoy.
Combina análisis de estado de créditos y análisis de pagos/abonos.
"""

import os
import sys
import django
from datetime import datetime, date
from decimal import Decimal
from django.db.models import Q, Sum, Count
from django.utils import timezone

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.fintech.models import Credit, User, AccountMethodAmount, Transaction


def mostrar_menu():
    """
    Muestra el menú principal de opciones
    """
    print("\n" + "=" * 60)
    print("ANÁLISIS COMPLETO DE CRÉDITOS - MENÚ PRINCIPAL")
    print("=" * 60)
    print("1. Análisis general de estado de créditos")
    print("2. Análisis detallado de pagos y abonos")
    print("3. Análisis completo (ambos)")
    print("4. Generar reporte CSV de créditos")
    print("5. Generar reporte CSV de pagos")
    print("6. Salir")
    print("=" * 60)


def analisis_general_creditos():
    """
    Análisis general del estado de créditos
    """
    print("\n" + "=" * 80)
    print("ANÁLISIS GENERAL DE ESTADO DE CRÉDITOS")
    print("Período: Mayo 2025 - Hoy")
    print("=" * 80)
    
    fecha_inicio = date(2025, 5, 1)
    fecha_fin = timezone.now().date()
    
    # Obtener créditos del período
    creditos_periodo = Credit.objects.filter(
        created_at__date__range=[fecha_inicio, fecha_fin]
    ).select_related('user', 'subcategory', 'currency')
    
    total_creditos = creditos_periodo.count()
    
    if total_creditos == 0:
        print("No se encontraron créditos en el período especificado.")
        return
    
    # Estadísticas generales
    total_solicitado = creditos_periodo.aggregate(total=Sum('price'))['total'] or Decimal('0.00')
    total_abonado = creditos_periodo.aggregate(total=Sum('total_abonos'))['total'] or Decimal('0.00')
    total_pendiente = creditos_periodo.aggregate(total=Sum('pending_amount'))['total'] or Decimal('0.00')
    
    print(f"📊 ESTADÍSTICAS GENERALES:")
    print(f"   • Total de créditos: {total_creditos}")
    print(f"   • Monto total solicitado: ${total_solicitado:,.2f}")
    print(f"   • Monto total abonado: ${total_abonado:,.2f}")
    print(f"   • Monto total pendiente: ${total_pendiente:,.2f}")
    
    if total_solicitado > 0:
        porcentaje_pago = (total_abonado / total_solicitado) * 100
        print(f"   • Porcentaje de pago: {porcentaje_pago:.1f}%")
    
    # Clientes sin abonos
    clientes_sin_abonos = creditos_periodo.filter(total_abonos=0.00).values('user__username').distinct().count()
    print(f"\n🚨 CLIENTES SIN ABONOS:")
    print(f"   • Total de clientes sin abonos: {clientes_sin_abonos}")
    
    # Clientes con créditos atrasados
    clientes_atrasados = creditos_periodo.filter(
        Q(is_in_default=True) | 
        Q(morosidad_level__in=['mild_default', 'moderate_default', 'severe_default', 'recurrent_default', 'critical_default'])
    ).values('user__username').distinct().count()
    
    print(f"\n⚠️  CLIENTES CON CRÉDITOS ATRASADOS:")
    print(f"   • Total de clientes atrasados: {clientes_atrasados}")
    
    # Análisis por estado
    print(f"\n📋 ANÁLISIS POR ESTADO:")
    estados = creditos_periodo.values('state').annotate(
        count=Count('id'),
        total_amount=Sum('price')
    ).order_by('state')
    
    for estado in estados:
        print(f"   • {estado['state']}: {estado['count']} créditos (${estado['total_amount']:,.2f})")


def analisis_pagos_detallado():
    """
    Análisis detallado de pagos y abonos
    """
    print("\n" + "=" * 80)
    print("ANÁLISIS DETALLADO DE PAGOS Y ABONOS")
    print("Período: Mayo 2025 - Hoy")
    print("=" * 80)
    
    fecha_inicio = date(2025, 5, 1)
    fecha_fin = timezone.now().date()
    
    # Pagos realizados
    pagos_creditos = AccountMethodAmount.objects.filter(
        credit__created_at__date__range=[fecha_inicio, fecha_fin],
        transaction__transaction_type='income',
        transaction__status='confirmed'
    )
    
    total_pagos = pagos_creditos.count()
    total_monto_pagado = pagos_creditos.aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
    
    print(f"💰 ESTADÍSTICAS DE PAGOS:")
    print(f"   • Total de pagos realizados: {total_pagos}")
    print(f"   • Total monto pagado: ${total_monto_pagado:,.2f}")
    
    if total_pagos > 0:
        promedio_pago = total_monto_pagado / total_pagos
        print(f"   • Promedio por pago: ${promedio_pago:,.2f}")
    
    # Créditos sin pagos
    creditos_sin_pagos = Credit.objects.filter(
        created_at__date__range=[fecha_inicio, fecha_fin],
        total_abonos=0.00
    ).count()
    
    print(f"\n❌ CRÉDITOS SIN PAGOS:")
    print(f"   • Total de créditos sin pagos: {creditos_sin_pagos}")
    
    # Top 5 clientes con más pagos
    print(f"\n🏆 TOP 5 CLIENTES CON MÁS PAGOS:")
    top_clientes = pagos_creditos.values(
        'credit__user__username', 
        'credit__user__first_name', 
        'credit__user__last_name'
    ).annotate(
        total_pagado=Sum('amount_paid'),
        pagos_count=Count('id')
    ).order_by('-total_pagado')[:5]
    
    for i, cliente in enumerate(top_clientes, 1):
        nombre = f"{cliente['credit__user__first_name']} {cliente['credit__user__last_name']}".strip()
        if not nombre:
            nombre = cliente['credit__user__username']
        
        print(f"   {i}. {nombre}: ${cliente['total_pagado']:,.2f} ({cliente['pagos_count']} pagos)")


def generar_reporte_csv_creditos():
    """
    Genera reporte CSV de créditos
    """
    from django.db import connection
    import csv
    
    fecha_inicio = date(2025, 5, 1)
    fecha_fin = timezone.now().date()
    
    print(f"\n📄 Generando reporte CSV de créditos...")
    
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
    
    archivo_csv = f"reporte_creditos_{fecha_inicio}_{fecha_fin}.csv"
    
    with open(archivo_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'Username', 'Nombre', 'Apellido', 'Email', 'Total Créditos',
            'Créditos Sin Abono', 'Créditos Atrasados', 'Total Solicitado',
            'Total Abonado', 'Total Pendiente', 'Promedio Crédito',
            'Primer Crédito', 'Último Crédito'
        ])
        
        for row in resultados:
            writer.writerow(row)
    
    print(f"✅ Reporte generado: {archivo_csv}")


def generar_reporte_csv_pagos():
    """
    Genera reporte CSV de pagos
    """
    from django.db import connection
    import csv
    
    fecha_inicio = date(2025, 5, 1)
    fecha_fin = timezone.now().date()
    
    print(f"\n📄 Generando reporte CSV de pagos...")
    
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
    
    archivo_csv = f"reporte_pagos_creditos_{fecha_inicio}_{fecha_fin}.csv"
    
    with open(archivo_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'Username', 'Nombre', 'Apellido', 'Email', 'ID Crédito',
            'Monto Crédito', 'Total Abonado', 'Monto Pendiente',
            'Fecha Primer Pago', 'Fecha Segundo Pago', 'En Mora',
            'Nivel Morosidad', 'Estado', 'Cantidad Pagos',
            'Total Pagado', 'Promedio Pago', 'Primer Pago', 'Último Pago'
        ])
        
        for row in resultados:
            writer.writerow(row)
    
    print(f"✅ Reporte generado: {archivo_csv}")


def main():
    """
    Función principal del script
    """
    print("🚀 Iniciando análisis de créditos...")
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\nSeleccione una opción (1-6): ").strip()
            
            if opcion == '1':
                analisis_general_creditos()
            elif opcion == '2':
                analisis_pagos_detallado()
            elif opcion == '3':
                analisis_general_creditos()
                analisis_pagos_detallado()
            elif opcion == '4':
                generar_reporte_csv_creditos()
            elif opcion == '5':
                generar_reporte_csv_pagos()
            elif opcion == '6':
                print("\n👋 ¡Hasta luego!")
                break
            else:
                print("\n❌ Opción no válida. Por favor seleccione 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Análisis interrumpido por el usuario.")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
