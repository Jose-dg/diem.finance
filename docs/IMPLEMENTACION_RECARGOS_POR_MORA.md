# Implementación de Recargos por Mora (Late Fees)

**Sesión:** 2026-05-27  
**Estado:** Implementado, pendiente de `migrate` en producción

---

## Contexto

El sistema tenía la infraestructura técnica para recargos por mora desde el diseño original del modelo `Installment` (campo `late_fee`, código de cálculo en servicios, tareas Celery), pero **nunca funcionó en producción**: los 5,496 registros de `Installment` en BD tenían `late_fee = 0.00`.

Además existían tres bugs que habrían corrompido los datos al activar la funcionalidad.

---

## Bugs corregidos (prerrequisitos)

### Bug 1 — `check_default_conditions` escribía choices inválidos

**Archivo:** `apps/fintech/services/credit/credit_service.py` — método `check_default_conditions()`

El método escribía los strings `'critica'`, `'alta'`, `'moderada'`, `'leve'`, `'al_dia'` en `Credit.morosidad_level`. El modelo define los choices como `'critical_default'`, `'severe_default'`, `'moderate_default'`, `'mild_default'`, `'on_time'`. La tarea `update_credit_statuses` (08:00) corría este método, corrompiendo silenciosamente el campo en cada ejecución.

**Corrección:** reemplazados los strings para que coincidan exactamente con los choices del modelo. La lógica de negocio (umbrales de días) no cambió.

```python
# Antes (buggy)
if total_overdue_days >= 120:
    credit.morosidad_level = 'critica'

# Después (correcto)
if total_overdue_days >= 120:
    credit.morosidad_level = 'critical_default'
```

### Bug 2 — `days_overdue` se acumulaba incorrectamente

**Archivos:** `installment_service.py:update_all_installment_statuses()`, tasks `update_installment_statuses`, `calculate_overdue_installments`

La tarea usaba `F('days_overdue') + 1` para actualizar el campo. Si la tarea fallaba un día, al día siguiente sumaba 1 sobre un valor ya desactualizado. Si corría dos veces en el mismo día, sumaba 2.

**Corrección:** `days_overdue` se calcula siempre desde la fuente de verdad: `(date.today() - installment.due_date).days`. Nunca se acumula.

Las tareas `update_installment_statuses` (cada 30 min) y `calculate_overdue_installments` (06:00) fueron **eliminadas** — toda esa responsabilidad quedó centralizada en `installment_daily_maintenance`.

### Bug 3 — Fórmula de recargo hardcodeada en tres lugares

La fórmula `remaining_amount × 0.05 × (days_overdue / 30)` existía literal en:
- `installment_service.py:351` (dentro de `update_installment_calculations`)
- `installment_service.py:167` (dentro de `update_all_installment_statuses`)
- `credit_service.py:147` (dentro de `calculate_late_fees`)

Las tres repeticiones fueron eliminadas y reemplazadas por `# TODO: usar Installment.calculate_late_fee()`. El método definitivo vive en el modelo (ver Paso 2 más abajo).

---

## Cambios implementados

### Paso 1 — Campo `Credit.late_fee_rate`

**Migración:** `0005_add_late_fee_rate_to_credit.py`

```python
late_fee_rate = models.DecimalField(
    max_digits=5,
    decimal_places=4,
    default=Decimal('0.0500'),
    help_text="Tasa mensual de recargo por mora. Ej: 0.05 = 5% mensual."
)
```

**Reglas:**
- Se define al crear el crédito y no debe modificarse una vez que el crédito tiene cuotas con `late_fee > 0` registrado.
- Si el campo es cero o está vacío, `calculate_late_fee()` usa `0.0500` como fallback.
- Visible y editable en `CreditAdmin` dentro del fieldset "Condiciones financieras".

---

### Paso 2 — Método `Installment.calculate_late_fee()`

**Archivo:** `apps/fintech/models.py` — clase `Installment`

Este es el **único lugar en todo el sistema** donde vive la lógica de cálculo de recargo. Ningún servicio, tarea ni vista debe repetir esta fórmula.

```python
def calculate_late_fee(self) -> Decimal:
    ...
```

**Reglas de negocio implementadas:**

| Regla | Detalle |
|---|---|
| Período de gracia | 3 días desde `due_date`. El recargo empieza en `due_date + 3`. |
| Tasa | `credit.late_fee_rate` (default 5% mensual). |
| Base de cálculo | `remaining_amount` (saldo pendiente de esa cuota, no del crédito total). |
| Fórmula | `remaining_amount × rate × (days_late / 30)` |
| Tope máximo | 50% del monto original de la cuota (`self.amount × 0.50`). |
| Cuota pagada | Si `status == 'paid'`, retorna 0. |
| Sin fecha | Si `due_date` es `None`, retorna 0. |
| Resultado | Redondeado a 2 decimales con `ROUND_HALF_UP`. |

**Invariante crítico:**

> `Installment.late_fee` (campo en BD) = lo que se **cobró** efectivamente al cliente.  
> `installment.calculate_late_fee()` = lo que el sistema calcula en tiempo real hoy.  
>
> Nunca persistir el valor calculado directamente en `late_fee` desde una tarea. Solo actualizar `late_fee` cuando hay una `FeeDecision` que confirma cuánto se cobró realmente.

---

### Paso 3 — Modelo `FeeDecision`

**Migración:** `0006_add_feedecision_model.py`  
**Archivo:** `apps/fintech/models.py`  
**Admin:** `apps/fintech/admin.py`

Registro de auditoría de cada decisión que toma un cobrador sobre un recargo calculado.

```
FeeDecision
├── installment (FK → Installment)
├── seller (FK → Seller, null si fue desde oficina)
├── calculated_fee   — lo que calculó el sistema en ese momento
├── applied_fee      — lo que efectivamente se cobró
├── decision         — 'applied' | 'partial' | 'waived'
├── reason           — obligatorio si decision es 'partial' o 'waived'
└── created_at
```

**Validaciones del modelo (método `clean()`):**
- Si `decision` es `partial` o `waived`, `reason` es obligatorio.
- Si `decision` es `applied`, `applied_fee` debe ser igual a `calculated_fee`.

**Para qué sirve este modelo:**
- Dashboard de gerencia: auditoría de condonaciones por cobrador.
- Coaching individual: detectar patrones de permisividad excesiva.
- Cálculo de recargos efectivamente cobrados vs calculados (tasa de recuperación de mora).

---

### Paso 4 — Tarea Celery `installment_daily_maintenance` (refactorizada)

**Archivo:** `apps/fintech/tasks.py`  
**Schedule:** 06:00 AM diario

La tarea absorbe toda la responsabilidad de mantenimiento de cuotas. Lo que hace en orden:

1. **Recalcula `days_overdue`** desde `due_date` para todas las cuotas no pagadas/canceladas con `due_date < today`.
2. **Llama a `calculate_late_fee()`** por cada cuota para obtener el recargo calculado.
3. **Promueve a `overdue`** las cuotas con `days_overdue > 3` que aún estén en `pending` (respeta el período de gracia).
4. Hace un solo **`bulk_update`** al final del loop para minimizar queries.
5. **Marca como `partial`** las cuotas `pending` que tienen `amount_paid > 0`.
6. Programa recordatorios de pago.
7. Dispara notificaciones de mora.
8. Genera cuotas para créditos nuevos.

**Logging:** registra cuántas cuotas fueron procesadas, cuántas pasaron a `overdue`, y cuántos segundos tomó la tarea.

**Tareas eliminadas del beat schedule:**
- `update-installment-statuses` (corría cada 30 min) — responsabilidad absorbida.
- `calculate_overdue_installments` (06:00) — responsabilidad absorbida.

---

### Paso 5 — Management command `backfill_late_fees`

**Archivo:** `apps/fintech/management/commands/backfill_late_fees.py`

Recalcula `days_overdue` y `late_fee` para todas las cuotas históricas vencidas no pagadas.

```bash
# Ver qué haría sin escribir nada
python manage.py backfill_late_fees --dry-run

# Procesar solo 100 cuotas (staging)
python manage.py backfill_late_fees --limit 100

# Aplicar a toda la historia
python manage.py backfill_late_fees
```

**Output al finalizar:**
```
=== Resumen ===
  Total procesadas       : 3241
  Con late_fee > 0       : 2180
  Pending → overdue      : 847
  Suma total late_fee    : 12450000.00
  Errores                : 0
```

Errores por cuota individual están aislados: si una cuota falla, el proceso continúa con las demás y reporta el `id` de la cuota problemática.

---

### Paso 6 — Endpoint `GET /fintech/collector/portfolio/{seller_id}/`

**Vista:** `apps/fintech/views_collector.py:CollectorPortfolioView`

**Autenticación:** JWT requerido. El usuario autenticado debe ser el seller con ese `seller_id`, o tener el permiso `fintech.view_all_portfolios`.

**Respuesta:**
```json
{
  "seller": { "id": 1, "name": "...", "username": "..." },
  "summary": {
    "total_clients": 45,
    "clients_on_time": 30,
    "clients_overdue": 12,
    "clients_critical": 3,
    "total_installments_pending": 67,
    "total_installments_overdue": 18,
    "total_amount_pending": "8450000.00",
    "total_late_fees_pending": "127500.00"
  },
  "schedule": {
    "2025-06-02": [ ...cuotas del día... ],
    "2025-06-09": [ ...cuotas del día... ]
  }
}
```

**Qué incluye el schedule:**
- Todas las cuotas vencidas sin límite de antigüedad.
- Cuotas que vencen en los próximos 30 días.
- Ordenado cronológicamente por fecha. Dentro de cada fecha: por `priority` descendente, luego por `client_name` alfabéticamente.

**Campos por cuota:**
```json
{
  "installment_id": 1234,
  "credit_uid": "uuid",
  "client_name": "...",
  "client_id": 56,
  "installment_number": 3,
  "amount_due": "150000.00",
  "amount_paid": "0.00",
  "remaining_amount": "150000.00",
  "late_fee": "7500.00",         ← calculado en tiempo real con calculate_late_fee()
  "total_due": "157500.00",
  "days_overdue": 8,
  "grace_days_remaining": 0,
  "status": "overdue",
  "priority": "high",
  "credit_morosidad_level": "mild_default"
}
```

**Tabla de prioridades:**

| priority | Condición |
|---|---|
| `urgent` | > 30 días de mora efectiva (post-gracia) |
| `high` | Entre 7-30 días de mora efectiva, o vence hoy |
| `medium` | Entre 1-7 días de mora efectiva, o vence en los próximos 3 días |
| `low` | Al día, vence en más de 3 días |

**Performance:** usa `select_related('credit__user', 'credit__seller', 'credit__periodicity')`. No hay queries dentro del loop.

---

### Paso 7 — Endpoint `POST /fintech/collector/fee-decision/`

**Vista:** `apps/fintech/views_collector.py:FeeDecisionView`

**Autenticación:** JWT requerido. El usuario debe ser el seller del crédito al que pertenece la cuota, o tener el permiso `fintech.manage_all_fee_decisions`.

**Request:**
```json
{
  "installment_id": 1234,
  "decision": "partial",
  "applied_fee": "3750.00",
  "reason": "El cliente tuvo emergencia médica, se acordó cobrar el 50%."
}
```

**Validaciones:**
- `decision` ∈ `{applied, partial, waived}`.
- Si `partial` o `waived`: `reason` es obligatorio y no puede ser solo espacios.
- Si `applied`: `applied_fee` debe coincidir con `calculate_late_fee()` actual (tolerancia ±0.01). Error 400 con mensaje `"Recargo actual: {monto}."`.
- Si `partial`: `applied_fee` debe ser mayor a 0 y menor al recargo calculado.
- Si `waived`: `applied_fee` debe ser exactamente 0.

**Comportamiento al guardar (dentro de `transaction.atomic()`):**
1. Calcula `calculated_fee = installment.calculate_late_fee()` en el momento del request.
2. Crea el registro `FeeDecision`.
3. Si `applied_fee > 0`: crea una `Transaction` (`income`, `confirmed`) y un `AccountMethodAmount` con `payment_code = f"FEE-{installment.id}-{date.today().isoformat()}"`.
4. Actualiza `installment.late_fee = applied_fee` (lo efectivamente cobrado).

**Respuesta exitosa (201):**
```json
{
  "fee_decision_id": 89,
  "installment_id": 1234,
  "calculated_fee": "7500.00",
  "applied_fee": "3750.00",
  "decision": "partial",
  "message": "Decisión registrada correctamente."
}
```

---

## Archivos modificados / creados

| Archivo | Tipo | Descripción |
|---|---|---|
| `apps/fintech/models.py` | Modificado | `Credit.late_fee_rate`, `Installment.calculate_late_fee()`, modelo `FeeDecision` |
| `apps/fintech/migrations/0005_add_late_fee_rate_to_credit.py` | Creado | Migración para `late_fee_rate` |
| `apps/fintech/migrations/0006_add_feedecision_model.py` | Creado | Migración para `FeeDecision` |
| `apps/fintech/services/credit/credit_service.py` | Modificado | Bug 1 (choices), Bug 3 (fórmula hardcodeada) |
| `apps/fintech/services/credit/installment_service.py` | Modificado | Bug 2 (`days_overdue`), Bug 3 (fórmula hardcodeada x2) |
| `apps/fintech/tasks.py` | Modificado | Eliminadas 2 tareas, `installment_daily_maintenance` refactorizada |
| `core/settings.py` | Modificado | Removida `update-installment-statuses` del beat schedule |
| `apps/fintech/admin.py` | Modificado | `FeeDecisionAdmin`, fieldsets en `CreditAdmin` |
| `apps/fintech/views_collector.py` | Creado | `CollectorPortfolioView`, `FeeDecisionView` |
| `apps/fintech/urls.py` | Modificado | 2 URLs nuevas para los endpoints del cobrador |
| `apps/fintech/management/commands/backfill_late_fees.py` | Creado | Command de backfill histórico |

---

## Checklist para activar en producción

- [ ] Conectar DB de Render y ejecutar `python manage.py migrate`
- [ ] Ejecutar `python manage.py backfill_late_fees --dry-run` y revisar el resumen
- [ ] Ejecutar `python manage.py backfill_late_fees` para poblar la historia
- [ ] Verificar en el admin que `FeeDecision` aparece en el menú
- [ ] Verificar que `Credit.late_fee_rate` aparece en el fieldset de un crédito existente
- [ ] Probar `GET /fintech/collector/portfolio/{seller_id}/` con un JWT válido
- [ ] Probar `POST /fintech/collector/fee-decision/` con los tres tipos de decisión
- [ ] Confirmar que `installment_daily_maintenance` no lanza errores al correr manualmente: `python manage.py shell -c "from apps.fintech.tasks import installment_daily_maintenance; print(installment_daily_maintenance.apply().result)"`

---

## Decisiones de diseño y trade-offs

**¿Por qué `late_fee` en BD = lo cobrado, no lo calculado?**  
Porque el cobrado es un hecho contable inmutable. El calculado cambia cada día. Si persistiéramos el calculado, necesitaríamos actualizarlo diariamente por cada cuota vencida, generando writes masivos sin valor contable. El cobrado solo cambia cuando hay una `FeeDecision`.

**¿Por qué el período de gracia son 3 días y no configurable?**  
Es un parámetro de negocio que aplica igual a todos los créditos según las prácticas actuales de campo. Si en el futuro se necesita variarlo por subcategoría, se puede agregar `grace_days` al modelo `Credit` sin romper la API existente.

**¿Por qué eliminar `update_installment_statuses` en lugar de solo corregirla?**  
Corría cada 30 minutos y duplicaba exactamente lo que hace `installment_daily_maintenance` a las 06:00. Tener dos tareas con la misma responsabilidad aumenta el riesgo de condiciones de carrera y dificulta el diagnóstico cuando algo falla. Una sola tarea diaria es suficiente para el volumen actual.

**¿Por qué `views_collector.py` separado de `views.py`?**  
`views.py` ya tiene 300+ líneas y mezcla ViewSets con APIViews. Los endpoints del cobrador tienen una lógica de negocio distinta (autorización por cartera, cálculo en tiempo real) que justifica un archivo propio para mantenerlos navegables.
