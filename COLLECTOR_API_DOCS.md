# API para Cobradores/Asesores

## 📋 Endpoints Disponibles

### 1. Dashboard Principal
**GET** `/api/collector/dashboard/`

Resumen general para cobradores con estadísticas de cuotas.

**Respuesta:**
```json
{
    "summary": {
        "due_today": 15,
        "due_tomorrow": 8,
        "overdue": 23,
        "total_pending": 156
    },
    "date": "2024-01-15"
}
```

### 2. Cuotas que Vencen Hoy
**GET** `/api/collector/due-today/`

Lista de cuotas que vencen hoy.

**Respuesta:**
```json
{
    "count": 15,
    "date": "2024-01-15",
    "installments": [
        {
            "id": 123,
            "number": 5,
            "due_date": "2024-01-15",
            "amount": "1000.00",
            "status": "pending",
            "credit_uid": "550e8400-e29b-41d4-a716-446655440000",
            "user_name": "Juan Pérez",
            "remaining_amount_calc": "1000.00",
            "days_overdue_calc": 0,
            "late_fee_calc": "0.00",
            "total_amount_due": "1000.00"
        }
    ]
}
```

### 3. Cuotas que Vencen Mañana
**GET** `/api/collector/due-tomorrow/`

Lista de cuotas que vencen mañana.

**Respuesta:** Similar a due-today pero con fecha de mañana.

### 4. Cuotas Próximas a Vencer
**GET** `/api/collector/upcoming/?days=7`

Lista de cuotas que vencen en los próximos días.

**Parámetros:**
- `days` (opcional): Número de días hacia adelante (default: 7)

**Respuesta:**
```json
{
    "count": 45,
    "start_date": "2024-01-15",
    "end_date": "2024-01-22",
    "days_ahead": 7,
    "installments": [...]
}
```

### 5. Cuotas Vencidas
**GET** `/api/collector/overdue/`

Lista de cuotas que ya vencieron y están pendientes.

**Respuesta:**
```json
{
    "count": 23,
    "date": "2024-01-15",
    "installments": [
        {
            "id": 456,
            "number": 3,
            "due_date": "2024-01-10",
            "amount": "1500.00",
            "status": "pending",
            "credit_uid": "550e8400-e29b-41d4-a716-446655440001",
            "user_name": "María García",
            "remaining_amount_calc": "1500.00",
            "days_overdue_calc": 5,
            "late_fee_calc": "37.50",
            "total_amount_due": "1537.50"
        }
    ]
}
```

## 🔐 Autenticación

Todas las APIs requieren autenticación JWT:

```bash
# Obtener token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "tu_usuario", "password": "tu_password"}'

# Usar token
curl -X GET http://localhost:8000/api/collector/due-today/ \
  -H "Authorization: Bearer TU_TOKEN_JWT"
```

## 📊 Campos de Respuesta

### Campos de Cuota:
- `id`: ID de la cuota
- `number`: Número de cuota
- `due_date`: Fecha de vencimiento
- `amount`: Monto original
- `status`: Estado (pending, paid, overdue, partial)
- `credit_uid`: UUID del crédito
- `user_name`: Nombre completo del cliente

### Campos Calculados:
- `remaining_amount_calc`: Monto restante por pagar
- `days_overdue_calc`: Días de mora
- `late_fee_calc`: Recargo por mora
- `total_amount_due`: Total a pagar (incluye recargos)

## 🚀 Ejemplos de Uso

### 1. Ver cuotas que vencen hoy:
```bash
curl -X GET http://localhost:8000/api/collector/due-today/ \
  -H "Authorization: Bearer TU_TOKEN"
```

### 2. Ver cuotas próximas a vencer (15 días):
```bash
curl -X GET "http://localhost:8000/api/collector/upcoming/?days=15" \
  -H "Authorization: Bearer TU_TOKEN"
```

### 3. Ver dashboard completo:
```bash
curl -X GET http://localhost:8000/api/collector/dashboard/ \
  -H "Authorization: Bearer TU_TOKEN"
```

## ⚡ Optimizaciones

- **Cache inteligente**: Los cálculos se cachean por 1 hora
- **Consultas optimizadas**: Solo se cargan campos necesarios
- **Paginación**: Las respuestas están paginadas
- **Cálculos en background**: Los campos se calculan automáticamente

## 🔄 Actualización Automática

Los datos se actualizan automáticamente:
- **Diario a las 2 AM**: Cálculo masivo de campos
- **Diario a las 6 AM**: Actualización de cuotas vencidas
- **Diario a las 8 AM**: Actualización de estados de créditos
- **En tiempo real**: Al hacer cambios en cuotas 