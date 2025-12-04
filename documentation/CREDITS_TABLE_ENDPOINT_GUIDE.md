# Guía de Uso: Endpoint de Tabla de Créditos

Este documento detalla cómo utilizar el endpoint de la tabla de créditos, con énfasis en las nuevas funcionalidades de filtrado por vendedor.

## 📍 Endpoint

**URL:** `/insights/credits/table/`  
**Método:** `GET`  
**Autenticación:** Requerida (`Bearer Token`)

---

## 🔍 Parámetros de Consulta (Query Params)

| Parámetro | Tipo | Requerido | Descripción | Ejemplo |
|-----------|------|-----------|-------------|---------|
| `date_from` | Date | ✅ Sí | Fecha inicio (YYYY-MM-DD) | `2025-01-01` |
| `date_to` | Date | ✅ Sí | Fecha fin (YYYY-MM-DD) | `2025-12-31` |
| `page` | Int | No | Número de página (default: 1) | `1` |
| `page_size` | Int | No | Resultados por página (default: 20) | `50` |
| `seller_id` | Int | No | **Filtrar por vendedor específico** | `45` |
| `state` | String | No | Filtrar por estado | `pending` |
| `morosidad_level`| String | No | Filtrar por nivel de mora | `mild_default` |
| `risk_level` | String | No | Filtrar por riesgo (low, medium, high)| `high` |
| `sort_by` | String | No | Campo de ordenamiento | `created_at` |
| `sort_order` | String | No | Orden (asc, desc) | `desc` |

---

## 👤 Filtrado por Vendedor (Seller)

Para implementar el filtro de vendedores en el frontend, sigue estos pasos:

### 1. Obtener la lista de vendedores disponibles

En la respuesta del endpoint, dentro de `data.distributions`, encontrarás una nueva lista llamada `credits_by_seller`. Esta lista contiene todos los vendedores que tienen créditos en el rango de fechas seleccionado.

```json
"distributions": {
    // ... otras distribuciones
    "credits_by_seller": [
        {
            "id": 45,
            "name": "Carlos Vendedor",
            "count": 80
        },
        {
            "id": 12,
            "name": "Ana Agente",
            "count": 40
        }
    ]
}
```

### 2. Mostrar el filtro en el Frontend

Usa esta lista para poblar un componente `Select` o `Dropdown`:
- **Label:** Muestra el campo `name` ("Carlos Vendedor")
- **Value:** Usa el campo `id` (45)
- **Hint:** Puedes mostrar el `count` para indicar cuántos créditos tiene ese vendedor (80)

### 3. Aplicar el filtro

Cuando el usuario seleccione un vendedor, recarga la tabla enviando el `id` seleccionado en el parámetro `seller_id`.

**Ejemplo de petición filtrada:**
`GET /insights/credits/table/?date_from=2025-01-01&date_to=2025-12-31&seller_id=45`

---

## 📦 Estructura de Respuesta (JSON)

```json
{
    "success": true,
    "data": {
        // 1. Lista de Créditos
        "credits": [
            {
                "uid": "...",
                "seller_id": 45,
                "seller_name": "Carlos Vendedor",
                // ... resto de campos del crédito
            }
        ],
        
        // 2. Resumen de Métricas
        "summary": {
            "total_credits": 120,
            "total_amount": 150000.0,
            // ...
        },
        
        // 3. Distribuciones (Para Gráficos y Filtros)
        "distributions": {
            "credits_by_state": [...],
            "credits_by_morosidad_level": [...],
            "credits_by_risk_level": [...],
            
            // ✅ NUEVO: Lista para el filtro de vendedores
            "credits_by_seller": [
                {
                    "id": 45,
                    "name": "Carlos Vendedor",
                    "count": 80
                },
                {
                    "id": 12,
                    "name": "Ana Agente",
                    "count": 40
                }
            ]
        },
        
        // 4. Paginación
        "pagination": {
            "current_page": 1,
            "total_pages": 6,
            "total_count": 120,
            "page_size": 20,
            "has_next": true,
            // ...
        }
    },
    "parameters": {
        "date_from": "2025-01-01",
        "date_to": "2025-12-31",
        "seller_id": 45, // ID del filtro aplicado
        // ...
    }
}
```
