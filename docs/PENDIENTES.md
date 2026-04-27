# Pendientes técnicos — diem.finance

_Última actualización: 2026-04-26_

---

## ✅ Completado en esta iteración

- `AUTH_USER_MODEL = 'fintech.User'` establecido correctamente
- `UserWrapper` anti-patrón eliminado de `backends.py`
- FK de todos los modelos migradas a `settings.AUTH_USER_MODEL`
- `groups` / `user_permissions` redundantes eliminados del modelo `User`
- Managers muertos (`CreditManager`, `TransactionManager`) removidos
- Migraciones fintech consolidadas (9 archivos → 2)
- ETL (`migrar_datos.py`) ejecutado: 611 usuarios, 2007 créditos migrados a nueva BD
- `build.sh` corregido (usaba `auth.User` swapped → ahora `get_user_model()`)
- 28 vistas de `insights` con `AllowAny` → `IsAuthenticated` restaurado

---

## 🔴 Urgente — Seguridad

### 1. Collector endpoints sin autenticación
5 funciones en `apps/fintech/views.py` tienen el decorador `@permission_classes([IsAuthenticated])` comentado:
- `collector_dashboard`
- `due_today_installments`
- `due_tomorrow_installments`
- `upcoming_installments`
- `overdue_installments`

Exponen datos de cuotas y clientes sin ningún control. Descomentar y verificar que el frontend envía el token JWT en esas llamadas.

### 2. `SECRET_KEY` en historial de git
`core/.env` fue commiteado en versiones anteriores. Aunque la BD vieja ya fue reemplazada, la `SECRET_KEY` podría seguir siendo la misma. Si se rota la `SECRET_KEY`:
- Todos los tokens JWT activos quedan inválidos (logout forzado de todos los usuarios)
- Hay que actualizar la variable en Render y en local
- Hacerlo en una ventana de bajo tráfico y avisar al frontend

### 3. Rate limiting en `/api/token/`
El endpoint de login no tiene límite de intentos. Un atacante puede hacer fuerza bruta sobre contraseñas. Opciones:
- `django-ratelimit` (simple, decorador)
- `django-axes` (más completo, bloquea IPs)

---

## 🟡 Corto plazo — Deuda técnica activa

### 4. `Role.is_staff_role` — campo redundante
`Role` tiene `is_staff_role = BooleanField` que intenta distinguir roles de staff vs. clientes. Django ya provee `User.is_staff` para eso. El campo no aporta lógica diferencial y confunde el propósito de `Role` como clasificador de negocio puro.
- **Acción**: eliminar el campo, generar migración, verificar que nada lo lea.
- **Esfuerzo**: 2 horas. **Riesgo**: bajo.

### 5. `get_user_model()` en services y serializers
Los siguientes archivos aún usan `User = get_user_model()` al nivel de módulo:
- `apps/fintech/serializers.py`
- `apps/fintech/views.py`
- `apps/fintech/services/payment/payment_service.py`
- `apps/fintech/services/utils/audit/audit_logger.py`
- `apps/fintech/management/commands/creditos_por_usuario.py`
- `apps/fintech/management/commands/estadisticas_usuarios.py`
- `apps/fintech/management/commands/usuarios_y_creditos.py`
- `apps/dashboard/models.py`

Funcionan correctamente porque `AUTH_USER_MODEL` ya está configurado. La limpieza es estética y de consistencia — no es urgente, pero debería hacerse antes de incorporar nuevos colaboradores.

### 6. Índices de base de datos
Con 2007 créditos y 10.800 transacciones, las queries frecuentes no tienen índices explícitos en columnas de alta cardinalidad. Candidatos prioritarios:

| Modelo | Campo | Razón |
|---|---|---|
| `Credit` | `state` | Filtro más común en dashboard |
| `Credit` | `user_id` | Join frecuente |
| `Credit` | `created_at` | Reportes por fecha |
| `Installment` | `status` | Filtro en collector y Celery tasks |
| `Installment` | `due_date` | Queries de vencimiento diario |
| `Transaction` | `date` | Reportes financieros |

- **Acción**: agregar `db_index=True` en los campos o `Meta.indexes` con índices compuestos.
- **Esfuerzo**: 2 horas. **Riesgo**: bajo (solo lectura de rendimiento).

### 7. `migrar_datos.py` — script de un solo uso en el codebase
El comando vive en `apps/fintech/management/commands/migrar_datos.py`. Ya cumplió su función. Opciones:
- Moverlo a `/scripts/` fuera del árbol de management commands (no ejecutable accidentalmente)
- O dejarlo pero documentar claramente que es un comando destructivo de una sola vez

### 8. App `forecasting` — incompleta
La app está en `INSTALLED_APPS` y tiene modelos (`CreditPrediction`, `SeasonalPattern`, `RiskAssessment`) pero no tiene endpoints ni lógica activa. Genera migraciones vacías y confusión. Opciones:
- Activarla con endpoints reales cuando haya roadmap claro
- O sacarla de `INSTALLED_APPS` temporalmente para no cargarla sin propósito

---

## 🟢 Calidad — sin urgencia operacional

### 9. Cobertura de tests
El sistema no tiene tests sobre los flujos más críticos del negocio:
- Registro de pago y recálculo de `pending_amount`
- Ciclo completo de crédito: creación → cuotas → pago → cierre
- Cambio de `morosidad_level` al vencer cuotas
- Autenticación por teléfono (`ClientAuthenticationBackend`)

Sin tests, cualquier cambio en `Credit.save()` o `InstallmentManager` puede romper silenciosamente la lógica de cartera.

### 10. Imports no utilizados en `models.py`
- `ROUND_HALF_UP` (importado, no usado)
- `math` (importado, no usado)

Limpieza de 2 líneas.

### 11. SMTP — recuperación de contraseña no funcional
Con `fintech.User` como `AUTH_USER_MODEL`, Django puede hacer password reset nativo, pero no hay servidor de email configurado. El flujo existe pero no envía nada. Configurar con SendGrid, Mailgun o SES cuando haya decisión de proveedor.

---

## ⏸ Diferir — alta complejidad, bajo beneficio inmediato

### 12. `total_abonos` y `pending_amount` como campos calculados
El documento de deuda técnica propone convertirlos a `@property` que calculen en tiempo real. El problema: estos campos son centrales en `Credit.save()`, `update_total_abonos()`, `update_pending_amount()` y en todas las Celery tasks de recálculo. Tocarlos sin un plan de migración de datos y tests exhaustivos es muy arriesgado.
- **Veredicto**: diferir hasta tener cobertura de tests sólida (ítem 9).

### 13. Rediseño de `Installment`
Propuesta de separar en `ScheduledPayment` + `AmortizationRow` + `ActualPayment`. Arquitectónicamente correcto para un sistema bancario formal, pero implica migrar 5.391 registros, reescribir `installment_service.py` y 5 Celery tasks.
- **Veredicto**: diferir. El modelo actual cubre los requerimientos de negocio actuales.

### 14. Separación de modelos por app
Dividir `fintech/models.py` en apps más pequeñas. `Meta.db_table` elimina el riesgo de BD (sin `ALTER TABLE`) pero no resuelve el refactor de imports en ~30 archivos, los problemas de `ContentType` en el admin, ni la dependencia de `AUTH_USER_MODEL`. Los modelos de `fintech` son además genuinamente interdependientes (`Credit` ↔ `Installment` ↔ `Transaction` ↔ `User`). El service layer ya provee la separación de responsabilidades que importa operacionalmente.
- **Patrón adoptado**: nuevas funcionalidades en apps nuevas (`interactions`). Los modelos existentes permanecen en `fintech`.
- **Veredicto**: no hacer. Reevaluar solo si el equipo crece significativamente.

### 15. `InstallmentManager` → ORM inline en el service
Los métodos del manager (`pending_installments()`, `overdue_installments()`, etc.) son filtros simples que podrían estar directamente en `installment_service.py`. Es una mejora de consistencia con la filosofía "nativo Django" que adoptamos.
- **Veredicto**: diferir junto con cualquier refactor de `installment_service.py`.

---

## 🚀 Próxima feature — App `interactions`

Plan completo en `docs/PLAN_GEOLOCALIZACION_Y_COBRANZA.md`.

**Decisiones de arquitectura ya tomadas:**
- Será una **nueva app Django independiente** (`apps/interactions/`) — no se agrega código a `fintech`
- Las FK apuntan hacia `fintech` pero `fintech` no importa nada de `interactions`
- Usa `settings.AUTH_USER_MODEL` en toda referencia a usuario — nunca el modelo directo
- PKs híbridos: `BigAutoField` + `uid (UUIDField)` en `InteractionLog`
- Requiere agregar `collection_notes = TextField(blank=True)` en `fintech.Credit` para notas persistentes del cliente (instrucciones para el cobrador que no cambian entre visitas)

**Resumen de fases:**

| Fase | Objetivo | Modelos / Endpoints |
|---|---|---|
| 1 | Fundación de la app | `CollectionPoint`, `InteractionLog` + signal auto-creación |
| 2 | Integración transaccional | FK opcional a `fintech.Transaction` + validación de cobro |
| 3 | API offline-first | `POST /api/interactions/sync` con idempotencia por UUID |
| 4 | Observabilidad | Mapas de calor en `insights`, KPIs de asesor |
| 5 | Evolución futura | Biometría, `django-simple-history` |

**Decisiones de diseño ya tomadas:**
- Nombre de app: `interactions`
- PKs: `BigAutoField` + campo `uid (UUID)` en modelos que se exponen externamente
- Idempotencia: el dispositivo móvil genera el UUID antes de enviar

---

## Priorización sugerida

```
Inmediato   → #1 Collector auth, #2 SECRET_KEY (coordinar con frontend)
Esta semana → #3 Rate limiting, #4 Role.is_staff_role, #6 Índices DB
Próxima     → #9 Tests (requisito previo para #12 y #13), #8 Forecasting
Feature     → interactions app (doc separado)
Diferir     → #12, #13, #14, #15
```
