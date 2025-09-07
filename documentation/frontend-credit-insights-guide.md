# 🎨 Guía Frontend - Vistas de Insights por Crédito

## 📋 Índice
1. [Configuración Inicial](#configuración-inicial)
2. [Autenticación y Permisos](#autenticación-y-permisos)
3. [Vista de Insights por Crédito Individual](#vista-de-insights-por-crédito-individual)
4. [Vista de Análisis Comparativo](#vista-de-análisis-comparativo)
5. [Vista de Métricas de Rendimiento](#vista-de-métricas-de-rendimiento)
6. [Componentes de UI Recomendados](#componentes-de-ui-recomendados)
7. [Manejo de Errores](#manejo-de-errores)
8. [Ejemplos de Implementación](#ejemplos-de-implementación)

---

## 🔧 Configuración Inicial

### Base URL
```javascript
const API_BASE_URL = 'https://tu-dominio.com/api/insights';
```

### Headers Requeridos
```javascript
const getHeaders = (token) => ({
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json',
  'Accept': 'application/json'
});
```

---

## 🔐 Autenticación y Permisos

### Verificación de Permisos
```javascript
// Verificar si el usuario es admin
const isAdmin = (user) => user.is_staff || user.is_superuser;

// Verificar si el usuario es propietario del crédito
const isCreditOwner = (user, creditUserId) => user.id === creditUserId;
```

---

## 📊 Vista de Insights por Crédito Individual

### Endpoint
```
GET /api/insights/credits/insights/{credit_id}/
```

### Uso Básico
```javascript
// Función para obtener insights de un crédito
const getCreditInsights = async (creditId, token) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/credits/insights/${creditId}/`,
      {
        method: 'GET',
        headers: getHeaders(token)
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching credit insights:', error);
    throw error;
  }
};
```

### Ejemplo de Uso en Componente React
```jsx
import React, { useState, useEffect } from 'react';

const CreditInsightsComponent = ({ creditId, user, token }) => {
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInsights = async () => {
      try {
        setLoading(true);
        const data = await getCreditInsights(creditId, token);
        
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

    if (creditId && token) {
      fetchInsights();
    }
  }, [creditId, token]);

  if (loading) return <div>Cargando insights...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!insights) return <div>No se encontraron insights</div>;

  return (
    <div className="credit-insights">
      {/* Información Básica */}
      <CreditBasicInfo data={insights.credit_basic_info} />
      
      {/* Análisis de Pagos */}
      <PaymentAnalysis data={insights.payment_analysis} />
      
      {/* Evaluación de Riesgo */}
      <RiskAssessment data={insights.risk_assessment} />
      
      {/* Métricas de Rendimiento */}
      <PerformanceMetrics data={insights.performance_metrics} />
      
      {/* Desglose de Cuotas */}
      <InstallmentBreakdown data={insights.installment_breakdown} />
      
      {/* Análisis Temporal */}
      <TimelineAnalysis data={insights.timeline_analysis} />
      
      {/* Análisis Comparativo */}
      <ComparativeAnalysis data={insights.comparative_analysis} />
      
      {/* Recomendaciones */}
      <Recommendations data={insights.recommendations} />
    </div>
  );
};
```

### Componentes de UI Recomendados

#### 1. Información Básica del Crédito
```jsx
const CreditBasicInfo = ({ data }) => (
  <div className="card">
    <h3>Información del Crédito</h3>
    <div className="info-grid">
      <div className="info-item">
        <label>Monto Total:</label>
        <span className="amount">${data.amounts.price.toLocaleString()}</span>
      </div>
      <div className="info-item">
        <label>Monto Pendiente:</label>
        <span className="amount pending">${data.amounts.pending_amount.toLocaleString()}</span>
      </div>
      <div className="info-item">
        <label>Estado:</label>
        <span className={`status ${data.status.state}`}>
          {data.status.state}
        </span>
      </div>
      <div className="info-item">
        <label>Nivel de Morosidad:</label>
        <span className={`morosidad ${data.status.morosidad_level}`}>
          {data.status.morosidad_level}
        </span>
      </div>
    </div>
  </div>
);
```

#### 2. Análisis de Pagos
```jsx
const PaymentAnalysis = ({ data }) => (
  <div className="card">
    <h3>Análisis de Pagos</h3>
    
    {/* Resumen de Cuotas */}
    <div className="payment-summary">
      <div className="metric">
        <span className="value">{data.installment_summary.payment_rate.toFixed(1)}%</span>
        <span className="label">Tasa de Pago</span>
      </div>
      <div className="metric">
        <span className="value">{data.installment_summary.paid_installments}</span>
        <span className="label">Cuotas Pagadas</span>
      </div>
      <div className="metric">
        <span className="value">{data.installment_summary.pending_installments}</span>
        <span className="label">Cuotas Pendientes</span>
      </div>
    </div>

    {/* Comportamiento de Pagos */}
    <div className="payment-behavior">
      <h4>Comportamiento de Pagos</h4>
      <div className="behavior-metrics">
        <div className="metric">
          <span className="value">{data.payment_behavior.punctuality_rate.toFixed(1)}%</span>
          <span className="label">Puntualidad</span>
        </div>
        <div className="metric">
          <span className="value">{data.payment_behavior.avg_delay_days}</span>
          <span className="label">Días Promedio de Retraso</span>
        </div>
      </div>
    </div>

    {/* Progreso de Pago */}
    <div className="payment-progress">
      <h4>Progreso de Pago</h4>
      <div className="progress-bar">
        <div 
          className="progress-fill" 
          style={{ width: `${data.amounts.payment_progress}%` }}
        ></div>
      </div>
      <span className="progress-text">
        {data.amounts.payment_progress.toFixed(1)}% completado
      </span>
    </div>
  </div>
);
```

#### 3. Evaluación de Riesgo
```jsx
const RiskAssessment = ({ data }) => {
  const getRiskColor = (level) => {
    switch (level) {
      case 'low': return '#4CAF50';
      case 'medium': return '#FF9800';
      case 'high': return '#F44336';
      case 'critical': return '#9C27B0';
      default: return '#757575';
    }
  };

  return (
    <div className="card">
      <h3>Evaluación de Riesgo</h3>
      
      {/* Score de Riesgo */}
      <div className="risk-score">
        <div className="score-circle">
          <div 
            className="score-fill" 
            style={{ 
              background: `conic-gradient(${getRiskColor(data.risk_level)} ${data.risk_score * 3.6}deg, #e0e0e0 0deg)` 
            }}
          >
            <span className="score-value">{data.risk_score}</span>
          </div>
        </div>
        <div className="score-info">
          <span className="risk-level" style={{ color: getRiskColor(data.risk_level) }}>
            {data.risk_level.toUpperCase()}
          </span>
          <span className="score-label">Score de Riesgo</span>
        </div>
      </div>

      {/* Factores de Riesgo */}
      <div className="risk-factors">
        <h4>Factores de Riesgo</h4>
        <ul>
          {data.risk_factors.map((factor, index) => (
            <li key={index} className="risk-factor">
              <span className="risk-icon">⚠️</span>
              {factor}
            </li>
          ))}
        </ul>
      </div>

      {/* Métricas de Riesgo */}
      <div className="risk-metrics">
        <div className="metric">
          <span className="value">{data.days_in_default}</span>
          <span className="label">Días en Mora</span>
        </div>
        <div className="metric">
          <span className="value">{data.overdue_installments_count}</span>
          <span className="label">Cuotas Vencidas</span>
        </div>
        <div className="metric">
          <span className="value">${data.overdue_amount.toLocaleString()}</span>
          <span className="label">Monto Vencido</span>
        </div>
      </div>
    </div>
  );
};
```

#### 4. Desglose de Cuotas
```jsx
const InstallmentBreakdown = ({ data }) => (
  <div className="card">
    <h3>Desglose de Cuotas</h3>
    <div className="table-container">
      <table className="installments-table">
        <thead>
          <tr>
            <th>Cuota</th>
            <th>Fecha Vencimiento</th>
            <th>Monto</th>
            <th>Estado</th>
            <th>Días Vencido</th>
            <th>Capital</th>
            <th>Interés</th>
          </tr>
        </thead>
        <tbody>
          {data.map((installment, index) => (
            <tr key={index} className={`installment-row ${installment.status}`}>
              <td>{installment.number}</td>
              <td>{new Date(installment.due_date).toLocaleDateString()}</td>
              <td>${installment.amount.toLocaleString()}</td>
              <td>
                <span className={`status-badge ${installment.status}`}>
                  {installment.status}
                </span>
              </td>
              <td>
                {installment.days_overdue > 0 && (
                  <span className="overdue-days">
                    {installment.days_overdue} días
                  </span>
                )}
              </td>
              <td>${installment.principal_amount.toLocaleString()}</td>
              <td>${installment.interest_amount.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);
```

#### 5. Recomendaciones
```jsx
const Recommendations = ({ data }) => {
  const getRecommendationIcon = (type) => {
    switch (type) {
      case 'urgent': return '🚨';
      case 'high': return '⚠️';
      case 'medium': return '💡';
      case 'positive': return '✅';
      default: return 'ℹ️';
    }
  };

  const getRecommendationColor = (type) => {
    switch (type) {
      case 'urgent': return '#F44336';
      case 'high': return '#FF9800';
      case 'medium': return '#2196F3';
      case 'positive': return '#4CAF50';
      default: return '#757575';
    }
  };

  return (
    <div className="card">
      <h3>Recomendaciones</h3>
      <div className="recommendations-list">
        {data.map((rec, index) => (
          <div 
            key={index} 
            className={`recommendation ${rec.type}`}
            style={{ borderLeftColor: getRecommendationColor(rec.type) }}
          >
            <div className="recommendation-header">
              <span className="recommendation-icon">
                {getRecommendationIcon(rec.type)}
              </span>
              <span className="recommendation-title">{rec.title}</span>
            </div>
            <p className="recommendation-description">{rec.description}</p>
            <div className="recommendation-action">
              <button className="action-button">
                {rec.action === 'contact_client' && 'Contactar Cliente'}
                {rec.action === 'payment_plan' && 'Crear Plan de Pagos'}
                {rec.action === 'monitor' && 'Monitorear'}
                {rec.action === 'reward' && 'Recompensar'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
```

---

## 📈 Vista de Análisis Comparativo

### Endpoint
```
GET /api/insights/credits/analysis/comparative/
```

### Uso con Filtros
```javascript
const getComparativeAnalysis = async (filters = {}, token) => {
  try {
    const queryParams = new URLSearchParams();
    
    if (filters.start_date) queryParams.append('start_date', filters.start_date);
    if (filters.end_date) queryParams.append('end_date', filters.end_date);
    if (filters.subcategory_id) queryParams.append('subcategory_id', filters.subcategory_id);
    if (filters.user_id) queryParams.append('user_id', filters.user_id);

    const response = await fetch(
      `${API_BASE_URL}/credits/analysis/comparative/?${queryParams}`,
      {
        method: 'GET',
        headers: getHeaders(token)
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching comparative analysis:', error);
    throw error;
  }
};
```

### Componente de Filtros
```jsx
const ComparativeAnalysisFilters = ({ onFiltersChange }) => {
  const [filters, setFilters] = useState({
    start_date: '',
    end_date: '',
    subcategory_id: '',
    user_id: ''
  });

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFiltersChange(newFilters);
  };

  return (
    <div className="filters-panel">
      <h3>Filtros de Análisis</h3>
      <div className="filters-grid">
        <div className="filter-group">
          <label>Fecha Inicio:</label>
          <input
            type="date"
            value={filters.start_date}
            onChange={(e) => handleFilterChange('start_date', e.target.value)}
          />
        </div>
        <div className="filter-group">
          <label>Fecha Fin:</label>
          <input
            type="date"
            value={filters.end_date}
            onChange={(e) => handleFilterChange('end_date', e.target.value)}
          />
        </div>
        <div className="filter-group">
          <label>Subcategoría:</label>
          <select
            value={filters.subcategory_id}
            onChange={(e) => handleFilterChange('subcategory_id', e.target.value)}
          >
            <option value="">Todas</option>
            {/* Opciones de subcategorías */}
          </select>
        </div>
        <div className="filter-group">
          <label>Usuario:</label>
          <input
            type="number"
            placeholder="ID del usuario"
            value={filters.user_id}
            onChange={(e) => handleFilterChange('user_id', e.target.value)}
          />
        </div>
      </div>
    </div>
  );
};
```

### Componente de Análisis Comparativo
```jsx
const ComparativeAnalysisComponent = ({ token }) => {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({});

  const fetchAnalysis = async (newFilters) => {
    try {
      setLoading(true);
      const data = await getComparativeAnalysis(newFilters, token);
      
      if (data.success) {
        setAnalysis(data.data);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalysis(filters);
  }, [filters]);

  if (loading) return <div>Cargando análisis...</div>;
  if (!analysis) return <div>No hay datos disponibles</div>;

  return (
    <div className="comparative-analysis">
      <ComparativeAnalysisFilters onFiltersChange={setFilters} />
      
      {/* Resumen General */}
      <div className="summary-cards">
        <div className="summary-card">
          <h4>Total Créditos</h4>
          <span className="summary-value">{analysis.summary.total_credits}</span>
        </div>
        <div className="summary-card">
          <h4>Monto Total</h4>
          <span className="summary-value">
            ${analysis.summary.total_amount.toLocaleString()}
          </span>
        </div>
        <div className="summary-card">
          <h4>Tasa de Morosidad</h4>
          <span className="summary-value">
            {analysis.summary.default_rate.toFixed(1)}%
          </span>
        </div>
        <div className="summary-card">
          <h4>Tasa de Recaudación</h4>
          <span className="summary-value">
            {analysis.summary.collection_rate.toFixed(1)}%
          </span>
        </div>
      </div>

      {/* Análisis por Categoría */}
      <div className="category-analysis">
        <h3>Análisis por Categoría</h3>
        <div className="category-chart">
          {/* Implementar gráfico de barras o dona */}
        </div>
      </div>

      {/* Top Créditos */}
      <div className="top-credits">
        <h3>Top Créditos por Monto</h3>
        <div className="credits-table">
          {/* Tabla de créditos */}
        </div>
      </div>
    </div>
  );
};
```

---

## 📊 Vista de Métricas de Rendimiento

### Endpoint
```
GET /api/insights/credits/performance/
```

### Uso con Parámetros
```javascript
const getPerformanceMetrics = async (period = '30d', metricType = 'all', token) => {
  try {
    const queryParams = new URLSearchParams();
    queryParams.append('period', period);
    queryParams.append('metric_type', metricType);

    const response = await fetch(
      `${API_BASE_URL}/credits/performance/?${queryParams}`,
      {
        method: 'GET',
        headers: getHeaders(token)
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching performance metrics:', error);
    throw error;
  }
};
```

### Componente de Métricas de Rendimiento
```jsx
const PerformanceMetricsComponent = ({ token }) => {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [period, setPeriod] = useState('30d');
  const [metricType, setMetricType] = useState('all');

  const fetchMetrics = async () => {
    try {
      setLoading(true);
      const data = await getPerformanceMetrics(period, metricType, token);
      
      if (data.success) {
        setMetrics(data.data);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
  }, [period, metricType]);

  if (loading) return <div>Cargando métricas...</div>;
  if (!metrics) return <div>No hay métricas disponibles</div>;

  return (
    <div className="performance-metrics">
      {/* Controles */}
      <div className="metrics-controls">
        <div className="control-group">
          <label>Período:</label>
          <select value={period} onChange={(e) => setPeriod(e.target.value)}>
            <option value="7d">Últimos 7 días</option>
            <option value="30d">Últimos 30 días</option>
            <option value="90d">Últimos 90 días</option>
            <option value="1y">Último año</option>
          </select>
        </div>
        <div className="control-group">
          <label>Tipo de Métrica:</label>
          <select value={metricType} onChange={(e) => setMetricType(e.target.value)}>
            <option value="all">Todas</option>
            <option value="collection">Recaudación</option>
            <option value="risk">Riesgo</option>
            <option value="performance">Rendimiento</option>
          </select>
        </div>
      </div>

      {/* Métricas de Recaudación */}
      {metrics.metrics.collection && (
        <div className="metrics-section">
          <h3>Métricas de Recaudación</h3>
          <div className="metrics-grid">
            <div className="metric-card">
              <span className="metric-value">
                {metrics.metrics.collection.avg_collection_rate.toFixed(1)}%
              </span>
              <span className="metric-label">Tasa Promedio de Recaudación</span>
            </div>
            <div className="metric-card">
              <span className="metric-value">
                ${metrics.metrics.collection.total_collected.toLocaleString()}
              </span>
              <span className="metric-label">Total Recaudado</span>
            </div>
          </div>
        </div>
      )}

      {/* Métricas de Riesgo */}
      {metrics.metrics.risk && (
        <div className="metrics-section">
          <h3>Métricas de Riesgo</h3>
          <div className="metrics-grid">
            <div className="metric-card">
              <span className="metric-value">
                {metrics.metrics.risk.default_rate.toFixed(1)}%
              </span>
              <span className="metric-label">Tasa de Morosidad</span>
            </div>
            <div className="metric-card">
              <span className="metric-value">
                {metrics.metrics.risk.total_in_default}
              </span>
              <span className="metric-label">Créditos en Mora</span>
            </div>
          </div>
        </div>
      )}

      {/* Métricas de Rendimiento */}
      {metrics.metrics.performance && (
        <div className="metrics-section">
          <h3>Métricas de Rendimiento</h3>
          <div className="metrics-grid">
            <div className="metric-card">
              <span className="metric-value">
                {metrics.metrics.performance.avg_roi.toFixed(1)}%
              </span>
              <span className="metric-label">ROI Promedio</span>
            </div>
            <div className="metric-card">
              <span className="metric-value">
                ${metrics.metrics.performance.total_earnings.toLocaleString()}
              </span>
              <span className="metric-label">Ganancias Totales</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
```

---

## 🚨 Manejo de Errores

### Función de Manejo de Errores
```javascript
const handleApiError = (error, response) => {
  if (response) {
    switch (response.status) {
      case 401:
        return 'No autorizado. Por favor, inicia sesión nuevamente.';
      case 403:
        return 'No tienes permisos para acceder a esta información.';
      case 404:
        return 'El crédito solicitado no fue encontrado.';
      case 400:
        return 'Datos de entrada inválidos. Verifica los parámetros.';
      case 500:
        return 'Error interno del servidor. Intenta nuevamente más tarde.';
      default:
        return 'Error inesperado. Contacta al administrador.';
    }
  }
  return error.message || 'Error desconocido';
};
```

### Componente de Error
```jsx
const ErrorComponent = ({ error, onRetry }) => (
  <div className="error-container">
    <div className="error-icon">⚠️</div>
    <h3>Error</h3>
    <p className="error-message">{error}</p>
    {onRetry && (
      <button className="retry-button" onClick={onRetry}>
        Intentar Nuevamente
      </button>
    )}
  </div>
);
```

---

## 🎨 Estilos CSS Recomendados

```css
/* Estilos base para las tarjetas */
.card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Grid de información */
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-item label {
  font-weight: 600;
  color: #666;
  margin-bottom: 5px;
}

.amount {
  font-size: 1.2em;
  font-weight: bold;
  color: #2e7d32;
}

.amount.pending {
  color: #d32f2f;
}

/* Estados de crédito */
.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8em;
  font-weight: bold;
  text-transform: uppercase;
}

.status.completed { background: #e8f5e8; color: #2e7d32; }
.status.pending { background: #fff3e0; color: #f57c00; }
.status.checking { background: #e3f2fd; color: #1976d2; }

/* Niveles de morosidad */
.morosidad {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8em;
  font-weight: bold;
  text-transform: uppercase;
}

.morosidad.on_time { background: #e8f5e8; color: #2e7d32; }
.morosidad.mild_default { background: #fff3e0; color: #f57c00; }
.morosidad.moderate_default { background: #fce4ec; color: #c2185b; }
.morosidad.severe_default { background: #ffebee; color: #d32f2f; }

/* Métricas */
.metric {
  text-align: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.metric .value {
  display: block;
  font-size: 2em;
  font-weight: bold;
  color: #1976d2;
}

.metric .label {
  display: block;
  font-size: 0.9em;
  color: #666;
  margin-top: 5px;
}

/* Barra de progreso */
.progress-bar {
  width: 100%;
  height: 20px;
  background: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  margin: 10px 0;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4caf50, #8bc34a);
  transition: width 0.3s ease;
}

/* Score de riesgo */
.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  position: relative;
  margin: 0 auto;
}

.score-fill {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.score-value {
  font-size: 2em;
  font-weight: bold;
  color: white;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

/* Tabla de cuotas */
.installments-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

.installments-table th,
.installments-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.installments-table th {
  background: #f5f5f5;
  font-weight: 600;
}

.installment-row.overdue {
  background: #ffebee;
}

.installment-row.paid {
  background: #e8f5e8;
}

/* Recomendaciones */
.recommendation {
  border-left: 4px solid;
  padding: 15px;
  margin-bottom: 15px;
  background: #f8f9fa;
  border-radius: 0 8px 8px 0;
}

.recommendation.urgent {
  border-left-color: #f44336;
  background: #ffebee;
}

.recommendation.high {
  border-left-color: #ff9800;
  background: #fff3e0;
}

.recommendation.medium {
  border-left-color: #2196f3;
  background: #e3f2fd;
}

.recommendation.positive {
  border-left-color: #4caf50;
  background: #e8f5e8;
}

/* Responsive */
@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .installments-table {
    font-size: 0.9em;
  }
  
  .installments-table th,
  .installments-table td {
    padding: 8px;
  }
}
```

---

## 📱 Ejemplos de Implementación Completa

### Hook Personalizado para Insights
```javascript
import { useState, useEffect } from 'react';

export const useCreditInsights = (creditId, token) => {
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInsights = async () => {
      if (!creditId || !token) return;
      
      try {
        setLoading(true);
        setError(null);
        
        const data = await getCreditInsights(creditId, token);
        
        if (data.success) {
          setInsights(data.data);
        } else {
          setError(data.error);
        }
      } catch (err) {
        setError(handleApiError(err));
      } finally {
        setLoading(false);
      }
    };

    fetchInsights();
  }, [creditId, token]);

  const refetch = () => {
    setLoading(true);
    setError(null);
    // Lógica de refetch
  };

  return { insights, loading, error, refetch };
};
```

### Página Completa de Insights
```jsx
import React from 'react';
import { useCreditInsights } from './hooks/useCreditInsights';

const CreditInsightsPage = ({ match, user, token }) => {
  const { creditId } = match.params;
  const { insights, loading, error, refetch } = useCreditInsights(creditId, token);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Cargando insights del crédito...</p>
      </div>
    );
  }

  if (error) {
    return (
      <ErrorComponent 
        error={error} 
        onRetry={refetch} 
      />
    );
  }

  if (!insights) {
    return (
      <div className="no-data">
        <h3>No se encontraron insights</h3>
        <p>No hay datos disponibles para este crédito.</p>
      </div>
    );
  }

  return (
    <div className="credit-insights-page">
      <div className="page-header">
        <h1>Insights del Crédito</h1>
        <div className="header-actions">
          <button className="btn btn-secondary" onClick={refetch}>
            Actualizar
          </button>
          <button className="btn btn-primary">
            Exportar Reporte
          </button>
        </div>
      </div>

      <div className="insights-content">
        <CreditBasicInfo data={insights.credit_basic_info} />
        <PaymentAnalysis data={insights.payment_analysis} />
        <RiskAssessment data={insights.risk_assessment} />
        <PerformanceMetrics data={insights.performance_metrics} />
        <InstallmentBreakdown data={insights.installment_breakdown} />
        <TimelineAnalysis data={insights.timeline_analysis} />
        <ComparativeAnalysis data={insights.comparative_analysis} />
        <Recommendations data={insights.recommendations} />
      </div>
    </div>
  );
};

export default CreditInsightsPage;
```

---

## 🔗 Enlaces Útiles

- **Documentación de la API:** `/docs/credit-insights-api-documentation.md`
- **Ejemplos de Postman:** Disponibles en la colección de la API
- **Guía de Autenticación:** Documentación del sistema de autenticación
- **Componentes de UI:** Biblioteca de componentes reutilizables

---

## 📞 Soporte

Para dudas o problemas con la implementación:
- **Email:** dev-team@fintech.com
- **Slack:** #frontend-support
- **Documentación:** Wiki interno del proyecto
