# 📋 Guía del Endpoint de Créditos - Frontend

## 🔗 Información General

**Endpoint:** `GET/POST /dashboard/credits/`  
**Autenticación:** JWT Token requerido  
**Paginación:** Sí (StandardResultsSetPagination)  
**Versión:** 1.0

---

## 🎯 Propósito

Este endpoint permite consultar y filtrar créditos según el rol del usuario autenticado. Soporta tanto consultas GET (con parámetros en URL) como POST (con parámetros en el body).

---

## 🔐 Control de Acceso por Rol

### **Super Admin** (`is_superuser = True`)
- ✅ Ve **TODOS** los créditos del sistema
- ✅ Puede filtrar por cualquier usuario
- ✅ Acceso completo a todos los datos

### **Admin** (`is_staff = True`, sin seller_profile)
- ✅ Ve **TODOS** los créditos del sistema
- ✅ Puede filtrar por cualquier usuario
- ✅ Acceso completo a todos los datos

### **Vendedor** (con `seller_profile`)
- ✅ Ve **solo** créditos que él vendió
- ❌ No puede ver créditos de otros vendedores
- ✅ Puede filtrar por usuario (solo dentro de sus créditos)

### **Cliente** (usuario regular)
- ✅ Ve **solo** sus propios créditos
- ❌ No puede ver créditos de otros usuarios
- ❌ No puede filtrar por usuario

---

## 📡 Métodos HTTP

### **GET** `/dashboard/credits/`

#### Parámetros de Query (URL):
```javascript
// Ejemplo de URL
GET /dashboard/credits/?start_date=2024-01-01&end_date=2024-12-31&status=pending&user=john
```

| Parámetro | Tipo | Requerido | Descripción | Ejemplo |
|-----------|------|-----------|-------------|---------|
| `start_date` | string | ❌ | Fecha inicio (YYYY-MM-DD) | `"2024-01-01"` |
| `end_date` | string | ❌ | Fecha fin (YYYY-MM-DD) | `"2024-12-31"` |
| `status` | string | ❌ | Estado del crédito | `"pending"`, `"completed"` |
| `user` | string | ❌ | Nombre de usuario (búsqueda parcial) | `"john"` |

#### Ejemplo de Request:
```javascript
const response = await fetch('/dashboard/credits/?start_date=2024-01-01&end_date=2024-12-31', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer YOUR_JWT_TOKEN',
    'Content-Type': 'application/json'
  }
});
```

### **POST** `/dashboard/credits/`

#### Body Parameters:
```javascript
{
  "start_date": "2024-01-01",     // ✅ REQUERIDO
  "end_date": "2024-12-31",       // ✅ REQUERIDO
  "status": "pending",            // ❌ Opcional
  "user": "john"                  // ❌ Opcional
}
```

#### Ejemplo de Request:
```javascript
const response = await fetch('/dashboard/credits/', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_JWT_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    start_date: '2024-01-01',
    end_date: '2024-12-31',
    status: 'pending',
    user: 'john'
  })
});
```

---

## 📊 Respuesta

### **Estructura de Respuesta Paginada:**
```javascript
{
  "count": 150,                    // Total de registros
  "next": "http://...?page=2",     // URL siguiente página
  "previous": null,                // URL página anterior
  "results": [                     // Array de créditos
    {
      // ... datos del crédito
    }
  ]
}
```

### **Estructura de Respuesta Simple:**
```javascript
[
  {
    // ... datos del crédito
  }
]
```

---

## 📋 Estructura de Datos del Crédito

### **Campos Principales:**
```javascript
{
  "id": 123,
  "uid": "550e8400-e29b-41d4-a716-446655440000",
  "state": "pending",              // checking, pending, completed, to_solve, preorder
  "cost": "1000.00",              // Costo del crédito
  "price": "1200.00",             // Precio final
  "earnings": "200.00",           // Ganancia calculada
  "interest": "5.50",             // Tasa de interés
  "credit_days": 30,              // Días del crédito
  "description": "Préstamo personal",
  "first_date_payment": "2024-01-15",
  "second_date_payment": "2024-02-15",
  "total_abonos": "300.00",       // Total pagado
  "pending_amount": "900.00",     // Monto pendiente
  "installment_number": 3,        // Número de cuotas
  "installment_value": "400.00",  // Valor por cuota
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### **Relaciones Incluidas:**

#### **Usuario:**
```javascript
"user": {
  "id": 456,
  "username": "john_doe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone_1": {
    "country_code": "+57",
    "phone_number": "3001234567"
  },
  "label": {
    "name": "Cliente Premium",
    "position": "top"
  }
}
```

#### **Vendedor:**
```javascript
"seller": {
  "id": 789,
  "user": {
    "id": 789,
    "username": "seller_jane",
    "first_name": "Jane",
    "last_name": "Smith"
  },
  "total_sales": "50000.00",
  "commissions": "2500.00",
  "returns": "0.00"
}
```

#### **Categoría y Subcategoría:**
```javascript
"subcategory": {
  "name": "Préstamo Personal",
  "category_name": "Créditos"
}
```

#### **Moneda:**
```javascript
"currency": {
  "id_currency": 1,
  "currency": "COP",
  "exchange_rate": 1.0
}
```

#### **Periodicidad:**
```javascript
"periodicity": {
  "id": 1,
  "name": "Mensual",
  "days": 30
},
"periodicity_days": 30  // Campo calculado
```

#### **Cuenta de Pago:**
```javascript
"payment": {
  "id_payment_method": 1,
  "name": "Cuenta Principal",
  "account_number": "123456789",
  "balance": "50000.00",
  "currency": {
    "id_currency": 1,
    "currency": "COP",
    "exchange_rate": 1.0
  }
}
```

### **Pagos Realizados:**
```javascript
"payments": [
  {
    "payment_method": {
      "id_payment_method": 1,
      "name": "Efectivo",
      "account_number": null,
      "balance": "0.00",
      "currency": {
        "id_currency": 1,
        "currency": "COP",
        "exchange_rate": 1.0
      }
    },
    "payment_code": "PAY001",
    "amount": "400.00",
    "amount_paid": "400.00",
    "currency": "COP",
    "transaction_date": "2024-01-15T10:00:00Z"
  }
]
```

### **Ajustes:**
```javascript
"adjustments": [
  {
    "id": 1,
    "type": 1,
    "adjustment_type": "DESC",
    "adjustment_name": "Descuento por Pronto Pago",
    "amount": "50.00",
    "added_on": "2024-01-10",
    "reason": "Pago anticipado",
    "created_at": "2024-01-10T10:00:00Z",
    "is_positive": true,
    "sign": "+"
  }
],
"total_adjustments": 50.00,      // Total neto de ajustes
"total_discounts": 50.00,        // Total de descuentos
"total_charges": 0.00,           // Total de cargos
"adjustments_summary": {
  "Descuento por Pronto Pago": {
    "type_code": "DESC",
    "total_amount": 50.00,
    "count": 1,
    "is_positive": true
  }
}
```

### **Cuotas:**
```javascript
"installments": [
  {
    "id": 1,
    "number": 1,
    "due_date": "2024-01-15",
    "amount": "400.00",
    "paid": true,
    "paid_on": "2024-01-15",
    "principal_amount": "400.00",
    "interest_amount": "0.00",
    "late_fee": "0.00",
    "status": "paid",
    "notification_sent": true,
    "reminder_count": 0,
    "amount_paid": "400.00",
    "remaining_amount": "0.00",
    "days_overdue": 0,
    "is_scheduled": false,
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-15T10:00:00Z"
  }
]
```

---

## ⚠️ Códigos de Error

### **400 Bad Request:**
```javascript
{
  "error": "start_date y end_date son requeridos"
}
```
```javascript
{
  "error": "Formato de fecha inválido. Use YYYY-MM-DD"
}
```

### **401 Unauthorized:**
```javascript
{
  "detail": "Authentication credentials were not provided."
}
```

### **403 Forbidden:**
```javascript
{
  "detail": "You do not have permission to perform this action."
}
```

### **500 Internal Server Error:**
```javascript
{
  "error": "Error interno del servidor: [detalles del error]"
}
```

---

## 🔍 Estados de Crédito

| Estado | Descripción |
|--------|-------------|
| `checking` | En verificación |
| `pending` | Pendiente |
| `completed` | Completado |
| `to_solve` | Requiere atención |
| `preorder` | Pre-orden |

---

## 📝 Ejemplos de Uso

### **1. Obtener todos los créditos del usuario:**
```javascript
// GET sin parámetros
const response = await fetch('/dashboard/credits/', {
  headers: { 'Authorization': 'Bearer YOUR_JWT_TOKEN' }
});
```

### **2. Filtrar por rango de fechas:**
```javascript
// POST con fechas requeridas
const response = await fetch('/dashboard/credits/', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_JWT_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    start_date: '2024-01-01',
    end_date: '2024-12-31'
  })
});
```

### **3. Filtrar por estado y usuario:**
```javascript
// GET con múltiples filtros
const response = await fetch('/dashboard/credits/?start_date=2024-01-01&end_date=2024-12-31&status=pending&user=john', {
  headers: { 'Authorization': 'Bearer YOUR_JWT_TOKEN' }
});
```

### **4. Manejo de paginación:**
```javascript
const response = await fetch('/dashboard/credits/?page=2', {
  headers: { 'Authorization': 'Bearer YOUR_JWT_TOKEN' }
});

const data = await response.json();
console.log(`Total: ${data.count}`);
console.log(`Página siguiente: ${data.next}`);
console.log(`Página anterior: ${data.previous}`);
console.log(`Resultados: ${data.results.length}`);
```

---

## 🚀 Optimizaciones del Frontend

### **1. Cache de Datos:**
```javascript
// Implementar cache para evitar requests repetidos
const creditCache = new Map();

async function getCredits(params) {
  const cacheKey = JSON.stringify(params);
  if (creditCache.has(cacheKey)) {
    return creditCache.get(cacheKey);
  }
  
  const response = await fetch('/dashboard/credits/', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: JSON.stringify(params)
  });
  
  const data = await response.json();
  creditCache.set(cacheKey, data);
  return data;
}
```

### **2. Debounce para Filtros:**
```javascript
// Evitar requests excesivos al filtrar
let filterTimeout;

function handleFilterChange(params) {
  clearTimeout(filterTimeout);
  filterTimeout = setTimeout(() => {
    getCredits(params);
  }, 300);
}
```

### **3. Loading States:**
```javascript
const [loading, setLoading] = useState(false);
const [credits, setCredits] = useState([]);

async function loadCredits(params) {
  setLoading(true);
  try {
    const data = await getCredits(params);
    setCredits(data.results || data);
  } catch (error) {
    console.error('Error loading credits:', error);
  } finally {
    setLoading(false);
  }
}
```

---

## 🔧 Consideraciones Técnicas

### **1. Ordenamiento:**
- Los créditos se ordenan por `created_at` descendente (más recientes primero)
- No se puede cambiar el ordenamiento desde el frontend

### **2. Paginación:**
- Usa `StandardResultsSetPagination`
- Parámetro: `?page=N`
- Incluye `count`, `next`, `previous`, `results`

### **3. Optimizaciones del Backend:**
- Eager loading de relaciones (`select_related`, `prefetch_related`)
- Filtros aplicados a nivel de base de datos
- Consultas optimizadas según el rol del usuario

### **4. Seguridad:**
- Validación de fechas en el servidor
- Filtrado por rol automático
- Sanitización de parámetros de búsqueda

---

## 📞 Soporte

Para dudas o problemas con este endpoint, contactar al equipo de backend con:
- URL del endpoint
- Parámetros enviados
- Respuesta recibida
- Logs del servidor (si están disponibles)
