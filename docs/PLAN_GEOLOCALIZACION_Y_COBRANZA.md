# Plan de Implementación — App `interactions`
## Geolocalización y Control de Cobranza de Campo

_Última revisión: 2026-04-26_

---

## Propósito

Vincular coordenadas GPS reales a los tres eventos críticos del ciclo de crédito:
- **Entrega del crédito** — dónde se hizo el desembolso
- **Visita de cobro** — dónde estaba el cliente cuando se fue a cobrar
- **Cobro efectivo** — dónde ocurrió el pago

El GPS se captura automáticamente en el momento de cada acción desde el dispositivo del cobrador. No es auto-reporte: el cobrador no puede manipular o elegir la ubicación — el sistema la toma. Esto sirve para dos cosas:
1. **Localizar al cliente**: acumulamos dónde ha sido encontrado realmente, no dónde dice que vive
2. **Anti-fraude**: un cobro registrado lejos de cualquier ubicación histórica del cliente es una alerta

---

## Decisión de nombre

**`interactions`** — agrupa todos los eventos de contacto con el cliente (visitas, cobros, entregas) independientemente del canal.

---

## Estrategia de claves primarias

- `id`: `BigAutoField` — joins internos con `fintech`
- `uid`: `UUIDField` — en `InteractionLog` para idempotencia offline

---

## Modelo de datos

### `CollectionPoint`

Representa una ubicación real donde el cliente ha sido encontrado o donde se realizó un evento. **No es ingresada manualmente** — se construye automáticamente a partir de los GPS capturados en `InteractionLog`. Un cliente acumula múltiples puntos según el historial de visitas.

| Campo | Tipo | Notas |
|---|---|---|
| `id` | BigAutoField PK | |
| `client` | FK → `settings.AUTH_USER_MODEL` | Cliente al que pertenece |
| `label` | CharField choices | `credit_delivery`, `visit`, `payment` |
| `latitude` | DecimalField(9,6) | Capturado automáticamente |
| `longitude` | DecimalField(9,6) | Capturado automáticamente |
| `address_text` | CharField blank | Geocodificación inversa opcional |
| `interaction` | OneToOneField → `InteractionLog` | El evento que originó este punto |
| `created_at` | DateTimeField auto | |

Un `CollectionPoint` se crea automáticamente (signal post-save) cuando llega un `InteractionLog` con GPS. No hay endpoint para crearlo manualmente.

---

### `InteractionLog`

Registro inmutable de cada evento. Una vez creado, no se modifica.

| Campo | Tipo | Notas |
|---|---|---|
| `id` | BigAutoField PK | |
| `uid` | UUIDField unique | Generado en cliente para idempotencia |
| `agent` | FK → `fintech.Seller` | Cobrador que ejecutó la acción |
| `credit` | FK → `fintech.Credit` | Crédito gestionado |
| `interaction_type` | CharField choices | Ver tabla abajo |
| `latitude` | DecimalField(9,6) null | GPS automático del dispositivo |
| `longitude` | DecimalField(9,6) null | GPS automático del dispositivo |
| `distance_variance` | IntegerField null | Metros vs. punto histórico más cercano del cliente |
| `promise_date` | DateField null | Solo si `interaction_type = promise` |
| `promise_fulfilled` | BooleanField null | Se actualiza cuando vence la promesa |
| `notes` | TextField blank | Observaciones del cobrador |
| `source` | CharField choices | `mobile`, `office` |
| `captured_at` | DateTimeField | Timestamp del dispositivo (puede ser offline) |
| `synced_at` | DateTimeField auto_now_add | Timestamp del servidor al recibir |
| `sync_lag_seconds` | IntegerField null | `(synced_at - captured_at).seconds` — detecta trampas de fecha |
| `offline_sync` | BooleanField default=False | True si vino de cola offline |
| `transaction` | FK → `fintech.Transaction` null | Solo si hubo cobro efectivo |

**Tipos de interacción:**

| Código | Descripción | ¿GPS requerido? | ¿Crea `CollectionPoint`? |
|---|---|---|---|
| `credit_delivery` | Entrega/desembolso del crédito | Sí | Sí |
| `payment_full` | Cobro completo en campo | Sí | Sí |
| `payment_partial` | Cobro parcial en campo | Sí | Sí |
| `office_payment` | Pago en oficina | No | No |
| `visit` | Visita sin cobro (ausente, negativa) | Sí | Sí |
| `promise` | Promesa de pago | Sí | Sí |
| `call` | Llamada telefónica | No | No |

**Regla de negocio clave**: si `interaction_type` es `payment_*` y `transaction` es null, la señal post-save rechaza el registro. Un cobro en campo siempre necesita respaldo contable.

---

## Lógica automática (signals)

```
InteractionLog.post_save
  ├── Si tiene GPS y interaction_type crea punto:
  │     → crear CollectionPoint vinculado a credit.client
  ├── Si interaction_type = payment_* y transaction is None:
  │     → raise ValidationError ("cobro sin transacción contable")
  ├── Calcular distance_variance:
  │     → buscar CollectionPoint más cercano del cliente (Haversine)
  │     → guardar distancia en metros
  └── Calcular sync_lag_seconds:
        → (synced_at - captured_at).total_seconds()
```

---

## Fases de implementación

### FASE 1 — Modelos y signals
- Crear app `interactions`
- Definir `CollectionPoint` e `InteractionLog`
- Implementar signals (auto-creación de punto, validación de cobro, cálculo de distancia)
- Agregar a `INSTALLED_APPS` y migrar

### FASE 2 — API offline-first

**`POST /interactions/sync/`**
Recibe array de interacciones pendientes. Idempotente por `uid`.

Payload mínimo:
```json
[
  {
    "uid": "uuid-generado-en-dispositivo",
    "credit_uid": "uuid-del-credito",
    "interaction_type": "visit",
    "latitude": 4.6097,
    "longitude": -74.0817,
    "captured_at": "2026-04-26T10:15:00",
    "offline_sync": true,
    "notes": "No estaba en casa"
  }
]
```

Respuesta:
```json
{ "processed": 2, "skipped_duplicates": 1, "errors": [] }
```
Nunca expone `id` interno — solo `uid`.

**`GET /interactions/credit/<uid>/`**
Historial de interacciones de un crédito: qué visitas se han hecho, cuándo, desde dónde.

**`GET /interactions/client/<uid>/locations/`**
Puntos GPS históricos del cliente: dónde ha sido encontrado. El cobrador los consulta antes de salir para saber a dónde ir.

### FASE 3 — Observabilidad en dashboards (`insights`)

1. **Mapa de ubicaciones por cliente**: todos los `CollectionPoint` del cliente — dónde ha sido encontrado realmente vs. dirección declarada
2. **Alertas de distancia**: `distance_variance > 500m` en un cobro → alerta para el supervisor
3. **Alertas de rezago**: `sync_lag_seconds > 86400` (más de 24h) → posible trampa de fecha
4. **KPIs por cobrador**: visitas totales, cobros efectivos, promesas generadas vs. cumplidas
5. **Créditos sin ningún `CollectionPoint`**: cartera sin ubicación conocida del cliente — riesgo alto de incobrabilidad

### FASE 4 — Maduración operacional

- Notificaciones push cuando vence un `promise_date` sin pago registrado
- Generación automática de lista de visitas del día por cobrador (cuotas vencidas o próximas a vencer sin `InteractionLog` reciente)
- `django-simple-history` en `InteractionLog` para auditoría regulatoria

---

## Consideraciones de arquitectura

- **`interactions` no modifica `fintech/models.py`**: las FKs apuntan hacia `fintech`, pero `fintech` no importa nada de `interactions`
- **Usar `settings.AUTH_USER_MODEL`** en toda FK a usuario — nunca el modelo directo
- **`CollectionPoint` se construye, no se declara**: nadie ingresa coordenadas manualmente; salen de eventos reales capturados en campo
- **El cobrador organiza su ruta libremente**: el sistema no impone orden de visitas. Lo que sí impone es que cualquier acción (cobro, visita) capture GPS — así el cobrador no puede registrar eventos sin estar presente físicamente
