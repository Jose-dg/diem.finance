# 📋 URLs Correctas para Frontend - Dashboard Insights

## 🚨 Problema Identificado

El frontend estaba intentando acceder a URLs con prefijo `/api/insights/` que no existen en el backend, causando errores 404.

## ✅ URLs Correctas del Backend

### **Base URL:** `/insights/`

### **Endpoints de Dashboard Disponibles:**

| Endpoint | URL Completa | Descripción |
|----------|--------------|-------------|
| **Dashboard Ejecutivo** | `GET /insights/dashboard/executive/` | Vista ejecutiva general |
| **Dashboard de Créditos** | `GET /insights/dashboard/credits/` | Análisis de créditos |
| **Dashboard de Riesgo** | `GET /insights/dashboard/risk/` | Análisis de riesgo |
| **Dashboard de Usuarios** | `GET /insights/dashboard/users/` | Análisis de usuarios |
| **Dashboard Operacional** | `GET /insights/dashboard/operational/` | Vista operacional |
| **Dashboard de Ingresos** | `GET /insights/dashboard/revenue/` | Análisis de ingresos |

### **Otros Endpoints Disponibles:**

| Endpoint | URL Completa | Descripción |
|----------|--------------|-------------|
| **Portfolio Overview** | `GET /insights/portfolio/overview/` | Resumen del portafolio |
| **Análisis de Créditos** | `GET /insights/credits/analysis/` | Análisis detallado de créditos |
| **Resumen de Insights** | `GET /insights/summary/` | Resumen general |
| **Health Check** | `GET /insights/health-check/` | Verificación de estado |

## 🔧 Cambios Necesarios en el Frontend

### **1. Actualizar URLs Base**

```javascript
// ❌ INCORRECTO (causa 404)
const API_BASE = '/api/insights/';

// ✅ CORRECTO
const API_BASE = '/insights/';
```

### **2. Ejemplos de Implementación**

```javascript
// Configuración de API
const API_CONFIG = {
  baseURL: '/insights/',
  endpoints: {
    executive: 'dashboard/executive/',
    credits: 'dashboard/credits/',
    risk: 'dashboard/risk/',
    users: 'dashboard/users/',
    operational: 'dashboard/operational/',
    revenue: 'dashboard/revenue/',
    portfolio: 'portfolio/overview/',
    summary: 'summary/'
  }
};

// Función para construir URLs
function buildInsightsURL(endpoint, params = {}) {
  const url = new URL(`${API_CONFIG.baseURL}${endpoint}`, window.location.origin);
  
  // Agregar parámetros de query
  Object.keys(params).forEach(key => {
    if (params[key]) {
      url.searchParams.append(key, params[key]);
    }
  });
  
  return url.toString();
}

// Ejemplos de uso
const executiveURL = buildInsightsURL(API_CONFIG.endpoints.executive, {
  date_from: '2025-09-01',
  date_to: '2025-09-12'
});

const creditsURL = buildInsightsURL(API_CONFIG.endpoints.credits, {
  date_from: '2025-09-01',
  date_to: '2025-09-12'
});
```

### **3. URLs Completas con Parámetros**

```javascript
// Dashboard Ejecutivo
GET /insights/dashboard/executive/?date_from=2025-09-01&date_to=2025-09-12

// Dashboard de Créditos
GET /insights/dashboard/credits/?date_from=2025-09-01&date_to=2025-09-12

// Dashboard de Riesgo
GET /insights/dashboard/risk/?date_from=2025-09-01&date_to=2025-09-12

// Dashboard de Usuarios
GET /insights/dashboard/users/?date_from=2025-09-01&date_to=2025-09-12

// Portfolio Overview
GET /insights/portfolio/overview/?date_from=2025-09-01&date_to=2025-09-12
```

## 📝 Parámetros de Query Soportados

Todos los endpoints de dashboard soportan los siguientes parámetros:

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `date_from` | string | Fecha de inicio (YYYY-MM-DD) | `2025-09-01` |
| `date_to` | string | Fecha de fin (YYYY-MM-DD) | `2025-09-12` |
| `days` | integer | Número de días hacia atrás | `30` |

## 🧪 Testing de URLs

### **Usando cURL:**
```bash
# Dashboard ejecutivo
curl -X GET "http://localhost:8000/insights/dashboard/executive/?date_from=2025-09-01&date_to=2025-09-12"

# Dashboard de créditos
curl -X GET "http://localhost:8000/insights/dashboard/credits/?date_from=2025-09-01&date_to=2025-09-12"

# Dashboard de riesgo
curl -X GET "http://localhost:8000/insights/dashboard/risk/?date_from=2025-09-01&date_to=2025-09-12"
```

### **Usando JavaScript Fetch:**
```javascript
// Función para hacer requests
async function fetchInsightsData(endpoint, params = {}) {
  const url = buildInsightsURL(endpoint, params);
  
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        // Agregar headers de autenticación si es necesario
        'Authorization': `Bearer ${getAuthToken()}`
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching insights data:', error);
    throw error;
  }
}

// Ejemplos de uso
const executiveData = await fetchInsightsData('dashboard/executive/', {
  date_from: '2025-09-01',
  date_to: '2025-09-12'
});
```

## ⚠️ Notas Importantes

1. **Eliminar completamente** el prefijo `/api/` de todas las URLs de insights
2. **Usar** `/insights/` como base para todos los endpoints
3. **Mantener** los parámetros de query existentes (`date_from`, `date_to`)
4. **Verificar** que el servidor Django esté corriendo en `http://localhost:8000`
5. **Asegurar** que las vistas de insights estén correctamente implementadas

## 🔍 Verificación

Después de implementar los cambios, verificar que:

- ✅ No hay errores 404 en la consola del navegador
- ✅ Los datos del dashboard se cargan correctamente
- ✅ Los parámetros de fecha se envían correctamente
- ✅ Las respuestas JSON tienen la estructura esperada

---

**Fecha de actualización:** 11 de Septiembre, 2025  
**Versión:** 1.0  
**Autor:** Sistema Fintech
