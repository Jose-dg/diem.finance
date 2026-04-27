# 📋 Tareas Pendientes - Optimización de Campos UID e Idempotencia

## 🎯 Objetivo
Optimizar el uso de campos `uid` en los modelos fintech bajo una estrategia **Híbrida** para mejorar el rendimiento de la base de datos sin sacrificar la seguridad y capacidades de sincronización offline (mobile).

## 📊 Análisis Realizado

### **Modelos CON campo `uid` (actualmente):**
1. **Label** (línea 63) ❌ **NO SE USA**
2. **CategoryType** (línea 78) ❌ **NO SE USA**  
3. **Category** (línea 86) ❌ **NO SE USA**
4. **SubCategory** (línea 96) ❌ **NO SE USA**
5. **Credit** (línea 298) ✅ **SÍ SE USA** (Requerido para seguridad)
6. **Transaction** (línea 678) ✅ **SÍ SE USA** (Requerido para App Offline)
7. **Expense** (línea 696) ✅ **SÍ SE USA** (Requerido para App Offline)
8. **Adjustment** (línea 712) ❌ **NO SE USA**

### **Modelos SIN campo `uid`:**
- Country, ParamsLocation, PhoneNumber, DocumentType, Identifier, Language, Address, Currency, Account, Periodicity, AccountMethodAmount, Role, Seller, User (tiene `id_user`), CreditAdjustment, Installment

## 🎯 Recomendación Arquitectónica Definitiva

**Estrategia Híbrida: BigAutoField (Interno) + UUID (Externo/Offline)**

La Primary Key de TODOS los modelos seguirá siendo `id` (`BigAutoField`) garantizando la máxima eficiencia relacional. Se mantendrá un campo secundario `uid` indexado **únicamente** en datos que tocan el exterior o nacen fuera del backend.

### **Acciones a Realizar:**
1. ✅ **Mantener** `Credit.uid` (para blindar URLs públicas y APIS de raspado).
2. ✅ **Mantener** `Transaction.uid` y `Expense.uid` (para garantizar Idempotencia en la futura aplicación móvil, permitiendo que el móvil genere la transacción sin conexión).
3. ❌ **Eliminar** UIDs de cualquier catálogo estático (Label, Categories, Adjustments).
4. 🛑 **NUNCA** exponer los PKs (`id`) en las devoluciones de JSON de APIs públicas de Créditos/Transacciones.

### **Beneficios:**
- ✅ Rapidez B-Tree masiva en BD interna.
- ✅ Ocultamiento del tamaño real de transacciones y créditos frente a competencia.
- ✅ Compatibilidad Inmediata garantizada para el Plan de Terreno y Mobile Offline Sync (Fase futura).

## 📝 Tareas Pendientes

### **🔴 ALTA PRIORIDAD - Eliminar UIDs de Catálogos (No Utilizados)**

#### **1. Eliminar campo `uid` de Label**
```python
# Archivo: apps/fintech/models.py
# Línea: 63
class Label(models.Model):
    # ❌ ELIMINAR uid = models.UUIDField(...)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True, null=True)
```

#### **2. Eliminar campo `uid` de CategoryType**
```python
# Archivo: apps/fintech/models.py
# Línea: 78
class CategoryType(models.Model):
    # ❌ ELIMINAR uid = models.UUIDField(...)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
```

#### **3. Eliminar campo `uid` de Category**
```python
# Archivo: apps/fintech/models.py
# Línea: 86
class Category(models.Model):
    # ❌ ELIMINAR uid = models.UUIDField(...)
    name = models.CharField(max_length=100)
    category_type = models.ForeignKey(CategoryType, on_delete=models.SET_NULL, null=True, related_name='categories')
```

#### **4. Eliminar campo `uid` de SubCategory**
```python
# Archivo: apps/fintech/models.py
# Línea: 96
class SubCategory(models.Model):
    # ❌ ELIMINAR uid = models.UUIDField(...)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
```

#### **5. Eliminar campo `uid` de Adjustment**
```python
# Archivo: apps/fintech/models.py
# Línea: 712
class Adjustment(models.Model):
    # ❌ ELIMINAR uid = models.UUIDField(...)
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
```

*(NOTA: Transaction.uid y Expense.uid han sido blindados y EXCLUIDOS de las tareas de eliminación).*

### **🟡 MEDIA PRIORIDAD - Crear Migraciones**

#### **6. Crear migración para eliminar campos UID remanentes**
```bash
python3 manage.py makemigrations fintech --name remove_unused_catalog_uid_fields
python3 manage.py migrate
```

### **🟢 BAJA PRIORIDAD - Verificaciones**

#### **7. Verificar dependencias de los UIDs eliminados**
- [ ] Buscar en el código cualquier referencia a `Label.uid`
- [ ] Buscar en el código cualquier referencia a `CategoryType.uid`
- [ ] Buscar en el código cualquier referencia a `Category.uid`
- [ ] Buscar en el código cualquier referencia a `SubCategory.uid`
- [ ] Buscar en el código cualquier referencia a `Adjustment.uid`

#### **8. Actualizar documentación**
- [ ] Actualizar documentación de modelos publicando el enfoque híbrido.

## ⚠️ Consideraciones Importantes

### **Antes de Proceder:**
1. **Backup de la base de datos** - Crear respaldo antes de ejecutar migraciones
2. **Verificar dependencias** - Asegurar que no hay código que dependa de estos UIDs

### **Orden de Ejecución:**
1. Eliminar campos del modelo (Catálogos)
2. Crear migración
3. Ejecutar migración en desarrollo
4. Aplicar en staging/producción

## 📊 Impacto Esperado

### **Beneficios:**
- ✅ **Desempeño y Movilidad**: Optimización selectiva sin quebrar el roadmap logístico (App Móvil).
- ✅ **Mantenimiento**: Código limpio y aligerado en áreas administrativas estáticas.

## 🎯 Criterios de Éxito
- [ ] Todos los campos UID en modelos estáticos eliminados.
- [ ] Modelos transaccionales conservan su UID listo para la app móvil.
- [ ] Migración ejecutada exitosamente en todos los ambientes.

---

**Fecha de actualización:** 22 de Abril, 2026  
**Prioridad:** Alta  
**Estado:** Pendiente
