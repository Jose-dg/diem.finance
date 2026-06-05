# Preguntas para Frontend - Calendario de Cobranza

Este documento resume las preguntas que necesitamos confirmar con frontend y la interpretacion tecnica de las consultas que estan haciendo actualmente contra el backend.

## Contexto

El frontend esta intentando construir una vista calendario para saber cuanto se espera cobrar por dia segun las cuotas pactadas de los creditos.

En los logs del backend se observo:

```txt
OPTIONS //fintech/collector/portfolio/606/ HTTP/1.1" 200 0
GET //fintech/collector/portfolio/606/ HTTP/1.1" 404 23
GET /api/orders/list/?page=1 HTTP/1.1" 404
```

## Preguntas para confirmar con frontend

### 1. Que representa el valor `606`?

Necesitamos confirmar si `606` es:

- `Seller.id`
- `User.id`
- ID del cliente
- ID del cobrador en otro sistema
- Otro identificador interno del frontend

El endpoint actual espera especificamente:

```txt
Seller.id
```

No espera `User.id`.

Ejemplo correcto:

```txt
Seller.id = 3
Seller.user_id = 606
```

La URL correcta seria:

```http
GET /fintech/collector/portfolio/3/
```

No:

```http
GET /fintech/collector/portfolio/606/
```

### 2. De donde esta saliendo el `sellerId` en frontend?

Necesitamos saber si el frontend esta usando:

- El `id` del usuario autenticado.
- Un campo `seller_id` recibido en login.
- Un valor guardado en local storage/session.
- Un parametro de ruta.
- Un valor hardcodeado o temporal.

Si el login no devuelve `seller.id`, hay que decidir como lo va a obtener frontend.

### 3. El frontend tiene disponible el perfil de vendedor/cobrador?

El backend modela al cobrador como `Seller`.

Relacion importante:

```txt
Seller.user -> User
```

Por eso frontend necesita conocer el `Seller.id` asociado al usuario autenticado.

Si hoy solo tiene `user.id`, no alcanza para llamar correctamente:

```http
GET /fintech/collector/portfolio/{seller_id}/
```

### 4. Estan construyendo la URL con doble slash?

En el log aparece:

```txt
GET //fintech/collector/portfolio/606/
```

Eso sugiere que frontend combina una base URL terminada en `/` con un path que tambien empieza por `/`.

Ejemplo problematico:

```js
const API_BASE_URL = "http://127.0.0.1:8000/";
const path = `/fintech/collector/portfolio/${sellerId}/`;
const url = `${API_BASE_URL}${path}`;
```

Resultado:

```txt
http://127.0.0.1:8000//fintech/collector/portfolio/606/
```

Recomendado:

```js
const API_BASE_URL = "http://127.0.0.1:8000";
const path = `/fintech/collector/portfolio/${sellerId}/`;
const url = `${API_BASE_URL}${path}`;
```

### 5. Por que frontend esta llamando `/api/orders/list/`?

En el backend actual no existe:

```http
GET /api/orders/list/
```

Necesitamos confirmar si esa llamada viene de:

- Codigo viejo del frontend.
- Una pantalla reutilizada de ordenes.
- Un servicio API anterior.
- Una confusion entre ordenes y creditos.

Para creditos, la ruta existente es:

```http
GET /fintech/credits/
```

Para calendario de cobranza, la ruta recomendada es:

```http
GET /fintech/collector/portfolio/{seller_id}/
```

### 6. La pantalla necesita cartera por cobrador o calendario global?

El endpoint actual esta pensado para la cartera de un cobrador:

```http
GET /fintech/collector/portfolio/{seller_id}/
```

Si frontend necesita una vista global para administradores, hay que confirmar si se espera:

- Usar un `seller_id` especifico.
- Permitir que admins consulten cualquier `seller_id`.
- Crear un endpoint global sin `seller_id`.
- Crear un endpoint que use el usuario autenticado y no reciba parametros.

## Mi lectura tecnica de los logs

### `OPTIONS 200`

```txt
OPTIONS //fintech/collector/portfolio/606/ HTTP/1.1" 200 0
```

Esto solo significa que el preflight de CORS respondio bien.

No confirma que el `GET` vaya a encontrar datos.

### `GET 404 23` en portfolio

```txt
GET //fintech/collector/portfolio/606/ HTTP/1.1" 404 23
```

Mi interpretacion mas probable es:

- La ruta existe.
- La vista se ejecuto.
- La vista intento buscar `Seller.id = 606`.
- No encontro ese seller.
- Django REST Framework respondio `{"detail":"Not found."}`.

El tamano `23` coincide con una respuesta corta tipo:

```json
{"detail":"Not found."}
```

Por eso no parece un problema principal de routing. Parece un problema de identificador.

### `GET /api/orders/list/ 404`

```txt
GET /api/orders/list/?page=1 HTTP/1.1" 404
```

Mi interpretacion:

- Ese endpoint no pertenece al backend actual.
- Frontend esta llamando una ruta vieja o incorrecta.
- Para esta funcionalidad no debe depender de `/api/orders/list/`.

## Recomendacion para frontend

Para la vista calendario, frontend deberia:

1. Obtener el `seller.id` real del usuario cobrador.
2. Construir la URL sin doble slash.
3. Llamar:

```http
GET /fintech/collector/portfolio/{seller_id}/
Authorization: Bearer <token>
```

4. Leer los compromisos desde:

```js
response.schedule["YYYY-MM-DD"]
```

5. Calcular el total esperado con:

```js
items.reduce((total, item) => total + Number(item.total_due), 0)
```

## Mejora backend implementada

Para reducir errores de integracion, se creo un endpoint que no requiere `seller_id`:

```http
GET /fintech/collector/my-portfolio/
```

Ese endpoint usaria el usuario autenticado:

```python
request.user.seller_profile
```

Ventaja:

- Frontend no tendria que saber el `Seller.id`.
- Evita confundir `User.id` con `Seller.id`.
- Reduce errores 404 por identificador incorrecto.

El endpoint anterior sigue existiendo para administracion y soporte:

```http
GET /fintech/collector/portfolio/{seller_id}/
```

Frontend debe usar `my-portfolio` para la pantalla normal de calendario.

## Resumen para enviar a frontend

Por favor confirmen:

- Que representa el `606` que estan enviando.
- De donde sale ese valor en el codigo frontend.
- Si tienen disponible `seller.id` o solo `user.id`.
- Por que se sigue llamando `/api/orders/list/`.
- Si la vista debe ser por cobrador o global/admin.
- Que van a cambiar la pantalla normal para consumir `/fintech/collector/my-portfolio/`.
