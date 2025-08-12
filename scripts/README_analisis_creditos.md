# Scripts de Análisis de Créditos

Este directorio contiene scripts para analizar el estado de los créditos desde mayo de 2025 hasta hoy, identificando clientes que solicitaron crédito y no han hecho abono o están atrasados.

## Scripts Disponibles

### 1. `analisis_completo_creditos.py` (RECOMENDADO)
Script principal con menú interactivo que combina todos los análisis.

**Características:**
- Menú interactivo fácil de usar
- Análisis general de estado de créditos
- Análisis detallado de pagos y abonos
- Generación de reportes CSV
- Interfaz amigable con emojis y formato claro

**Uso:**
```bash
cd /ruta/a/tu/proyecto
python3 scripts/analisis_completo_creditos.py
```

### 2. `analisis_estado_creditos.py`
Script específico para análisis del estado general de créditos.

**Características:**
- Análisis por estado de crédito
- Identificación de clientes sin abonos
- Identificación de clientes con créditos atrasados
- Análisis detallado por cliente
- Resumen ejecutivo

**Uso:**
```bash
cd /ruta/a/tu/proyecto
python3 scripts/analisis_estado_creditos.py
```

### 3. `analisis_pagos_abonos.py`
Script específico para análisis de pagos y abonos.

**Características:**
- Análisis general de pagos
- Análisis de pagos por mes
- Identificación de clientes con mejor comportamiento de pago
- Análisis de créditos sin pagos
- Análisis de morosidad por días

**Uso:**
```bash
cd /ruta/a/tu/proyecto
python3 scripts/analisis_pagos_abonos.py
```

## Información Analizada

### Período de Análisis
- **Fecha de inicio:** 1 de mayo de 2025
- **Fecha de fin:** Fecha actual

### Métricas Incluidas

#### Análisis General de Créditos:
- Total de créditos solicitados
- Monto total solicitado, abonado y pendiente
- Porcentaje de pago general
- Clientes sin abonos
- Clientes con créditos atrasados
- Análisis por estado de crédito

#### Análisis de Pagos:
- Total de pagos realizados
- Monto total pagado
- Promedio por pago
- Análisis de pagos por mes
- Top clientes con mejor comportamiento de pago
- Créditos sin pagos
- Análisis de morosidad por días

#### Información por Cliente:
- Nombre completo del cliente
- Total de créditos solicitados
- Créditos sin abono
- Créditos atrasados
- Monto total solicitado, abonado y pendiente
- Porcentaje de pago individual
- Fechas de primer y último crédito

## Reportes CSV

Los scripts pueden generar reportes en formato CSV con la siguiente información:

### Reporte de Créditos:
- Username, nombre, apellido, email del cliente
- Total de créditos, créditos sin abono, créditos atrasados
- Montos totales solicitado, abonado y pendiente
- Promedio de crédito
- Fechas de primer y último crédito

### Reporte de Pagos:
- Información detallada de cada crédito
- Estado de morosidad y nivel de morosidad
- Cantidad de pagos realizados
- Montos pagados y promedios
- Fechas de primer y último pago

## Requisitos

- Python 3.8+
- Django 4.2+
- Base de datos configurada y accesible
- Variables de entorno configuradas

## Estructura de la Base de Datos

Los scripts utilizan los siguientes modelos de Django:

- `Credit`: Información de créditos
- `User`: Información de clientes
- `AccountMethodAmount`: Información de pagos
- `Transaction`: Información de transacciones

## Campos Clave Analizados

### Modelo Credit:
- `price`: Monto del crédito
- `total_abonos`: Total abonado
- `pending_amount`: Monto pendiente
- `is_in_default`: Si está en mora
- `morosidad_level`: Nivel de morosidad
- `state`: Estado del crédito
- `first_date_payment`: Fecha del primer pago
- `created_at`: Fecha de creación

### Modelo AccountMethodAmount:
- `amount_paid`: Monto pagado
- `transaction`: Transacción relacionada

## Ejemplos de Uso

### Ejecutar análisis completo:
```bash
python3 scripts/analisis_completo_creditos.py
```

### Ejecutar solo análisis de estado:
```bash
python3 scripts/analisis_estado_creditos.py
```

### Ejecutar solo análisis de pagos:
```bash
python3 scripts/analisis_pagos_abonos.py
```

## Salida de Ejemplo

```
================================================================================
ANÁLISIS GENERAL DE ESTADO DE CRÉDITOS
Período: Mayo 2025 - Hoy
================================================================================
📊 ESTADÍSTICAS GENERALES:
   • Total de créditos: 150
   • Monto total solicitado: $1,250,000.00
   • Monto total abonado: $875,000.00
   • Monto total pendiente: $375,000.00
   • Porcentaje de pago: 70.0%

🚨 CLIENTES SIN ABONOS:
   • Total de clientes sin abonos: 25

⚠️  CLIENTES CON CRÉDITOS ATRASADOS:
   • Total de clientes atrasados: 15

📋 ANÁLISIS POR ESTADO:
   • pending: 100 créditos ($800,000.00)
   • completed: 50 créditos ($450,000.00)
```

## Notas Importantes

1. **Configuración de Django**: Los scripts configuran automáticamente Django, pero asegúrate de que las variables de entorno estén configuradas correctamente.

2. **Base de Datos**: Los scripts asumen que la base de datos está accesible y contiene datos desde mayo de 2025.

3. **Permisos**: Asegúrate de tener permisos de lectura en la base de datos.

4. **Rendimiento**: Para bases de datos grandes, los scripts pueden tardar varios minutos en ejecutarse.

5. **Archivos CSV**: Los reportes CSV se generan en el directorio actual del script.

## Solución de Problemas

### Error de configuración de Django:
```bash
export DJANGO_SETTINGS_MODULE=core.settings
```

### Error de conexión a la base de datos:
Verifica que las credenciales de la base de datos estén configuradas correctamente en `core/settings.py`.

### Error de permisos:
Asegúrate de tener permisos de lectura en las tablas de la base de datos.

## Contribuciones

Para mejorar estos scripts, considera:

1. Agregar más métricas de análisis
2. Mejorar la visualización de datos
3. Agregar filtros por fechas personalizables
4. Implementar análisis de tendencias
5. Agregar gráficos y visualizaciones
