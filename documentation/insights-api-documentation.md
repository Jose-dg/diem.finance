# 📊 Documentación de API Insights - Dashboard Interactivo

## 🎯 Descripción General

La API de Insights proporciona endpoints especializados para crear dashboards interactivos y analíticos en el frontend. Todos los endpoints están diseñados para consumir datos de la aplicación `fintech` y transformarlos en métricas, analytics y visualizaciones útiles para la toma de decisiones.

### 🔐 Autenticación
Todos los endpoints requieren autenticación JWT. Incluye el token en el header:
```
Authorization: Bearer <your-jwt-token>
```

### 📋 Formato de Respuesta
Todas las respuestas siguen el formato estándar:
```json
{
  "success": true,
  "data": {
    // Datos específicos del endpoint
  }
}
```

---

## 🏢 Dashboard Ejecutivo

### 📈 Executive Dashboard
**Endpoint:** `GET /api/insights/dashboard/executive/`  
**Permisos:** Administradores  
**Descripción:** KPIs principales para la alta dirección

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "total_portfolio": "1500000.00",
    "active_credits": 1250,
    "monthly_disbursements": "85000.00",
    "monthly_earnings": "12500.00",
    "pending_amount": "45000.00",
    "overdue_credits": 45,
    "new_users_this_month": 28,
    "total_users": 850,
    "collection_rate": 97.0,
    "default_rate": 3.6
  }
}
```

**Campos:**
- `total_portfolio`: Valor total del portafolio de créditos
- `active_credits`: Número de créditos activos
- `monthly_disbursements`: Desembolsos del mes actual
- `monthly_earnings`: Ganancias del mes actual
- `pending_amount`: Monto pendiente de cobro
- `overdue_credits`: Créditos en mora
- `new_users_this_month`: Nuevos usuarios del mes
- `total_users`: Total de usuarios registrados
- `collection_rate`: Tasa de cobranza (%)
- `default_rate`: Tasa de morosidad (%)

---

## 💳 Analytics de Créditos

### 📊 Credit Analytics Dashboard
**Endpoint:** `GET /api/insights/dashboard/credits/?days=30`  
**Permisos:** Usuarios autenticados  
**Parámetros:** `days` (opcional, default: 30)

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "monthly_trends": [
      {
        "month": "2024-01",
        "total_credits": 45,
        "total_amount": "125000.00",
        "total_earnings": "18750.00",
        "completed_credits": 42
      }
    ],
    "category_distribution": [
      {
        "subcategory__name": "Préstamos Personales",
        "count": 25,
        "total_amount": "75000.00",
        "avg_amount": "3000.00"
      }
    ],
    "credit_states": [
      {
        "state": "completed",
        "count": 1200,
        "total_amount": "1500000.00"
      }
    ],
    "top_sellers": [
      {
        "seller__user__username": "vendedor1",
        "credits_created": 15,
        "total_amount": "45000.00",
        "completion_rate": 93.3
      }
    ],
    "credits_by_status": [
      {
        "state": "pending",
        "count": 25,
        "total_amount": "75000.00"
      }
    ],
    "credits_by_category": [
      {
        "subcategory__name": "Préstamos Personales",
        "count": 30,
        "total_amount": "90000.00",
        "avg_amount": "3000.00"
      }
    ],
    "daily_trends": [
      {
        "date": "2024-01-15",
        "count": 3,
        "total_amount": "9000.00"
      }
    ],
    "period_days": 30
  }
}
```

**Visualizaciones Recomendadas:**
- **Gráfico de líneas:** Tendencias mensuales
- **Gráfico de dona:** Distribución por categorías
- **Gráfico de barras:** Estados de créditos
- **Tabla:** Top vendedores
- **Gráfico de líneas:** Tendencias diarias

---

## ⚠️ Dashboard de Riesgos

### 🛡️ Risk Dashboard
**Endpoint:** `GET /api/insights/dashboard/risk/`  
**Permisos:** Administradores  
**Descripción:** Métricas de gestión de riesgos

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "overdue_by_days": [
      {
        "days": 1,
        "credits_count": 5,
        "amount": "15000.00"
      },
      {
        "days": 7,
        "credits_count": 12,
        "amount": "35000.00"
      }
    ],
    "default_by_category": [
      {
        "subcategory__name": "Préstamos Personales",
        "total_credits": 500,
        "overdue_credits": 15,
        "total_pending": "45000.00",
        "default_rate": 3.0
      }
    ],
    "overdue_installments": {
      "count": 45,
      "total_amount": "125000.00",
      "avg_days_overdue": 12.5
    },
    "risk_prediction": [
      {
        "subcategory__name": "Préstamos Personales",
        "total_credits": 500,
        "defaulted_credits": 15,
        "risk_score": 3.0
      }
    ],
    "overdue_credits": 45,
    "overdue_installments": 45,
    "default_distribution": [
      {
        "morosidad_level": "baja",
        "count": 35,
        "total_amount": "105000.00"
      }
    ],
    "risk_by_category": [
      {
        "subcategory__name": "Préstamos Personales",
        "count": 15,
        "total_pending": "45000.00",
        "avg_pending": "3000.00"
      }
    ]
  }
}
```

**Visualizaciones Recomendadas:**
- **Gráfico de barras:** Créditos en mora por días
- **Gráfico de dona:** Distribución de morosidad por categoría
- **Tarjetas de métricas:** Resumen de cuotas vencidas
- **Gráfico de barras:** Predicción de riesgo por categoría
- **Gráfico de líneas:** Evolución de morosidad

---

## 👥 Insights de Usuarios

### 👤 User Insights Dashboard
**Endpoint:** `GET /api/insights/dashboard/users/`  
**Permisos:** Usuarios autenticados  
**Descripción:** Análisis de comportamiento de usuarios

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "user_segments": {
      "high_value": 85,
      "medium_value": 320,
      "low_value": 445,
      "new_users": 28
    },
    "top_users": [
      {
        "id_user": "uuid-123",
        "username": "usuario1",
        "credit_count": 5,
        "total_amount": "25000.00",
        "transaction_count": 12
      }
    ],
    "active_users": [
      {
        "id_user": "uuid-123",
        "username": "usuario1",
        "credit_count": 5,
        "transaction_count": 12,
        "total_credit_amount": "25000.00",
        "last_activity": "2024-01-15T10:30:00Z"
      }
    ]
  }
}
```

**Visualizaciones Recomendadas:**
- **Gráfico de dona:** Segmentación de usuarios por valor
- **Tabla:** Top usuarios más activos
- **Gráfico de barras:** Distribución de usuarios por segmento
- **Tarjetas de métricas:** Resumen de usuarios nuevos

---

## ⚙️ Dashboard Operacional

### 🔧 Operational Dashboard
**Endpoint:** `GET /api/insights/dashboard/operational/`  
**Permisos:** Administradores  
**Descripción:** Métricas de eficiencia operacional

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "processing_efficiency": {
      "total_credits": 150,
      "completed_credits": 135,
      "pending_credits": 10,
      "rejected_credits": 5,
      "completion_rate": 90.0
    },
    "seller_performance": [
      {
        "seller__user__username": "vendedor1",
        "credits_created": 25,
        "total_amount": "75000.00",
        "completion_rate": 92.0,
        "avg_amount": "3000.00"
      }
    ],
    "alerts": {
      "overdue_credits": 45,
      "pending_approvals": 15,
      "low_balance_accounts": 8
    }
  }
}
```

**Visualizaciones Recomendadas:**
- **Gráfico de dona:** Eficiencia de procesamiento
- **Tabla:** Rendimiento de vendedores
- **Tarjetas de alertas:** Alertas operacionales
- **Gráfico de barras:** Comparación de vendedores

---

## 💰 Dashboard de Ingresos

### 💵 Revenue Dashboard
**Endpoint:** `GET /api/insights/dashboard/revenue/`  
**Permisos:** Administradores  
**Descripción:** Análisis de ingresos y rentabilidad

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "revenue_trends": [
      {
        "month": "2024-01",
        "total_revenue": "125000.00",
        "total_credits": 45,
        "total_amount": "750000.00",
        "avg_earnings": "2777.78"
      }
    ],
    "profitability_by_category": [
      {
        "subcategory__name": "Préstamos Personales",
        "total_revenue": "75000.00",
        "total_cost": "60000.00",
        "total_price": "750000.00",
        "credit_count": 25,
        "profit_margin": 10.0,
        "roi": 25.0
      }
    ],
    "top_products": [
      {
        "subcategory__name": "Préstamos Personales",
        "total_revenue": "75000.00",
        "profit_margin": 10.0,
        "roi": 25.0
      }
    ],
    "current_month_revenue": "125000.00",
    "growth_rate": 15.5
  }
}
```

**Visualizaciones Recomendadas:**
- **Gráfico de líneas:** Tendencias de ingresos
- **Gráfico de barras:** Rentabilidad por categoría
- **Tabla:** Top productos por rentabilidad
- **Tarjetas de métricas:** Ingresos actuales y crecimiento

---

## 📊 Analytics Específicos

### 🏦 Portfolio Overview
**Endpoint:** `GET /api/insights/portfolio/overview/`  
**Permisos:** Usuarios autenticados  
**Descripción:** Vista general del portafolio

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "total_credits": 1500,
    "active_credits": 1250,
    "pending_credits": 250,
    "total_portfolio_value": "1500000.00",
    "total_pending_amount": "45000.00",
    "avg_credit_amount": "1200.00",
    "collection_rate": 97.0
  }
}
```

### 🔮 Predictive Insights
**Endpoint:** `GET /api/insights/predictive/insights/`  
**Permisos:** Administradores  
**Descripción:** Insights predictivos y tendencias

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "demand_prediction": [
      {
        "month": "2024-02",
        "demand": 52,
        "total_amount": "156000.00"
      }
    ],
    "payment_patterns": [
      {
        "day_of_week": 1,
        "day_of_month": 15,
        "payment_count": 25
      }
    ],
    "default_prediction": [
      {
        "subcategory__name": "Préstamos Personales",
        "total_credits": 500,
        "defaulted_credits": 15,
        "default_rate": 3.0
      }
    ]
  }
}
```

---

## 📋 Resumen Completo

### 📈 Insights Summary
**Endpoint:** `GET /api/insights/summary/`  
**Permisos:** Usuarios autenticados  
**Descripción:** Resumen de todos los insights disponibles

**Respuesta:**
```json
{
  "success": true,
  "data": {
    "portfolio": { /* Portfolio Overview */ },
    "user_behavior": { /* User Behavior Analytics */ },
    "risk": { /* Risk Analytics */ },
    "revenue": { /* Revenue Analytics */ },
    "operational": { /* Operational Metrics */ },
    "predictive": { /* Predictive Insights */ }
  }
}
```

---

## 🔧 Utilidades

### 🏥 Health Check
**Endpoint:** `GET /api/insights/health-check/`  
**Permisos:** Usuarios autenticados  
**Descripción:** Verificar estado de la API

### 📤 Export Data
**Endpoint:** `GET /api/insights/export/?type=summary&format=json`  
**Permisos:** Usuarios autenticados  
**Parámetros:** 
- `type`: summary, portfolio, user_behavior, risk, revenue, operational, predictive
- `format`: json, csv, excel

---

## 🎨 Guías de Implementación Frontend

### 📱 Componentes Recomendados:
1. **Tarjetas de Métricas:** Para KPIs principales
2. **Gráficos de Líneas:** Para tendencias temporales
3. **Gráficos de Barras:** Para comparaciones
4. **Gráficos de Dona:** Para distribuciones
5. **Tablas Interactivas:** Para datos detallados
6. **Alertas Visuales:** Para métricas críticas

### 🔄 Actualización de Datos:
- **Tiempo real:** Cada 30 segundos para dashboards críticos
- **Semi-real:** Cada 5 minutos para analytics generales
- **Manual:** Botón de refresh para datos históricos

### 📱 Responsive Design:
- **Desktop:** Dashboards completos con múltiples gráficos
- **Tablet:** Layout adaptativo con gráficos principales
- **Mobile:** Métricas clave en tarjetas apiladas

### 🎯 Interactividad:
- **Filtros:** Por fecha, categoría, vendedor
- **Drill-down:** Click en gráficos para ver detalles
- **Export:** Botones para descargar datos
- **Comparación:** Múltiples períodos en un gráfico

---

## 🚀 Próximos Pasos

1. **Implementar componentes base** para cada tipo de visualización
2. **Crear sistema de filtros** reutilizable
3. **Implementar actualización automática** de datos
4. **Agregar interactividad** y drill-down
5. **Optimizar rendimiento** para grandes volúmenes de datos
6. **Implementar exportación** de datos
7. **Agregar notificaciones** para alertas críticas

Esta documentación proporciona toda la información necesaria para crear un dashboard interactivo completo y funcional.

