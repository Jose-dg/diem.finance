#!/usr/bin/env python3
"""
Script de Análisis Financiero
Responde las consultas:
1. Ganancias en mayo, junio, julio
2. Estado actual (cómo vamos)
3. Qué necesitamos para ganar $15,000 al mes
"""
import os
import sys
import django
from datetime import datetime, date
from decimal import Decimal

# Configurar Django
sys.path.append('/Users/ojeda/Documents/Dev/fintech')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.fintech.models import Credit, Transaction, AccountMethodAmount
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta

def formato_moneda(valor):
    """Formatea valores monetarios"""
    return f"${valor:,.2f}" if valor else "$0.00"

def analisis_mensual(mes, año):
    """Analiza las ganancias de un mes específico"""
    print(f"\n📅 ANÁLISIS {mes.upper()} {año}")
    print("=" * 50)
    
    # Definir fechas del mes
    if mes == "mayo":
        start_date = date(año, 5, 1)
        end_date = date(año, 5, 31)
    elif mes == "junio":
        start_date = date(año, 6, 1)
        end_date = date(año, 6, 30)
    elif mes == "julio":
        start_date = date(año, 7, 1)
        end_date = date(año, 7, 31)
    else:
        print(f"❌ Mes no válido: {mes}")
        return None
    
    # Consultar créditos del mes
    creditos_mes = Credit.objects.filter(
        created_at__date__range=[start_date, end_date]
    )
    
    # Métricas básicas
    total_creditos = creditos_mes.count()
    total_earnings = creditos_mes.aggregate(total=Sum('earnings'))['total'] or Decimal('0.00')
    total_prestado = creditos_mes.aggregate(total=Sum('price'))['total'] or Decimal('0.00')
    total_costo = creditos_mes.aggregate(total=Sum('cost'))['total'] or Decimal('0.00')
    
    # Promedios
    promedio_earnings = total_earnings / total_creditos if total_creditos > 0 else Decimal('0.00')
    promedio_prestado = total_prestado / total_creditos if total_creditos > 0 else Decimal('0.00')
    
    # Margen de ganancia
    margen_ganancia = (total_earnings / total_prestado * 100) if total_prestado > 0 else 0
    
    print(f"💰 GANANCIAS TOTALES: {formato_moneda(total_earnings)}")
    print(f"📊 CRÉDITOS OTORGADOS: {total_creditos}")
    print(f"💵 TOTAL PRESTADO: {formato_moneda(total_prestado)}")
    print(f"💸 TOTAL COSTO: {formato_moneda(total_costo)}")
    print(f"📈 PROMEDIO POR CRÉDITO: {formato_moneda(promedio_earnings)}")
    print(f"📊 PROMEDIO PRESTADO: {formato_moneda(promedio_prestado)}")
    print(f"🎯 MARGEN DE GANANCIA: {margen_ganancia:.2f}%")
    
    # Análisis por estado
    estados = creditos_mes.values('state').annotate(
        count=Count('id'),
        earnings=Sum('earnings')
    )
    
    print(f"\n📋 ANÁLISIS POR ESTADO:")
    for estado in estados:
        print(f"   • {estado['state']}: {estado['count']} créditos - {formato_moneda(estado['earnings'])}")
    
    return {
        'total_earnings': total_earnings,
        'total_creditos': total_creditos,
        'promedio_earnings': promedio_earnings,
        'margen_ganancia': margen_ganancia
    }

def estado_actual():
    """Analiza el estado actual del negocio"""
    print(f"\n🎯 ESTADO ACTUAL - CÓMO VAMOS")
    print("=" * 50)
    
    # Fecha actual
    hoy = timezone.now().date()
    mes_actual = hoy.month
    año_actual = hoy.year
    
    # Mes actual
    if mes_actual == 1:
        start_mes = date(año_actual, 1, 1)
        end_mes = date(año_actual, 1, 31)
    elif mes_actual == 2:
        start_mes = date(año_actual, 2, 1)
        end_mes = date(año_actual, 2, 28) if año_actual % 4 != 0 else date(año_actual, 2, 29)
    elif mes_actual == 3:
        start_mes = date(año_actual, 3, 1)
        end_mes = date(año_actual, 3, 31)
    elif mes_actual == 4:
        start_mes = date(año_actual, 4, 1)
        end_mes = date(año_actual, 4, 30)
    elif mes_actual == 5:
        start_mes = date(año_actual, 5, 1)
        end_mes = date(año_actual, 5, 31)
    elif mes_actual == 6:
        start_mes = date(año_actual, 6, 1)
        end_mes = date(año_actual, 6, 30)
    elif mes_actual == 7:
        start_mes = date(año_actual, 7, 1)
        end_mes = date(año_actual, 7, 31)
    elif mes_actual == 8:
        start_mes = date(año_actual, 8, 1)
        end_mes = date(año_actual, 8, 31)
    elif mes_actual == 9:
        start_mes = date(año_actual, 9, 1)
        end_mes = date(año_actual, 9, 30)
    elif mes_actual == 10:
        start_mes = date(año_actual, 10, 1)
        end_mes = date(año_actual, 10, 31)
    elif mes_actual == 11:
        start_mes = date(año_actual, 11, 1)
        end_mes = date(año_actual, 11, 30)
    else:  # diciembre
        start_mes = date(año_actual, 12, 1)
        end_mes = date(año_actual, 12, 31)
    
    # Créditos del mes actual
    creditos_mes_actual = Credit.objects.filter(
        created_at__date__range=[start_mes, hoy]
    )
    
    earnings_mes_actual = creditos_mes_actual.aggregate(total=Sum('earnings'))['total'] or Decimal('0.00')
    creditos_mes_actual_count = creditos_mes_actual.count()
    
    # Proyección del mes
    dias_transcurridos = (hoy - start_mes).days + 1
    dias_mes = (end_mes - start_mes).days + 1
    porcentaje_mes = (dias_transcurridos / dias_mes) * 100
    
    if porcentaje_mes > 0:
        proyeccion_mes = earnings_mes_actual / Decimal(str(porcentaje_mes / 100))
    else:
        proyeccion_mes = Decimal('0.00')
    
    # Comparación con meses anteriores
    mes_anterior = mes_actual - 1 if mes_actual > 1 else 12
    año_mes_anterior = año_actual if mes_actual > 1 else año_actual - 1
    
    if mes_anterior == 1:
        start_mes_anterior = date(año_mes_anterior, 1, 1)
        end_mes_anterior = date(año_mes_anterior, 1, 31)
    elif mes_anterior == 2:
        start_mes_anterior = date(año_mes_anterior, 2, 1)
        end_mes_anterior = date(año_mes_anterior, 2, 28) if año_mes_anterior % 4 != 0 else date(año_mes_anterior, 2, 29)
    elif mes_anterior == 3:
        start_mes_anterior = date(año_mes_anterior, 3, 1)
        end_mes_anterior = date(año_mes_anterior, 3, 31)
    elif mes_anterior == 4:
        start_mes_anterior = date(año_mes_anterior, 4, 1)
        end_mes_anterior = date(año_mes_anterior, 4, 30)
    elif mes_anterior == 5:
        start_mes_anterior = date(año_mes_anterior, 5, 1)
        end_mes_anterior = date(año_mes_anterior, 5, 31)
    elif mes_anterior == 6:
        start_mes_anterior = date(año_mes_anterior, 6, 1)
        end_mes_anterior = date(año_mes_anterior, 6, 30)
    elif mes_anterior == 7:
        start_mes_anterior = date(año_mes_anterior, 7, 1)
        end_mes_anterior = date(año_mes_anterior, 7, 31)
    elif mes_anterior == 8:
        start_mes_anterior = date(año_mes_anterior, 8, 1)
        end_mes_anterior = date(año_mes_anterior, 8, 31)
    elif mes_anterior == 9:
        start_mes_anterior = date(año_mes_anterior, 9, 1)
        end_mes_anterior = date(año_mes_anterior, 9, 30)
    elif mes_anterior == 10:
        start_mes_anterior = date(año_mes_anterior, 10, 1)
        end_mes_anterior = date(año_mes_anterior, 10, 31)
    elif mes_anterior == 11:
        start_mes_anterior = date(año_mes_anterior, 11, 1)
        end_mes_anterior = date(año_mes_anterior, 11, 30)
    else:  # diciembre
        start_mes_anterior = date(año_mes_anterior, 12, 1)
        end_mes_anterior = date(año_mes_anterior, 12, 31)
    
    earnings_mes_anterior = Credit.objects.filter(
        created_at__date__range=[start_mes_anterior, end_mes_anterior]
    ).aggregate(total=Sum('earnings'))['total'] or Decimal('0.00')
    
    # Variación
    if earnings_mes_anterior > 0:
        variacion = float(((earnings_mes_actual - earnings_mes_anterior) / earnings_mes_anterior) * 100)
    else:
        variacion = 0
    
    print(f"📅 MES ACTUAL: {mes_actual}/{año_actual}")
    print(f"💰 GANANCIAS ACUMULADAS: {formato_moneda(earnings_mes_actual)}")
    print(f"📊 CRÉDITOS OTORGADOS: {creditos_mes_actual_count}")
    print(f"📈 PROGRESO DEL MES: {porcentaje_mes:.1f}% ({dias_transcurridos}/{dias_mes} días)")
    print(f"🎯 PROYECCIÓN MENSUAL: {formato_moneda(proyeccion_mes)}")
    print(f"📊 MES ANTERIOR: {formato_moneda(earnings_mes_anterior)}")
    print(f"🔄 VARIACIÓN: {variacion:+.2f}%")
    
    # Estado general
    if variacion > 10:
        estado = "🚀 CRECIENDO FUERTE"
    elif variacion > 0:
        estado = "📈 CRECIENDO"
    elif variacion > -10:
        estado = "➡️ ESTABLE"
    else:
        estado = "📉 DECRECIENDO"
    
    print(f"🎯 ESTADO: {estado}")
    
    return {
        'earnings_mes_actual': earnings_mes_actual,
        'proyeccion_mes': proyeccion_mes,
        'variacion': variacion,
        'estado': estado
    }

def analisis_objetivo_15000():
    """Analiza qué necesitamos para ganar $15,000 al mes"""
    print(f"\n🎯 ANÁLISIS: OBJETIVO $15,000/MES")
    print("=" * 50)
    
    objetivo_mensual = Decimal('15000.00')
    
    # Obtener datos históricos de los últimos 6 meses
    hoy = timezone.now().date()
    seis_meses_atras = hoy - timedelta(days=180)
    
    creditos_historicos = Credit.objects.filter(
        created_at__date__range=[seis_meses_atras, hoy]
    )
    
    # Métricas históricas
    total_earnings_historico = creditos_historicos.aggregate(total=Sum('earnings'))['total'] or Decimal('0.00')
    total_creditos_historico = creditos_historicos.count()
    promedio_earnings_historico = total_earnings_historico / 6  # 6 meses
    promedio_creditos_mes = total_creditos_historico / 6
    
    print(f"📊 DATOS HISTÓRICOS (Últimos 6 meses):")
    print(f"   • Ganancias totales: {formato_moneda(total_earnings_historico)}")
    print(f"   • Promedio mensual: {formato_moneda(promedio_earnings_historico)}")
    print(f"   • Créditos totales: {total_creditos_historico}")
    print(f"   • Promedio créditos/mes: {promedio_creditos_mes:.1f}")
    
    # Análisis de brecha
    brecha = objetivo_mensual - promedio_earnings_historico
    porcentaje_incremento = float((brecha / promedio_earnings_historico * 100)) if promedio_earnings_historico > 0 else 0
    
    print(f"\n🎯 ANÁLISIS DE BRECHA:")
    print(f"   • Objetivo mensual: {formato_moneda(objetivo_mensual)}")
    print(f"   • Promedio actual: {formato_moneda(promedio_earnings_historico)}")
    print(f"   • Brecha: {formato_moneda(brecha)}")
    print(f"   • Incremento necesario: {porcentaje_incremento:+.2f}%")
    
    # Estrategias para alcanzar el objetivo
    print(f"\n💡 ESTRATEGIAS PARA ALCANZAR $15,000/MES:")
    
    # Estrategia 1: Aumentar número de créditos
    if promedio_earnings_historico > 0:
        creditos_necesarios = objetivo_mensual / (promedio_earnings_historico / Decimal(str(promedio_creditos_mes)))
        creditos_adicionales = creditos_necesarios - Decimal(str(promedio_creditos_mes))
        print(f"   1️⃣ AUMENTAR VOLUMEN:")
        print(f"      • Créditos actuales/mes: {promedio_creditos_mes:.1f}")
        print(f"      • Créditos necesarios/mes: {float(creditos_necesarios):.1f}")
        print(f"      • Créditos adicionales necesarios: {float(creditos_adicionales):.1f}")
    
    # Estrategia 2: Aumentar margen por crédito
    promedio_earnings_por_credito = promedio_earnings_historico / Decimal(str(promedio_creditos_mes)) if promedio_creditos_mes > 0 else Decimal('0.00')
    earnings_por_credito_necesario = objetivo_mensual / Decimal(str(promedio_creditos_mes)) if promedio_creditos_mes > 0 else Decimal('0.00')
    incremento_por_credito = earnings_por_credito_necesario - promedio_earnings_por_credito
    
    print(f"\n   2️⃣ AUMENTAR MARGEN POR CRÉDITO:")
    print(f"      • Earnings actual/credito: {formato_moneda(promedio_earnings_por_credito)}")
    print(f"      • Earnings necesario/credito: {formato_moneda(earnings_por_credito_necesario)}")
    print(f"      • Incremento necesario/credito: {formato_moneda(incremento_por_credito)}")
    
    # Estrategia 3: Combinación
    print(f"\n   3️⃣ ESTRATEGIA COMBINADA:")
    print(f"      • Mantener {promedio_creditos_mes:.1f} créditos/mes")
    print(f"      • Aumentar earnings/credito a {formato_moneda(earnings_por_credito_necesario)}")
    print(f"      • O aumentar a {float(creditos_necesarios):.1f} créditos/mes")
    print(f"      • Manteniendo earnings/credito actual")
    
    # Recomendación
    print(f"\n🎯 RECOMENDACIÓN:")
    if brecha > 0:
        if porcentaje_incremento < 50:
            print(f"   ✅ El objetivo es alcanzable con un incremento moderado")
            print(f"   📈 Enfoque recomendado: Estrategia combinada")
        else:
            print(f"   ⚠️ El objetivo requiere un incremento significativo")
            print(f"   🚀 Enfoque recomendado: Aumentar volumen de créditos")
    else:
        print(f"   🎉 ¡Ya superas el objetivo! Mantén el ritmo actual")
    
    return {
        'objetivo_mensual': objetivo_mensual,
        'promedio_actual': promedio_earnings_historico,
        'brecha': brecha,
        'porcentaje_incremento': porcentaje_incremento,
        'creditos_necesarios': creditos_necesarios if 'creditos_necesarios' in locals() else Decimal('0.00'),
        'earnings_por_credito_necesario': earnings_por_credito_necesario
    }

def main():
    """Función principal"""
    print("🚀 ANÁLISIS FINANCIERO COMPLETO")
    print("=" * 60)
    
    # 1. Análisis mensual (mayo, junio, julio)
    print("\n1️⃣ CONSULTA: GANANCIAS EN MAYO, JUNIO, JULIO")
    print("=" * 60)
    
    año_actual = timezone.now().year
    meses_analisis = ["mayo", "junio", "julio"]
    resultados_mensuales = {}
    
    for mes in meses_analisis:
        resultado = analisis_mensual(mes, año_actual)
        if resultado:
            resultados_mensuales[mes] = resultado
    
    # Resumen de los 3 meses
    if resultados_mensuales:
        total_3_meses = sum(r['total_earnings'] for r in resultados_mensuales.values())
        promedio_3_meses = total_3_meses / 3
        print(f"\n📊 RESUMEN 3 MESES:")
        print(f"   • Total ganancias: {formato_moneda(total_3_meses)}")
        print(f"   • Promedio mensual: {formato_moneda(promedio_3_meses)}")
    
    # 2. Estado actual
    print("\n2️⃣ CONSULTA: CÓMO VAMOS")
    print("=" * 60)
    estado_actual()
    
    # 3. Análisis objetivo $15,000
    print("\n3️⃣ CONSULTA: OBJETIVO $15,000/MES")
    print("=" * 60)
    analisis_objetivo_15000()
    
    print(f"\n✅ ANÁLISIS COMPLETADO")
    print("=" * 60)

if __name__ == "__main__":
    main()
