# Guía del Frontend - Endpoint de Tabla de Créditos

## 🎯 Endpoint Implementado

**URL:** `GET /insights/credits/table/`

Este endpoint proporciona datos estructurados para construir una tabla de créditos completa y un dashboard robusto de análisis de riesgo. Complementa la funcionalidad existente de la "tabla de clientes" y proporciona insights detallados sobre el comportamiento de los créditos individuales.

## 📋 Parámetros de Consulta

### Parámetros Requeridos:
- **`date_from`** (string): Fecha de inicio del período (YYYY-MM-DD)
- **`date_to`** (string): Fecha de fin del período (YYYY-MM-DD)

### Parámetros Opcionales:
- **`page`** (integer): Número de página (default: 1)
- **`page_size`** (integer): Tamaño de página (default: 20, máximo: 100)
- **`state`** (string): Filtrar por estado del crédito (checking, pending, completed, to_solve, preorder)
- **`morosidad_level`** (string): Filtrar por nivel de morosidad
- **`risk_level`** (string): Filtrar por nivel de riesgo (low, medium, high)
- **`seller_id`** (integer): Filtrar por vendedor específico
- **`sort_by`** (string): Campo de ordenamiento (default: 'created_at')
- **`sort_order`** (string): Orden (asc, desc, default: 'desc')

## 🔧 Ejemplo de Uso

```javascript
// Ejemplo básico
const response = await fetch('/insights/credits/table/?date_from=2025-09-01&date_to=2025-09-12&page=1&page_size=20', {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
});

// Ejemplo con filtros avanzados
const params = new URLSearchParams({
    date_from: '2025-09-01',
    date_to: '2025-09-12',
    page: 1,
    page_size: 50,
    state: 'pending',
    risk_level: 'high',
    sort_by: 'risk_score',
    sort_order: 'desc'
});

const response = await fetch(`/insights/credits/table/?${params}`, {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
});
```

## 📊 Estructura de Respuesta

```json
{
    "success": true,
    "data": {
        "credits": [
            {
                "uid": "uuid-string",
                "state": "pending",
                "user_full_name": "Juan Pérez",
                "user_username": "jperez",
                "seller_name": "María García",
                "price": 1000000.00,
                "pending_amount": 750000.00,
                "percentage_paid": 25.0,
                "risk_score": 75,
                "morosidad_level": "mild_default",
                "is_high_risk": true,
                "collection_priority": "high",
                "days_since_creation": 45,
                "overdue_installments_count": 2,
                "next_due_date": "2025-10-15",
                "expected_completion_date": "2026-03-15",
                "profitability_score": 85.5,
                "created_at": "2025-08-01T10:30:00Z",
                "updated_at": "2025-09-11T15:45:00Z"
            }
        ],
        "summary": {
            "total_credits": 150,
            "total_amount": 150000000.00,
            "total_pending": 45000000.00,
            "total_paid": 105000000.00,
            "average_risk_score": 45.2,
            "high_risk_credits_count": 23,
            "default_rate": 15.3
        },
        "distributions": {
            "credits_by_state": [...],
            "credits_by_morosidad_level": [...],
            "credits_by_risk_level": [...]
        },
        "pagination": {
            "current_page": 1,
            "total_pages": 8,
            "total_count": 150,
            "page_size": 20,
            "has_next": true,
            "has_previous": false
        }
    },
    "parameters": {
        "date_from": "2025-09-01",
        "date_to": "2025-09-12",
        "page": 1,
        "page_size": 20
    }
}
```

## 🎨 Campos Disponibles para la Tabla

### Información Básica:
- `uid`, `state`, `created_at`, `updated_at`, `description`

### Información del Usuario:
- `user_id`, `user_full_name`, `user_username`, `user_email`

### Información Financiera:
- `price`, `pending_amount`, `percentage_paid`, `total_abonos`, `cost`, `earnings`

### Información de Riesgo:
- `risk_score`, `morosidad_level`, `is_high_risk`, `collection_priority`

### Información de Cuotas:
- `total_installments_count`, `paid_installments_count`, `overdue_installments_count`

### Información de Fechas:
- `next_due_date`, `expected_completion_date`, `days_since_creation`

## ⚡ Optimizaciones Implementadas

- **Paginación eficiente** con LIMIT y OFFSET
- **Queries optimizadas** con select_related() para evitar N+1 queries
- **Filtrado avanzado** con múltiples criterios
- **Ordenamiento** por múltiples campos
- **Métricas calculadas** en tiempo real

## 🚨 Manejo de Errores

```javascript
try {
    const response = await fetch('/insights/credits/table/?date_from=2025-09-01&date_to=2025-09-12');
    const data = await response.json();
    
    if (!data.success) {
        console.error('Error:', data.error);
        // Manejar error
    } else {
        // Procesar datos exitosamente
        console.log('Credits:', data.data.credits);
        console.log('Summary:', data.data.summary);
    }
} catch (error) {
    console.error('Network error:', error);
}
```

## 🔐 Autenticación

El endpoint requiere:
- Usuario autenticado
- Permisos de administrador (`IsAdminUser`)

## 📈 Casos de Uso Recomendados

1. **Dashboard de Riesgo**: Usar `risk_score` y `is_high_risk` para identificar créditos problemáticos
2. **Tabla de Recaudo**: Usar `collection_priority` y `overdue_installments_count` para priorizar cobros
3. **Análisis de Rentabilidad**: Usar `profitability_score` y `earnings` para evaluar rendimiento
4. **Seguimiento Temporal**: Usar `days_since_creation` y `expected_completion_date` para control de tiempos

Este endpoint está listo para ser integrado en el frontend y proporcionará una base sólida para el dashboard de riesgo y análisis de créditos.
