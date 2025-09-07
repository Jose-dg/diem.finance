# 📊 Documentación API - Insights por Crédito

## 🎯 Descripción General

Este documento describe las nuevas vistas API para generar insights detallados por crédito individual y análisis comparativo de créditos, aprovechando la robustez de los modelos de créditos existentes.

## 🚀 Endpoints Disponibles

### 1. **CreditInsightsView** - Insights Detallados por Crédito

**Endpoint:** `GET /api/insights/credits/insights/<credit_id>/`  
**Permisos:** Usuarios autenticados (propietario del crédito o administradores)  
**Descripción:** Obtiene insights detallados de un crédito específico

#### Parámetros:
- `credit_id` (path): UUID del crédito

#### Respuesta:
```json
{
  "success": true,
  "data": {
    "credit_basic_info": {
      "uid": "123e4567-e89b-12d3-a456-426614174000",
      "user": {
        "id": 1,
        "username": "usuario_ejemplo",
        "email": "usuario@ejemplo.com"
      },
      "subcategory": {
        "name": "Préstamos Personales",
        "category": "Créditos"
      },
      "amounts": {
        "price": 50000.00,
        "cost": 45000.00,
        "earnings": 5000.00,
        "pending_amount": 25000.00,
        "total_abonos": 25000.00,
        "refinancing": 0.00
      },
      "terms": {
        "credit_days": 365,
        "interest_rate": 12.5,
        "installment_number": 12,
        "installment_value": 4166.67,
        "periodicity": "Mensual"
      },
      "dates": {
        "created_at": "2024-01-15T10:30:00Z",
        "first_date_payment": "2024-02-15",
        "second_date_payment": "2025-01-15",
        "updated_at": "2024-01-20T14:45:00Z"
      },
      "status": {
        "state": "completed",
        "is_in_default": false,
        "morosidad_level": "on_time"
      }
    },
    "payment_analysis": {
      "installment_summary": {
        "total_installments": 12,
        "paid_installments": 6,
        "overdue_installments": 0,
        "pending_installments": 6,
        "payment_rate": 50.0
      },
      "payment_behavior": {
        "on_time_payments": 5,
        "late_payments": 1,
        "punctuality_rate": 83.33,
        "avg_delay_days": 3.5
      },
      "amounts": {
        "total_paid": 25000.00,
        "total_pending": 25000.00,
        "payment_progress": 50.0
      }
    },
    "risk_assessment": {
      "risk_score": 15,
      "risk_level": "low",
      "days_in_default": 0,
      "overdue_installments_count": 0,
      "overdue_amount": 0.00,
      "morosidad_history": 1,
      "risk_factors": ["1 pagos tardíos en historial"]
    },
    "performance_metrics": {
      "roi": 11.11,
      "collection_efficiency": 50.0,
      "avg_payment_interval_days": 30.5,
      "expected_vs_actual_payments": {
        "expected": 12,
        "actual": 6,
        "variance": -6
      }
    },
    "installment_breakdown": [
      {
        "number": 1,
        "due_date": "2024-02-15",
        "amount": 4166.67,
        "paid": true,
        "paid_on": "2024-02-15",
        "status": "paid",
        "days_overdue": 0,
        "principal_amount": 3750.00,
        "interest_amount": 416.67,
        "late_fee": 0.00,
        "amount_paid": 4166.67
      }
    ],
    "timeline_analysis": {
      "credit_lifecycle": {
        "total_days": 365,
        "elapsed_days": 180,
        "progress_percentage": 49.32,
        "remaining_days": 185
      },
      "monthly_payment_trends": [
        {
          "month": "2024-02-01T00:00:00Z",
          "count": 1,
          "total_amount": 4166.67
        }
      ]
    },
    "comparative_analysis": {
      "user_comparison": {
        "user_avg_payment_rate": 75.0,
        "current_payment_rate": 50.0,
        "performance_vs_user_avg": -25.0
      },
      "category_comparison": {
        "category_avg_default_rate": 5.2,
        "current_is_in_default": false,
        "performance_vs_category": "better"
      }
    },
    "recommendations": [
      {
        "type": "medium",
        "title": "Historial de pagos tardíos",
        "description": "1 pagos tardíos detectados. Monitorear de cerca.",
        "action": "monitor"
      }
    ]
  }
}
```

---

### 2. **CreditAnalysisView** - Análisis Comparativo de Créditos

**Endpoint:** `GET /api/insights/credits/analysis/comparative/`  
**Permisos:** Solo administradores  
**Descripción:** Análisis comparativo de múltiples créditos con filtros

#### Parámetros de consulta:
- `start_date` (opcional): Fecha de inicio (YYYY-MM-DD)
- `end_date` (opcional): Fecha de fin (YYYY-MM-DD)
- `subcategory_id` (opcional): ID de la subcategoría
- `user_id` (opcional): ID del usuario

#### Respuesta:
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_credits": 150,
      "total_amount": 7500000.00,
      "total_pending": 2500000.00,
      "default_rate": 8.5,
      "collection_rate": 66.67
    },
    "category_analysis": [
      {
        "subcategory__name": "Préstamos Personales",
        "count": 75,
        "total_amount": 3750000.00,
        "default_count": 8,
        "avg_amount": 50000.00
      }
    ],
    "state_analysis": [
      {
        "state": "completed",
        "count": 120,
        "total_amount": 6000000.00
      }
    ],
    "morosidad_analysis": [
      {
        "morosidad_level": "on_time",
        "count": 120,
        "total_amount": 6000000.00
      }
    ],
    "top_credits": [
      {
        "uid": "123e4567-e89b-12d3-a456-426614174000",
        "user__username": "usuario_ejemplo",
        "subcategory__name": "Préstamos Personales",
        "price": 100000.00,
        "pending_amount": 50000.00,
        "is_in_default": false
      }
    ]
  }
}
```

---

### 3. **CreditPerformanceView** - Métricas de Rendimiento

**Endpoint:** `GET /api/insights/credits/performance/`  
**Permisos:** Solo administradores  
**Descripción:** Métricas de rendimiento de créditos por período

#### Parámetros de consulta:
- `period` (opcional): Período de análisis (7d, 30d, 90d, 1y) - Default: 30d
- `metric_type` (opcional): Tipo de métrica (collection, risk, performance, all) - Default: all

#### Respuesta:
```json
{
  "success": true,
  "data": {
    "period": "30d",
    "start_date": "2024-01-01T00:00:00Z",
    "end_date": "2024-01-31T23:59:59Z",
    "metrics": {
      "collection": {
        "total_credits": 50,
        "total_amount": 2500000.00,
        "total_collected": 1500000.00,
        "avg_collection_rate": 60.0,
        "collection_status": {
          "fully_collected": 20,
          "partially_collected": 25,
          "low_collection": 5
        }
      },
      "risk": {
        "total_in_default": 5,
        "default_rate": 10.0,
        "avg_days_in_default": 15.5,
        "morosidad_distribution": [
          {
            "morosidad_level": "on_time",
            "count": 40,
            "total_amount": 2000000.00
          }
        ]
      },
      "performance": {
        "avg_credit_amount": 50000.00,
        "avg_credit_days": 365,
        "avg_interest_rate": 12.5,
        "total_earnings": 250000.00,
        "avg_roi": 10.0
      }
    }
  }
}
```

---

## 🔧 Características Técnicas

### **Robustez de los Modelos Aprovechada:**

1. **Modelo Credit:**
   - Estados de crédito (checking, pending, completed, to_solve, preorder)
   - Niveles de morosidad detallados
   - Campos de seguimiento de pagos (total_abonos, pending_amount)
   - Relaciones con usuarios, subcategorías, periodos

2. **Modelo Installment:**
   - Estados de cuotas (pending, paid, overdue, cancelled, partial)
   - Seguimiento de pagos parciales
   - Sistema de notificaciones y recordatorios
   - Desglose de capital, intereses y recargos

3. **Modelo Transaction:**
   - Tipos de transacciones (income, expense)
   - Estados de transacciones
   - Fuentes de transacciones

### **Funcionalidades Avanzadas:**

- **Análisis de Riesgo:** Score de riesgo 0-100 con factores identificados
- **Análisis Comparativo:** Comparación con créditos del usuario y categoría
- **Recomendaciones Inteligentes:** Sugerencias basadas en comportamiento
- **Métricas de Rendimiento:** ROI, eficiencia de cobro, tendencias
- **Análisis Temporal:** Progreso del crédito y tendencias de pago
- **Desglose Detallado:** Información completa de cada cuota

### **Seguridad y Permisos:**

- **CreditInsightsView:** Usuarios autenticados (solo propietario o admin)
- **CreditAnalysisView:** Solo administradores
- **CreditPerformanceView:** Solo administradores
- Validación de acceso a créditos individuales
- Manejo de errores robusto

### **Optimizaciones de Performance:**

- Uso de `select_related` y `prefetch_related` para consultas eficientes
- Agregaciones optimizadas con `annotate` y `aggregate`
- Cálculos en base de datos para mejor rendimiento
- Paginación para grandes volúmenes de datos

---

## 📈 Casos de Uso

### **Para Usuarios Finales:**
- Ver el estado detallado de sus créditos
- Entender su historial de pagos
- Recibir recomendaciones personalizadas
- Comparar su rendimiento con otros usuarios

### **Para Administradores:**
- Análisis comparativo de cartera de créditos
- Identificación de patrones de riesgo
- Monitoreo de métricas de rendimiento
- Toma de decisiones basada en datos

### **Para Analistas:**
- Insights detallados por crédito individual
- Análisis de tendencias y patrones
- Evaluación de políticas de crédito
- Reportes de rendimiento

---

## 🚀 Ejemplos de Uso

### **Obtener insights de un crédito específico:**
```bash
curl -H "Authorization: Bearer <token>" \
     "https://api.fintech.com/insights/credits/insights/123e4567-e89b-12d3-a456-426614174000/"
```

### **Análisis comparativo con filtros:**
```bash
curl -H "Authorization: Bearer <token>" \
     "https://api.fintech.com/insights/credits/analysis/comparative/?start_date=2024-01-01&end_date=2024-01-31&subcategory_id=1"
```

### **Métricas de rendimiento del último mes:**
```bash
curl -H "Authorization: Bearer <token>" \
     "https://api.fintech.com/insights/credits/performance/?period=30d&metric_type=collection"
```

---

## 📝 Notas de Implementación

- Todas las vistas incluyen manejo robusto de errores
- Respuestas validadas con serializers de Django REST Framework
- Logging detallado para debugging y monitoreo
- Documentación inline en el código para mantenimiento
- Compatible con el sistema de permisos existente
- Optimizado para grandes volúmenes de datos
