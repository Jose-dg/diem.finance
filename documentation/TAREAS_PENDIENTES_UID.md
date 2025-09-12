# 📋 Tareas Pendientes - Optimización de Campos UID

## 🎯 Objetivo
Optimizar el uso de campos `uid` en los modelos fintech para mejorar el rendimiento y mantener consistencia en el código.

## 📊 Análisis Realizado

### **Modelos CON campo `uid` (actualmente):**
1. **Label** (línea 63) ❌ **NO SE USA**
2. **CategoryType** (línea 78) ❌ **NO SE USA**  
3. **Category** (línea 86) ❌ **NO SE USA**
4. **SubCategory** (línea 96) ❌ **NO SE USA**
5. **Credit** (línea 298) ✅ **SÍ SE USA**
6. **Transaction** (línea 678) ❌ **NO SE USA**
7. **Expense** (línea 696) ❌ **NO SE USA**
8. **Adjustment** (línea 712) ❌ **NO SE USA**

### **Modelos SIN campo `uid`:**
- Country, ParamsLocation, PhoneNumber, DocumentType, Identifier, Language, Address, Currency, Account, Periodicity, AccountMethodAmount, Role, Seller, User (tiene `id_user`), CreditAdjustment, Installment

## 🎯 Recomendación Aprobada

**Opción C: Mantener solo donde se necesita**

### **Acciones a Realizar:**
1. ✅ **Mantener** `Credit.uid` (ya se usa extensivamente)
2. ❌ **Eliminar** los demás UIDs no utilizados
3. ➕ **Agregar** `uid` solo a modelos que realmente lo necesiten en el futuro

### **Beneficios:**
- ✅ Reduce la complejidad innecesaria
- ✅ Mejora el rendimiento (menos campos)
- ✅ Mantiene consistencia con el uso real
- ✅ Evita confusión futura

## 📝 Tareas Pendientes

### **🔴 ALTA PRIORIDAD - Eliminar UIDs No Utilizados**

#### **1. Eliminar campo `uid` de Label**
```python
# Archivo: apps/fintech/models.py
# Línea: 63
# ANTES:
class Label(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # ❌ ELIMINAR
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True, null=True)

# DESPUÉS:
class Label(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True, null=True)
```

#### **2. Eliminar campo `uid` de CategoryType**
```python
# Archivo: apps/fintech/models.py
# Línea: 78
# ANTES:
class CategoryType(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # ❌ ELIMINAR
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

# DESPUÉS:
class CategoryType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
```

#### **3. Eliminar campo `uid` de Category**
```python
# Archivo: apps/fintech/models.py
# Línea: 86
# ANTES:
class Category(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # ❌ ELIMINAR
    name = models.CharField(max_length=100)
    category_type = models.ForeignKey(CategoryType, on_delete=models.SET_NULL, null=True, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# DESPUÉS:
class Category(models.Model):
    name = models.CharField(max_length=100)
    category_type = models.ForeignKey(CategoryType, on_delete=models.SET_NULL, null=True, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### **4. Eliminar campo `uid` de SubCategory**
```python
# Archivo: apps/fintech/models.py
# Línea: 96
# ANTES:
class SubCategory(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # ❌ ELIMINAR
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# DESPUÉS:
class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### **5. Eliminar campo `uid` de Transaction**
```python
# Archivo: apps/fintech/models.py
# Línea: 678
# ANTES:
class Transaction(models.Model):
    # ... otros campos ...
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # ❌ ELIMINAR
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    # ... resto de campos ...

# DESPUÉS:
class Transaction(models.Model):
    # ... otros campos ...
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)
    # ... resto de campos ...
```

#### **6. Eliminar campo `uid` de Expense**
```python
# Archivo: apps/fintech/models.py
# Línea: 696
# ANTES:
class Expense(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # ❌ ELIMINAR
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, related_name='expenses')
    # ... resto de campos ...

# DESPUÉS:
class Expense(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, related_name='expenses')
    # ... resto de campos ...
```

#### **7. Eliminar campo `uid` de Adjustment**
```python
# Archivo: apps/fintech/models.py
# Línea: 712
# ANTES:
class Adjustment(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # ❌ ELIMINAR
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_positive = models.BooleanField(default=True)

# DESPUÉS:
class Adjustment(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_positive = models.BooleanField(default=True)
```

### **🟡 MEDIA PRIORIDAD - Crear Migraciones**

#### **8. Crear migración para eliminar campos UID**
```bash
# Comando a ejecutar después de eliminar los campos
python3 manage.py makemigrations fintech --name remove_unused_uid_fields
python3 manage.py migrate
```

### **🟢 BAJA PRIORIDAD - Verificaciones**

#### **9. Verificar que no hay referencias a los UIDs eliminados**
- [ ] Buscar en el código cualquier referencia a `Label.uid`
- [ ] Buscar en el código cualquier referencia a `CategoryType.uid`
- [ ] Buscar en el código cualquier referencia a `Category.uid`
- [ ] Buscar en el código cualquier referencia a `SubCategory.uid`
- [ ] Buscar en el código cualquier referencia a `Transaction.uid`
- [ ] Buscar en el código cualquier referencia a `Expense.uid`
- [ ] Buscar en el código cualquier referencia a `Adjustment.uid`

#### **10. Actualizar documentación**
- [ ] Actualizar documentación de modelos
- [ ] Actualizar documentación de API si es necesario
- [ ] Actualizar tests si hay referencias a los UIDs eliminados

## ⚠️ Consideraciones Importantes

### **Antes de Proceder:**
1. **Backup de la base de datos** - Crear respaldo antes de ejecutar migraciones
2. **Verificar dependencias** - Asegurar que no hay código que dependa de estos UIDs
3. **Testing** - Ejecutar tests después de cada cambio
4. **Staging** - Probar en ambiente de staging antes de producción

### **Orden de Ejecución:**
1. Eliminar campos del modelo
2. Crear migración
3. Ejecutar migración en desarrollo
4. Verificar que todo funciona
5. Ejecutar tests
6. Aplicar en staging
7. Aplicar en producción

## 📊 Impacto Esperado

### **Beneficios:**
- ✅ **Rendimiento**: Menos campos = consultas más rápidas
- ✅ **Mantenimiento**: Código más limpio y consistente
- ✅ **Claridad**: Solo campos que realmente se usan
- ✅ **Escalabilidad**: Base de datos más eficiente

### **Riesgos:**
- ⚠️ **Migración**: Posibles problemas durante la migración
- ⚠️ **Dependencias**: Código que pueda depender de estos campos
- ⚠️ **Rollback**: Necesidad de plan de rollback si algo falla

## 🎯 Criterios de Éxito

- [ ] Todos los campos UID no utilizados eliminados
- [ ] Migración ejecutada exitosamente
- [ ] Todos los tests pasando
- [ ] No hay errores en la aplicación
- [ ] Rendimiento mejorado (opcional: medir antes/después)

---

**Fecha de creación:** 11 de Septiembre, 2025  
**Prioridad:** Alta  
**Estimación:** 2-3 horas  
**Responsable:** Equipo de Desarrollo  
**Estado:** Pendiente
