# Sistema de Interés Adicional

## 📋 Descripción

El sistema de interés adicional utiliza el modelo `Adjustment` existente (código `C0001`) para aplicar automáticamente intereses cuando un crédito no cumple con el pago pactado.

## 🎯 Lógica de Negocio

### Regla Principal
- **Interés Adicional = Price - Cost**
- Se aplica cuando `total_abonos < price`
- Ejemplo: Crédito con `cost=100`, `price=105`, `total_abonos=80`
  - Interés adicional = 105 - 100 = **5**
  - Monto pendiente = (105 - 80) + 5 = **30**

### Cuándo se Aplica
1. **Automáticamente** después de cada transacción de pago
2. **Diariamente** a las 12 PM via Celery
3. **Manual** via management command

## 🏗️ Arquitectura

### Componentes Principales

#### 1. CreditAdjustmentService
```python
# apps/fintech/services/credit_adjustment_service.py
class CreditAdjustmentService:
    ADDITIONAL_INTEREST_CODE = 'C0001'
    
    @classmethod
    def calculate_additional_interest(cls, credit)
    @classmethod
    def should_apply_additional_interest(cls, credit)
    @classmethod
    def apply_additional_interest(cls, credit, reason=None)
```

#### 2. Signals Automáticos
```python
# apps/fintech/signals.py
@receiver(post_save, sender=Transaction)
def check_additional_interest_after_payment(sender, instance, created, **kwargs)
```

#### 3. Tarea Celery Periódica
```python
# apps/fintech/tasks.py
@shared_task
def check_additional_interest_daily()
```

#### 4. Management Command
```bash
python manage.py apply_additional_interest
```

## 🚀 Uso

### 1. Aplicación Automática
El sistema se ejecuta automáticamente:
- ✅ Después de cada transacción de pago
- ✅ Diariamente a las 12 PM
- ✅ Sin intervención manual

### 2. Aplicación Manual
```bash
# Simular sin aplicar cambios
python manage.py apply_additional_interest --dry-run

# Aplicar a todos los créditos
python manage.py apply_additional_interest

# Aplicar a un crédito específico
python manage.py apply_additional_interest --credit-uid=550e8400-e29b-41d4-a716-446655440000

# Forzar aplicación (incluso si ya existe)
python manage.py apply_additional_interest --force
```

### 3. Verificación Programática
```python
from apps.fintech.services.credit_adjustment_service import CreditAdjustmentService

# Calcular interés adicional
interest = CreditAdjustmentService.calculate_additional_interest(credit)

# Verificar si debe aplicar
should_apply = CreditAdjustmentService.should_apply_additional_interest(credit)

# Aplicar manualmente
amount = CreditAdjustmentService.apply_additional_interest(credit, "Razón")
```

## 📊 Ejemplos Prácticos

### Ejemplo 1: Pago Parcial
```
Crédito:
- Cost: $100
- Price: $105
- Cuotas: 2 de $52.5 cada una

Comportamiento:
- Cuota 1: Paga $30 (debería $52.5)
- Cuota 2: Paga $50 (debería $52.5)
- Total pagado: $80
- Total pactado: $105
- Faltante: $25
- Interés adicional: $5 (105 - 100)

Resultado:
- Cuota 3: Debe pagar $30 ($25 faltante + $5 interés)
```

### Ejemplo 2: Sin Interés Adicional
```
Crédito:
- Cost: $100
- Price: $100
- Total pagado: $80

Resultado:
- No hay interés adicional (price = cost)
- Solo debe $20 faltante
```

## 🔧 Configuración

### 1. Verificar Adjustment C0001
```python
# En Django shell
from apps.fintech.models import Adjustment

# Verificar que existe
adjustment = Adjustment.objects.get(code='C0001')
print(f"Adjustment: {adjustment.name} - Positivo: {adjustment.is_positive}")
```

### 2. Configuración de Celery
```python
# core/celery.py
'check-additional-interest-daily': {
    'task': 'apps.fintech.tasks.check_additional_interest_daily',
    'schedule': crontab(hour=12, minute=0),
},
```

## 📈 Monitoreo

### 1. Ver Créditos con Interés Adicional
```python
from apps.fintech.models import CreditAdjustment, Adjustment

# Créditos con interés adicional
credits_with_interest = CreditAdjustment.objects.filter(
    type__code='C0001'
).select_related('credit')

for adj in credits_with_interest:
    print(f"Crédito: {adj.credit.uid}")
    print(f"Interés: ${adj.amount}")
    print(f"Fecha: {adj.added_on}")
```

### 2. Reporte de Mora
```python
from apps.fintech.services.credit_adjustment_service import CreditAdjustmentService

# Para un crédito específico
total_adjustments = CreditAdjustmentService.get_total_adjustments(credit)
history = CreditAdjustmentService.get_adjustment_history(credit)
```

## 🧪 Testing

### 1. Script de Prueba
```bash
python scripts/test_additional_interest.py
```

### 2. Tests Unitarios
```bash
python manage.py test apps.fintech.tests.test_credit_adjustment_service
```

### 3. Prueba Manual
```python
# En Django shell
from apps.fintech.services.credit_adjustment_service import CreditAdjustmentService

# Crear crédito de prueba
credit = Credit.objects.create(
    cost=100, price=105, total_abonos=80
)

# Aplicar interés
amount = CreditAdjustmentService.apply_additional_interest(credit)
print(f"Interés aplicado: ${amount}")
```

## ⚠️ Consideraciones

### 1. No Duplicados
- El sistema evita aplicar el mismo ajuste múltiples veces
- Solo se aplica una vez por crédito

### 2. Transacciones Atómicas
- Todas las operaciones usan `transaction.atomic()`
- Garantiza consistencia de datos

### 3. Logging
- Todas las operaciones se registran en logs
- Facilita debugging y auditoría

### 4. Performance
- Usa queries optimizadas
- Cache inteligente para cálculos
- Procesamiento en lotes

## 🔍 Troubleshooting

### Problema: No se aplica interés adicional
```bash
# 1. Verificar que existe el Adjustment
python manage.py shell
>>> from apps.fintech.models import Adjustment
>>> Adjustment.objects.get(code='C0001')

# 2. Verificar crédito
>>> credit = Credit.objects.get(uid='...')
>>> print(f"Price: {credit.price}, Cost: {credit.cost}")
>>> print(f"Total abonos: {credit.total_abonos}")

# 3. Probar manualmente
>>> from apps.fintech.services.credit_adjustment_service import CreditAdjustmentService
>>> CreditAdjustmentService.apply_additional_interest(credit)
```

### Problema: Celery no ejecuta
```bash
# 1. Verificar Celery
celery -A core worker --loglevel=info

# 2. Verificar Celery Beat
celery -A core beat --loglevel=info

# 3. Ejecutar manualmente
python manage.py shell
>>> from apps.fintech.tasks import check_additional_interest_daily
>>> check_additional_interest_daily()
```

## 📝 Logs de Ejemplo

```
[INFO] Verificación diaria completada. Interés aplicado a 3 créditos
[INFO] Interés adicional aplicado a crédito 550e8400-e29b-41d4-a716-446655440000: $5.00
[INFO] CreditAdjustment creado: ID=123, Amount=$5.00, Reason="Pago parcial detectado"
```

## 🎯 Beneficios

1. **Automático**: No requiere intervención manual
2. **Consistente**: Usa reglas claras y predecibles
3. **Auditable**: Historial completo de ajustes
4. **Flexible**: Configurable por tipo de crédito
5. **Eficiente**: Procesamiento optimizado
6. **Seguro**: Transacciones atómicas

## 🔮 Futuras Mejoras

1. **Configuración por Tipo de Crédito**: Diferentes tasas según categoría
2. **Interés Compuesto**: Cálculo de interés sobre interés
3. **Notificaciones**: Alertas automáticas de interés aplicado
4. **Reportes**: Dashboard de interés adicional
5. **API**: Endpoints para consultar y aplicar ajustes 