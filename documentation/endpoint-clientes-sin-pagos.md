# Endpoint: Clientes Sin Pagos

## Descripción
Nuevo endpoint que permite obtener la lista específica de clientes que no han realizado ningún pago en un período determinado. Esto complementa el endpoint existente que solo mostraba la cantidad de clientes sin pagos.

## URL
```
GET /insights/credits/analysis/clients-without-payments/
```

## Parámetros Requeridos
- `start_date`: Fecha de inicio en formato YYYY-MM-DD
- `end_date`: Fecha de fin en formato YYYY-MM-DD

## Parámetros Opcionales
- `limit`: Número máximo de clientes a retornar (default: 100, máximo: 500)
- `sort_by`: Campo para ordenar los resultados
  - `total_requested`: Por monto total solicitado
  - `total_pending`: Por monto pendiente
  - `days_since_first_credit`: Por días desde el primer crédito
  - `avg_days_overdue`: Por días promedio de mora
  - `overdue_installments_count`: Por cantidad de cuotas vencidas
- `include_summary`: Incluir resumen estadístico (true/false, default: true)

## Ejemplo de Uso

### Solicitud
```bash
GET /insights/credits/analysis/clients-without-payments/?start_date=2024-01-01&end_date=2024-01-31&limit=50&sort_by=total_requested&include_summary=true
```

### Respuesta
```json
{
  "success": true,
  "data": {
    "clients": [
      {
        "client_id": 123,
        "username": "cliente_ejemplo",
        "full_name": "Juan Pérez",
        "email": "juan.perez@email.com",
        "phone": "+1234567890",
        "total_credits": 2,
        "total_requested": 500000.00,
        "total_pending": 500000.00,
        "avg_credit_amount": 250000.00,
        "max_credit_amount": 300000.00,
        "min_credit_amount": 200000.00,
        "first_credit_date": "2024-01-15T10:30:00Z",
        "last_credit_date": "2024-01-20T14:45:00Z",
        "total_installments": 8,
        "overdue_installments": 3,
        "overdue_installments_count": 3,
        "avg_days_overdue": 15.5,
        "subcategories_count": 2,
        "subcategories_detail": [
          {
            "subcategory__name": "Préstamo Personal",
            "count": 1,
            "total_amount": 300000.00
          },
          {
            "subcategory__name": "Préstamo Vehículo",
            "count": 1,
            "total_amount": 200000.00
          }
        ],
        "risk_level": "HIGH",
        "payment_status": "NO_PAYMENTS",
        "days_since_first_credit": 16
      }
    ],
    "total_clients": 1,
    "summary": {
      "total_clients_without_payments": 1,
      "total_credits": 2,
      "total_requested_amount": 500000.00,
      "total_pending_amount": 500000.00,
      "average_days_overdue": 15.5,
      "risk_distribution": {
        "HIGH": 1
      },
      "period": {
        "start_date": "2024-01-01",
        "end_date": "2024-01-31"
      }
    }
  },
  "parameters": {
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "limit": 50,
    "sort_by": "total_requested",
    "include_summary": true
  }
}
```

## Información Detallada por Cliente

Cada cliente en la respuesta incluye:

### Información Básica
- `client_id`: ID único del cliente
- `username`: Nombre de usuario
- `full_name`: Nombre completo
- `email`: Correo electrónico
- `phone`: Teléfono

### Información de Créditos
- `total_credits`: Número total de créditos en el período
- `total_requested`: Monto total solicitado
- `total_pending`: Monto total pendiente
- `avg_credit_amount`: Monto promedio por crédito
- `max_credit_amount`: Monto máximo de un crédito
- `min_credit_amount`: Monto mínimo de un crédito

### Información Temporal
- `first_credit_date`: Fecha del primer crédito en el período
- `last_credit_date`: Fecha del último crédito en el período
- `days_since_first_credit`: Días transcurridos desde el primer crédito

### Información de Cuotas
- `total_installments`: Total de cuotas generadas
- `overdue_installments`: Cuotas vencidas
- `overdue_installments_count`: Cantidad de cuotas vencidas
- `avg_days_overdue`: Días promedio de mora

### Información de Categorías
- `subcategories_count`: Número de subcategorías diferentes
- `subcategories_detail`: Detalle por subcategoría con montos

### Información de Riesgo
- `risk_level`: Nivel de riesgo (LOW/MEDIUM/HIGH)
- `payment_status`: Estado de pagos (siempre "NO_PAYMENTS")

## Resumen Estadístico

Cuando `include_summary=true`, se incluye un resumen con:
- Total de clientes sin pagos
- Total de créditos
- Montos totales solicitados y pendientes
- Promedio de días de mora
- Distribución por nivel de riesgo
- Período analizado

## Casos de Uso

1. **Seguimiento de Morosidad**: Identificar clientes que no han realizado ningún pago
2. **Gestión de Cobranza**: Priorizar clientes para contactar
3. **Análisis de Riesgo**: Evaluar el nivel de riesgo de clientes sin pagos
4. **Reportes Ejecutivos**: Generar reportes detallados de clientes problemáticos
5. **Análisis de Tendencias**: Entender patrones de no pago por período

## Diferencias con el Endpoint Existente

| Aspecto | Endpoint Existente | Nuevo Endpoint |
|---------|-------------------|----------------|
| Información | Solo cantidad | Lista detallada de clientes |
| Detalles | Resumen general | Información completa por cliente |
| Filtros | Limitados | Múltiples opciones de ordenamiento |
| Resumen | Básico | Estadísticas detalladas |
| Casos de Uso | Dashboard general | Gestión específica de morosidad |

## Permisos
- Requiere autenticación (`IsAuthenticated`)
- Requiere permisos de administrador (`IsAdminUser`)

## Límites
- Máximo 500 clientes por consulta
- Límite por defecto: 100 clientes
- Timeout recomendado: 30 segundos para consultas grandes
