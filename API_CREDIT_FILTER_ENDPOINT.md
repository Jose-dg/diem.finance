# API Endpoint: Filtrado de Créditos

## 📋 **Información General**

**Endpoint:** `POST /dashboard/credits/filter/`  
**Autenticación:** JWT Bearer Token  
**Content-Type:** `application/json`  
**Base URL:** `https://fintech-7wkz.onrender.com`

## 🔐 **Autenticación**

```http
Authorization: Bearer <your_jwt_token>
```

## 📊 **Parámetros de Filtrado Disponibles**

### **1. Filtros de Usuario**

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `first_name` | string | Nombre del cliente (búsqueda parcial) | `"Maria"` |
| `last_name` | string | Apellido del cliente (búsqueda parcial) | `"Daniela"` |
| `phone_number` | string | Número de teléfono (búsqueda parcial) | `"123456789"` |
| `label` | string | Etiqueta del cliente (búsqueda parcial) | `"Restaurante"` |

### **2. Filtros de Periodicidad**

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `periodicity_days` | number | Días de la periodicidad (exacto) | `30` |
| `periodicity_id` | UUID | ID de la periodicidad (exacto) | `"uuid-here"` |

### **3. Filtros de Estado**

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `is_in_default` | boolean | Si está en mora | `true` |
| `morosidad_level` | string | Nivel de morosidad (exacto) | `"mild_default"` |
| `state` | string | Estado del crédito (exacto) | `"pending"` |

### **4. Búsqueda Combinada**

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `search` | string | Búsqueda en múltiples campos | `"Maria Daniela"` |

## 🎯 **Ejemplos de Consultas**

### **Ejemplo 1: Búsqueda por Nombre Completo**

```json
{
  "first_name": "Maria",
  "last_name": "Daniela"
}
```

**Resultado:** Encuentra créditos de usuarios cuyo nombre contenga "Maria" Y apellido contenga "Daniela"

### **Ejemplo 2: Búsqueda por Etiqueta con Espacios**

```json
{
  "label": "Restaurante Pinto"
}
```

**Resultado:** Encuentra créditos de usuarios con etiqueta que contenga "Restaurante Pinto"

### **Ejemplo 3: Búsqueda Combinada (Recomendada)**

```json
{
  "search": "Maria Daniela"
}
```

**Resultado:** Busca en nombre, apellido, etiqueta y descripción del crédito

### **Ejemplo 4: Filtros Múltiples**

```json
{
  "search": "Restaurante",
  "state": "pending",
  "is_in_default": false,
  "periodicity_days": 30
}
```

**Resultado:** Créditos pendientes, no en mora, con periodicidad de 30 días y que contengan "Restaurante"

### **Ejemplo 5: Solo por Estado**

```json
{
  "state": "active"
}
```

**Resultado:** Todos los créditos activos

## 📝 **Instrucciones para el Frontend**

### **1. Manejo de Espacios en Nombres**

Para buscar nombres con espacios como "Maria Daniela" o "Restaurante Pinto":

#### **Opción A: Búsqueda Combinada (Recomendada)**
```javascript
const searchData = {
  search: "Maria Daniela"
};

// POST request
fetch('/dashboard/credits/filter/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify(searchData)
});
```

#### **Opción B: Filtros Separados**
```javascript
const searchData = {
  first_name: "Maria",
  last_name: "Daniela"
};
```

### **2. Implementación de Búsqueda Inteligente**

```javascript
class CreditFilterService {
  constructor(baseUrl, token) {
    this.baseUrl = baseUrl;
    this.token = token;
  }

  async filterCredits(filters) {
    try {
      const response = await fetch(`${this.baseUrl}/dashboard/credits/filter/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.token}`
        },
        body: JSON.stringify(filters)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error filtering credits:', error);
      throw error;
    }
  }

  // Método para búsqueda inteligente
  async smartSearch(query) {
    const filters = {};
    
    // Si la consulta contiene espacios, usar búsqueda combinada
    if (query.includes(' ')) {
      filters.search = query;
    } else {
      // Si es una sola palabra, buscar en múltiples campos
      filters.search = query;
    }

    return this.filterCredits(filters);
  }

  // Método para filtros específicos
  async advancedFilter(params) {
    const filters = {};
    
    if (params.name) {
      // Separar nombre y apellido si hay espacios
      const nameParts = params.name.split(' ');
      if (nameParts.length > 1) {
        filters.first_name = nameParts[0];
        filters.last_name = nameParts.slice(1).join(' ');
      } else {
        filters.search = params.name;
      }
    }

    if (params.label) filters.label = params.label;
    if (params.state) filters.state = params.state;
    if (params.isInDefault !== undefined) filters.is_in_default = params.isInDefault;
    if (params.periodicityDays) filters.periodicity_days = params.periodicityDays;

    return this.filterCredits(filters);
  }
}
```

### **3. Ejemplo de Uso en React**

```jsx
import React, { useState } from 'react';

const CreditFilter = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({});
  const [credits, setCredits] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const filterService = new CreditFilterService(
        'https://fintech-7wkz.onrender.com',
        localStorage.getItem('token')
      );

      let searchFilters = {};
      
      if (searchQuery.includes(' ')) {
        // Búsqueda con espacios - usar search combinado
        searchFilters.search = searchQuery;
      } else {
        // Búsqueda simple
        searchFilters.search = searchQuery;
      }

      // Combinar con filtros adicionales
      const finalFilters = { ...searchFilters, ...filters };
      
      const result = await filterService.filterCredits(finalFilters);
      setCredits(result.results || result);
    } catch (error) {
      console.error('Error searching credits:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Buscar por nombre, etiqueta, etc..."
      />
      <button onClick={handleSearch} disabled={loading}>
        {loading ? 'Buscando...' : 'Buscar'}
      </button>
      
      {/* Mostrar resultados */}
      <div>
        {credits.map(credit => (
          <div key={credit.id}>
            <h3>{credit.user.first_name} {credit.user.last_name}</h3>
            <p>Estado: {credit.state}</p>
            <p>Monto: ${credit.price}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
```

## 📊 **Respuesta del API**

### **Estructura de Respuesta**

```json
{
  "count": 25,
  "next": "https://fintech-7wkz.onrender.com/dashboard/credits/filter/?page=2",
  "previous": null,
  "results": [
    {
      "id": 123,
      "uid": "uuid-here",
      "user": {
        "id": 456,
        "username": "mariadaniela",
        "first_name": "Maria",
        "last_name": "Daniela",
        "email": "maria@example.com"
      },
      "state": "active",
      "price": "5000.00",
      "pending_amount": "2500.00",
      "currency": {
        "id": 1,
        "currency": "USD",
        "id_currency": "USD"
      },
      "subcategory": {
        "id": 1,
        "name": "Crédito de Consumo"
      },
      "periodicity_days": 30,
      "installment_number": 12,
      "installment_value": "416.67",
      "first_date_payment": "2025-01-27",
      "second_date_payment": "2025-02-26",
      "created_at": "2025-01-27T10:30:00Z",
      "is_in_default": false,
      "morosidad_level": "on_time",
      "payments": [...],
      "adjustments": [...],
      "installments": [...]
    }
  ]
}
```

### **Campos Importantes en la Respuesta**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `count` | number | Total de resultados |
| `next` | string | URL para siguiente página |
| `previous` | string | URL para página anterior |
| `results` | array | Lista de créditos |

## ⚠️ **Consideraciones Importantes**

### **1. Paginación**
- El API devuelve resultados paginados
- Por defecto: 20 resultados por página
- Usar `next` y `previous` para navegación

### **2. Permisos por Usuario**
- **Super Admin:** Ve todos los créditos
- **Admin:** Ve todos los créditos
- **Vendedor:** Ve solo créditos que vendió
- **Cliente:** Ve solo sus créditos

### **3. Búsqueda Case-Insensitive**
- Todas las búsquedas son insensibles a mayúsculas/minúsculas
- `"maria"` encuentra "Maria", "MARIA", "maria"

### **4. Búsqueda Parcial**
- `"Mar"` encuentra "Maria", "Mario", "Martha"
- `"Rest"` encuentra "Restaurante", "Restaurante Pinto"

## 🚀 **Mejores Prácticas**

### **1. Para Nombres con Espacios**
```javascript
// ✅ Recomendado
{ "search": "Maria Daniela" }

// ❌ No recomendado
{ "first_name": "Maria", "last_name": "Daniela" }
```

### **2. Para Búsquedas Específicas**
```javascript
// ✅ Para etiquetas específicas
{ "label": "Restaurante Pinto" }

// ✅ Para estados específicos
{ "state": "pending", "is_in_default": false }
```

### **3. Para Filtros Múltiples**
```javascript
// ✅ Combinar búsqueda con filtros
{
  "search": "Maria",
  "state": "active",
  "periodicity_days": 30
}
```

## 🔧 **Códigos de Error**

| Código | Descripción | Solución |
|--------|-------------|----------|
| `400` | Parámetros inválidos | Verificar formato de datos |
| `401` | No autenticado | Verificar JWT token |
| `403` | No autorizado | Verificar permisos de usuario |
| `500` | Error interno | Contactar soporte |

---

**Nota:** Este endpoint está optimizado para manejar búsquedas con espacios y caracteres especiales. La búsqueda combinada (`search`) es la opción más robusta para consultas complejas.
