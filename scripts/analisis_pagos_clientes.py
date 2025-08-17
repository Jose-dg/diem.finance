#!/usr/bin/env python3
"""
Análisis Riguroso de Pagos de Clientes
Desde Mayo hasta Hoy
"""
import os
import sys
import django
from datetime import datetime, date, timedelta
from decimal import Decimal
from collections import defaultdict

# Configurar Django
sys.path.append('/Users/ojeda/Documents/Dev/fintech')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.fintech.models import Credit, Transaction, AccountMethodAmount, Installment
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from django.db.models.functions import TruncDate, TruncMonth

def formato_moneda(valor):
    """Formatea valores monetarios"""
    return f"${valor:,.2f}" if valor else "$0.00"

def formato_porcentaje(valor):
    """Formatea porcentajes"""
    return f"{valor:.2f}%" if valor else "0.00%"

def analisis_pagos_periodo():
    """Análisis completo de pagos desde mayo hasta hoy"""
    print("🔍 ANÁLISIS RIGUROSO DE PAGOS DE CLIENTES")
    print("=" * 60)
    
    # Definir período de análisis
    hoy = timezone.now().date()
    inicio_mayo = date(2025, 5, 1)
    
    print(f"📅 PERÍODO DE ANÁLISIS: {inicio_mayo} hasta {hoy}")
    print(f"📊 DÍAS ANALIZADOS: {(hoy - inicio_mayo).days + 1}")
    
    # 1. ANÁLISIS DE CRÉDITOS OTORGADOS EN EL PERÍODO
    print(f"\n1️⃣ CRÉDITOS OTORGADOS EN EL PERÍODO")
    print("-" * 50)
    
    creditos_periodo = Credit.objects.filter(
        created_at__date__range=[inicio_mayo, hoy]
    )
    
    total_creditos = creditos_periodo.count()
    total_prestado = creditos_periodo.aggregate(total=Sum('price'))['total'] or Decimal('0.00')
    total_earnings = creditos_periodo.aggregate(total=Sum('earnings'))['total'] or Decimal('0.00')
    
    print(f"📊 Total créditos otorgados: {total_creditos}")
    print(f"💵 Total prestado: {formato_moneda(total_prestado)}")
    print(f"💰 Total earnings esperados: {formato_moneda(total_earnings)}")
    
    # 2. ANÁLISIS DE PAGOS REALIZADOS
    print(f"\n2️⃣ PAGOS REALIZADOS EN EL PERÍODO")
    print("-" * 50)
    
    # Pagos de transacciones de ingreso
    pagos_periodo = AccountMethodAmount.objects.filter(
        transaction__transaction_type='income',
        transaction__date__date__range=[inicio_mayo, hoy],
        credit__isnull=False
    )
    
    total_pagado = pagos_periodo.aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
    total_transacciones = pagos_periodo.count()
    
    print(f"💰 Total pagado por clientes: {formato_moneda(total_pagado)}")
    print(f"📊 Total transacciones de pago: {total_transacciones}")
    
    # 3. ANÁLISIS DE CUMPLIMIENTO
    print(f"\n3️⃣ ANÁLISIS DE CUMPLIMIENTO")
    print("-" * 50)
    
    # Créditos con pagos
    creditos_con_pagos = creditos_periodo.filter(payments__isnull=False).distinct()
    creditos_sin_pagos = creditos_periodo.filter(payments__isnull=True)
    
    creditos_con_pagos_count = creditos_con_pagos.count()
    creditos_sin_pagos_count = creditos_sin_pagos.count()
    
    porcentaje_con_pagos = (creditos_con_pagos_count / total_creditos * 100) if total_creditos > 0 else 0
    porcentaje_sin_pagos = (creditos_sin_pagos_count / total_creditos * 100) if total_creditos > 0 else 0
    
    print(f"✅ Créditos con al menos 1 pago: {creditos_con_pagos_count} ({formato_porcentaje(porcentaje_con_pagos)})")
    print(f"❌ Créditos sin pagos: {creditos_sin_pagos_count} ({formato_porcentaje(porcentaje_sin_pagos)})")
    
    # 4. ANÁLISIS DE CUOTAS
    print(f"\n4️⃣ ANÁLISIS DE CUOTAS")
    print("-" * 50)
    
    cuotas_periodo = Installment.objects.filter(
        credit__created_at__date__range=[inicio_mayo, hoy]
    )
    
    total_cuotas = cuotas_periodo.count()
    cuotas_pagadas = cuotas_periodo.filter(paid=True).count()
    cuotas_pendientes = cuotas_periodo.filter(paid=False).count()
    cuotas_vencidas = cuotas_periodo.filter(
        paid=False,
        due_date__lt=hoy
    ).count()
    
    porcentaje_cuotas_pagadas = (cuotas_pagadas / total_cuotas * 100) if total_cuotas > 0 else 0
    porcentaje_cuotas_vencidas = (cuotas_vencidas / total_cuotas * 100) if total_cuotas > 0 else 0
    
    print(f"📊 Total cuotas generadas: {total_cuotas}")
    print(f"✅ Cuotas pagadas: {cuotas_pagadas} ({formato_porcentaje(porcentaje_cuotas_pagadas)})")
    print(f"⏳ Cuotas pendientes: {cuotas_pendientes}")
    print(f"🚨 Cuotas vencidas: {cuotas_vencidas} ({formato_porcentaje(porcentaje_cuotas_vencidas)})")
    
    # 5. ANÁLISIS MENSUAL DE PAGOS
    print(f"\n5️⃣ ANÁLISIS MENSUAL DE PAGOS")
    print("-" * 50)
    
    pagos_mensuales = pagos_periodo.annotate(
        mes=TruncMonth('transaction__date')
    ).values('mes').annotate(
        total_pagado=Sum('amount_paid'),
        total_transacciones=Count('id'),
        creditos_unicos=Count('credit', distinct=True)
    ).order_by('mes')
    
    for pago_mensual in pagos_mensuales:
        mes = pago_mensual['mes'].strftime('%B %Y')
        total = pago_mensual['total_pagado']
        transacciones = pago_mensual['total_transacciones']
        creditos = pago_mensual['creditos_unicos']
        
        print(f"📅 {mes}:")
        print(f"   💰 Total pagado: {formato_moneda(total)}")
        print(f"   📊 Transacciones: {transacciones}")
        print(f"   👥 Créditos únicos: {creditos}")
        print(f"   📈 Promedio por transacción: {formato_moneda(total/transacciones) if transacciones > 0 else '$0.00'}")
    
    # 6. ANÁLISIS DE MÉTODOS DE PAGO
    print(f"\n6️⃣ ANÁLISIS DE MÉTODOS DE PAGO")
    print("-" * 50)
    
    metodos_pago = pagos_periodo.values(
        'payment_method__name'
    ).annotate(
        total_pagado=Sum('amount_paid'),
        total_transacciones=Count('id')
    ).order_by('-total_pagado')
    
    total_por_metodos = sum(m['total_pagado'] for m in metodos_pago)
    
    for metodo in metodos_pago:
        nombre = metodo['payment_method__name']
        total = metodo['total_pagado']
        transacciones = metodo['total_transacciones']
        porcentaje = (total / total_por_metodos * 100) if total_por_metodos > 0 else 0
        
        print(f"💳 {nombre}:")
        print(f"   💰 Total: {formato_moneda(total)} ({formato_porcentaje(porcentaje)})")
        print(f"   📊 Transacciones: {transacciones}")
        print(f"   📈 Promedio: {formato_moneda(total/transacciones) if transacciones > 0 else '$0.00'}")
    
    # 7. ANÁLISIS DE MOROSIDAD
    print(f"\n7️⃣ ANÁLISIS DE MOROSIDAD")
    print("-" * 50)
    
    creditos_en_mora = creditos_periodo.filter(
        is_in_default=True
    )
    
    creditos_mora_count = creditos_en_mora.count()
    porcentaje_mora = (creditos_mora_count / total_creditos * 100) if total_creditos > 0 else 0
    
    print(f"🚨 Créditos en mora: {creditos_mora_count} ({formato_porcentaje(porcentaje_mora)})")
    
    # Análisis por nivel de morosidad
    niveles_mora = creditos_en_mora.values('morosidad_level').annotate(
        count=Count('id'),
        total_prestado=Sum('price'),
        total_pendiente=Sum('pending_amount')
    ).order_by('morosidad_level')
    
    for nivel in niveles_mora:
        level = nivel['morosidad_level']
        count = nivel['count']
        prestado = nivel['total_prestado']
        pendiente = nivel['total_pendiente']
        
        print(f"   📊 Nivel {level}: {count} créditos")
        print(f"      💵 Prestado: {formato_moneda(prestado)}")
        print(f"      ⏳ Pendiente: {formato_moneda(pendiente)}")
    
    # 8. ANÁLISIS DE TENDENCIAS SEMANALES
    print(f"\n8️⃣ ANÁLISIS DE TENDENCIAS SEMANALES")
    print("-" * 50)
    
    # Últimas 4 semanas
    for i in range(4):
        fin_semana = hoy - timedelta(days=i*7)
        inicio_semana = fin_semana - timedelta(days=6)
        
        pagos_semana = pagos_periodo.filter(
            transaction__date__date__range=[inicio_semana, fin_semana]
        )
        
        total_semana = pagos_semana.aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
        transacciones_semana = pagos_semana.count()
        
        print(f"📅 Semana {i+1} ({inicio_semana} a {fin_semana}):")
        print(f"   💰 Total pagado: {formato_moneda(total_semana)}")
        print(f"   📊 Transacciones: {transacciones_semana}")
    
    # 9. RESUMEN Y RECOMENDACIONES
    print(f"\n9️⃣ RESUMEN Y RECOMENDACIONES")
    print("-" * 50)
    
    # Tasa de recuperación
    tasa_recuperacion = (total_pagado / total_prestado * 100) if total_prestado > 0 else 0
    
    print(f"📊 TASA DE RECUPERACIÓN: {formato_porcentaje(tasa_recuperacion)}")
    print(f"💰 PENDIENTE POR COBRAR: {formato_moneda(total_prestado - total_pagado)}")
    
    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    
    if porcentaje_cuotas_vencidas > 10:
        print(f"   ⚠️ ALTA MOROSIDAD: {formato_porcentaje(porcentaje_cuotas_vencidas)} de cuotas vencidas")
        print(f"   🎯 Acción: Reforzar cobranza y seguimiento")
    
    if porcentaje_sin_pagos > 30:
        print(f"   ⚠️ BAJA PARTICIPACIÓN: {formato_porcentaje(porcentaje_sin_pagos)} sin pagos")
        print(f"   🎯 Acción: Revisar estrategia de colocación")
    
    if tasa_recuperacion < 50:
        print(f"   ⚠️ BAJA RECUPERACIÓN: {formato_porcentaje(tasa_recuperacion)}")
        print(f"   🎯 Acción: Optimizar procesos de cobranza")
    
    # Método de pago más popular
    if metodos_pago:
        metodo_popular = metodos_pago[0]
        print(f"   ✅ MÉTODO MÁS POPULAR: {metodo_popular['payment_method__name']}")
        print(f"   🎯 Acción: Fortalecer este canal de pago")
    
    return {
        'total_creditos': total_creditos,
        'total_prestado': total_prestado,
        'total_pagado': total_pagado,
        'tasa_recuperacion': tasa_recuperacion,
        'porcentaje_cuotas_vencidas': porcentaje_cuotas_vencidas,
        'creditos_en_mora': creditos_mora_count
    }

def analisis_detallado_creditos():
    """Análisis detallado de créditos específicos"""
    print(f"\n🔍 ANÁLISIS DETALLADO DE CRÉDITOS")
    print("=" * 60)
    
    hoy = timezone.now().date()
    inicio_mayo = date(2025, 5, 1)
    
    # Créditos con problemas de pago
    creditos_problema = Credit.objects.filter(
        created_at__date__range=[inicio_mayo, hoy],
        is_in_default=True
    ).select_related('user', 'seller').prefetch_related('payments', 'installments')
    
    print(f"🚨 CRÉDITOS CON PROBLEMAS DE PAGO: {creditos_problema.count()}")
    print("-" * 50)
    
    for i, credito in enumerate(creditos_problema[:10], 1):  # Mostrar solo los primeros 10
        pagos_credito = credito.payments.aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
        cuotas_pagadas = credito.installments.filter(paid=True).count()
        cuotas_vencidas = credito.installments.filter(paid=False, due_date__lt=hoy).count()
        
        print(f"{i}. Crédito {str(credito.uid)[:8]}...")
        print(f"   👤 Cliente: {credito.user.username}")
        print(f"   💰 Prestado: {formato_moneda(credito.price)}")
        print(f"   💵 Pagado: {formato_moneda(pagos_credito)}")
        print(f"   ⏳ Pendiente: {formato_moneda(credito.pending_amount)}")
        print(f"   📊 Cuotas pagadas: {cuotas_pagadas}")
        print(f"   🚨 Cuotas vencidas: {cuotas_vencidas}")
        print(f"   📈 Nivel mora: {credito.morosidad_level}")
        print()

def main():
    """Función principal"""
    print("🚀 ANÁLISIS RIGUROSO DE PAGOS DE CLIENTES")
    print("=" * 60)
    
    # Análisis principal
    resultados = analisis_pagos_periodo()
    
    # Análisis detallado
    analisis_detallado_creditos()
    
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 60)

if __name__ == "__main__":
    main()
