# Plan de Refactorización por Aplicaciones - Análisis de `fintech/`

## 📊 Análisis de la Aplicación `fintech/`

### **Situación Actual:**
- **25 modelos** en un solo archivo (`apps/fintech/models.py`)
- **672 líneas** de código en modelos
- **Múltiples dominios** mezclados
- **Dependencias complejas** entre modelos
- **Nombres genéricos** que violan las convenciones de Django

---

## 🎯 Nuevas Aplicaciones Identificadas (Siguiendo Convenciones)

### **1. `core/` - Configuración Base del Sistema**
**Prioridad:** 🔴 **ALTA** (Fundamental para otras aplicaciones)

**Modelos Base (10 modelos):**
```python
# apps/core/models.py
class Country(models.Model):                    # Ubicaciones geográficas
class Currency(models.Model):                   # Monedas y tipos de cambio
class Language(models.Model):                   # Idiomas del sistema
class DocumentType(models.Model):               # Tipos de documentos
class TransactionCategoryType(models.Model):    # Tipos de categorías de transacciones
class TransactionCategory(models.Model):        # Categorías principales de transacciones
class TransactionSubCategory(models.Model):     # Subcategorías de transacciones
class PaymentPeriodicity(models.Model):         # Periodicidades de pago
class Location(models.Model):                   # Ubicaciones geográficas (antes ParamsLocation)
class SystemLabel(models.Model):                # Etiquetas del sistema (antes Label)
```

**Justificación:**
- **Dependencias**: Todas las demás aplicaciones dependen de estos modelos
- **Estabilidad**: Modelos que raramente cambian
- **Reutilización**: Usados en múltiples contextos
- **Convenciones**: Nombres específicos y descriptivos

---

### **2. `users/` - Gestión de Usuarios y Autenticación**
**Prioridad:** 🔴 **ALTA** (Base para el sistema)

**Modelos de Usuario (6 modelos):**
```python
# apps/users/models.py
class User(AbstractUser):                       # Usuario principal del sistema
class UserRole(models.Model):                   # Roles y permisos (antes Role)
class UserSeller(models.Model):                 # Perfil de vendedor (antes Seller)
class UserPhoneNumber(models.Model):            # Números de teléfono (antes PhoneNumber)
class UserIdentifier(models.Model):             # Documentos de identificación (antes Identifier)
class UserAddress(models.Model):                # Direcciones de usuarios (antes Address)
```

**Justificación:**
- **Autenticación**: Base del sistema de seguridad
- **Dependencias**: Créditos y transacciones dependen de usuarios
- **Complejidad**: Lógica de roles y permisos
- **Convenciones**: Prefijos específicos para claridad

---

### **3. `credits/` - Gestión de Créditos y Préstamos**
**Prioridad:** 🟡 **MEDIA** (Dominio principal del negocio)

**Modelos de Créditos (4 modelos):**
```python
# apps/credits/models.py
class Credit(models.Model):                     # Crédito principal
class CreditInstallment(models.Model):          # Cuotas del crédito (antes Installment)
class CreditAdjustmentType(models.Model):       # Tipos de ajustes (antes Adjustment)
class CreditAdjustment(models.Model):           # Ajustes aplicados a créditos
```

**Justificación:**
- **Dominio principal**: Core del negocio fintech
- **Complejidad**: Lógica de cálculo de intereses y cuotas
- **Volumen**: Mayor cantidad de datos y transacciones
- **Convenciones**: Prefijos específicos para el dominio

---

### **4. `transactions/` - Transacciones Financieras**
**Prioridad:** 🟡 **MEDIA** (Operaciones del sistema)

**Modelos de Transacciones (2 modelos):**
```python
# apps/transactions/models.py
class Transaction(models.Model):                # Transacción principal
class TransactionExpense(models.Model):         # Gastos del sistema (antes Expense)
```

**Justificación:**
- **Operaciones**: Registro de todas las transacciones
- **Auditoría**: Trazabilidad de operaciones
- **Reportes**: Base para análisis financiero
- **Convenciones**: Nombres específicos del dominio

---

### **5. `payments/` - Procesamiento de Pagos**
**Prioridad:** 🟢 **BAJA** (Especialización)

**Modelos de Pagos (2 modelos):**
```python
# apps/payments/models.py
class PaymentAccount(models.Model):             # Cuentas de pago (antes Account)
class PaymentMethodAmount(models.Model):        # Métodos y montos de pago (antes AccountMethodAmount)
```

**Justificación:**
- **Especialización**: Lógica específica de pagos
- **Integración**: Futuras integraciones con gateways
- **Complejidad**: Manejo de diferentes métodos de pago
- **Convenciones**: Nombres específicos del dominio

---

## 📋 Orden de Prioridad para Creación

### **Fase 1: Fundación (Semana 1)**
#### **1.1 Crear `core/` (Día 1-2)**
```bash
python3 manage.py startapp core
```

**Razones de prioridad:**
- **Dependencias**: Todas las demás aplicaciones dependen de `core/`
- **Estabilidad**: Modelos que no cambian frecuentemente
- **Riesgo bajo**: No afecta lógica de negocio existente
- **Convenciones**: Aplicar nombres específicos desde el inicio

**Tareas:**
- [ ] Crear aplicación `core/`
- [ ] Mover modelos base con `app_label` y `db_table`
- [ ] **Renombrar modelos genéricos** según convenciones
- [ ] Actualizar imports en `admin.py`
- [ ] Testing básico

#### **1.2 Crear `users/` (Día 3-4)**
```bash
python3 manage.py startapp users
```

**Razones de prioridad:**
- **Autenticación**: Base del sistema de seguridad
- **Dependencias**: Créditos y transacciones dependen de usuarios
- **Complejidad**: Manejo de roles y permisos
- **Convenciones**: Aplicar prefijos específicos

**Tareas:**
- [ ] Crear aplicación `users/`
- [ ] Mover modelos de usuario con `app_label` y `db_table`
- [ ] **Renombrar modelos** con prefijos específicos
- [ ] Actualizar `AUTH_USER_MODEL` en settings
- [ ] Migrar admin y serializers
- [ ] Testing de autenticación

### **Fase 2: Dominios Principales (Semana 2)**
#### **2.1 Crear `credits/` (Día 1-3)**
```bash
python3 manage.py startapp credits
```

**Razones de prioridad:**
- **Dominio principal**: Core del negocio fintech
- **Complejidad**: Lógica de cálculo más compleja
- **Volumen**: Mayor cantidad de datos
- **Convenciones**: Aplicar prefijos específicos del dominio

**Tareas:**
- [ ] Crear aplicación `credits/`
- [ ] Mover modelos de créditos con `app_label` y `db_table`
- [ ] **Renombrar modelos** con prefijos específicos
- [ ] Migrar servicios de créditos
- [ ] Actualizar views y serializers
- [ ] Testing de lógica de negocio

#### **2.2 Crear `transactions/` (Día 4-5)**
```bash
python3 manage.py startapp transactions
```

**Razones de prioridad:**
- **Operaciones**: Registro de todas las transacciones
- **Dependencias**: Depende de usuarios y créditos
- **Auditoría**: Trazabilidad importante
- **Convenciones**: Aplicar nombres específicos del dominio

**Tareas:**
- [ ] Crear aplicación `transactions/`
- [ ] Mover modelos de transacciones
- [ ] **Renombrar modelos** con prefijos específicos
- [ ] Migrar servicios de transacciones
- [ ] Actualizar views y serializers
- [ ] Testing de operaciones

### **Fase 3: Especialización (Semana 3)**
#### **3.1 Crear `payments/` (Día 1-2)**
```bash
python3 manage.py startapp payments
```

**Razones de prioridad:**
- **Especialización**: Lógica específica de pagos
- **Menor dependencia**: Puede desarrollarse en paralelo
- **Futuras integraciones**: Preparación para gateways
- **Convenciones**: Aplicar nombres específicos del dominio

**Tareas:**
- [ ] Crear aplicación `payments/`
- [ ] Mover modelos de pagos
- [ ] **Renombrar modelos** con prefijos específicos
- [ ] Migrar servicios de pagos
- [ ] Actualizar views y serializers
- [ ] Testing de procesamiento de pagos

---

## 🏗️ Estructura Final Propuesta (Siguiendo Convenciones)

```
apps/
├── core/                    # Configuración base (Semana 1)
│   ├── models.py           # 10 modelos base con nombres específicos
│   ├── admin.py
│   ├── serializers.py
│   └── services/
├── users/                   # Gestión de usuarios (Semana 1)
│   ├── models.py           # 6 modelos de usuario con prefijos
│   ├── admin.py
│   ├── serializers.py
│   └── services/
├── credits/                 # Gestión de créditos (Semana 2)
│   ├── models.py           # 4 modelos de créditos con prefijos
│   ├── admin.py
│   ├── serializers.py
│   └── services/
├── transactions/            # Transacciones (Semana 2)
│   ├── models.py           # 2 modelos de transacciones con prefijos
│   ├── admin.py
│   ├── serializers.py
│   └── services/
├── payments/                # Pagos (Semana 3)
│   ├── models.py           # 2 modelos de pagos con prefijos
│   ├── admin.py
│   ├── serializers.py
│   └── services/
├── dashboard/               # Existente (NO TOCAR)
├── insights/                # Existente (NO TOCAR)
├── forecasting/             # Existente (NO TOCAR)
├── revenue/                 # Existente (NO TOCAR)
├── notifications/           # Existente (NO TOCAR)
└── fintech/                 # Mantener temporalmente
    ├── models.py           # Solo imports y compatibilidad
    ├── views.py            # Migrar gradualmente
    └── urls.py             # Mantener rutas existentes
```

---

## 📊 Análisis de Dependencias

### **Dependencias entre Aplicaciones:**

```
core/ ← users/ ← credits/
  ↑        ↑        ↑
  └── transactions/
  ↑        ↑
  └── payments/
```

### **Orden de Dependencias:**
1. **`core/`** - Sin dependencias externas
2. **`users/`** - Depende de `core/`
3. **`credits/`** - Depende de `core/` y `users/`
4. **`transactions/`** - Depende de `core/`, `users/` y `credits/`
5. **`payments/`** - Depende de `core/`, `users/` y `credits/`

---

## 🎯 Criterios de Priorización

### **1. Dependencias Técnicas (40%)**
- **`core/`**: Base para todas las demás aplicaciones
- **`users/`**: Autenticación y seguridad del sistema
- **`credits/`**: Dominio principal del negocio

### **2. Complejidad de Negocio (30%)**
- **`credits/`**: Lógica más compleja (cálculos, cuotas, intereses)
- **`transactions/`**: Operaciones críticas del sistema
- **`payments/`**: Lógica especializada

### **3. Volumen de Datos (20%)**
- **`credits/`**: Mayor volumen (300 activos, creciendo a 10,000)
- **`transactions/`**: Alto volumen de operaciones
- **`users/`**: Volumen moderado pero crítico

### **4. Riesgo de Cambio (10%)**
- **`core/`**: Riesgo bajo (modelos estables)
- **`users/`**: Riesgo medio (autenticación crítica)
- **`credits/`**: Riesgo alto (lógica de negocio compleja)

---

## 🚀 Plan de Implementación Detallado (Siguiendo Convenciones)

### **Semana 1: Fundación**

#### **Día 1-2: `core/`**
```bash
# Crear aplicación
python3 manage.py startapp core

# Configurar en settings
INSTALLED_APPS = [
    # ... apps existentes
    'apps.core',
]

# Mover modelos base con nombres específicos
# apps/core/models.py
class Country(models.Model):
    class Meta:
        app_label = 'core'
        db_table = 'fintech_country'

class TransactionCategory(models.Model):  # Antes Category
    class Meta:
        app_label = 'core'
        db_table = 'fintech_category'

class PaymentPeriodicity(models.Model):  # Antes Periodicity
    class Meta:
        app_label = 'core'
        db_table = 'fintech_periodicity'

class Location(models.Model):  # Antes ParamsLocation
    class Meta:
        app_label = 'core'
        db_table = 'fintech_paramslocation'
```

#### **Día 3-4: `users/`**
```bash
# Crear aplicación
python3 manage.py startapp users

# Configurar en settings
AUTH_USER_MODEL = 'users.User'
INSTALLED_APPS = [
    # ... apps existentes
    'apps.users',
]

# Mover modelos de usuario con prefijos específicos
# apps/users/models.py
class User(AbstractUser):
    class Meta:
        app_label = 'users'
        db_table = 'fintech_user'

class UserRole(models.Model):  # Antes Role
    class Meta:
        app_label = 'users'
        db_table = 'fintech_role'

class UserSeller(models.Model):  # Antes Seller
    class Meta:
        app_label = 'users'
        db_table = 'fintech_seller'
```

### **Semana 2: Dominios Principales**

#### **Día 1-3: `credits/`**
```bash
# Crear aplicación
python3 manage.py startapp credits

# Configurar en settings
INSTALLED_APPS = [
    # ... apps existentes
    'apps.credits',
]

# Mover modelos de créditos con prefijos específicos
# apps/credits/models.py
class Credit(models.Model):
    class Meta:
        app_label = 'credits'
        db_table = 'fintech_credit'

class CreditInstallment(models.Model):  # Antes Installment
    class Meta:
        app_label = 'credits'
        db_table = 'fintech_installment'

class CreditAdjustmentType(models.Model):  # Antes Adjustment
    class Meta:
        app_label = 'credits'
        db_table = 'fintech_adjustment'
```

#### **Día 4-5: `transactions/`**
```bash
# Crear aplicación
python3 manage.py startapp transactions

# Configurar en settings
INSTALLED_APPS = [
    # ... apps existentes
    'apps.transactions',
]

# Mover modelos de transacciones con prefijos específicos
# apps/transactions/models.py
class Transaction(models.Model):
    class Meta:
        app_label = 'transactions'
        db_table = 'fintech_transaction'

class TransactionExpense(models.Model):  # Antes Expense
    class Meta:
        app_label = 'transactions'
        db_table = 'fintech_expense'
```

### **Semana 3: Especialización**

#### **Día 1-2: `payments/`**
```bash
# Crear aplicación
python3 manage.py startapp payments

# Configurar en settings
INSTALLED_APPS = [
    # ... apps existentes
    'apps.payments',
]

# Mover modelos de pagos con prefijos específicos
# apps/payments/models.py
class PaymentAccount(models.Model):  # Antes Account
    class Meta:
        app_label = 'payments'
        db_table = 'fintech_account'

class PaymentMethodAmount(models.Model):  # Antes AccountMethodAmount
    class Meta:
        app_label = 'payments'
        db_table = 'fintech_accountmethodamount'
```

---

## 📝 Checklist de Implementación (Siguiendo Convenciones)

### **Fase 1: Fundación**
- [ ] Crear aplicación `core/`
- [ ] Mover 10 modelos base con nombres específicos
- [ ] **Renombrar modelos genéricos** según convenciones
- [ ] Configurar `app_label` y `db_table`
- [ ] Actualizar imports en admin
- [ ] Testing básico
- [ ] Crear aplicación `users/`
- [ ] Mover 6 modelos de usuario con prefijos
- [ ] **Renombrar modelos** con prefijos específicos
- [ ] Configurar `AUTH_USER_MODEL`
- [ ] Migrar autenticación
- [ ] Testing de seguridad

### **Fase 2: Dominios Principales**
- [ ] Crear aplicación `credits/`
- [ ] Mover 4 modelos de créditos con prefijos
- [ ] **Renombrar modelos** con prefijos específicos
- [ ] Migrar servicios de créditos
- [ ] Actualizar views y serializers
- [ ] Testing de lógica de negocio
- [ ] Crear aplicación `transactions/`
- [ ] Mover 2 modelos de transacciones con prefijos
- [ ] **Renombrar modelos** con prefijos específicos
- [ ] Migrar servicios de transacciones
- [ ] Actualizar views y serializers
- [ ] Testing de operaciones

### **Fase 3: Especialización**
- [ ] Crear aplicación `payments/`
- [ ] Mover 2 modelos de pagos con prefijos
- [ ] **Renombrar modelos** con prefijos específicos
- [ ] Migrar servicios de pagos
- [ ] Actualizar views y serializers
- [ ] Testing de procesamiento

### **Fase 4: Limpieza**
- [ ] Eliminar modelos de `fintech/`
- [ ] Actualizar imports restantes
- [ ] Testing completo del sistema
- [ ] Documentación final

---

## 🎯 Beneficios Esperados (Siguiendo Convenciones)

### **Inmediatos (Semana 1-3):**
- **Organización**: Código más limpio y mantenible
- **Colaboración**: Mejor división de trabajo entre desarrolladores
- **Testing**: Tests más específicos por dominio
- **Documentación**: Mejor auto-documentación
- **Convenciones**: Nombres específicos y descriptivos

### **Mediano Plazo (Mes 2-3):**
- **Performance**: Optimizaciones específicas por dominio
- **Escalabilidad**: Preparación para crecimiento a 10,000 créditos
- **Mantenibilidad**: Cambios más seguros y controlados
- **Claridad**: Nombres que explican su propósito

### **Largo Plazo (Mes 6+):**
- **Flexibilidad**: Posibilidad de separación de bases de datos
- **Integración**: Facilidad para nuevas funcionalidades
- **Competitividad**: Arquitectura preparada para el futuro
- **Estándares**: Cumplimiento con mejores prácticas de Django

---

## 🔧 Cambios Específicos de Nomenclatura

### **Modelos Renombrados Según Convenciones:**

#### **`core/`:**
- `Category` → `TransactionCategory`
- `SubCategory` → `TransactionSubCategory`
- `Periodicity` → `PaymentPeriodicity`
- `ParamsLocation` → `Location`
- `Label` → `SystemLabel`

#### **`users/`:**
- `Role` → `UserRole`
- `Seller` → `UserSeller`
- `PhoneNumber` → `UserPhoneNumber`
- `Identifier` → `UserIdentifier`
- `Address` → `UserAddress`

#### **`credits/`:**
- `Installment` → `CreditInstallment`
- `Adjustment` → `CreditAdjustmentType`
- `CreditAdjustment` → `CreditAdjustment` (mantener)

#### **`transactions/`:**
- `Expense` → `TransactionExpense`

#### **`payments/`:**
- `Account` → `PaymentAccount`
- `AccountMethodAmount` → `PaymentMethodAmount`

---

**Nota**: Este plan actualizado sigue rigurosamente las convenciones de nomenclatura de Django establecidas en `django-naming-conventions.md`, priorizando nombres específicos, descriptivos y sin abreviaciones.
