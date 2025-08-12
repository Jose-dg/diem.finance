# API Endpoints - Análisis de Créditos
## Documentación Técnica para Frontend

### Información General

**Base URL:** `http://localhost:8000/insights/`  
**Content-Type:** `application/json`  
**Autenticación:** Bearer Token (JWT)  
**Versión:** 1.0

---

## 🔐 Autenticación

Todas las peticiones requieren autenticación mediante JWT Bearer Token en el header:

```http
Authorization: Bearer <your_jwt_token>
```

### Permisos Requeridos:
- **Vistas principales:** Requieren permisos de administrador
- **Vista de resumen:** Solo requiere autenticación básica

---

## 📊 Endpoint 1: Análisis Completo de Créditos

### `GET /insights/credits/analysis/`

**Descripción:** Obtiene un análisis completo de créditos incluyendo resumen, tabla de clientes, análisis de pagos y análisis de morosidad.

**Permisos:** Requiere permisos de administrador

### Parámetros de Query:

| Parámetro | Tipo | Requerido | Descripción | Ejemplo |
|-----------|------|-----------|-------------|---------|
| `start_date` | string | ✅ | Fecha de inicio (YYYY-MM-DD) | `2025-05-01` |
| `end_date` | string | ✅ | Fecha de fin (YYYY-MM-DD) | `2025-12-31` |
| `limit` | integer | ❌ | Límite de clientes en la tabla (default: sin límite) | `10` |
| `include_payments` | boolean | ❌ | Incluir análisis de pagos (default: true) | `true` |
| `include_defaults` | boolean | ❌ | Incluir análisis de morosidad (default: true) | `true` |

### Ejemplo de Petición:

```bash
curl -X GET "http://localhost:8000/insights/credits/analysis/?start_date=2025-05-01&end_date=2025-12-31&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

### Respuesta Exitosa (200):

```json
{
  "success": true,
  "data": {
    "summary": {
      "period": {
        "start_date": "2025-05-01",
        "end_date": "2025-12-31"
      },
      "summary": {
        "total_credits": 150,
        "total_requested": 1250000.0,
        "total_paid": 875000.0,
        "total_pending": 375000.0,
        "unique_clients": 45,
        "clients_without_payments": 12,
        "clients_in_default": 8,
        "payment_percentage": 70.0
      }
    },
    "clients_table": [
      {
        "client_id": 1,
        "username": "cliente1",
        "full_name": "Juan Pérez",
        "email": "juan@example.com",
        "total_credits": 3,
        "credits_without_payment": 0,
        "credits_in_default": 0,
        "total_requested": 50000.0,
        "total_paid": 50000.0,
        "total_pending": 0.0,
        "payment_percentage": 100.0,
        "avg_credit_amount": 16666.67,
        "max_credit_amount": 25000.0,
        "min_credit_amount": 10000.0,
        "first_credit_date": "2025-06-01T10:00:00Z",
        "last_credit_date": "2025-08-15T14:30:00Z",
        "total_payments_made": 5,
        "total_amount_paid": 50000.0,
        "avg_payment_amount": 10000.0,
        "avg_days_overdue": 0.0,
        "risk_level": "LOW"
      }
    ],
    "payments_analysis": {
      "payment_summary": {
        "total_payments": 250,
        "total_amount_paid": 875000.0,
        "avg_payment_amount": 3500.0
      },
      "payments_by_month": [
        {
          "month": 5,
          "year": 2025,
          "total_payments": 45,
          "total_amount": 157500.0,
          "avg_amount": 3500.0
        }
      ],
      "top_paying_clients": [
        {
          "client_id": 1,
          "username": "cliente1",
          "full_name": "Juan Pérez",
          "total_payments": 15,
          "total_amount_paid": 75000.0,
          "avg_payment": 5000.0
        }
      ]
    },
    "default_analysis": {
      "default_summary": {
        "total_defaulted_credits": 15,
        "total_defaulted_amount": 375000.0,
        "default_rate": 10.0
      },
      "default_by_level": [
        {
          "level": "LOW",
          "count": 5,
          "amount": 125000.0
        }
      ],
      "top_defaulted_clients": [
        {
          "client_id": 2,
          "username": "cliente2",
          "full_name": "María García",
          "defaulted_credits": 2,
          "defaulted_amount": 50000.0,
          "avg_days_overdue": 30.5
        }
      ]
    }
  },
  "parameters": {
    "start_date": "2025-05-01",
    "end_date": "2025-12-31",
    "limit": 10,
    "include_payments": true,
    "include_defaults": true
  }
}
```

### Respuesta de Error (400):

```json
{
  "success": false,
  "error": "Parámetros inválidos",
  "details": {
    "start_date": ["Este campo es requerido."],
    "end_date": ["Formato de fecha inválido. Use YYYY-MM-DD."]
  }
}
```

### Respuesta de Error (401):

```json
{
  "success": false,
  "error": "No autenticado",
  "details": "Se requiere autenticación para acceder a este recurso."
}
```

### Respuesta de Error (403):

```json
{
  "success": false,
  "error": "Permisos insuficientes",
  "details": "Se requieren permisos de administrador para acceder a este recurso."
}
```

---

## 📈 Endpoint 2: Resumen de Análisis

### `GET /insights/credits/analysis/summary/`

**Descripción:** Obtiene un resumen rápido del análisis de créditos sin detalles de clientes individuales.

**Permisos:** Solo requiere autenticación

### Parámetros de Query:

| Parámetro | Tipo | Requerido | Descripción | Ejemplo |
|-----------|------|-----------|-------------|---------|
| `start_date` | string | ✅ | Fecha de inicio (YYYY-MM-DD) | `2025-05-01` |
| `end_date` | string | ✅ | Fecha de fin (YYYY-MM-DD) | `2025-12-31` |

### Ejemplo de Petición:

```bash
curl -X GET "http://localhost:8000/insights/credits/analysis/summary/?start_date=2025-05-01&end_date=2025-12-31" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

### Respuesta Exitosa (200):

```json
{
  "success": true,
  "data": {
    "period": {
      "start_date": "2025-05-01",
      "end_date": "2025-12-31"
    },
    "summary": {
      "total_credits": 150,
      "total_requested": 1250000.0,
      "total_paid": 875000.0,
      "total_pending": 375000.0,
      "unique_clients": 45,
      "clients_without_payments": 12,
      "clients_in_default": 8,
      "payment_percentage": 70.0
    }
  },
  "parameters": {
    "start_date": "2025-05-01",
    "end_date": "2025-12-31"
  }
}
```

---

## 👥 Endpoint 3: Tabla de Clientes

### `GET /insights/credits/analysis/clients/`

**Descripción:** Obtiene la tabla detallada de clientes con información completa de créditos, pagos y nivel de riesgo.

**Permisos:** Requiere permisos de administrador

### Parámetros de Query:

| Parámetro | Tipo | Requerido | Descripción | Ejemplo |
|-----------|------|-----------|-------------|---------|
| `start_date` | string | ✅ | Fecha de inicio (YYYY-MM-DD) | `2025-05-01` |
| `end_date` | string | ✅ | Fecha de fin (YYYY-MM-DD) | `2025-12-31` |
| `limit` | integer | ❌ | Límite de clientes (default: sin límite) | `20` |
| `sort_by` | string | ❌ | Campo de ordenamiento (default: "total_requested") | `payment_percentage` |
| `risk_level` | string | ❌ | Filtro por nivel de riesgo (LOW/MEDIUM/HIGH) | `HIGH` |

**Valores válidos para `sort_by`:**
- `total_credits`
- `total_requested`
- `total_paid`
- `total_pending`
- `payment_percentage`
- `avg_credit_amount`
- `avg_days_overdue`
- `risk_level`

**Valores válidos para `risk_level`:**
- `LOW`
- `MEDIUM`
- `HIGH`

### Ejemplo de Petición:

```bash
curl -X GET "http://localhost:8000/insights/credits/analysis/clients/?start_date=2025-05-01&end_date=2025-12-31&limit=10&risk_level=HIGH&sort_by=payment_percentage" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

### Respuesta Exitosa (200):

```json
{
  "success": true,
  "data": {
    "clients": [
      {
        "client_id": 1,
        "username": "cliente1",
        "full_name": "Juan Pérez",
        "email": "juan@example.com",
        "total_credits": 3,
        "credits_without_payment": 0,
        "credits_in_default": 0,
        "total_requested": 50000.0,
        "total_paid": 50000.0,
        "total_pending": 0.0,
        "payment_percentage": 100.0,
        "avg_credit_amount": 16666.67,
        "max_credit_amount": 25000.0,
        "min_credit_amount": 10000.0,
        "first_credit_date": "2025-06-01T10:00:00Z",
        "last_credit_date": "2025-08-15T14:30:00Z",
        "total_payments_made": 5,
        "total_amount_paid": 50000.0,
        "avg_payment_amount": 10000.0,
        "avg_days_overdue": 0.0,
        "risk_level": "LOW"
      }
    ],
    "pagination": {
      "total_clients": 45,
      "limit": 10,
      "has_more": true
    }
  },
  "parameters": {
    "start_date": "2025-05-01",
    "end_date": "2025-12-31",
    "limit": 10,
    "sort_by": "payment_percentage",
    "risk_level": "HIGH"
  }
}
```

### Respuesta de Error (400) - Nivel de Riesgo Inválido:

```json
{
  "success": false,
  "error": "Parámetro inválido",
  "details": {
    "risk_level": ["Valor inválido. Opciones válidas: LOW, MEDIUM, HIGH"]
  }
}
```

---

## 📋 Estructura de Datos

### Cliente (Client Object)

```typescript
interface Client {
  client_id: number;
  username: string;
  full_name: string;
  email: string;
  total_credits: number;
  credits_without_payment: number;
  credits_in_default: number;
  total_requested: number;
  total_paid: number;
  total_pending: number;
  payment_percentage: number;
  avg_credit_amount: number;
  max_credit_amount: number;
  min_credit_amount: number;
  first_credit_date: string; // ISO 8601
  last_credit_date: string; // ISO 8601
  total_payments_made: number;
  total_amount_paid: number;
  avg_payment_amount: number;
  avg_days_overdue: number;
  risk_level: "LOW" | "MEDIUM" | "HIGH";
}
```

### Resumen (Summary Object)

```typescript
interface Summary {
  total_credits: number;
  total_requested: number;
  total_paid: number;
  total_pending: number;
  unique_clients: number;
  clients_without_payments: number;
  clients_in_default: number;
  payment_percentage: number;
}
```

### Análisis de Pagos (Payments Analysis)

```typescript
interface PaymentsAnalysis {
  payment_summary: {
    total_payments: number;
    total_amount_paid: number;
    avg_payment_amount: number;
  };
  payments_by_month: Array<{
    month: number;
    year: number;
    total_payments: number;
    total_amount: number;
    avg_amount: number;
  }>;
  top_paying_clients: Array<{
    client_id: number;
    username: string;
    full_name: string;
    total_payments: number;
    total_amount_paid: number;
    avg_payment: number;
  }>;
}
```

### Análisis de Morosidad (Default Analysis)

```typescript
interface DefaultAnalysis {
  default_summary: {
    total_defaulted_credits: number;
    total_defaulted_amount: number;
    default_rate: number;
  };
  default_by_level: Array<{
    level: string;
    count: number;
    amount: number;
  }>;
  top_defaulted_clients: Array<{
    client_id: number;
    username: string;
    full_name: string;
    defaulted_credits: number;
    defaulted_amount: number;
    avg_days_overdue: number;
  }>;
}
```

---

## ⚠️ Códigos de Error

| Código | Descripción | Causa |
|--------|-------------|-------|
| 400 | Bad Request | Parámetros inválidos o faltantes |
| 401 | Unauthorized | Token de autenticación faltante o inválido |
| 403 | Forbidden | Permisos insuficientes |
| 404 | Not Found | Endpoint no encontrado |
| 500 | Internal Server Error | Error interno del servidor |

---

## 🔧 Ejemplos de Implementación Frontend

### JavaScript/TypeScript

```typescript
class CreditAnalysisAPI {
  private baseURL = 'http://localhost:8000/insights';
  private token: string;

  constructor(token: string) {
    this.token = token;
  }

  private async request(endpoint: string, params: Record<string, any> = {}) {
    const url = new URL(`${this.baseURL}${endpoint}`);
    Object.keys(params).forEach(key => 
      url.searchParams.append(key, params[key].toString())
    );

    const response = await fetch(url.toString(), {
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
  }

  async getCompleteAnalysis(startDate: string, endDate: string, options: {
    limit?: number;
    includePayments?: boolean;
    includeDefaults?: boolean;
  } = {}) {
    return this.request('/credits/analysis/', {
      start_date: startDate,
      end_date: endDate,
      ...options
    });
  }

  async getSummary(startDate: string, endDate: string) {
    return this.request('/credits/analysis/summary/', {
      start_date: startDate,
      end_date: endDate
    });
  }

  async getClientsTable(startDate: string, endDate: string, options: {
    limit?: number;
    sortBy?: string;
    riskLevel?: 'LOW' | 'MEDIUM' | 'HIGH';
  } = {}) {
    return this.request('/credits/analysis/clients/', {
      start_date: startDate,
      end_date: endDate,
      ...options
    });
  }
}

// Uso
const api = new CreditAnalysisAPI('your_jwt_token');

// Obtener análisis completo
const analysis = await api.getCompleteAnalysis('2025-05-01', '2025-12-31', {
  limit: 10,
  includePayments: true,
  includeDefaults: true
});

// Obtener solo resumen
const summary = await api.getSummary('2025-05-01', '2025-12-31');

// Obtener tabla de clientes con filtros
const clients = await api.getClientsTable('2025-05-01', '2025-12-31', {
  limit: 20,
  sortBy: 'payment_percentage',
  riskLevel: 'HIGH'
});
```

### React Hook

```typescript
import { useState, useEffect } from 'react';

interface UseCreditAnalysisOptions {
  startDate: string;
  endDate: string;
  limit?: number;
  includePayments?: boolean;
  includeDefaults?: boolean;
}

export function useCreditAnalysis(options: UseCreditAnalysisOptions) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await fetch(`/insights/credits/analysis/?${new URLSearchParams({
          start_date: options.startDate,
          end_date: options.endDate,
          ...(options.limit && { limit: options.limit.toString() }),
          ...(options.includePayments !== undefined && { 
            include_payments: options.includePayments.toString() 
          }),
          ...(options.includeDefaults !== undefined && { 
            include_defaults: options.includeDefaults.toString() 
          })
        })}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const result = await response.json();
        setData(result.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [options.startDate, options.endDate, options.limit, options.includePayments, options.includeDefaults]);

  return { data, loading, error };
}
```

---

## 📝 Notas Importantes

1. **Formato de Fechas:** Todas las fechas deben estar en formato `YYYY-MM-DD`
2. **Zona Horaria:** Las fechas se manejan en UTC
3. **Límites:** El parámetro `limit` es opcional, sin límite por defecto
4. **Ordenamiento:** El ordenamiento es ascendente por defecto
5. **Paginación:** Solo disponible en el endpoint de clientes
6. **Caché:** Se recomienda implementar caché en el frontend para consultas frecuentes
7. **Rate Limiting:** No hay límites de rate implementados actualmente

---

**Documento generado:** 2025-01-27  
**Versión de la API:** 1.0  
**Última actualización:** 2025-01-27
