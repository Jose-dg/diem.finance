# 🎯 Guía Frontend - Endpoints de Insights por Crédito

## 📋 Endpoints Disponibles

### 1. **Insights por Crédito Individual**
```
GET /api/insights/credits/insights/{credit_id}/
```
**Permisos:** Usuario autenticado (propietario del crédito o admin)

**Headers:**
```javascript
{
  'Authorization': 'Bearer {token}',
  'Content-Type': 'application/json'
}
```

**Ejemplo de uso:**
```javascript
const getCreditInsights = async (creditId, token) => {
  const response = await fetch(`/api/insights/credits/insights/${creditId}/`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return await response.json();
};
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "credit_basic_info": { /* info básica del crédito */ },
    "payment_analysis": { /* análisis de pagos */ },
    "risk_assessment": { /* evaluación de riesgo */ },
    "performance_metrics": { /* métricas de rendimiento */ },
    "installment_breakdown": [ /* desglose de cuotas */ ],
    "timeline_analysis": { /* análisis temporal */ },
    "comparative_analysis": { /* análisis comparativo */ },
    "recommendations": [ /* recomendaciones */ ]
  }
}
```

---

### 2. **Análisis Comparativo de Créditos**
```
GET /api/insights/credits/analysis/comparative/
```
**Permisos:** Solo administradores

**Parámetros opcionales:**
- `start_date`: YYYY-MM-DD
- `end_date`: YYYY-MM-DD  
- `subcategory_id`: ID de subcategoría
- `user_id`: ID de usuario

**Ejemplo de uso:**
```javascript
const getComparativeAnalysis = async (filters, token) => {
  const params = new URLSearchParams(filters);
  const response = await fetch(`/api/insights/credits/analysis/comparative/?${params}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return await response.json();
};

// Uso:
getComparativeAnalysis({
  start_date: '2024-01-01',
  end_date: '2024-01-31',
  subcategory_id: '1'
}, token);
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_credits": 150,
      "total_amount": 7500000.00,
      "default_rate": 8.5,
      "collection_rate": 66.67
    },
    "category_analysis": [ /* análisis por categoría */ ],
    "state_analysis": [ /* análisis por estado */ ],
    "morosidad_analysis": [ /* análisis por morosidad */ ],
    "top_credits": [ /* top créditos */ ]
  }
}
```

---

### 3. **Métricas de Rendimiento**
```
GET /api/insights/credits/performance/
```
**Permisos:** Solo administradores

**Parámetros opcionales:**
- `period`: 7d, 30d, 90d, 1y (default: 30d)
- `metric_type`: collection, risk, performance, all (default: all)

**Ejemplo de uso:**
```javascript
const getPerformanceMetrics = async (period = '30d', metricType = 'all', token) => {
  const params = new URLSearchParams({ period, metric_type: metricType });
  const response = await fetch(`/api/insights/credits/performance/?${params}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return await response.json();
};
```

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "period": "30d",
    "start_date": "2024-01-01T00:00:00Z",
    "end_date": "2024-01-31T23:59:59Z",
    "metrics": {
      "collection": { /* métricas de recaudación */ },
      "risk": { /* métricas de riesgo */ },
      "performance": { /* métricas de rendimiento */ }
    }
  }
}
```

---

## 🚨 Manejo de Errores

**Códigos de estado comunes:**
- `401`: No autorizado - token inválido
- `403`: Sin permisos - usuario no es admin o propietario
- `404`: Crédito no encontrado
- `400`: Parámetros inválidos
- `500`: Error del servidor

**Ejemplo de manejo:**
```javascript
const handleApiCall = async (apiCall) => {
  try {
    const response = await apiCall();
    if (!response.success) {
      throw new Error(response.error);
    }
    return response.data;
  } catch (error) {
    console.error('API Error:', error.message);
    throw error;
  }
};
```

---

## 🎨 Componentes UI Esenciales

### Tarjeta de Información Básica
```jsx
const CreditBasicInfo = ({ data }) => (
  <div className="card">
    <h3>Información del Crédito</h3>
    <div className="info-grid">
      <div>
        <label>Monto Total:</label>
        <span>${data.amounts.price.toLocaleString()}</span>
      </div>
      <div>
        <label>Pendiente:</label>
        <span>${data.amounts.pending_amount.toLocaleString()}</span>
      </div>
      <div>
        <label>Estado:</label>
        <span className={`status ${data.status.state}`}>
          {data.status.state}
        </span>
      </div>
    </div>
  </div>
);
```

### Análisis de Riesgo
```jsx
const RiskAssessment = ({ data }) => (
  <div className="card">
    <h3>Evaluación de Riesgo</h3>
    <div className="risk-score">
      <span className="score">{data.risk_score}</span>
      <span className={`level ${data.risk_level}`}>
        {data.risk_level.toUpperCase()}
      </span>
    </div>
    <ul>
      {data.risk_factors.map((factor, i) => (
        <li key={i}>⚠️ {factor}</li>
      ))}
    </ul>
  </div>
);
```

### Tabla de Cuotas
```jsx
const InstallmentTable = ({ data }) => (
  <div className="card">
    <h3>Desglose de Cuotas</h3>
    <table>
      <thead>
        <tr>
          <th>Cuota</th>
          <th>Fecha</th>
          <th>Monto</th>
          <th>Estado</th>
        </tr>
      </thead>
      <tbody>
        {data.map((installment, i) => (
          <tr key={i} className={installment.status}>
            <td>{installment.number}</td>
            <td>{new Date(installment.due_date).toLocaleDateString()}</td>
            <td>${installment.amount.toLocaleString()}</td>
            <td>{installment.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);
```

---

## 📱 Ejemplo de Página Completa

```jsx
import React, { useState, useEffect } from 'react';

const CreditInsightsPage = ({ creditId, token }) => {
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInsights = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/insights/credits/insights/${creditId}/`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await response.json();
        
        if (data.success) {
          setInsights(data.data);
        } else {
          setError(data.error);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchInsights();
  }, [creditId, token]);

  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!insights) return <div>No hay datos</div>;

  return (
    <div>
      <CreditBasicInfo data={insights.credit_basic_info} />
      <RiskAssessment data={insights.risk_assessment} />
      <InstallmentTable data={insights.installment_breakdown} />
    </div>
  );
};
```

---

## 🎯 Casos de Uso Rápidos

### Para Usuarios:
- Ver estado de su crédito: `GET /credits/insights/{credit_id}/`
- Ver recomendaciones personalizadas

### Para Admins:
- Análisis de cartera: `GET /credits/analysis/comparative/`
- Métricas de rendimiento: `GET /credits/performance/`
- Comparar créditos por período

### Filtros Útiles:
```javascript
// Últimos 30 días
{ start_date: '2024-01-01', end_date: '2024-01-31' }

// Por categoría
{ subcategory_id: '1' }

// Por usuario específico
{ user_id: '123' }

// Métricas de recaudación del último mes
{ period: '30d', metric_type: 'collection' }
```

---

## ✅ Checklist de Implementación

- [ ] Configurar headers de autenticación
- [ ] Manejar estados de carga y error
- [ ] Validar permisos de usuario
- [ ] Implementar componentes básicos de UI
- [ ] Agregar filtros para análisis comparativo
- [ ] Mostrar métricas de rendimiento
- [ ] Implementar tabla de cuotas
- [ ] Mostrar recomendaciones
