# Calendario de Cobranza - Guia Unificada Frontend

## Endpoint principal

Para la pantalla normal del cobrador autenticado, frontend debe usar:

```http
GET /fintech/collector/my-portfolio/
Authorization: Bearer <token>
```

No debe enviar `seller_id`. Backend resuelve internamente:

```txt
request.user.seller_profile
```

Endpoint administrativo/soporte:

```http
GET /fintech/collector/portfolio/{seller_id}/
```

`{seller_id}` es `Seller.id`, no `User.id`, no cliente y no `credit_uid`.

## Response

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
    "total_late_fees_pending": "127500.00",
    "installments_by_periodicity": [
      {
        "periodicity_days": 1,
        "periodicity_name": "Daily",
        "installments_count": 42,
        "total_remaining_amount": "420000.00",
        "total_due": "420000.00"
      }
    ]
  },
  "schedule": {
    "2026-06-05": [
      {
        "installment_id": 1234,
        "credit_uid": "a3f8e2b1-...",
        "due_date": "2026-06-05",
        "client_name": "Ana Garcia",
        "client_id": 56,
        "installment_number": 3,
        "credit_periodicity_name": "Daily",
        "credit_periodicity_days": 1,
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
    ]
  }
}
```

## Fuente de verdad

Para calendario, la fuente de verdad es la cuota:

```txt
Installment.due_date
Installment.status
Installment.remaining_amount
Installment.total_due
```

No usar para pintar el calendario:

- `Credit.next_due_date`
- `Credit.price`
- `Credit.pending_amount`
- `Credit.state`

## Como renderizar

Cada item de `schedule[date]` es un compromiso de pago independiente.

```ts
const dateKey = "2026-06-05"
const items = response.schedule[dateKey] ?? []

const events = items.map(item => ({
  id: item.installment_id,
  creditUid: item.credit_uid,
  date: item.due_date,
  title: item.client_name,
  amount: Number(item.total_due),
  remainingAmount: Number(item.remaining_amount),
  lateFee: Number(item.late_fee),
  status: item.status,
  priority: item.priority,
  periodicityDays: item.credit_periodicity_days,
}))
```

## Seleccion de dia en calendario

Cuando el usuario selecciona un dia, frontend debe mostrar todas las cuotas esperadas para esa fecha, mezclando todas las periodicidades:

- Diarias.
- Semanales.
- Quincenales.
- Mensuales u otras periodicidades existentes.

No se debe hacer una consulta distinta por periodicidad. El backend ya entrega todas las cuotas elegibles dentro de:

```ts
response.schedule["YYYY-MM-DD"]
```

Ejemplo:

```ts
type PeriodicityFilter = "all" | number

function getInstallmentsForDate(
  schedule: Record<string, CalendarInstallment[]>,
  dateKey: string,
  periodicityFilter: PeriodicityFilter = "all"
) {
  const items = schedule[dateKey] ?? []

  if (periodicityFilter === "all") {
    return items
  }

  return items.filter(
    item => item.credit_periodicity_days === periodicityFilter
  )
}
```

Uso esperado:

```ts
const selectedDate = "2026-06-05"

const allItems = getInstallmentsForDate(response.schedule, selectedDate, "all")
const dailyItems = getInstallmentsForDate(response.schedule, selectedDate, 1)
const weeklyItems = getInstallmentsForDate(response.schedule, selectedDate, 7)
const biweeklyItems = getInstallmentsForDate(response.schedule, selectedDate, 15)
```

La lista principal del dia debe salir de `allItems`. El filtro de periodicidad solo cambia la lista visible y los totales visibles, no la fecha seleccionada.

## Filtros por periodicidad

El filtro debe construirse desde los datos recibidos, no con valores hardcodeados obligatorios. Cada cuota trae:

```txt
credit_periodicity_days
credit_periodicity_name
```

Para generar opciones de filtro del dia seleccionado:

```ts
const periodicityOptions = Array.from(
  new Map(
    allItems.map(item => [
      item.credit_periodicity_days,
      {
        days: item.credit_periodicity_days,
        name: item.credit_periodicity_name,
      },
    ])
  ).values()
)
```

Siempre incluir una opcion inicial:

```ts
{ label: "Todas", value: "all" }
```

Ejemplo de equivalencias habituales:

| `credit_periodicity_days` | Periodicidad |
| --- | --- |
| `1` | Diaria |
| `7` | Semanal |
| `15` | Quincenal |
| `30` | Mensual |

No ocultar cuotas diarias. Si `credit_periodicity_days === 1`, esa cuota debe mostrarse en la fecha seleccionada igual que cualquier otra.

## KPIs del dia seleccionado

Los KPIs visibles del dia deben calcularse sobre la lista filtrada actualmente.

```ts
function buildDayKpis(items: CalendarInstallment[]) {
  return {
    installmentsCount: items.length,
    expectedTotal: items.reduce(
      (total, item) => total + Number(item.total_due),
      0
    ),
    remainingTotal: items.reduce(
      (total, item) => total + Number(item.remaining_amount),
      0
    ),
    lateFeeTotal: items.reduce(
      (total, item) => total + Number(item.late_fee),
      0
    ),
    overdueCount: items.filter(item => item.status === "overdue").length,
    partialCount: items.filter(item => item.status === "partial").length,
    pendingCount: items.filter(item => item.status === "pending").length,
  }
}
```

Si el filtro esta en `Todas`, los KPIs representan todo lo esperado cobrar ese dia. Si el filtro esta en `Diaria`, los KPIs representan solo cuotas diarias de ese dia.

Total esperado del dia:

```ts
const expectedTotal = items.reduce(
  (total, item) => total + Number(item.total_due),
  0
)
```

Solo saldo de cuota sin mora:

```ts
const remainingTotal = items.reduce(
  (total, item) => total + Number(item.remaining_amount),
  0
)
```

Mora/recargo:

```ts
const lateFeeTotal = items.reduce(
  (total, item) => total + Number(item.late_fee),
  0
)
```

## Creditos diarios

El endpoint no filtra por periodicidad. Un credito diario aparece si tiene cuotas elegibles:

- `credit.seller` es el cobrador autenticado.
- La cuota esta en `pending`, `partial` u `overdue`.
- La cuota tiene `due_date <= hoy + 30 dias`.
- La cuota no esta `paid` ni `cancelled`.

Para verificar si backend esta enviando cuotas diarias, revisar:

```ts
response.summary.installments_by_periodicity
```

Si aparece:

```json
{
  "periodicity_days": 1,
  "installments_count": 42
}
```

backend si esta entregando compromisos diarios.

Frontend debe evitar:

```ts
uniqBy(items, "credit_uid")
```

Usar siempre:

```ts
item.installment_id
```

Un mismo `credit_uid` diario puede aparecer muchas veces, con diferentes `installment_id` y `due_date`.

## Fechas y timezone

Las fechas vienen como strings `YYYY-MM-DD`. Usarlas como llaves de calendario sin convertirlas a `Date`:

```ts
const dateKey = item.due_date
```

Evitar:

```ts
new Date(item.due_date).toISOString()
```

Eso puede mover el dia por timezone.

## Estados

El estado visual debe venir de:

```txt
item.status
```

Valores:

| Estado | Significado |
| --- | --- |
| `pending` | Cuota pendiente |
| `partial` | Cuota con pago parcial |
| `overdue` | Cuota vencida |
| `paid` | Cuota pagada |
| `cancelled` | Cuota cancelada |

## Prioridad

Usar `priority` para orden visual, color o badge:

| Prioridad | Condicion |
| --- | --- |
| `urgent` | Mas de 30 dias de mora |
| `high` | 7 a 30 dias de mora, o vence hoy |
| `medium` | 1 a 7 dias de mora, o vence en proximos 3 dias |
| `low` | Al dia, vence en mas de 3 dias |

## Errores comunes

### Doble slash

Evitar:

```txt
GET //fintech/collector/my-portfolio/
```

Recomendado:

```ts
const API_BASE_URL = "http://127.0.0.1:8000"
const url = `${API_BASE_URL}/fintech/collector/my-portfolio/`
```

### `/api/orders/list/`

Este endpoint no existe en este backend:

```http
GET /api/orders/list/
```

Para calendario usar:

```http
GET /fintech/collector/my-portfolio/
```

### `portfolio/606/`

Si usan:

```http
GET /fintech/collector/portfolio/606/
```

`606` debe ser `Seller.id`. Si es `User.id`, puede dar:

```json
{"detail": "Not found."}
```

Para la pantalla normal, no usar ese endpoint. Usar `my-portfolio`.

## Checklist frontend

- Consumir `/fintech/collector/my-portfolio/`.
- No depender de `/api/orders/list/`.
- No enviar `seller_id` para la pantalla normal.
- Usar `schedule["YYYY-MM-DD"]`.
- Usar `installment_id` como key del evento.
- Usar `due_date` como fecha.
- Usar `total_due` como monto principal si incluye mora.
- Usar `remaining_amount` si se necesita solo cuota sin mora.
- Usar `status` de la cuota, no `Credit.state`.
- No agrupar por `credit_uid`.
- No excluir `credit_periodicity_days === 1`.
- No convertir fechas `YYYY-MM-DD` a `Date` para decidir el dia.

## Checklist backend si no aparecen diarios

## Situacion actual detectada

El diagnostico ejecutado el 2026-06-05 mostro:

```txt
Creditos Daily: 315
Con seller: 314
Sin seller: 1
Con cuotas: 126
Sin cuotas: 189

Cuotas de creditos diarios: 3678
Cuotas diarias elegibles para calendario: 1503
Vencidas o de hoy: 1503
Futuras hasta horizonte: 0

Status:
  paid: 2175
  partial: 45
  pending: 1458
```

Interpretacion:

- Si existen creditos diarios.
- Muchos creditos diarios no tienen cuotas creadas: 189 de 315.
- El calendario solo puede servir cuotas existentes, por eso esos 189 creditos diarios quedan invisibles.
- Las cuotas diarias elegibles actuales estan concentradas en `seller_id=2`.
- Hay cuotas `pending` con `remaining_amount=0.00`, lo que indica datos inconsistentes: deberian estar `paid` o recalculadas.
- No hay cuotas diarias futuras dentro de los proximos 30 dias; por eso el calendario no puede proyectar recaudo diario futuro correctamente.

Conclusion: no basta con ajustar frontend. Hay que reparar/generar cuotas y normalizar estados/saldos para que calendario, KPIs de recaudo y morosidad tengan datos confiables.

Ejecutar el diagnostico:

```bash
python3 manage.py diagnosticar_calendario_diario
```

Para un cobrador especifico:

```bash
python3 manage.py diagnosticar_calendario_diario --seller-id 3
```

El comando muestra:

- Periodicidades existentes en creditos.
- Total de creditos con `periodicity.days = 1`.
- Creditos diarios con y sin cuotas.
- Cuotas diarias por status.
- Cuotas diarias creadas en domingo.
- Cuotas diarias que cumplen exactamente el criterio del calendario.
- Cuotas diarias elegibles agrupadas por `seller_id`.
- Muestra de cuotas que deberian aparecer en `schedule`.

Si `installments_by_periodicity` no trae `periodicity_days: 1`, revisar en BD:

- Que el credito tenga `periodicity.days = 1`.
- Que el credito tenga `seller_id` del cobrador autenticado.
- Que existan `Installment` para ese credito.
- Que las cuotas tengan `due_date`.
- Que las cuotas esten en `pending`, `partial` u `overdue`.
- Que las cuotas no esten `paid` ni `cancelled`.
- Que las fechas sean vencidas o esten dentro de los proximos 30 dias.

Nota: los creditos diarios pueden saltar domingos si la regla de negocio excluye domingos. Frontend no debe inventar cuotas; debe pintar solo las cuotas recibidas en `schedule`.

## Reparacion de cuotas diarias

Existe un comando en modo seguro para reparar la data:

```bash
python3 manage.py backfill_cuotas_diarias --create-missing --repair-existing
```

Por defecto no escribe en BD; solo muestra lo que haria.

Para probar con pocos creditos:

```bash
python3 manage.py backfill_cuotas_diarias --create-missing --repair-existing --limit 10
```

Para un cobrador especifico:

```bash
python3 manage.py backfill_cuotas_diarias --seller-id 2 --create-missing --repair-existing
```

Para aplicar cambios:

```bash
python3 manage.py backfill_cuotas_diarias --seller-id 2 --create-missing --repair-existing --apply
```

Caso puntual revisado:

```txt
Cliente: ErnestoReyes
Credito: 39064a3a-a5c5-46e3-b39f-3560e85ea28f
Periodicidad: Daily (1 dia)
Precio: 120.00
Pagado confirmado: 5.00
Saldo: 115.00
first_date_payment: 2026-06-03
second_date_payment: 2026-06-04
credit_days: 24
installments: 0
```

Este credito no aparece en calendario porque no tiene cuotas. Para creditos diarios, `credit_days` debe interpretarse como dias cobrables/cuotas, no como dias calendario. Con `credit_days=24` y precio `120.00`, el backfill genera 24 cuotas de `5.00`, empezando el 2026-06-03 y saltando domingos.

Dry-run recomendado para este credito:

```bash
python3 manage.py backfill_cuotas_diarias \
  --credit-uid 39064a3a-a5c5-46e3-b39f-3560e85ea28f \
  --create-missing \
  --show-dates
```

Si el dry-run se ve correcto, aplicar solo ese credito:

```bash
python3 manage.py backfill_cuotas_diarias \
  --credit-uid 39064a3a-a5c5-46e3-b39f-3560e85ea28f \
  --create-missing \
  --apply
```

El comando hace dos cosas:

- `--create-missing`: crea cuotas para creditos diarios que no tienen ninguna cuota.
- `--repair-existing`: recalcula `amount_paid`, `remaining_amount`, `paid`, `paid_on`, `status` y `days_overdue` de cuotas existentes segun pagos confirmados.

Regla de generacion:

- Usa `Credit.first_date_payment` como primera fecha de cuota.
- Para creditos diarios (`periodicity.days = 1`) no crea cuotas en domingo.
- Calcula el numero de cuotas desde `installment_number`; si no existe y el credito es diario, usa `credit_days` como numero de cuotas/dias cobrables.
- Divide `Credit.price` entre cuotas y ajusta la ultima cuota para que la suma sea exacta.
- Aplica pagos confirmados en orden cronologico sobre cuotas en orden de vencimiento.

Orden recomendado:

1. Ejecutar diagnostico.
2. Ejecutar backfill en dry-run para un `seller_id`.
3. Revisar muestra de cambios.
4. Ejecutar con `--apply`.
5. Ejecutar diagnostico nuevamente.
6. Confirmar que `/fintech/collector/my-portfolio/` trae `summary.installments_by_periodicity` con `periodicity_days=1`.

## Riesgos y decisiones pendientes

Antes de aplicar en produccion, confirmar:

- Si los pagos historicos deben distribuirse estrictamente por fecha de transaccion o solo por monto acumulado.
- Si `paid_on` historico puede quedar como la fecha del pago que completo cada cuota.
- Si los domingos se excluyen solo para creditos diarios. El backfill nuevo aplica esta regla explicitamente: `periodicity.days = 1` no genera cuotas en domingo.
- Si creditos con `pending_amount <= 0` deben quedar fuera del calendario aunque tengan cuotas mal marcadas.
- Si se debe crear una tarea periodica que garantice que todo credito nuevo tenga cuotas desde su creacion.

Para que el calendario sea confiable a futuro, la regla debe ser: todo credito activo debe tener cuotas creadas al momento de crearse o importarse. El frontend no debe calcular compromisos desde `Credit`; debe leer cuotas reales desde `Installment`.

## Backfill general desde 1 de mayo

Para crear compromisos/cuotas faltantes de creditos recientes, existe un comando general:

```bash
python3 manage.py backfill_compromisos_pago --from-date 2026-05-01 --create-missing
```

Por defecto corre en `DRY-RUN`: no escribe en BD, solo muestra que creditos procesaria y cuantas cuotas crearia.

Para revisar una muestra:

```bash
python3 manage.py backfill_compromisos_pago \
  --from-date 2026-05-01 \
  --create-missing \
  --limit 20 \
  --show-dates
```

Para revisar por cobrador:

```bash
python3 manage.py backfill_compromisos_pago \
  --from-date 2026-05-01 \
  --seller-id 2 \
  --create-missing \
  --show-dates
```

Para aplicar cambios:

```bash
python3 manage.py backfill_compromisos_pago \
  --from-date 2026-05-01 \
  --create-missing \
  --apply
```

Para aplicar por cobrador:

```bash
python3 manage.py backfill_compromisos_pago \
  --from-date 2026-05-01 \
  --seller-id 2 \
  --create-missing \
  --apply
```

Este comando procesa todas las periodicidades, no solo diarias:

- Diarias: genera una cuota por dia cobrable y no crea cuotas en domingo.
- Semanales: genera cuotas cada 7 dias.
- Quincenales: genera cuotas cada 15 dias.
- Mensuales: genera cuotas cada 30 dias.
- Otras: usa `credit.periodicity.days`.

Regla de cantidad de cuotas:

- Si `Credit.installment_number` existe y es mayor que cero, usa ese valor.
- Si el credito es diario y no tiene `installment_number`, usa `Credit.credit_days` como cantidad de cuotas/dias cobrables.
- Si el credito no es diario y no tiene `installment_number`, calcula `ceil(credit_days / periodicity.days)`.

Tambien puede reparar cuotas existentes:

```bash
python3 manage.py backfill_compromisos_pago \
  --from-date 2026-05-01 \
  --repair-existing
```

Y aplicar reparacion:

```bash
python3 manage.py backfill_compromisos_pago \
  --from-date 2026-05-01 \
  --repair-existing \
  --apply
```

Orden recomendado:

1. Ejecutar dry-run con `--limit 20 --show-dates`.
2. Ejecutar dry-run por `seller_id`.
3. Revisar fechas y cantidades.
4. Aplicar por `seller_id` si la muestra es correcta.
5. Ejecutar diagnosticos del calendario.
6. Confirmar que frontend ve las cuotas nuevas en `/fintech/collector/my-portfolio/`.
