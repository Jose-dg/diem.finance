# 🏦 FINANCIAL CONTROL SYSTEM & INSIGHTS

## 📋 Resumen Ejecutivo

El **Financial Control System** es una extensión del módulo de insights que proporciona herramientas avanzadas para el seguimiento, análisis y gestión de clientes morosos. El sistema se integra perfectamente con la infraestructura existente y sigue las mejores prácticas de Django.

## 🎯 Objetivos del Sistema

- ✅ **Seguimiento de Morosidad**: Monitoreo en tiempo real de clientes con pagos vencidos
- ✅ **Evaluación de Riesgo**: Sistema de puntuación automática de riesgo crediticio
- ✅ **Alertas Inteligentes**: Notificaciones automáticas para casos críticos
- ✅ **Reportes Detallados**: Generación automática de reportes de morosos
- ✅ **Paginación Optimizada**: Gestión eficiente de grandes volúmenes de datos
- ✅ **Dashboard Ejecutivo**: Vista consolidada de métricas financieras

## 🏗️ Arquitectura del Sistema

### Modelos Implementados

#### 1. **FinancialControlMetrics**
```python
# Métricas de control financiero por usuario
- total_overdue_amount: Monto total en mora
- overdue_credits_count: Número de créditos en mora
- risk_level: Nivel de riesgo (low/medium/high/critical)
- risk_score: Puntuación de riesgo (0-100)
- payment_frequency: Frecuencia de pagos
- default_history: Historial de morosidad
```

#### 2. **FinancialAlert**
```python
# Sistema de alertas financieras
- alert_type: Tipo de alerta (payment_overdue, risk_increase, etc.)
- priority: Prioridad (low/medium/high/urgent)
- status: Estado (active/acknowledged/resolved/expired)
- assigned_to: Usuario asignado para gestión
- expires_at: Fecha de expiración automática
```

#### 3. **DefaultersReport**
```python
# Reportes detallados de morosos
- report_type: Tipo de reporte (daily/weekly/monthly)
- total_defaulters: Total de clientes morosos
- risk_distribution: Distribución por niveles de riesgo
- recovery_potential: Análisis de potencial de recuperación
```

### Servicios Implementados

#### **FinancialControlService**
- `calculate_user_financial_metrics()`: Cálculo de métricas por usuario
- `get_defaulters_list()`: Lista paginada de morosos con filtros
- `create_financial_alert()`: Creación de alertas automáticas
- `generate_defaulters_report()`: Generación de reportes
- `get_financial_control_dashboard()`: Dashboard ejecutivo

## 🚀 ENDPOINTS DISPONIBLES

### 📊 **DASHBOARDS PRINCIPALES**

#### 1. Dashboard Ejecutivo
```http
GET /api/insights/dashboard/executive/
```
**Descripción**: KPIs principales para la alta dirección
**Respuesta**:
```json
{
  "success": true,
  "data": {
    "total_portfolio": "1000000.00",
    "active_credits": 150,
    "monthly_disbursements": "50000.00",
    "monthly_earnings": "5000.00",
    "pending_amount": "75000.00",
    "overdue_credits": 25,
    "collection_rate": 92.5,
    "default_rate": 16.67
  }
}
```

#### 2. Dashboard de Créditos
```http
GET /api/insights/dashboard/credits/?days=30
```
**Descripción**: Analytics detallados de créditos
**Parámetros**:
- `days`: Período de análisis (default: 30)

#### 3. Dashboard de Riesgos
```http
GET /api/insights/dashboard/risk/
```
**Descripción**: Métricas de riesgo crediticio

#### 4. Dashboard de Usuarios
```http
GET /api/insights/dashboard/users/
```
**Descripción**: Insights de comportamiento de usuarios

#### 5. Dashboard Operacional
```http
GET /api/insights/dashboard/operational/
```
**Descripción**: Métricas operacionales

#### 6. Dashboard de Ingresos
```http
GET /api/insights/dashboard/revenue/
```
**Descripción**: Analytics de ingresos

### 📈 **ANALYTICS ESPECÍFICOS**

#### 1. Vista General del Portafolio
```http
GET /api/insights/portfolio/overview/
```
**Descripción**: Resumen completo del portafolio de créditos

#### 2. Insights Predictivos
```http
GET /api/insights/predictive/insights/
```
**Descripción**: Análisis predictivo y tendencias futuras

#### 3. Análisis de Créditos
```http
GET /api/insights/credits/analysis/?start_date=2024-01-01&end_date=2024-12-31
```
**Descripción**: Análisis detallado de créditos por período
**Parámetros**:
- `start_date`: Fecha de inicio (YYYY-MM-DD)
- `end_date`: Fecha de fin (YYYY-MM-DD)

#### 4. Resumen de Créditos
```http
GET /api/insights/credits/analysis/summary/
```
**Descripción**: Resumen ejecutivo de análisis de créditos

#### 5. Análisis de Clientes
```http
GET /api/insights/credits/analysis/clients/
```
**Descripción**: Análisis específico de comportamiento de clientes

### 🏦 **FINANCIAL CONTROL SYSTEM**

#### 1. Dashboard de Control Financiero
```http
GET /api/insights/financial-control/dashboard/
```
**Descripción**: Dashboard específico para control financiero
**Respuesta**:
```json
{
  "success": true,
  "data": {
    "total_metrics": 150,
    "active_defaulters": 25,
    "total_overdue_amount": "150000.00",
    "risk_distribution": [
      {
        "risk_level": "low",
        "count": 5,
        "total_amount": "5000.00"
      },
      {
        "risk_level": "high",
        "count": 15,
        "total_amount": "120000.00"
      }
    ],
    "active_alerts": 8,
    "new_defaulters_30_days": 5,
    "default_rate": 16.67
  }
}
```

#### 2. Lista de Clientes Morosos (Con Paginación)
```http
GET /api/insights/financial-control/defaulters/?page=1&page_size=20&risk_level=high&min_overdue_amount=1000
```
**Descripción**: Lista paginada de clientes morosos con filtros avanzados
**Parámetros de Filtro**:
- `page`: Número de página (default: 1)
- `page_size`: Elementos por página (1-100, default: 20)
- `risk_level`: low/medium/high/critical
- `min_overdue_amount`: Monto mínimo en mora
- `max_overdue_amount`: Monto máximo en mora
- `min_days_overdue`: Días mínimos en mora

**Respuesta**:
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": 1,
        "user": {
          "id": 123,
          "username": "cliente_moroso",
          "email": "cliente@example.com",
          "first_name": "Juan",
          "last_name": "Pérez"
        },
        "total_overdue_amount": "5000.00",
        "overdue_credits_count": 2,
        "risk_level": "high",
        "risk_score": 75.5,
        "days_in_default": 45,
        "overdue_percentage": 66.67,
        "is_high_risk": true
      }
    ],
    "pagination": {
      "count": 25,
      "num_pages": 2,
      "current_page": 1,
      "has_next": true,
      "next_page": 2,
      "has_previous": false,
      "previous_page": null
    }
  }
}
```

#### 3. Insights Mejorados de Morosos
```http
GET /api/insights/financial-control/defaulters/enhanced/
```
**Descripción**: Análisis completo y mejorado de clientes morosos
**Respuesta**:
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_defaulters": 25,
      "total_overdue_amount": "150000.00",
      "new_defaulters_7_days": 3,
      "default_rate": 16.67
    },
    "risk_distribution": [
      {
        "risk_level": "low",
        "count": 5,
        "total_amount": "5000.00",
        "avg_days": 15.2
      }
    ],
    "top_defaulters": [
      {
        "user": {
          "id": 123,
          "username": "cliente_moroso",
          "email": "cliente@example.com"
        },
        "total_overdue_amount": "5000.00",
        "overdue_credits_count": 2,
        "days_in_default": 45,
        "risk_level": "high",
        "risk_score": 75.5
      }
    ],
    "alerts_by_priority": [
      {
        "priority": "high",
        "count": 5
      },
      {
        "priority": "urgent",
        "count": 3
      }
    ],
    "recovery_potential": {
      "high": 8,
      "medium": 12,
      "total_recoverable": 20
    }
  }
}
```

#### 4. Métricas de Usuario Específico
```http
GET /api/insights/financial-control/metrics/user/123/
```
**Descripción**: Métricas financieras detalladas de un usuario específico
**Respuesta**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user": {
      "id": 123,
      "username": "cliente_moroso",
      "email": "cliente@example.com",
      "first_name": "Juan",
      "last_name": "Pérez"
    },
    "total_overdue_amount": "5000.00",
    "overdue_credits_count": 2,
    "days_in_default": 45,
    "max_days_overdue": 60,
    "risk_level": "high",
    "risk_score": 75.5,
    "payment_frequency": 2.5,
    "avg_payment_delay": 5.2,
    "overdue_percentage": 66.67,
    "is_high_risk": true,
    "last_calculation": "2024-01-15T10:30:00Z"
  }
}
```

#### 5. Gestión de Alertas
```http
# Obtener alertas
GET /api/insights/financial-control/alerts/?page=1&page_size=20&status=active&priority=high

# Crear nueva alerta
POST /api/insights/financial-control/alerts/
Content-Type: application/json

{
  "user_id": 123,
  "alert_type": "risk_increase",
  "title": "Usuario de alto riesgo detectado",
  "description": "El usuario ha incrementado su nivel de riesgo a crítico",
  "priority": "urgent",
  "alert_data": {
    "risk_score": 85.5,
    "overdue_amount": 5000.00
  }
}
```

#### 6. Reportes de Morosos
```http
# Obtener reportes
GET /api/insights/financial-control/reports/?page=1&page_size=10&report_type=weekly

# Generar nuevo reporte
POST /api/insights/financial-control/reports/
Content-Type: application/json

{
  "report_type": "weekly"
}
```

### 🔧 **UTILIDADES Y HERRAMIENTAS**

#### 1. Resumen General de Insights
```http
GET /api/insights/summary/
```
**Descripción**: Resumen consolidado de todos los insights disponibles

#### 2. Health Check
```http
GET /api/insights/health-check/
```
**Descripción**: Verificación del estado del sistema de insights

#### 3. Exportación de Datos
```http
GET /api/insights/export/?format=json&type=defaulters
```
**Descripción**: Exportación de datos en diferentes formatos
**Parámetros**:
- `format`: json/csv/excel
- `type`: defaulters/alerts/reports

## 📝 **GUÍA DE USO PASO A PASO**

### 🔍 **1. Consultas Básicas de Insights**

#### Obtener Dashboard Ejecutivo
```bash
curl -X GET "http://localhost:8000/api/insights/dashboard/executive/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Obtener Análisis de Créditos
```bash
curl -X GET "http://localhost:8000/api/insights/credits/analysis/?start_date=2024-01-01&end_date=2024-12-31" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 🏦 **2. Consultas de Financial Control**

#### Obtener Lista de Morosos
```bash
# Obtener primera página de morosos
curl -X GET "http://localhost:8000/api/insights/financial-control/defaulters/?page=1&page_size=20" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Filtrar por riesgo alto
curl -X GET "http://localhost:8000/api/insights/financial-control/defaulters/?risk_level=high&min_overdue_amount=1000" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Obtener morosos con más de 30 días en mora
curl -X GET "http://localhost:8000/api/insights/financial-control/defaulters/?min_days_overdue=30" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Obtener Insights Mejorados
```bash
curl -X GET "http://localhost:8000/api/insights/financial-control/defaulters/enhanced/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Obtener Métricas de Usuario Específico
```bash
curl -X GET "http://localhost:8000/api/insights/financial-control/metrics/user/123/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 📊 **3. Gestión de Alertas**

#### Obtener Alertas Activas
```bash
curl -X GET "http://localhost:8000/api/insights/financial-control/alerts/?status=active&priority=high" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Crear Nueva Alerta
```bash
curl -X POST "http://localhost:8000/api/insights/financial-control/alerts/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 123,
    "alert_type": "risk_increase",
    "title": "Usuario de alto riesgo",
    "description": "Riesgo crítico detectado",
    "priority": "urgent"
  }'
```

### 📈 **4. Generación de Reportes**

#### Generar Reporte Diario
```bash
curl -X POST "http://localhost:8000/api/insights/financial-control/reports/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"report_type": "daily"}'
```

#### Obtener Reportes Existentes
```bash
curl -X GET "http://localhost:8000/api/insights/financial-control/reports/?report_type=weekly" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔧 Configuración y Uso

### 1. Migraciones
```bash
python3 manage.py makemigrations insights
python3 manage.py migrate
```

### 2. Cálculo Inicial de Métricas
```python
from apps.insights.services.financial_control_service import FinancialControlService
from apps.fintech.models import User

# Calcular métricas para todos los usuarios
for user in User.objects.all():
    FinancialControlService.calculate_user_financial_metrics(user)
```

### 3. Tareas Automatizadas (Celery)
```python
# Configurar en settings.py
CELERY_BEAT_SCHEDULE = {
    'calculate-financial-metrics-daily': {
        'task': 'apps.insights.tasks.calculate_all_financial_metrics',
        'schedule': crontab(hour=2, minute=0),  # 2:00 AM diario
    },
    'generate-daily-defaulters-report': {
        'task': 'apps.insights.tasks.generate_daily_defaulters_report',
        'schedule': crontab(hour=6, minute=0),  # 6:00 AM diario
    },
    'cleanup-expired-alerts': {
        'task': 'apps.insights.tasks.cleanup_expired_alerts',
        'schedule': crontab(hour=1, minute=0),  # 1:00 AM diario
    },
    'create-high-risk-alerts': {
        'task': 'apps.insights.tasks.create_high_risk_alerts',
        'schedule': crontab(hour=8, minute=0),  # 8:00 AM diario
    },
}
```

## 📊 Métricas y KPIs

### Métricas Principales
- **Total de Morosos**: Número de clientes con pagos vencidos
- **Monto Total en Mora**: Suma de todos los montos vencidos
- **Tasa de Morosidad**: Porcentaje de clientes morosos
- **Distribución por Riesgo**: Clasificación por niveles de riesgo
- **Potencial de Recuperación**: Análisis de probabilidad de pago

### Cálculo de Riesgo
```python
# Algoritmo de puntuación de riesgo (0-100)
risk_score = (
    amount_factor * 40 +    # Máximo 40 puntos por monto
    count_factor * 30 +     # Máximo 30 puntos por cantidad
    days_factor * 30        # Máximo 30 puntos por días
)
```

### Niveles de Riesgo
- **Low (0-29)**: Riesgo bajo
- **Medium (30-59)**: Riesgo medio
- **High (60-79)**: Riesgo alto
- **Critical (80-100)**: Riesgo crítico

## 🔔 Sistema de Alertas

### Tipos de Alertas
1. **payment_overdue**: Pago vencido
2. **multiple_overdue**: Múltiples pagos vencidos
3. **risk_increase**: Incremento de riesgo
4. **payment_pattern_change**: Cambio en patrón de pagos
5. **credit_limit_exceeded**: Límite de crédito excedido
6. **recovery_opportunity**: Oportunidad de recuperación

### Prioridades
- **Low**: Baja prioridad
- **Medium**: Prioridad media
- **High**: Alta prioridad
- **Urgent**: Urgente

### Estados
- **Active**: Alerta activa
- **Acknowledged**: Reconocida por un usuario
- **Resolved**: Resuelta
- **Expired**: Expirada automáticamente

## 📈 Reportes Automáticos

### Tipos de Reporte
- **Daily**: Reporte diario
- **Weekly**: Reporte semanal
- **Monthly**: Reporte mensual
- **Quarterly**: Reporte trimestral
- **Custom**: Reporte personalizado

### Contenido de Reportes
- Resumen ejecutivo
- Distribución por riesgo
- Top morosos por monto
- Análisis de tendencias
- Potencial de recuperación
- Recomendaciones de acción

## 🛡️ Seguridad y Permisos

### Permisos Requeridos
- **IsAuthenticated**: Usuario autenticado
- **IsAdminUser**: Solo administradores para vistas críticas

### Validaciones
- Límites de paginación (1-100 elementos por página)
- Validación de parámetros de filtro
- Sanitización de datos de entrada
- Manejo de errores robusto

## 🔄 Integración con Sistema Existente

### Compatibilidad
- ✅ Utiliza modelos existentes de `fintech`
- ✅ Aprovecha managers personalizados
- ✅ Integra con sistema de paginación global
- ✅ Compatible con autenticación existente
- ✅ Utiliza configuración de Celery existente

### Extensiones Futuras
- Integración con sistema de notificaciones
- Exportación a Excel/PDF
- API para integración con sistemas externos
- Dashboard en tiempo real con WebSockets
- Machine Learning para predicción de morosidad

## 📝 Ejemplos de Uso

### Ejemplo 1: Obtener Morosos de Alto Riesgo
```python
from apps.insights.services.financial_control_service import FinancialControlService

# Obtener lista paginada de morosos de alto riesgo
result = FinancialControlService.get_defaulters_list(
    page=1,
    page_size=20,
    filters={'risk_level': 'high'}
)

for defaulter in result['results']:
    print(f"Usuario: {defaulter.user.username}")
    print(f"Monto en mora: ${defaulter.total_overdue_amount}")
    print(f"Riesgo: {defaulter.risk_level}")
```

### Ejemplo 2: Crear Alerta Automática
```python
# Crear alerta para usuario de alto riesgo
alert = FinancialControlService.create_financial_alert(
    user=user,
    alert_type='risk_increase',
    title=f"Usuario de alto riesgo: {user.username}",
    description=f"Riesgo crítico detectado",
    priority='urgent',
    alert_data={'risk_score': 85.5}
)
```

### Ejemplo 3: Generar Reporte Personalizado
```python
# Generar reporte semanal
report = FinancialControlService.generate_defaulters_report(
    report_type='weekly',
    generated_by=request.user
)

print(f"Reporte generado: {report.id}")
print(f"Total morosos: {report.total_defaulters}")
print(f"Monto total: ${report.total_overdue_amount}")
```

### Ejemplo 4: Consulta Completa de Insights
```python
import requests

# Configurar headers
headers = {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
}

# 1. Obtener dashboard ejecutivo
response = requests.get(
    'http://localhost:8000/api/insights/dashboard/executive/',
    headers=headers
)
executive_data = response.json()

# 2. Obtener análisis de créditos
response = requests.get(
    'http://localhost:8000/api/insights/credits/analysis/?days=30',
    headers=headers
)
credits_data = response.json()

# 3. Obtener morosos de alto riesgo
response = requests.get(
    'http://localhost:8000/api/insights/financial-control/defaulters/?risk_level=high&page_size=10',
    headers=headers
)
defaulters_data = response.json()

# 4. Generar reporte
response = requests.post(
    'http://localhost:8000/api/insights/financial-control/reports/',
    headers=headers,
    json={'report_type': 'daily'}
)
report_data = response.json()

print("Dashboard Ejecutivo:", executive_data)
print("Análisis de Créditos:", credits_data)
print("Morosos de Alto Riesgo:", defaulters_data)
print("Reporte Generado:", report_data)
```

## 🎯 Beneficios del Sistema

1. **Visibilidad Completa**: Dashboard ejecutivo con métricas clave
2. **Gestión Proactiva**: Alertas automáticas para casos críticos
3. **Análisis Detallado**: Reportes con insights accionables
4. **Escalabilidad**: Paginación optimizada para grandes volúmenes
5. **Automatización**: Tareas programadas para mantenimiento
6. **Flexibilidad**: Filtros y parámetros configurables
7. **Integración**: Compatible con sistema existente
8. **Seguridad**: Permisos y validaciones robustas

## 🔧 Mantenimiento

### Tareas Diarias
- Cálculo automático de métricas
- Limpieza de alertas expiradas
- Generación de reportes diarios

### Tareas Semanales
- Generación de reportes semanales
- Análisis de tendencias
- Optimización de consultas

### Tareas Mensuales
- Generación de reportes mensuales
- Revisión de algoritmos de riesgo
- Actualización de configuraciones

## 📚 **REFERENCIA RÁPIDA DE ENDPOINTS**

### Dashboards
- `GET /api/insights/dashboard/executive/` - Dashboard ejecutivo
- `GET /api/insights/dashboard/credits/?days=30` - Dashboard de créditos
- `GET /api/insights/dashboard/risk/` - Dashboard de riesgos
- `GET /api/insights/dashboard/users/` - Dashboard de usuarios
- `GET /api/insights/dashboard/operational/` - Dashboard operacional
- `GET /api/insights/dashboard/revenue/` - Dashboard de ingresos

### Analytics
- `GET /api/insights/portfolio/overview/` - Vista general del portafolio
- `GET /api/insights/predictive/insights/` - Insights predictivos
- `GET /api/insights/credits/analysis/?start_date=2024-01-01&end_date=2024-12-31` - Análisis de créditos
- `GET /api/insights/credits/analysis/summary/` - Resumen de créditos
- `GET /api/insights/credits/analysis/clients/` - Análisis de clientes

### Financial Control
- `GET /api/insights/financial-control/dashboard/` - Dashboard de control financiero
- `GET /api/insights/financial-control/defaulters/?page=1&page_size=20` - Lista de morosos
- `GET /api/insights/financial-control/defaulters/enhanced/` - Insights mejorados
- `GET /api/insights/financial-control/metrics/user/123/` - Métricas de usuario
- `GET /api/insights/financial-control/alerts/` - Gestión de alertas
- `POST /api/insights/financial-control/alerts/` - Crear alerta
- `GET /api/insights/financial-control/reports/` - Obtener reportes
- `POST /api/insights/financial-control/reports/` - Generar reporte

### Utilidades
- `GET /api/insights/summary/` - Resumen general
- `GET /api/insights/health-check/` - Health check
- `GET /api/insights/export/?format=json&type=defaulters` - Exportar datos

---

**🎉 El Financial Control System está listo para uso en producción!**
