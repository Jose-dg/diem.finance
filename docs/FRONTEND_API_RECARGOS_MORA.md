# Cambios de API — Recargos por Mora

**Fecha:** 2026-05-28  
**Para:** Equipo Frontend  
**De:** Backend  
**Requiere acción frontend:** Sí — hay cambios que rompen comportamiento existente

---

## Resumen ejecutivo

Activamos el sistema de recargos por mora que existía en el backend pero nunca funcionó en producción. Esto implica:

1. **Dos endpoints nuevos** para la app del cobrador.
2. **Dos endpoints existentes que cambian de comportamiento** (breaking change en filtros de estado).
3. **Un campo nuevo** en la respuesta de créditos.
4. **Cambio de comportamiento en `status` de cuotas** — el valor `'overdue'` ahora se usa correctamente.
5. **Dos campos del serializer con comportamiento inconsistente** — documentados abajo como deuda técnica pendiente.

---

## 1. BREAKING CHANGES — requieren cambio en el frontend

### 1.1 `GET /fintech/collector/overdue/` — filtro de estado roto

**Problema actual:** Este endpoint filtraba `status in ['pending', 'partial']` para encontrar cuotas vencidas. Funcionaba porque el sistema nunca cambiaba el estado a `'overdue'`. Ahora el sistema sí lo hace (después del período de gracia de 3 días).

**Efecto:** Cuotas correctamente marcadas como `overdue` desaparecen de este endpoint.

**Acción requerida:** Actualizar el filtro para incluir `'overdue'`:

```
Antes: filtraba status in ['pending', 'partial'] con due_date < hoy
Ahora: debe filtrar status in ['pending', 'partial', 'overdue'] con due_date < hoy
```

Esto es un fix de backend que hacemos nosotros. Sin embargo, si el frontend tiene algún filtro adicional client-side que excluya `status === 'overdue'`, hay que removerlo.

---

### 1.2 `GET /fintech/collector/dashboard/` — contador de vencidas incorrecto

**Problema actual:** El campo `summary.overdue` en este endpoint contaba `status in ['pending', 'partial']`. Por la misma razón que el punto anterior, ahora reportaría un número menor al real.

**Efecto:** El número que muestra el dashboard del cobrador como "cuotas vencidas" se subestimará.

**Acción requerida:** Mismo fix de backend que 1.1 — lo resolvemos nosotros. El frontend no necesita cambiar la lectura del campo `summary.overdue`, solo saber que el valor ahora será correcto.

---

### 1.3 Cambio en `Installment.status` — el valor `'overdue'` ahora es real

Antes de estos cambios, el status `'overdue'` prácticamente nunca aparecía en producción porque las tareas Celery no funcionaban correctamente. Las cuotas vencidas aparecían como `'pending'`.

**A partir de ahora:**

| Status | Significado | Cuándo ocurre |
|---|---|---|
| `pending` | Cuota pendiente, no vencida o dentro de período de gracia | due_date en el futuro, o hasta 3 días después de due_date |
| `overdue` | Cuota vencida más de 3 días, con recargo activo | due_date + 3 días < hoy |
| `partial` | Pago parcial registrado | amount_paid > 0 pero < amount |
| `paid` | Pagada completamente | amount_paid >= amount |
| `cancelled` | Cancelada | manual |

**Período de gracia:** 3 días desde `due_date`. Una cuota que vence el lunes pasa a `overdue` el jueves si no se ha pagado.

**Acción requerida:** Revisar cualquier lógica de UI que trate `'overdue'` como un estado "imposible" o lo ignore. Si hay badges, íconos o colores que solo manejaban `pending`/`partial`/`paid`, agregar el caso `overdue`.

---

## 2. CAMPOS NUEVOS EN RESPUESTAS EXISTENTES

### 2.1 `late_fee_rate` en respuesta de crédito

El endpoint `GET /fintech/credits/{id}/` ahora incluye el campo `late_fee_rate` en la respuesta (el serializer usa `__all__`).

```json
{
  "uid": "...",
  "late_fee_rate": "0.0500",
  ...
}
```

- Tipo: string decimal
- Valor por defecto: `"0.0500"` (5% mensual)
- Significado: tasa mensual de recargo por mora configurada para ese crédito

No rompe nada — es aditivo.

---

### 2.2 `late_fee` en cuotas — cambio de valor

El campo `late_fee` en `InstallmentSerializer` (aparece dentro de `installments[]` en la respuesta de crédito) siempre era `"0.00"` en producción.

**A partir de ahora:**

- `late_fee` = monto de recargo que **fue efectivamente cobrado** al cliente (inmutable una vez registrado).
- `late_fee_calc` = monto de recargo que **el sistema calcula hoy** para esa cuota (cambia cada día).

**Regla para la UI:**
- Para mostrar cuánto debe el cliente → usar `late_fee_calc` (o el campo `late_fee` de la cartera del cobrador).
- Para mostrar cuánto se cobró históricamente → usar `late_fee`.

---

## 3. ENDPOINTS NUEVOS

### 3.1 `GET /fintech/collector/portfolio/{seller_id}/`

Cartera completa de un cobrador: resumen del portafolio y agenda de cuotas ordenada por fecha.

**Auth:** JWT requerido (`Authorization: Bearer <token>`). Solo el cobrador con ese `seller_id` puede ver su propia cartera. Admins con permiso `fintech.view_all_portfolios` pueden ver cualquiera.

**Request:**
```
GET /fintech/collector/portfolio/3/
Authorization: Bearer eyJ...
```

**Response 200:**
```json
{
  "seller": {
    "id": 3,
    "name": "Carlos Mendoza",
    "username": "cmendoza"
  },
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
    "2026-05-20": [...cuotas vencidas sin pagar...],
    "2026-05-28": [...cuotas de hoy...],
    "2026-06-02": [...cuotas próximas...],
    "2026-06-09": [...]
  }
}
```

**Notas sobre `summary`:**
- `total_late_fees_pending` — suma de recargos calculados en tiempo real (`calculate_late_fee()`) para todas las cuotas de la cartera. No usa el `late_fee` persistido.
- `clients_critical` — clientes cuyos créditos tienen `morosidad_level = 'critical_default'`.

**Cobertura del `schedule`:**
- **Vencidas:** todas las cuotas con `due_date < hoy`, sin límite de antigüedad.
- **Próximas:** cuotas con `due_date` entre hoy y hoy + 30 días.
- Las fechas están en formato `YYYY-MM-DD`.
- Dentro de cada fecha, las cuotas están ordenadas por `priority` (urgente primero) y luego alfabéticamente por nombre del cliente.

**Estructura de cada cuota en el schedule:**
```json
{
  "installment_id": 1234,
  "credit_uid": "a3f8e2b1-...",
  "client_name": "Ana García",
  "client_id": 56,
  "installment_number": 3,
  "amount_due": "150000.00",
  "amount_paid": "0.00",
  "remaining_amount": "150000.00",
  "late_fee": "7500.00",
  "total_due": "157500.00",
  "days_overdue": 8,
  "grace_days_remaining": 0,
  "status": "overdue",
  "priority": "high",
  "credit_morosidad_level": "mild_default"
}
```

**Tabla de `priority`:**

| Valor | Condición |
|---|---|
| `"urgent"` | Más de 30 días de mora (post-gracia) |
| `"high"` | 7–30 días de mora, o vence hoy |
| `"medium"` | 1–7 días de mora, o vence en los próximos 3 días |
| `"low"` | Al día, vence en más de 3 días |

**Campo `grace_days_remaining`:**
- `0` — ya superó el período de gracia, el recargo está corriendo.
- `1`, `2`, `3` — días que quedan de gracia. El recargo aún no aplica.

**Sugerencia de UI:**
- Agrupar el `schedule` por fecha para mostrar una agenda diaria.
- Usar `priority` para colorear o reordenar dentro del día.
- Mostrar `grace_days_remaining > 0` con un ícono de reloj: "X días de gracia".
- `late_fee: "0.00"` con `grace_days_remaining > 0` → mostrar "En gracia".
- `late_fee: "0.00"` con `grace_days_remaining = 0` → cuota al día, sin mora.

**Errores:**
```json
// 403 — no autorizado
{ "detail": "No tiene permiso para ver esta cartera." }

// 404 — seller no existe
{ "detail": "Not found." }
```

---

### 3.2 `POST /fintech/collector/fee-decision/`

Registrar la decisión del cobrador sobre el recargo de una cuota. Debe llamarse cuando el cobrador confirma cuánto recargo se cobró (o si se condonó).

**Auth:** JWT requerido. El cobrador debe ser el seller del crédito de esa cuota, o tener permiso `fintech.manage_all_fee_decisions`.

**Request:**
```json
{
  "installment_id": 1234,
  "decision": "partial",
  "applied_fee": "3750.00",
  "reason": "Cliente tuvo emergencia médica verificada, se acordó 50% del recargo."
}
```

**Campos del request:**

| Campo | Tipo | Requerido | Descripción |
|---|---|---|---|
| `installment_id` | integer | Sí | ID de la cuota (no el número de cuota, el `id` del objeto) |
| `decision` | string | Sí | `"applied"`, `"partial"` o `"waived"` |
| `applied_fee` | string decimal | Sí | Monto de recargo que se cobra al cliente |
| `reason` | string | Condicional | Obligatorio si `decision` es `"partial"` o `"waived"` |

**Valores de `decision`:**

| Valor | Significado | `applied_fee` esperado |
|---|---|---|
| `"applied"` | Se cobra el recargo completo calculado | Debe coincidir con el recargo calculado (±$0.01) |
| `"partial"` | Se cobra una parte del recargo | Mayor a 0, menor al recargo calculado |
| `"waived"` | Se condona el recargo completo | Debe ser `"0.00"` |

**Flujo sugerido de UI:**
1. Cobrador abre la cuota desde el portfolio.
2. El frontend muestra `late_fee` del schedule (recargo calculado hoy).
3. El cobrador elige cuánto cobrar (slider, campo libre, o botón "cobrar todo").
4. Al confirmar, llama a este endpoint.
5. Si `decision = "partial"` o `"waived"`, mostrar campo de texto obligatorio para la justificación.

**Response 201:**
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

**Errores posibles:**

```json
// 400 — decision inválida
{ "detail": "decision debe ser uno de: applied, partial, waived." }

// 400 — reason faltante para partial/waived
{ "detail": "reason es obligatorio cuando decision es partial o waived." }

// 400 — applied_fee no coincide con el recargo calculado (para 'applied')
{
  "detail": "Para aplicar el recargo completo, applied_fee debe coincidir con el recargo calculado actualmente. Recargo actual: 7500.00."
}

// 400 — applied_fee fuera de rango (para 'partial')
{ "detail": "Para partial, applied_fee debe ser mayor a 0 y menor al recargo calculado." }

// 400 — applied_fee no es 0 (para 'waived')
{ "detail": "Para waived, applied_fee debe ser 0." }

// 403 — cuota no pertenece al cobrador autenticado
{ "detail": "No tiene permiso para gestionar recargos de esta cuota." }

// 404 — cuota no existe
{ "detail": "Not found." }
```

**Importante:** Este endpoint crea un pago interno (`AccountMethodAmount`) en el sistema si `applied_fee > 0`. No hace falta llamar a ningún otro endpoint para registrar el pago del recargo.

---

## 4. VALORES DE `morosidad_level` — tabla de referencia

El campo `morosidad_level` aparece en créditos (varios endpoints) y en el campo `credit_morosidad_level` de la cartera del cobrador.

**Valores válidos:**

| Valor | Display sugerido | Umbral |
|---|---|---|
| `"on_time"` | Al día | Sin cuotas vencidas |
| `"mild_default"` | Mora leve | 30–59 días totales de mora acumulada |
| `"moderate_default"` | Mora moderada | 60–89 días |
| `"severe_default"` | Mora severa | 90–119 días |
| `"recurrent_default"` | Mora recurrente | (uso manual / histórico) |
| `"critical_default"` | Mora crítica | 120+ días |

**Nota:** El valor `"none"` puede aparecer en registros antiguos de la BD (295 créditos). Es un valor heredado de un bug anterior, no es un valor válido del sistema. Tratar como `"on_time"` en la UI hasta que se limpie.

---

## 5. DEUDA TÉCNICA — campos con comportamiento pendiente de corrección

Los siguientes campos existen en las respuestas actuales pero tienen comportamiento inconsistente después de estos cambios. Son fixes de backend pendientes, pero el frontend debe saberlos para no confiar en esos valores:

### 5.1 `late_fee_calc` en `InstallmentSerializer`

**Aparece en:** cualquier endpoint que devuelva cuotas (`installments[]` en `/fintech/credits/{id}/`, `/fintech/collector/due-today/`, etc.)

**Problema:** Usa la fórmula antigua (5% fijo, sin período de gracia, sin tope, sin tasa por crédito). Además, solo calcula el recargo para cuotas con `status = 'pending'` o `'partial'`. Para cuotas con `status = 'overdue'` devuelve `0.00` incorrectamente.

**Workaround:** Para la app del cobrador, usar el campo `late_fee` que devuelve `GET /fintech/collector/portfolio/{seller_id}/` — ese sí usa la fórmula correcta con gracia y tasa por crédito.

### 5.2 `days_overdue_calc` en `InstallmentSerializer`

**Aparece en:** los mismos endpoints que 5.1.

**Problema:** Devuelve `0` para cuotas con `status = 'overdue'` (solo funciona para `'pending'`/`'partial'`). Después del cambio, la mayoría de cuotas vencidas estarán en `'overdue'`, así que este campo reportará `0` para ellas.

**Workaround:** Calcular `days_overdue` en el frontend con `(hoy - due_date).days` si `due_date < hoy`. Es exactamente lo que hace el backend.

---

## 6. RESUMEN DE ACCIONES POR EQUIPO

### Backend (próximos sprints)
- [ ] Corregir filtro en `GET /fintech/collector/overdue/` para incluir `status='overdue'`
- [ ] Corregir filtro en `GET /fintech/collector/dashboard/` para el conteo de vencidas
- [ ] Actualizar `InstallmentCalculator.get_late_fee()` para usar `calculate_late_fee()`
- [ ] Actualizar `InstallmentCalculator.get_days_overdue()` para funcionar con `status='overdue'`
- [ ] Limpiar los 295 registros con `morosidad_level = 'none'`

### Frontend — acción inmediata
- [ ] Agregar manejo del status `'overdue'` en todos los componentes que renderizan cuotas (badges, colores, texto)
- [ ] Agregar manejo del valor `"none"` de `morosidad_level` (tratar como `"on_time"`)
- [ ] No confiar en `late_fee_calc` ni `days_overdue_calc` de los endpoints existentes para la app del cobrador — usar `/fintech/collector/portfolio/{seller_id}/` en su lugar
- [ ] Integrar los dos endpoints nuevos de cartera y decisión de recargo

### Frontend — acción futura (cuando el backend corrija los items de arriba)
- [ ] Actualizar cualquier lógica que lea `late_fee_calc` y `days_overdue_calc` de `InstallmentSerializer`

---

## 7. AUTENTICACIÓN — recordatorio

Todos los endpoints nuevos requieren JWT. Los endpoints del cobrador existentes (`/fintech/collector/due-today/`, `/fintech/collector/overdue/`, etc.) tienen la autenticación **comentada** en el backend — aún son públicos. Los nuevos endpoints sí requieren token.

```
Authorization: Bearer <access_token>
```

Token de acceso válido por 8 horas. Refresh por 7 días con rotación.
