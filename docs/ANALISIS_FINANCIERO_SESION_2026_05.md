# Análisis Financiero — Sesión Mayo 2026

Documento de referencia para continuar el análisis financiero en sesiones futuras.
Registra las consultas realizadas, su propósito, los hallazgos y las preguntas pendientes.

---

## Contexto de la sesión

**Fecha:** 8–9 mayo 2026  
**Objetivo:** Determinar cuánto puede tomar la empresa de sus beneficios para pagar gastos fijos, analizando primero la empresa completa y luego al vendedor Héctor (Seller ID=2, username=HectorAA) que representa el **87.4% de los créditos y el 84% del capital**.

---

## 1. Modelos clave consultados

### Campos relevantes de `Credit`
```python
state         # 'pending' = activo, 'completed' = pagado, 'to_solve' = en resolución
cost          # capital desembolsado al cliente
price         # total a cobrar (capital + interés)
earnings      # ganancia pura (price - cost)
total_abonos  # total recaudado hasta hoy en ese crédito
pending_amount # saldo pendiente real (price - total_abonos)
is_in_default # booleano: está en mora
morosidad_level # 'none','on_time','mild_default','moderate_default',
                #  'severe_default','recurrent_default','critical_default'
interest       # tasa de interés (mensual, varía por crédito)
credit_days    # plazo del crédito en días (promedio ~33 días)
installment_number # número total de cuotas
installment_value  # valor por cuota (monto fijo)
seller         # FK a Seller
```

### Campos relevantes de `AccountMethodAmount` (AMA)
```python
amount       # monto del pago
amount_paid  # monto efectivamente pagado
credit       # FK directo a Credit  ← clave para filtrar por seller
transaction  # FK a Transaction
```

### Relaciones críticas para los filtros
```python
# Cobros de un vendedor (via AMA → credit → seller)
AccountMethodAmount.objects.filter(
    credit__seller=hector,
    transaction__transaction_type='income',
    transaction__date__gte=fecha_inicio
)

# Desembolsos de un vendedor (directamente en Credit)
Credit.objects.filter(
    seller=hector,
    created_at__date__gte=fecha_inicio
)
```

> **Gotcha:** `Transaction` NO tiene FK directo a `Credit`. El camino correcto es
> `AccountMethodAmount → credit → seller`, no `Transaction → credit`.

---

## 2. Consultas realizadas y su propósito

### 2.1 Cartera por estado
```python
Credit.objects.values('state').annotate(
    n=Count('id'),
    capital=Sum('cost'),
    precio=Sum('price'),
    pendiente=Sum('pending_amount'),
    abonado=Sum('total_abonos')
).order_by('state')
```
**Para qué sirve:** Visión macro del portafolio. Los tres estados activos son:
- `pending` = cartera viva (1,419 créditos empresa / 1,252 Héctor)
- `to_solve` = créditos en resolución o castigo (165 empresa / 127 Héctor)
- `completed` = pagados en su totalidad

---

### 2.2 Morosidad en cartera activa
```python
activos = Credit.objects.filter(seller=hector, state='pending')
mora = activos.filter(is_in_default=True).aggregate(
    n=Count('id'), capital=Sum('cost'), pendiente=Sum('pending_amount')
)
```
**Para qué sirve:** Medir la calidad real del portafolio. Con Héctor:
- **46.9%** de créditos en mora por volumen
- **66.4%** del saldo pendiente en mora

---

### 2.3 Niveles de morosidad
```python
activos.values('morosidad_level').annotate(
    n=Count('id'), pendiente=Sum('pending_amount'), capital=Sum('cost')
).order_by('morosidad_level')
```
**Para qué sirve:** Clasificar la mora por severidad para priorizar cobranza.
El nivel más grave es `critical_default` (502 créditos de Héctor, $60,864 pendiente).

---

### 2.4 Flujos mensuales — cobros vs desembolsos
```python
# Cobros mensuales
AccountMethodAmount.objects.filter(
    credit__seller=hector,
    transaction__transaction_type='income',
    transaction__date__gte=hace_12_meses
).annotate(mes=TruncMonth('transaction__date')).values('mes').annotate(
    total=Sum('amount'), n=Count('id')
).order_by('mes')

# Desembolsos mensuales
Credit.objects.filter(
    seller=hector, created_at__date__gte=hace_12_meses
).annotate(mes=TruncMonth('created_at')).values('mes').annotate(
    capital=Sum('cost'), n=Count('id')
).order_by('mes')
```
**Para qué sirve:** Calcular el **spread bruto mensual** (cobros − desembolsos).
Este es el único ingreso real neto antes de provisiones.

**Hallazgo Héctor (12 meses):**
- Cobros/mes prom: **$13,743**
- Desembolsos/mes prom: **$10,090**
- Spread bruto: **$3,652/mes**

**Hallazgo Héctor (2026 ene–abr):**
- Cobros/mes prom: **$11,881**
- Desembolsos/mes prom: **$7,815**
- Spread bruto: **$4,066/mes**

---

### 2.5 Discriminar cobros por vintage (nuevo vs legado)
```python
# Cobros de créditos creados en 2026
AccountMethodAmount.objects.filter(
    credit__seller=hector,
    credit__created_at__date__gte=inicio_2026,
    transaction__transaction_type='income',
    transaction__date__gte=inicio_2026
).annotate(mes=TruncMonth('transaction__date'))...

# Cobros de créditos legado (pre-2026)
AccountMethodAmount.objects.filter(
    credit__seller=hector,
    credit__created_at__date__lt=inicio_2026,
    transaction__transaction_type='income',
    transaction__date__gte=inicio_2026
)...
```
**Para qué sirve:** Entender de dónde vienen los cobros. Hallazgo clave:
- Enero 2026: 76% cobros venían del legado pre-2026
- Abril 2026: 90% ya son de créditos nuevos 2026
- **El portafolio sano pre-2026 se agotó.** Lo que queda del legado son los defaulters.

---

### 2.6 Tendencia de colocación con ticket y máximo
```python
Credit.objects.filter(seller=hector, created_at__date__gte=inicio).annotate(
    mes=TruncMonth('created_at')
).values('mes').annotate(
    capital=Sum('cost'), n=Count('id'),
    ticket_prom=Avg('cost'),
    ticket_max=Max('cost'),
).order_by('mes')
```
**Para qué sirve:** Detectar cambios en el comportamiento de colocación.

**Hallazgo crítico:**
- Hasta mayo 2025: ticket máximo $4,000
- Junio 2025 en adelante: ticket máximo cayó a $500–$1,000
- Diciembre 2025 en adelante: techo fijo en **$500**
- Volumen también cayó: de 120 créditos/mes → 44 créditos/mes

Esto explica directamente la caída en cobros (lag ~1 mes por plazo promedio de 33 días).

---

### 2.7 Ratio cobros/colocación por mes
**Fórmula:** `cobros_mes / desembolsos_mes × 100`

**Para qué sirve:** Si el ratio es consistentemente >100%, el portafolio se está **encogiendo** (se cobra más de lo que se coloca).

**Hallazgo:** Ratio de Héctor siempre >100% desde 2025, llegando a 172% en marzo 2026.
Contracción acumulada 2025+2026: **$62,928** de capital salido.

---

### 2.8 Estructura de cuotas
```python
Credit.objects.filter(seller=hector, state='pending').values(
    'installment_number'
).annotate(
    n=Count('id'),
    capital_prom=Avg('cost'),
    cuota_prom=Avg('installment_value'),
    dias_prom=Avg('credit_days'),
    pendiente_prom=Avg('pending_amount'),
)
```
**Para qué sirve:** Entender la estructura de pagos del portafolio para calcular
qué capital se necesita para alcanzar una meta de cobro.

**Hallazgo — distribución dominante de Héctor:**
| Cuotas | Créditos | Capital prom | Cuota prom | Días/cuota | Frecuencia |
|--------|----------|-------------|------------|------------|------------|
| 1      | 104      | $98         | $147       | 29 días    | Mensual    |
| **2**  | **545**  | **$111**    | **$81**    | **15 días**| **Quincenal** ← dominante |
| 3      | 158      | $178        | $98        | 15 días    | Quincenal  |
| 4      | 92       | $244        | $95        | 12 días    | Cada 12d   |
| 5      | 73       | $175        | $50        | 7 días     | Semanal    |
| 30     | 109      | $254        | $11        | 1 día      | Diario     |

---

### 2.9 Pérdida esperada (provisión técnica)
**Fórmula:** `Capital × PD × LGD`
- **PD** (Probability of Default) = tasa mora histórica de Héctor = **46.9%**
- **LGD** (Loss Given Default) = porcentaje no recuperable = **65%** (conservador para cartera informal)

```python
# Sobre créditos 2026 únicamente
capital_2026 = Credit.objects.filter(
    seller=hector, created_at__date__gte=inicio_2026, state='pending'
).aggregate(total=Sum('cost'))['total']

perdida_esperada = capital_2026 * Decimal('0.469') * Decimal('0.65')
provision_mensual = perdida_esperada / 18  # absorbida en 18 meses
```

---

## 3. Hallazgos principales

### Empresa completa
| Indicador | Valor |
|-----------|-------|
| Créditos activos | 1,419 |
| Capital desplegado | $262,275 |
| Saldo pendiente | $144,120 |
| Tasa mora (volumen) | 43.6% |
| Tasa mora (monto) | 50.3% |
| Spread bruto/mes | $2,721 |
| Spread tras provisiones | **~$0** (negativo técnicamente) |

### Héctor (2026)
| Indicador | Valor |
|-----------|-------|
| Participación en empresa | 87.4% créditos, 84% capital |
| Spread bruto/mes (2026) | $4,066 |
| Tasa mora (volumen) | 46.9% |
| Tasa mora (monto) | 66.4% |
| Critical default | 502 créditos, $60,864 pendiente |
| Máximo viable gastos fijos | **$2,500–$2,800/mes** |

---

## 4. Pregunta pendiente al momento de cortar sesión

**¿Cuánto capital necesita Héctor para recaudar $20,000 por quincena con 80% de tasa de pago?**

### Fórmula base (modelo 2 cuotas quincenal, producto dominante)
```
Créditos activos necesarios = Meta_quincena / tasa_pago / cuota_promedio
Capital necesario           = Créditos_necesarios × capital_promedio

= ($20,000 / 0.80 / $81) × $111
= 309 créditos × $111
= ~$34,300 en capital
```

### Lógica de la fórmula
- En un portafolio de 2-cuotas quincenales, **cada crédito activo genera 1 pago de $81 por quincena**.
- Con 80% de pago: de cada 10 créditos, 8 pagan → necesitas tener 309 activos para que 247 paguen → 247 × $81 = $20,007.
- Capital que respalda esos 309 créditos: 309 × $111 = $34,299.

### Tabla de sensibilidad (modelo 2-cuota quincenal, cuota $81, capital $111)
| Meta/quincena | 70% pago | 75% pago | **80% pago** | 85% pago |
|---------------|----------|----------|------------|----------|
| $10,000       | $19,712  | $18,400  | $17,222    | $16,209  |
| $15,000       | $29,568  | $27,600  | $25,833    | $24,314  |
| **$20,000**   | $39,424  | $36,800  | **$34,444**| $32,418  |
| $25,000       | $49,280  | $46,000  | $43,056    | $40,523  |
| $30,000       | $59,136  | $55,200  | $51,667    | $48,627  |

> **Nota:** Esta tabla usa el producto dominante (2 cuotas, $81/cuota, $111 capital prom).
> Para el mix real del portafolio de Héctor, el capital puede variar ±15% según la composición.
> El siguiente paso era calcular el capital ponderado por el mix completo de cuotas.

---

## 5. Lo que falta calcular (próxima sesión)

1. **Capital ponderado por mix de cuotas:** calcular el capital necesario usando todos los grupos (no solo el de 2 cuotas), ponderado por número de créditos actuales de Héctor.

2. **Créditos críticos recuperables:** de los 502 en `critical_default`, filtrar por monto bajo y menor antigüedad en mora para priorizar cobranza. Recuperar $15,000 de mora crítica duplicaría la capacidad de colocación actual.

3. **Simulación de crecimiento:** si Héctor vuelve a colocar $15,000–20,000/mes (vs. $7,215 en abril), proyectar cuándo los cobros llegan a $20,000/quincena y qué capital inicial se necesita para arrancar.

4. **Modelo de interés sobre morosos:** la mención del usuario sobre "aplicar intereses a los que están quedos" — entender cómo está modelado en `CreditAdjustment` o `Adjustment` y si ya hay lógica en `apply_additional_interest`.

---

## 6. Herramientas del sistema útiles para este análisis

```bash
# Recalcular todos los créditos (saldos, morosidad)
python manage.py recalcular_todos_creditos

# Actualizar niveles de morosidad
python manage.py update_morosidad

# Aplicar interés adicional a morosos
python manage.py apply_additional_interest

# Diagnóstico de inconsistencias
python manage.py diagnosticar_creditos
```

**Servicios de insights relevantes:**
- `apps/insights/services/financial_control_service.py` — métricas de mora, defaulters, alertas
- `apps/insights/services/dashboard_service.py` — KPIs ejecutivos, cobros, cartera
- `apps/insights/services/credit_analysis_service.py` — análisis por crédito/cliente

**Seller de Héctor:**
```python
from apps.fintech.models import Seller
hector = Seller.objects.get(id=2)  # username=HectorAA, user_id=610
```
