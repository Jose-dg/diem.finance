# Refactorización: Identidad Unificada (AUTH_USER_MODEL)

Estado: Documento de Referencia Final

---

## 1. Contexto Actual: La Dualidad de Identidad

El sistema opera con dos mundos separados para gestionar personas:

1. **Mundo Administrativo (`auth.User`):** Administradores y vendedores (Sellers). Tabla `auth_user`.
2. **Mundo de Negocio (`fintech.User`):** Clientes. Tabla `fintech_user`.

### ¿Cómo se refleja esto en el código?

`apps/fintech/models.py`:
- `from django.contrib.auth.models import User as Admin`
- `class User(AbstractUser):` — sin `USERNAME_FIELD`, sin manager propio
- `Seller.user` → `OneToOne` a `Admin`
- `Credit.registered_by` → FK a `Admin`
- `Credit.user` → FK a `fintech.User`
- `Expense.registered_by` → FK a `Admin`

`apps/fintech/backends.py`:
- `FintechAuthenticationBackend` — retorna un `UserWrapper` (objeto Python dinámico, no un modelo Django real) para que `fintech.User` pase por el sistema de auth.
- `ClientAuthenticationBackend` — permite buscar clientes por username, email o teléfono.

---

## 2. El Diagnóstico: ¿Qué sucede realmente?

### Problema central
Django solo reconoce como "usuarios reales" a los de `auth_user`. Para trabajar alrededor de eso, el proyecto tiene un `UserWrapper` en `backends.py` que envuelve un `fintech.User` en un objeto dinámico e intenta imitar a `auth.User`.

**Esta es la señal más clara del problema:** si necesitas un wrapper para que tu modelo de usuario funcione, es porque no es el modelo de usuario del sistema.

### Consecuencias concretas hoy

- **JWT roto para clientes:** Simple JWT, al refrescar un token, llama `get_user(user_id)` que busca en `auth_user` por `pk`. El `UserWrapper` tiene un `id` pero no es un registro real en `auth_user`. Los clientes no pueden refrescar tokens de forma confiable.
- **`get_user_model()` devuelve `auth.User`:** Los serializers (`fintech/serializers.py`), servicios (`payment_service.py`, `audit_logger.py`), comandos de gestión y tests usan `get_user_model()` pensando que obtienen el modelo de clientes — pero obtienen el de administradores.
- **`insights` models apuntan a `auth.User`:** `CustomerLifetimeValue`, `CustomerActivity`, `CreditRecommendation` y otros tienen FK a `settings.AUTH_USER_MODEL`, que hoy es `auth.User`. Los modelos de analítica apuntan al mundo administrativo, no a los clientes.
- **Imposibilidad de cruce de roles:** Si un cliente se convierte en vendedor, hay que crear un registro nuevo en la otra tabla, duplicando datos y perdiendo historial.

---

## 3. Riesgos de Escalabilidad

1. **Deuda técnica acumulada:** Cada nueva funcionalidad (notificaciones, geolocalización, auditoría) debe programarse dos veces o con chequeos manuales sobre a qué tabla preguntar.
2. **Riesgo de producción:** Cambiar `AUTH_USER_MODEL` con decenas de miles de créditos es una operación de alto riesgo. Con pocos registros actuales, el costo es mínimo comparado con hacerlo después.
3. **El `UserWrapper` se rompe silenciosamente:** Es un objeto dinámico sin `save()`, sin `Meta`, sin presencia en el ORM. Cualquier código que haga `isinstance(request.user, ...)` o intente guardar una relación a `request.user` falla de formas difíciles de depurar.

---

## 4. Solución: Usar AUTH_USER_MODEL de verdad

Establecer `AUTH_USER_MODEL = 'fintech.User'` en `settings.py`. Esto no es una simulación — es el mecanismo oficial de Django para definir el modelo de usuario del sistema.

Una vez hecho, Django garantiza:
- `get_user_model()` devuelve `fintech.User` en todo el proyecto.
- Simple JWT busca y emite tokens contra `fintech_user` directamente.
- El Django Admin gestiona `fintech.User` como el usuario nativo.
- Todos los subsistemas (permisos, sesiones, grupos) operan sobre `fintech.User`.

**Consecuencia directa sobre `backends.py`:** el `UserWrapper` y `FintechAuthenticationBackend` se eliminan por completo. Existen porque `fintech.User` no es el modelo nativo — cuando lo sea, no tienen razón de existir. El backend resultante es una clase simple que solo añade búsqueda por email/teléfono.

### El patrón correcto de referencias (recomendación oficial de Django)

**En FK de modelos** (en cualquier app):
```python
from django.conf import settings
user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

**En código Python** (views, services, serializers, signals):
```python
from django.contrib.auth import get_user_model
User = get_user_model()  # devuelve fintech.User una vez configurado AUTH_USER_MODEL
```

**Dentro de `apps/fintech/models.py` — la excepción:**
La app que define el modelo puede referenciarlo directamente o usar `'self'` en FKs recursivas. Usar `settings.AUTH_USER_MODEL` también es válido y preferible para consistencia.

---

## 5. Definición del Modelo de Usuario

### 5.1 Base: AbstractUser (no AbstractBaseUser)

`fintech.User` ya extiende `AbstractUser`. Esta decisión es correcta y se mantiene:
- Hereda `PermissionsMixin` (grupos, permisos) de forma nativa.
- Hereda estados de cuenta (`is_staff`, `is_active`, `is_superuser`).
- Hereda metadatos de auditoría (`date_joined`, `last_login`).

`AbstractBaseUser` requeriría reimplementar todo eso manualmente — es sobre-ingeniería para este caso.

### 5.2 Estrategia del campo `username` (no se elimina)

El modelo **mantiene `username` como obligatorio y único**. No se anula ni se pone a `None`.

**Justificación de seguridad:** el email es un dato sensible (PII). Tener un `username` permite que en capas futuras (APIs públicas, integraciones) el identificador visible del usuario sea su "handle" y no su correo, evitando exposición a spam y ataques dirigidos.

**Justificación técnica:** si se elimina el campo ahora y el negocio lo requiere después, generar usernames únicos para miles de registros existentes es una migración crítica propensa a errores. Mantenerlo no cuesta nada.

### 5.3 Configuración de autenticación

El modelo usará **`username` como credencial de login** — el default de `AbstractUser`, que no requiere declararse explícitamente.

**Por qué no `USERNAME_FIELD = 'email'`:** el 99.8% de los clientes en producción (604 de 605) no tienen email registrado. Aplicar `email = EmailField(unique=True)` como campo de autenticación es inviable con los datos actuales. El `username` en cambio está poblado en el 100% de los registros (605/605).

```python
class User(AbstractUser):
    # USERNAME_FIELD = 'username'  ← es el default, no hace falta declararlo
    REQUIRED_FIELDS = []  # createsuperuser pedirá username y contraseña
    
    email = models.EmailField(blank=True, default='')  # opcional, a completar progresivamente
    # ... resto de campos
```

Esto significa:
- El login (JWT, admin) acepta username + contraseña — como funciona hoy.
- `email` es un campo adicional que los clientes pueden completar en su perfil. No es `unique` ni requerido en esta fase.
- Cuando haya una masa crítica de emails registrados, se puede migrar a `USERNAME_FIELD = 'email'` en una segunda fase sin urgencia.

### 5.4 Custom Manager

`fintech.User` necesita un manager propio para que `create_user` y `create_superuser` funcionen correctamente con `USERNAME_FIELD = 'email'`:

```python
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('El username es obligatorio')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)
```

Y en el modelo:
```python
class User(AbstractUser):
    objects = UserManager()
    REQUIRED_FIELDS = []
    email = models.EmailField(blank=True, default='')
```

**Nota de nomenclatura:** el manager se llama `UserManager`, no `FintechUserManager`. Llamarlo `FintechUserManager` dentro de una app que ya se llama `fintech` es redundante — el módulo ya provee el contexto. El patrón Pythonic es `from apps.fintech.models import User, UserManager`, no `FintechUser, FintechUserManager`.

**Nota sobre `email`:** no se aplica `unique=True` ni `normalize_email` en esta fase porque 604/605 clientes tienen `email = ''`. Hacerlo ahora rompería la constraint de unicidad. Cuando se recolecten emails, se añade la constraint en una migración separada.

### 5.5 Estrategia del campo email

`email` es opcional en esta fase: `blank=True, default=''`. No es el campo de autenticación ni tiene constraint de unicidad.

**Situación real:** 604 de 605 clientes en producción no tienen email registrado. El identificador real y funcional de cada cliente hoy es el `username` (poblado al 100%).

El email queda disponible como campo de perfil a completar progresivamente. Cuando haya una masa crítica de emails registrados, se podrá:
1. Añadir `unique=True` en una migración separada (después de limpiar duplicados y vacíos).
2. Cambiar `USERNAME_FIELD = 'email'` en una segunda fase del refactor.

---

## 6. Decisión previa: modelo de roles

**Decisión para esta fase: mantener `Seller` sin cambios de lógica.**

`User` es identidad y autenticación. La lógica comercial vive en modelos separados. Por eso `Seller` no se rediseña ni se elimina en esta migración — solo se cambia a qué tabla apunta su FK:

- `Seller.user` pasa de `OneToOne(auth.User)` a `OneToOne(settings.AUTH_USER_MODEL)`.
- La lógica interna de `Seller` (comisiones, ventas, retornos) no se toca.
- `fintech.User` con `is_staff=True` sigue siendo el criterio para acceso administrativo.

**Arquitectura objetivo a futuro (no se implementa ahora):**

```
User               # identidad y autenticación
Seller             # perfil operativo del vendedor (ya existe)
CustomerProfile    # perfil extendido del cliente (futuro)
CommissionRule     # reglas de comisión por vendedor/producto (futuro)
CommissionEvent    # evento que genera una comisión (futuro)
Referral           # relación de referido entre usuarios (futuro)
Payout             # liquidación al vendedor (futuro)
```

Documentar esta visión evita que en el futuro se meta lógica comercial directamente en `User` "ya que estamos". `User` debe mantenerse limpio como modelo de identidad.

---

## 7. Plan de Ejecución

### Fase 0: Decisiones confirmadas (no requieren más discusión)
1. `Seller` se mantiene — solo cambia su FK. No se rediseña lógica comercial.
2. `username` es nullable y opcional. No se autogenera.
3. Migración vía base de datos limpia (Plan A). `SeparateDatabaseAndState` queda como Plan B de emergencia.

### Fase 1: Preparación del modelo

1. **`apps/fintech/models.py`:**
   - Añadir `UserManager` (ver sección 5.4).
   - Añadir a `User`: `objects = UserManager()`, `REQUIRED_FIELDS = []`, `email = EmailField(blank=True, default='')`.
   - `USERNAME_FIELD` no se declara — usa el default `'username'` de `AbstractUser`.
   - Eliminar `from django.contrib.auth.models import User as Admin`.
   - `Seller.user`: cambiar de `OneToOne(Admin, ...)` a `OneToOne(settings.AUTH_USER_MODEL, ...)`.
   - `Credit.registered_by`: cambiar de `FK(Admin, ...)` a `FK(settings.AUTH_USER_MODEL, ...)`.
   - `Expense.registered_by`: cambiar de `FK(Admin, ...)` a `FK(settings.AUTH_USER_MODEL, ...)`.

2. **`core/settings.py`:** Agregar `AUTH_USER_MODEL = 'fintech.User'`.

3. **`apps/fintech/backends.py`:**
   - Eliminar `UserWrapper` y `FintechAuthenticationBackend` — obsoletos.
   - Reescribir `ClientAuthenticationBackend` para buscar por email, username o teléfono directamente sobre `get_user_model()`. Sin wrapping.

4. **`apps/fintech/admin.py`:**
   - Registrar `fintech.User` con `UserAdmin` extendido.
   - Sobrescribir `fieldsets` para que email aparezca en la parte superior como campo principal.

5. **Apps secundarias — situación mixta:**
   - `insights/models.py`, `forecasting/models.py` — ya usan `settings.AUTH_USER_MODEL` en FK. Sin cambios de código, solo `makemigrations`.
   - `fintech/serializers.py`, servicios, comandos de gestión — ya usan `get_user_model()`. Sin cambios.
   - **`insights/views.py`, `insights/tasks.py`, `insights/signals.py` — importan `User` directamente como `from apps.fintech.models import User`.** Técnicamente siguen funcionando después del cambio (apuntan a la misma clase), pero violan la convención Django. Deben migrarse a `get_user_model()` como parte de este refactor.

   > El cambio de `settings.AUTH_USER_MODEL` se propaga solo para los archivos que ya siguen el patrón. Los que importan `User` directamente de `fintech.models` requieren una pasada de refactor manual.

6. **Tests:**
   - Los archivos que hacen `get_user_model().objects.create_user(...)` crearán `fintech.User` después del cambio.
   - `create_user` debe recibir `email` (no solo `username`) como primer argumento. Actualizar llamadas en tests de `insights`, `fintech` y `revenue`.

### Fase 2: Migración de base de datos

Esta fase tiene dos caminos. El Plan A es la ruta recomendada. El Plan B es el fallback para cuando no se puede hacer ETL completo.

---

#### Plan A — Base de datos limpia (recomendado)

Crear una base de datos nueva con `AUTH_USER_MODEL = 'fintech.User'` configurado desde el inicio y migrar los datos en orden controlado. Este camino es más auditable, más reversible en la práctica y deja el historial de migraciones sin deuda.

**Condición necesaria:** todos los datos de negocio deben poder exportarse e importarse de forma íntegra. Si hay registros de auditoría o relaciones con integridad referencial compleja que no se pueden serializar, evaluar Plan B.

**Colisión de IDs a tener en cuenta:** `auth_user` tiene IDs 1–6 y `fintech_user` tiene IDs 1–605. Si en la nueva base se insertan los 6 admins en la misma tabla `fintech_user`, colisionan con clientes existentes. Solución: insertar admins dejando que PostgreSQL asigne IDs nuevos (usar `INSERT` sin `id` explícito), luego actualizar las FK de `Seller` con los nuevos IDs. Los IDs de los 605 clientes sí se preservan con inserción explícita de `id`.

**Volumen real de datos a migrar:**
- 605 clientes + 6 admins
- 2 vendedores
- 2,007 créditos
- 5,391 cuotas
- 10,800 transacciones
- 391 gastos
- 656 CreditEarnings
- Modelos de `insights`: 0 registros — no requieren ETL

Pasos:
1. Aplicar todos los cambios de código de la Fase 1 (modelo, settings, backends).
2. Exportar datos de la base actual en orden de dependencias:
   - Catálogos base (Country, Currency, Category, etc.)
   - Usuarios/clientes (`fintech_user`)
   - Vendedores (`Seller`)
   - Créditos (`Credit`)
   - Cuotas (`Installment`)
   - Transacciones (`Transaction`)
   - Pagos y gastos
   - Ajustes y registros derivados
3. Crear base de datos nueva.
4. `python manage.py makemigrations` — genera migraciones limpias con el modelo correcto desde el inicio.
5. `python manage.py migrate` — aplica todo.
6. Reimportar datos en el mismo orden.

**Ventaja principal:** elimina completamente la necesidad de `SeparateDatabaseAndState`, scripts `RunPython` de migración de M2M, y manipulación de `django_content_type`. El historial de migraciones queda limpio desde el día uno.

---

#### Plan B — Migración quirúrgica en caliente (fallback)

Solo usar si los datos de producción no pueden exportarse/reimportarse (volumen muy alto, integridad referencial no serializable, sin ventana de mantenimiento).

Este es el camino de mayor riesgo. Django mismo advierte que cambiar `AUTH_USER_MODEL` a mitad de proyecto es una de las operaciones más difíciles del framework porque `User` está muy entrelazado internamente.

**Orden de ejecución crítico:** cambiar `AUTH_USER_MODEL` en `settings.py` y preparar la nueva tabla `fintech_user` **antes** de correr `makemigrations` en apps dependientes. Si se corre `makemigrations` con referencias circulares sin resolver, Django intentará reescribir todas las FK simultáneamente y producirá errores de dependencia circular.

1. **Backup total:** `pg_dump` completo antes de cualquier operación.

2. **Migración de datos con `RunPython`** dentro de una migración Django — no con script SQL externo:
   - Mover registros de superusuarios/staff de `auth_user` hacia `fintech_user` si no existen ya.
   - Actualizar las FK de `Seller.user`, `Credit.registered_by`, `Expense.registered_by` para apuntar a los IDs correctos en `fintech_user`.
   - **Migrar relaciones M2M explícitamente:** los registros de `auth_user` con grupos o permisos asignados (`auth_user_groups`, `auth_user_user_permissions`) no se mueven solos. El script debe transferirlos a las tablas equivalentes de `fintech_user`. Si se omite, los administradores migrados pierden todos sus permisos y grupos.

3. **Usar `SeparateDatabaseAndState`** para FK que cambian de tabla de referencia sin recrear columnas (`BigAutoField` es el mismo tipo en ambas tablas).

4. **Actualizar `django_content_type`:** limpiar entradas obsoletas de `auth.User` para que los permisos del admin no queden rotos.

   > `--fake-initial` no es la herramienta correcta aquí. Ese flag aplica migraciones iniciales sobre tablas ya existentes. Lo correcto es `SeparateDatabaseAndState` dentro de migraciones manuales.

### Fase 3: JWT

Simple JWT ya usa `get_user_model()` internamente — al cambiar `AUTH_USER_MODEL` buscará en `fintech_user` automáticamente. Solo verificar `settings.py`:

```python
SIMPLE_JWT = {
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
```

Con `USERNAME_FIELD = 'email'`, el payload del token contendrá el email como identificador de login pero el `id` (PK) como claim interno del token. Ambos comportamientos son correctos.

### Fase 4: Estabilización

1. `python manage.py makemigrations` — generar migraciones para todas las apps afectadas.
2. Ejecutar en staging con datos de prueba antes de producción.
3. Verificar en staging:
   - Login de cliente con email + contraseña (JWT obtener + refrescar).
   - Login de admin en Django Admin con email + contraseña.
   - Créditos asociados a sus clientes.
   - Reportes de `insights` apuntando a los clientes correctos.
4. Hacer squash de migraciones de `fintech` después del proceso para limpiar la historia.

---

## 8. Archivos afectados (resumen)

| Archivo | Cambio |
|---|---|
| `core/settings.py` | `AUTH_USER_MODEL = 'fintech.User'` |
| `apps/fintech/models.py` | `UserManager` (`username` como arg principal), `REQUIRED_FIELDS = []`, `email = EmailField(blank=True)`, eliminar `User as Admin`, cambiar 3 FKs |
| `apps/fintech/backends.py` | Eliminar `UserWrapper` + `FintechAuthenticationBackend`, reescribir `ClientAuthenticationBackend` |
| `apps/fintech/admin.py` | Registrar `fintech.User` con `UserAdmin` extendido, `fieldsets` con email al tope |
| `apps/fintech/migrations/` | Plan A: reset + `makemigrations` limpio sobre BD nueva. Plan B: `RunPython` (incl. M2M) + `SeparateDatabaseAndState` en caliente |
| `apps/insights/views.py` | `from apps.fintech.models import User` → `get_user_model()` |
| `apps/insights/tasks.py` | `from apps.fintech.models import User` → `get_user_model()` |
| `apps/insights/signals.py` | Verificar importaciones directas → `get_user_model()` |
| `apps/insights/migrations/` | `makemigrations` (FK targets actualizados automáticamente) |
| `apps/forecasting/migrations/` | `makemigrations` (ídem) |
| Tests en `fintech`, `insights`, `revenue` | Actualizar `create_user(email=..., username=...)` |

---

## Conclusión

El `UserWrapper` en `backends.py` no es una solución — es la evidencia del problema. Su existencia prueba que el sistema de identidad está partido.

El objetivo de este refactor no es mejorar el wrapper sino hacerlo obsoleto. El resultado es un sistema donde:
- `fintech.User` es el modelo nativo de Django.
- El login es por username + contraseña — como funciona hoy, sin romper nada. `email` es un campo de perfil opcional a completar progresivamente.
- `Seller` sigue siendo el perfil operativo del vendedor — la lógica comercial no se mezcla con la identidad.
- JWT, Admin, permisos y grupos funcionan sin código adicional.
- `get_user_model()` y `settings.AUTH_USER_MODEL` devuelven lo correcto en todo el proyecto.

Hacerlo ahora, con pocos registros, es el momento de menor costo posible.
