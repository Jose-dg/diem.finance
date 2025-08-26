# Documentación de Endpoints del Dashboard de Insights

## Vista 1: Lista Completa de Créditos con Cálculos

### Endpoint: `/api/credits/dashboard/`

**Descripción:** Retorna todos los créditos con información calculada y enriquecida para el dashboard principal.

**Método:** GET

**Permisos:** IsAuthenticated

**Parámetros de consulta:**
- `page`: Número de página (default: 1)
- `page_size`: Elementos por página (default: 50, max: 200)
- `ordering`: Campo para ordenar (default: '-created_at')

**Ejemplo de respuesta:**
```json
{
  "count": 1250,
  "next": "http://api.example.com/api/credits/dashboard/?page=3",
  "previous": "http://api.example.com/api/credits/dashboard/?page=1",
  "page_info": {
    "current_page": 2,
    "total_pages": 25,
    "page_size": 50,
    "has_next": true,
    "has_previous": true
  },
  "results": [
    {
      "uid": "uuid-del-credito",
      "client_info": {
        "id": "user_id",
        "full_name": "Nombre Apellido",
        "username": "username_fallback",
        "document_number": "12345678",
        "phone": "+57 300 123 4567"
      },
      "credit_details": {
        "subcategory": "Nombre subcategoría",
        "price": "1000000.00",
        "cost": "800000.00",
        "earnings": "200000.00",
        "currency": "COP",
        "state": "pending",
        "morosidad_level": "on_time",
        "created_at": "2024-01-15T10:30:00Z"
      },
      "payment_info": {
        "total_abonos": "300000.00",
        "pending_amount": "700000.00",
        "percentage_paid": 30.0,
        "payment_method": "Nombre método de pago"
      },
      "installment_info": {
        "periodicity_name": "Semanal",
        "periodicity_days": 7,
        "total_installments": 10,
        "installment_value": "100000.00",
        "paid_installments": 3,
        "overdue_installments": 1,
        "next_due_date": "2024-02-01"
      },
      "calculated_metrics": {
        "interest_rate": "2.5",
        "credit_days": 70,
        "days_since_creation": 45,
        "average_payment_delay": 3.2,
        "risk_score": 7.5
      },
      "seller_info": {
        "seller_name": "Nombre Vendedor",
        "seller_id": "seller_uuid"
      }
    }
  ]
}
```

**Ejemplos de uso:**
```bash
# Obtener primera página con 25 elementos
GET /api/credits/dashboard/?page=1&page_size=25

# Ordenar por precio descendente
GET /api/credits/dashboard/?ordering=-price

# Obtener página específica
GET /api/credits/dashboard/?page=3&page_size=100
```

---

## Vista 2: Recaudo Esperado con Proyecciones

### Endpoint: `/api/installments/expected-collection/`

**Descripción:** Retorna todas las cuotas programadas con información detallada para análisis de recaudo.

**Método:** GET

**Permisos:** IsAuthenticated

**Parámetros de consulta:**
- `page`: Número de página (default: 1)
- `page_size`: Elementos por página (default: 50, max: 200)
- `ordering`: Campo para ordenar (default: 'due_date')

**Ejemplo de respuesta:**
```json
{
  "count": 850,
  "next": "http://api.example.com/api/installments/expected-collection/?page=2",
  "previous": null,
  "page_info": {
    "current_page": 1,
    "total_pages": 17,
    "page_size": 50,
    "has_next": true,
    "has_previous": false
  },
  "results": [
    {
      "id": "installment_id",
      "credit_info": {
        "credit_uid": "uuid-del-credito",
        "client_full_name": "Nombre Cliente",
        "client_id": "user_id",
        "subcategory": "Tipo de crédito",
        "credit_state": "pending"
      },
      "installment_details": {
        "number": 3,
        "due_date": "2024-02-01",
        "amount": "100000.00",
        "amount_paid": "50000.00",
        "remaining_amount": "50000.00",
        "status": "partial",
        "late_fee": "5000.00",
        "percentage_paid": 50.0
      },
      "payment_tracking": {
        "paid_on": "2024-01-28",
        "days_overdue": 5,
        "is_overdue": true,
        "principal_amount": "45000.00",
        "interest_amount": "5000.00"
      },
      "periodicity_info": {
        "periodicity_name": "Semanal",
        "periodicity_days": 7,
        "currency": "COP"
      },
      "calculated_metrics": {
        "days_until_due": -5,
        "collection_priority": "high",
        "expected_collection_date": "2024-02-05",
        "risk_level": "medium",
        "payment_reliability": "medium"
      },
      "client_history": {
        "total_overdue_installments": 2,
        "average_delay_days": 4.5
      }
    }
  ]
}
```

**Ejemplos de uso:**
```bash
# Obtener cuotas ordenadas por fecha de vencimiento
GET /api/installments/expected-collection/?ordering=due_date

# Obtener cuotas con prioridad alta
GET /api/installments/expected-collection/?page_size=100

# Obtener cuotas vencidas
GET /api/installments/expected-collection/?ordering=due_date
```

---

## Vista 3: Métricas Resumidas del Dashboard

### Endpoint: `/api/dashboard/summary/`

**Descripción:** Retorna métricas calculadas para mostrar en la parte superior del dashboard.

**Método:** GET

**Permisos:** IsAuthenticated

**Ejemplo de respuesta:**
```json
{
  "success": true,
  "data": {
    "credits_summary": {
      "total_active_credits": 150,
      "total_amount_lent": "15000000.00",
      "total_pending_amount": "8500000.00",
      "total_collected": "6500000.00",
      "average_credit_amount": "100000.00",
      "collection_percentage": 43.33
    },
    "installments_summary": {
      "due_today": 25,
      "due_this_week": 87,
      "overdue_total": 45,
      "expected_collection_today": "500000.00",
      "expected_collection_week": "2100000.00"
    },
    "performance_metrics": {
      "on_time_payment_rate": 78.5,
      "average_delay_days": 5.2,
      "default_rate": 8.3,
      "recovery_rate": 85.7
    },
    "by_periodicity": [
      {
        "periodicity": "Semanal",
        "total_credits": 80,
        "pending_amount": "4000000.00",
        "overdue_percentage": 12.5
      },
      {
        "periodicity": "Quincenal",
        "total_credits": 45,
        "pending_amount": "2500000.00",
        "overdue_percentage": 8.9
      }
    ],
    "alerts": [
      {
        "type": "high_risk",
        "message": "15 créditos con más de 30 días de mora",
        "count": 15
      },
      {
        "type": "overdue_payments",
        "message": "23 cuotas vencidas por más de 7 días",
        "count": 23
      }
    ]
  }
}
```

---

## Vista 4: Analytics Avanzados de Créditos

### Endpoint: `/api/credits/analytics/`

**Descripción:** Retorna analytics detallados de créditos con filtros y agrupaciones.

**Método:** GET

**Permisos:** IsAuthenticated

**Parámetros de consulta:**
- `days`: Días para análisis temporal (default: 30)
- `periodicity`: Filtro por periodicidad
- `state`: Filtro por estado del crédito

**Ejemplo de respuesta:**
```json
{
  "success": true,
  "data": {
    "analytics_by_state": [
      {
        "state": "pending",
        "count": 150,
        "total_amount": "15000000.00",
        "avg_amount": "100000.00",
        "total_pending": "8500000.00"
      }
    ],
    "analytics_by_periodicity": [
      {
        "periodicity__name": "Semanal",
        "count": 80,
        "total_amount": "8000000.00",
        "avg_amount": "100000.00",
        "overdue_count": 10
      }
    ],
    "analytics_by_subcategory": [
      {
        "subcategory__name": "Préstamo Personal",
        "count": 45,
        "total_amount": "4500000.00",
        "avg_amount": "100000.00"
      }
    ],
    "temporal_analytics": [
      {
        "day": "2024-01-15",
        "count": 5,
        "total_amount": "500000.00"
      }
    ],
    "filters_applied": {
      "days": 30,
      "periodicity": null,
      "state": null
    }
  }
}
```

---

## Vista 5: Análisis de Riesgo

### Endpoint: `/api/risk/analysis/`

**Descripción:** Retorna análisis detallado de riesgo para administradores.

**Método:** GET

**Permisos:** IsAuthenticated, IsAdminUser

**Ejemplo de respuesta:**
```json
{
  "success": true,
  "data": {
    "risk_by_morosidad": [
      {
        "morosidad_level": "on_time",
        "count": 120,
        "total_amount": "12000000.00",
        "total_pending": "6000000.00",
        "avg_delay": 0.0
      }
    ],
    "high_risk_credits_count": 15,
    "overdue_analysis": [
      {
        "credit__morosidad_level": "severe_default",
        "count": 25,
        "total_amount": "2500000.00",
        "avg_days_overdue": 45.2
      }
    ],
    "potential_losses": "3500000.00",
    "risk_alerts": [
      {
        "type": "high_risk",
        "message": "15 créditos con más de 30 días de mora",
        "count": 15
      }
    ]
  }
}
```

---

## Optimizaciones Implementadas

### 1. Querysets Optimizados
- Uso de `select_related()` para relaciones ForeignKey
- Uso de `prefetch_related()` para relaciones Many-to-Many
- Uso de `annotate()` para cálculos en base de datos

### 2. Paginación Configurable
- Tamaño de página configurable (1-200 elementos)
- Información detallada de paginación
- Navegación eficiente

### 3. Cálculos en Base de Datos
- Métricas calculadas usando agregaciones de Django ORM
- Reducción de consultas N+1
- Cálculos optimizados para grandes volúmenes de datos

### 4. Manejo de Errores
- Respuestas consistentes con estructura de error
- Logs detallados para debugging
- Validación de parámetros de entrada

### 5. Métodos de Modelo
- Propiedades calculadas en los modelos
- Cálculos reutilizables
- Lógica de negocio encapsulada

---

## Consideraciones de Performance

### Índices Recomendados
```sql
-- Índices para optimizar consultas frecuentes
CREATE INDEX idx_credit_state ON fintech_credit(state);
CREATE INDEX idx_credit_created_at ON fintech_credit(created_at);
CREATE INDEX idx_installment_due_date ON fintech_installment(due_date);
CREATE INDEX idx_installment_status ON fintech_installment(status);
CREATE INDEX idx_credit_morosidad ON fintech_credit(morosidad_level);
```

### Cache Recomendado
- Cachear resultados de métricas que no cambian frecuentemente
- Usar cache de Redis para datos de resumen
- Implementar cache de consultas complejas

### Monitoreo
- Monitorear tiempo de respuesta de endpoints
- Alertas para consultas lentas
- Métricas de uso de base de datos
