# Frontend - Creditos diarios en calendario de cobranza

Este documento explica que esta pasando con los creditos de periodicidad diaria y que debe hacer frontend para mostrarlos correctamente en el calendario.

## Diagnostico backend

El endpoint recomendado para calendario es:

```http
GET /fintech/collector/my-portfolio/
```

Este endpoint no filtra por periodicidad. Consulta cuotas (`Installment`) con:

```txt
credit__seller = cobrador autenticado
status in ['pending', 'partial', 'overdue']
due_date <= hoy + 30 dias
```

Por tanto, un credito diario aparece en el calendario si cumple estas condiciones:

- Tiene cuotas (`Installment`) generadas.
- Las cuotas pertenecen a un credito del cobrador autenticado.
- La cuota esta en estado `pending`, `partial` u `overdue`.
- La cuota tiene `due_date` dentro de vencidas o proximos 30 dias.

El endpoint no usa `Credit.next_due_date`, `Credit.first_date_payment`, `Credit.second_date_payment` ni `Credit.periodicity` para decidir que dias pintar. La fuente de verdad del calendario es siempre:

```txt
Installment.due_date
```

## Que se agrego al contrato

Para evitar que frontend tenga que inferir datos, cada item del `schedule` ahora incluye:

```json
{
  "due_date": "2026-06-04",
  "credit_periodicity_name": "Daily",
  "credit_periodicity_days": 1
}
```

Estos campos se suman a los existentes:

```json
{
  "installment_id": 1234,
  "credit_uid": "a3f8e2b1-...",
  "installment_number": 5,
  "remaining_amount": "10000.00",
  "late_fee": "0.00",
  "total_due": "10000.00",
  "status": "pending",
  "priority": "high"
}
```

Ademas, `summary` incluye un agregado por periodicidad:

```json
{
  "summary": {
    "installments_by_periodicity": [
      {
        "periodicity_days": 1,
        "periodicity_name": "Daily",
        "installments_count": 42,
        "total_remaining_amount": "420000.00",
        "total_due": "420000.00"
      }
    ]
  }
}
```

Este campo sirve para diagnosticar rapido si backend esta entregando cuotas diarias. Si existe un item con `periodicity_days: 1` e `installments_count > 0`, backend si esta enviando compromisos diarios y el problema esta en el render/transformacion del frontend.

Si no aparece `periodicity_days: 1`, revisar en backend/base de datos si existen cuotas diarias elegibles para ese cobrador autenticado.

## Que probablemente esta pasando en frontend

Si los creditos diarios no se ven, pero si se ven otras periodicidades, el problema mas probable esta en la transformacion del frontend, no en el query principal del backend.

Casos comunes:

### 1. Frontend esta agrupando por credito y no por cuota

Incorrecto:

```ts
const uniqueCredits = uniqBy(items, "credit_uid")
```

Esto rompe creditos diarios porque un mismo credito puede tener muchas cuotas en diferentes fechas. Para calendario se debe renderizar cada cuota como un compromiso independiente.

Correcto:

```ts
const commitments = items // cada item es una cuota
```

La llave estable para render debe ser:

```ts
item.installment_id
```

No:

```ts
item.credit_uid
```

### 2. Frontend esta usando `Credit.next_due_date`

Incorrecto:

```ts
date = credit.next_due_date
```

`next_due_date` solo representa una proxima cuota del credito. En creditos diarios hay muchas cuotas, una por cada fecha pactada.

Correcto:

```ts
date = item.due_date
```

O usar la llave del `schedule`:

```ts
response.schedule["YYYY-MM-DD"]
```

### 3. Frontend esta filtrando periodicidades

Revisar si existe logica parecida a:

```ts
if (credit.periodicity !== "daily") return
```

o:

```ts
items.filter(item => item.credit_periodicity_days !== 1)
```

Para el calendario no debe excluirse `credit_periodicity_days = 1`.

### 4. Frontend esta asumiendo una cuota por credito

Incorrecto:

```ts
calendarEvents[credit.uid] = event
```

Correcto:

```ts
calendarEvents[item.installment_id] = event
```

En creditos diarios, el mismo `credit_uid` puede aparecer muchas veces con diferentes `installment_id` y diferentes `due_date`.

### 5. Frontend esta ocultando fechas sin normalizar timezone

Las fechas del backend son strings `YYYY-MM-DD`. No deben convertirse a `Date` con timezone si solo se usan como llave de calendario.

Recomendado:

```ts
const dateKey = item.due_date // "2026-06-04"
```

Evitar:

```ts
new Date(item.due_date).toISOString()
```

Eso puede mover la fecha por timezone dependiendo del navegador.

## Regla de render correcta

Frontend debe tratar cada item de `schedule[date]` como un compromiso de pago.

```ts
const itemsForDay = response.schedule[dateKey] ?? []

const events = itemsForDay.map(item => ({
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

Para calcular el total del dia:

```ts
const expectedTotal = itemsForDay.reduce(
  (total, item) => total + Number(item.total_due),
  0
)
```

Para calcular solo creditos diarios dentro del dia:

```ts
const dailyItems = itemsForDay.filter(
  item => item.credit_periodicity_days === 1
)
```

## Que debe revisar frontend ahora

Frontend debe confirmar:

- Que esta consumiendo `/fintech/collector/my-portfolio/`.
- Que no esta llamando `/api/orders/list/` para esta pantalla.
- Que no esta usando `credit_uid` como key unica del calendario.
- Que no esta agrupando por credito antes de renderizar.
- Que usa `installment_id` como identificador del evento.
- Que usa `item.due_date` o la llave de `schedule` como fecha.
- Que no excluye `credit_periodicity_days === 1`.
- Que no convierte `YYYY-MM-DD` a `Date` con timezone para decidir el dia.

## Nota sobre domingos

La generacion de cuotas para creditos diarios puede saltar domingos segun la regla de negocio actual. Eso significa que un credito diario puede no tener cuota un domingo.

Esto es esperado si la cuota no existe para ese dia. Frontend no debe inventar cuotas diarias; debe pintar solo las cuotas recibidas en `schedule`.

## Si un credito diario no aparece en backend

Si despues de corregir frontend un credito diario sigue sin aparecer en `schedule`, revisar en backend/base de datos:

- Que el credito tenga `seller_id` igual al cobrador autenticado.
- Que existan registros `Installment` para ese credito.
- Que las cuotas tengan `due_date`.
- Que las cuotas esten en `pending`, `partial` u `overdue`.
- Que no esten `paid` o `cancelled`.
- Que las fechas esten vencidas o dentro de los proximos 30 dias.

La pantalla calendario no debe generarse desde `Credit` directamente; debe generarse desde `Installment`.
