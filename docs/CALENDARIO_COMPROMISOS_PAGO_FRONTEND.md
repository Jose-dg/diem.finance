# Calendario de Compromisos de Pago - Guia Frontend

Este documento explica que datos debe usar el frontend para construir una vista calendario de recaudo esperado, basada en las fechas pactadas de las cuotas de cada credito.

## Objetivo

La vista calendario debe permitir responder:

- Cuanto se espera cobrar hoy.
- Cuanto se espera cobrar en los siguientes dias.
- Que clientes tienen cuotas pendientes, parciales o vencidas por fecha.
- Que monto corresponde a la cuota del dia y que monto corresponde a mora/recargo.

## Endpoint recomendado

Actualmente no existe un endpoint especifico con esta forma:

```http
GET /calendar/payment-commitments/?date=YYYY-MM-DD
```

El endpoint recomendado para construir la vista calendario del cobrador autenticado es:

```http
GET /fintech/collector/my-portfolio/
Authorization: Bearer <token>
```

Este endpoint resuelve internamente el cobrador desde el token:

```txt
request.user.seller_profile
```

Frontend no debe descubrir ni enviar `Seller.id` para la vista normal del cobrador.

Para casos administrativos tambien existe:

```http
GET /fintech/collector/portfolio/{seller_id}/
Authorization: Bearer <token>
```

Ejemplo:

```http
GET /fintech/collector/my-portfolio/
Authorization: Bearer eyJ...
```

Ejemplo administrativo:

```http
GET /fintech/collector/portfolio/3/
Authorization: Bearer eyJ...
```

Este endpoint devuelve la cartera del cobrador y un objeto `schedule` agrupado por fecha.

## URL exacta y parametros

La ruta esta registrada en Django asi:

```txt
core/urls.py
  /fintech/ -> apps.fintech.urls

apps/fintech/urls.py
  /collector/my-portfolio/
  /collector/portfolio/<seller_id>/
```

Por tanto, con el servidor local de Django, la URL completa recomendada para el cobrador autenticado es:

```http
http://127.0.0.1:8000/fintech/collector/my-portfolio/
```

La URL administrativa es:

```http
http://127.0.0.1:8000/fintech/collector/portfolio/{seller_id}/
```

Importante: `{seller_id}` solo aplica al endpoint administrativo. Es el ID del modelo `Seller`, no el ID del cliente, no el ID del usuario comun y no el `credit_uid`.

Modelo relacionado:

```txt
Seller.id        -> ID que debe ir en la URL
Seller.user_id   -> usuario asociado al cobrador/vendedor
Credit.seller_id -> seller responsable del credito
```

Si el frontend tiene un usuario autenticado y esta usando `user.id = 606`, eso no necesariamente sirve para esta URL. Primero debe conocer el `seller.id` asociado a ese usuario. Por ejemplo, si existe:

```txt
Seller.id = 3
Seller.user_id = 606
```

Para la vista normal, la llamada correcta seria:

```http
GET /fintech/collector/my-portfolio/
```

Si se usa el endpoint administrativo, la llamada correcta seria:

```http
GET /fintech/collector/portfolio/3/
```

No:

```http
GET /fintech/collector/portfolio/606/
```

## Errores comunes de integracion

### 404 con respuesta corta `{"detail":"Not found."}`

Ejemplo visto en logs:

```txt
Not Found: /fintech/collector/portfolio/606/
"GET //fintech/collector/portfolio/606/ HTTP/1.1" 404 23
```

Este caso normalmente significa que la ruta si existe, pero no existe un registro `Seller` con `id = 606`.

La vista hace esta busqueda:

```python
Seller.objects.get(id=seller_id)
```

Por eso el frontend debe enviar el `Seller.id` real.

### Doble slash en la URL

Ejemplo visto:

```txt
GET //fintech/collector/portfolio/606/
```

El frontend esta construyendo la URL con doble slash. Revisar la composicion entre `API_BASE_URL` y path.

Recomendado:

```js
const API_BASE_URL = "http://127.0.0.1:8000";
const path = "/fintech/collector/my-portfolio/";
const url = `${API_BASE_URL}${path}`;
```

Evitar combinar base y path asi:

```js
const API_BASE_URL = "http://127.0.0.1:8000/";
const path = "/fintech/collector/my-portfolio/";
const url = `${API_BASE_URL}${path}`; // genera //fintech
```

### 404 en `/api/orders/list/`

El endpoint:

```http
GET /api/orders/list/?page=1
```

no existe en este backend Django segun las rutas actuales. Para creditos existe:

```http
GET /fintech/credits/
```

Para calendario/cobranza usar:

```http
GET /fintech/collector/my-portfolio/
```

### 403 por permisos

Si el `seller_id` existe pero el usuario autenticado no es ese cobrador y tampoco tiene el permiso global, el backend responde `403`.

Regla actual:

- En `/fintech/collector/my-portfolio/`, el usuario autenticado solo ve su propia cartera.
- Puede ver la cartera si `request.user.seller_profile.id == seller_id`.
- O si tiene permiso `fintech.view_all_portfolios`.

## Estructura general de respuesta

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
    "2026-06-04": [],
    "2026-06-05": [],
    "2026-06-06": []
  }
}
```

## Como usar `schedule`

`schedule` es un objeto donde cada llave es una fecha en formato `YYYY-MM-DD`.

Para saber cuanto se espera cobrar hoy, el frontend debe buscar la fecha actual:

```js
const today = "2026-06-04";
const todayItems = response.schedule[today] ?? [];
```

Para calcular el total esperado del dia:

```js
const expectedToday = todayItems.reduce((total, item) => {
  return total + Number(item.total_due);
}, 0);
```

Si el calendario debe mostrar solo el saldo de la cuota sin mora:

```js
const installmentAmountToday = todayItems.reduce((total, item) => {
  return total + Number(item.remaining_amount);
}, 0);
```

## Estructura de cada cuota en el calendario

Cada item dentro de una fecha representa una cuota (`Installment`) pendiente, parcial o vencida.

```json
{
  "installment_id": 1234,
  "credit_uid": "a3f8e2b1-...",
  "due_date": "2026-06-04",
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
```

## Respuestas a las preguntas del frontend

### Existe un endpoint especifico para compromisos por fecha?

No existe actualmente un endpoint `/calendar/payment-commitments/?date=YYYY-MM-DD`.

Usar:

```http
GET /fintech/collector/my-portfolio/
```

El frontend filtra o consulta dentro de:

```js
response.schedule["YYYY-MM-DD"]
```

### Cual es la fecha correcta?

La fecha correcta para el calendario es:

```txt
Installment.due_date
```

En la respuesta del endpoint aparece como la llave del objeto `schedule`.

No usar `Credit.next_due_date` para pintar el calendario completo. `next_due_date` es una propiedad calculada del credito que obtiene solo la proxima cuota pendiente, util para resumen, pero no para agrupar todos los compromisos por dia.

No existen campos principales de compromiso tipo:

- `promise_date`
- `proposed_payment_date`
- `commitment_date`

Campos relacionados que existen:

- `Installment.due_date`: fecha pactada de pago de la cuota. Es el campo correcto para calendario.
- `Installment.scheduled_payment_date`: fecha programada para pago automatico. No debe tratarse como compromiso principal salvo que se defina una regla de negocio distinta.
- `Credit.first_date_payment`: primera fecha de pago del credito, usada para creacion/validacion de cuotas.
- `Credit.second_date_payment`: segunda fecha de pago del credito, usada para creacion/validacion de cuotas.

### Que monto debe mostrar el calendario?

No usar `Credit.price` para el calendario diario. `price` es el valor total original del credito.

No usar `Credit.pending_amount` como monto principal del dia. `pending_amount` es el saldo total pendiente del credito, no necesariamente lo que se espera cobrar en una fecha concreta.

Para calendario se deben usar montos de cuota:

| Campo | Uso recomendado |
| --- | --- |
| `amount_due` | Monto pactado original de la cuota. |
| `amount_paid` | Monto abonado a esa cuota. |
| `remaining_amount` | Saldo pendiente real de esa cuota. |
| `late_fee` | Recargo/mora calculado para esa cuota. |
| `total_due` | Total esperado a cobrar: `remaining_amount + late_fee`. |
| `due_date` | Fecha de la cuota en formato `YYYY-MM-DD`. Coincide con la llave del `schedule`. |
| `credit_periodicity_name` | Nombre de la periodicidad del credito. |
| `credit_periodicity_days` | Dias de periodicidad. Para creditos diarios normalmente es `1`. |

Recomendacion de UI:

- Mostrar `total_due` como monto principal si la vista de recaudo debe incluir mora.
- Mostrar `remaining_amount` si la vista debe mostrar solo el valor pendiente de la cuota sin recargos.
- Mostrar `late_fee` separado para explicar cuanto corresponde a mora.

### De donde viene el estado esperado?

El estado del calendario debe venir de la cuota:

```txt
Installment.status
```

En el endpoint aparece como:

```json
{
  "status": "overdue"
}
```

Valores actuales:

| Estado | Significado |
| --- | --- |
| `pending` | Cuota pendiente. |
| `partial` | Cuota con pago parcial. |
| `overdue` | Cuota vencida. |
| `paid` | Cuota pagada. |
| `cancelled` | Cuota cancelada. |

No usar `Credit.state` para el estado de una celda o item del calendario. `Credit.state` describe el estado general del credito, por ejemplo:

- `checking`
- `pending`
- `completed`
- `to_solve`
- `preorder`

Ese estado no representa si una cuota especifica esta vencida, parcial o pendiente.

## Cobertura de fechas del endpoint

El endpoint `collector/portfolio/{seller_id}/` incluye:

- Cuotas vencidas sin limite de antiguedad.
- Cuotas con `due_date` desde hoy hasta los proximos 30 dias.

Esto permite construir:

- Agenda del dia actual.
- Vista de proximos dias.
- Vista mensual cercana.
- Seccion de vencidas acumuladas.

## Orden y prioridad

Dentro de cada fecha, las cuotas se ordenan por prioridad y luego por nombre del cliente.

Valores de `priority`:

| Prioridad | Condicion general |
| --- | --- |
| `urgent` | Mas de 30 dias de mora. |
| `high` | 7 a 30 dias de mora, o vence hoy. |
| `medium` | 1 a 7 dias de mora, o vence en los proximos 3 dias. |
| `low` | Al dia, vence en mas de 3 dias. |

Uso recomendado:

- Usar `priority` para colores, badges o orden visual.
- Usar `status` para el estado funcional de la cuota.
- Usar `days_overdue` para mensajes de vencimiento.
- Usar `grace_days_remaining` para indicar periodo de gracia.

## Periodo de gracia y mora

El campo `grace_days_remaining` indica cuantos dias quedan de gracia antes de que aplique recargo.

Reglas de UI:

- `grace_days_remaining > 0`: mostrar que la cuota esta en periodo de gracia.
- `late_fee = "0.00"` y `grace_days_remaining > 0`: no hay recargo todavia.
- `late_fee > "0.00"`: mostrar mora/recargo.

El campo `late_fee` del endpoint de cartera se calcula en tiempo real usando la cuota y la tasa de mora del credito.

## Endpoints alternativos existentes

Existen endpoints mas simples para casos puntuales:

```http
GET /fintech/collector/due-today/
GET /fintech/collector/due-tomorrow/
GET /fintech/collector/upcoming/?days=7
GET /fintech/collector/overdue/
```

Para la pantalla normal del cobrador, usar `collector/my-portfolio/`, porque ya agrupa por fecha e incluye resumen, mora, prioridad y datos del cliente. Usar `collector/portfolio/{seller_id}/` solo en pantallas administrativas o de soporte.

## Resumen de implementacion frontend

Usar:

- Endpoint principal: `/fintech/collector/my-portfolio/`
- Endpoint administrativo: `/fintech/collector/portfolio/{seller_id}/`
- Fecha calendario: llave de `schedule`, basada en `Installment.due_date`
- Monto principal: `total_due` si incluye mora, `remaining_amount` si no incluye mora
- Estado del item: `status` de la cuota
- Prioridad visual: `priority`
- Periodicidad: `credit_periodicity_days`
- Identificador de cuota: `installment_id`
- Identificador de credito: `credit_uid`

Evitar:

- `Credit.price` para monto diario.
- `Credit.pending_amount` para monto diario.
- `Credit.state` para estado de cuota.
- `Credit.next_due_date` para pintar el calendario completo.
- Agrupar eventos por `credit_uid`; en creditos diarios un mismo credito puede tener muchas cuotas. Usar `installment_id`.
