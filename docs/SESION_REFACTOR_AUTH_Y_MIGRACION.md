# Sesión: Refactor AUTH_USER_MODEL + Migración de BD
_Realizada: 2026-04-26 / 2026-04-27_

---

## Objetivo de la sesión

Eliminar el anti-patrón `UserWrapper` en `backends.py` y establecer `fintech.User` como el modelo de usuario nativo de Django (`AUTH_USER_MODEL`), migrando todos los datos de producción a una nueva base de datos con el esquema corregido.

---

## Estado antes de empezar

- `AUTH_USER_MODEL` no estaba configurado → Django usaba `auth.User` por defecto
- `fintech.User` existía pero no era `AUTH_USER_MODEL` — era un modelo paralelo
- `backends.py` usaba `UserWrapper` (objeto Python falso que imitaba `auth.User`) para bridgear ambos modelos
- `Seller.user` → `auth.User`. `Credit.user` → `fintech.User`. Inconsistencia total
- Admins vivían en `auth_user` (tabla separada), clientes en `fintech_user`

---

## Cambios de código aplicados

### `core/settings.py`
- `AUTH_USER_MODEL = 'fintech.User'` agregado
- `AUTHENTICATION_BACKENDS` actualizado a `ClientAuthenticationBackend` (sin UserWrapper)

### `apps/fintech/models.py`
- `UserManager` agregado con `create_user` / `create_superuser`
- `User.REQUIRED_FIELDS = []` (sin email obligatorio — 604/605 clientes no tienen email)
- `User.email` → `EmailField(blank=True, default='')`
- `groups` y `user_permissions` eliminados del modelo (eran overrides para evitar clash — ya no necesarios con un solo AUTH_USER_MODEL)
- FK de `Credit.user`, `Credit.registered_by`, `Transaction.user`, `Expense.user`, `Expense.registered_by`, `Address.user`, `Seller.user` → todos cambiados a `settings.AUTH_USER_MODEL`
- `CreditManager` y `TransactionManager` eliminados (no tenían uso real)
- Método duplicado `is_overdue()` eliminado de `Installment` (quedó solo el `@property`)
- Método `get_total_amount_due()` eliminado de `Installment` (duplicaba `total_amount_due` property)
- Import de `Group` y `Permission` eliminado

### `apps/fintech/backends.py`
- Reescrito completamente — eliminado `UserWrapper` y `FintechAuthenticationBackend`
- `ClientAuthenticationBackend` extiende `ModelBackend` usando `get_user_model()` directamente
- Soporta login por `username`, `email` o `phone_1__phone_number`

### `apps/fintech/migrations/`
- Migraciones 0002–0009 eliminadas del repo (consolidadas en `0001_initial`)
- Nueva migración `0002_alter_user_groups_alter_user_user_permissions` aplicada

### `build.sh`
- Corregido: `from django.contrib.auth.models import User` → `from django.contrib.auth import get_user_model; User = get_user_model()`
- El comando anterior fallaba porque `auth.User` está "swapped" con el nuevo `AUTH_USER_MODEL`

### `apps/insights/views.py`
- 28 vistas con `AllowAny` → `IsAuthenticated` restaurado

### `apps/fintech/management/commands/migrar_datos.py`
- Nuevo comando ETL creado para migrar datos de esquema viejo a nuevo
- Corregido post-sesión: añadido paso `AccountMethodAmount` que faltaba

---

## Proceso de migración de datos

### Bases de datos involucradas

| Nombre | Tipo | Propósito |
|---|---|---|
| `fintech_replica` | Local PostgreSQL | Copia de producción original (esquema viejo) |
| `fintech_nueva` | Local PostgreSQL | Nueva BD local con esquema nuevo |
| `fintech_lb1k` (Render) | Cloud PostgreSQL 16 | Producción nueva |

### Pasos ejecutados

1. Backup de producción original: `backups/backup_prod_20260426.dump` (1.4MB)
2. `fintech_replica` creada localmente desde el backup
3. `fintech_nueva` creada localmente con schema nuevo vía `migrate`
4. ETL `migrar_datos.py` ejecutado: fintech_replica → fintech_nueva
5. Validación local: `manage.py check`, JWT login, endpoint `/fintech/credits/`
6. `pg_dump fintech_nueva | psql Render` para poblar la BD de producción
7. `.env` actualizado con nueva `DATABASE_URL` de Render

### Decisión crítica — IDs de admins

`auth_user` (IDs 1-6) y `fintech_user` (IDs 1-605) tenían colisión. Los 6 admins fueron insertados en `fintech_user` sin ID explícito → PostgreSQL asignó IDs 606–611.

| Admin | ID antiguo (auth_user) | ID nuevo (fintech_user) |
|---|---|---|
| admin | 1 | 606 |
| jose | 2 | 607 |
| lorena | 3 | 608 |
| danielojeda | 4 | 609 |
| HectorAA | 5 | 610 |
| (6to admin) | 6 | 611 |

### Bug encontrado y corregido post-migración

`AccountMethodAmount` (10,710 registros) fue omitido del ETL original. Detectado al verificar la tabla vacía en `fintech_nueva`.

**Corrección aplicada:**
- Local: `\COPY` directo de `fintech_replica` → `fintech_nueva` (10,710 registros)
- Producción: Render tenía 21 registros nuevos (pagos reales del 2026-04-27). Se copiaron los 10,710 históricos sin ID explícito para no colisionar con los 21 nuevos. Total final: **10,731 registros**.
- ETL corregido: `_account_method_amount()` añadido al comando para futuras ejecuciones.

---

## Estado final de producción

| Tabla | Registros |
|---|---|
| `fintech_user` | 611 (605 clientes + 6 admins) |
| `fintech_credit` | 2,007 |
| `fintech_installment` | 5,391 |
| `fintech_transaction` | 10,800+ (creciendo) |
| `fintech_expense` | 391 |
| `fintech_accountmethodamount` | 10,731 (10,710 históricos + 21 nuevos) |
| `revenue_creditearnings` | 656 |

---

## Configuración actual

```
core/.env → DATABASE_URL = postgresql://fintech_lb1k_user:...@render.com/fintech_lb1k
settings.py → AUTH_USER_MODEL = 'fintech.User'
settings.py → AUTHENTICATION_BACKENDS = ['ClientAuthenticationBackend', 'ModelBackend']
```

**Local** (`settings.py` tiene bloque hardcodeado comentado):
```python
# Descomentar para trabajar contra fintech_nueva local:
# DATABASES = {'default': {'ENGINE': '...postgresql', 'NAME': 'fintech_nueva', ...}}
# El bloque env.db("DATABASE_URL") debe quedar comentado mientras tanto
```

---

## Decisiones de arquitectura tomadas en esta sesión

| Decisión | Veredicto |
|---|---|
| `USERNAME_FIELD` = 'username' (no email) | 604/605 clientes no tienen email — mantener username |
| `settings.AUTH_USER_MODEL` en FKs de modelos | Adoptado — en lugar de `get_user_model()` o string directo |
| `get_user_model()` en services/serializers | Correcto para código fuera de models.py — no cambiar |
| Separación de modelos por app con `db_table` | Analizado y descartado — costo en imports/ContentType supera el beneficio |
| `RouteAssignment` en app `interactions` | Descartado — cobradores organizan su ruta libremente |
| `interactions` como nueva app Django | Confirmado — no agregar código a `fintech` |

---

## Pendientes al cierre de sesión

Ver `docs/PENDIENTES.md` para lista completa priorizada. Los más urgentes:

1. **Collector endpoints sin auth** — `fintech/views.py` tiene 5 funciones con `@permission_classes([IsAuthenticated])` comentado
2. **`SECRET_KEY` en historial git** — rotar en ventana de bajo tráfico
3. **`Role.is_staff_role`** — campo redundante con `User.is_staff`, eliminar
4. **Tests de ciclo de crédito** — no hay cobertura de los flujos críticos
5. **App `interactions`** — próxima feature, plan en `docs/PLAN_GEOLOCALIZACION_Y_COBRANZA.md`

---

## Cómo continuar en una nueva sesión

```bash
# Verificar que producción responde
source env/bin/activate
python manage.py check
python manage.py shell -c "from apps.fintech.models import User, Credit; print(User.objects.count(), Credit.objects.count())"

# Si necesitas trabajar contra fintech_nueva local:
# 1. Comentar env.db("DATABASE_URL") en settings.py
# 2. Descomentar el bloque hardcodeado con NAME='fintech_nueva'

# Ver migraciones aplicadas en producción
python manage.py showmigrations
```
