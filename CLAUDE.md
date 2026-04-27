# diem.finance

## Project overview
Django-based financial management system for credit lending operations. Tracks credits, installment payments, morosidad (default levels), and provides analytics dashboards for portfolio management. Deployed on Render with PostgreSQL + Redis + Celery.

## Architecture
Five Django apps under `apps/`:
- **fintech** — Core domain: User (clients), Credit, Installment, Transaction, Account, Seller. Holds all business logic via a service layer at `apps/fintech/services/`.
- **dashboard** — Read-only dashboard views that aggregate fintech data for the frontend.
- **insights** — Analytics engine: CLV, financial alerts, defaulter reports, credit analysis. Has its own service layer at `apps/insights/services/`.
- **revenue** — `CreditEarnings` model tracking realized vs. theoretical earnings per credit.
- **forecasting** — Forecasting models (early stage, minimal endpoints).

@docs/architecture.md

## Tech stack
- Django 4.2.16, DRF 3.14.0, SimpleJWT 5.3.1
- PostgreSQL (psycopg3), Redis (broker + result backend)
- Celery 5.5.3 with Beat scheduler
- Whitenoise (static), Gunicorn (WSGI)
- django-filter 24.3, django-cors-headers 4.1.0

## Development setup

### Prerequisites
Python 3.13, PostgreSQL running locally or `DATABASE_URL` pointing to Render, Redis instance.

### Running locally
```bash
cd /Users/jose/Documents/Dev/fintech
source env/bin/activate
# Copy and fill core/.env (see Environment variables below)
python manage.py migrate
python manage.py runserver
```

### Celery (required for scheduled tasks)
```bash
celery -A core.celery.task_app worker --loglevel=info
celery -A core.celery.task_app beat --loglevel=info
```

### Environment variables
File lives at `core/.env` (read automatically via `python-environ`).

| Variable | Required | Notes |
|---|---|---|
| `SECRET_KEY` | yes | Django secret |
| `DEBUG` | yes | `TRUE` / `FALSE` |
| `DATABASE_URL` | yes | `postgresql://user:pass@host/db` |
| `REDIS_URL` | yes | Celery broker + result backend |
| `ALLOWED_HOSTS` | yes | Comma-separated list |
| `CORS_ALLOW_ALL_ORIGINS` | yes | `True` / `False` |

## Common commands

### Development
```bash
python manage.py runserver
python manage.py shell
python manage.py migrate
python manage.py makemigrations
```

### Custom management commands (all in `apps/fintech/management/commands/`)
```bash
python manage.py recalcular_todos_creditos   # Recalculate all credit balances
python manage.py update_morosidad             # Update default levels on credits
python manage.py fix_credit_balances          # Fix balance inconsistencies
python manage.py apply_additional_interest    # Apply additional interest charges
python manage.py exportar_usuarios_creditos   # Export users + credits to file
python manage.py diagnosticar_creditos        # Diagnose credit inconsistencies
```

### Testing
```bash
python manage.py test                                # All tests
python manage.py test apps.fintech.tests             # One app
python manage.py test apps.fintech.tests.test_credit_lifecycle  # One file
```

### Deployment (Render)
```bash
./build.sh   # migrate + collectstatic + create superuser if missing
```

## Django conventions in this project

### Models
- `DEFAULT_AUTO_FIELD = BigAutoField` — all PKs are auto-incrementing integers.
- Many models add a `uid = UUIDField(default=uuid.uuid4, editable=False, unique=True)` as a stable external identifier (not the PK).
- No global BaseModel — `created_at`/`updated_at` are added per-model where needed.
- Custom managers: `CreditManager`, `TransactionManager`, `InstallmentManager`.
- `ATOMIC_REQUESTS = True` — every HTTP request is already wrapped in a DB transaction.
- `USE_TZ = False` — datetimes are naive (no timezone info). `TIME_ZONE = 'America/Bogota'`.

### Dual user model (critical)
There are **two separate user tables**:
- `django.contrib.auth.User` (`Admin` in imports) — staff/admins only. This is what `get_user_model()` returns.
- `apps.fintech.models.User` — clients. Extends `AbstractUser` but is NOT `AUTH_USER_MODEL`. Import explicitly as `from apps.fintech.models import User`.

`Seller.user` points to `auth.User`. `Credit.user` points to `apps.fintech.models.User`.

### Views / Viewsets
- `apps.fintech`: mix of `ModelViewSet` (manually wired, no Router) and `APIView` / `@api_view`.
- `apps.insights` / `apps.dashboard`: `APIView` classes only.
- Business logic lives in `services/`, not in views. Views call service methods and return `Response`.

### URL patterns
No API versioning. Prefix structure:
```
fintech/<resource>/          →  apps.fintech.urls
dashboard/<resource>/        →  apps.dashboard.urls
insights/<resource>/         →  apps.insights.urls
api/token/                   →  JWT obtain
api/token/refresh/           →  JWT refresh
```
ViewSets are wired manually (no `DefaultRouter`): `ViewSet.as_view({'get': 'list', 'post': 'create'})`.

### Serializers
`ModelSerializer` throughout. No global BaseSerializer. Nested serializers are used (e.g., `UserSerializer` inside `TransactionSerializer`). Avoid `from .models import *` — it's already in `fintech/serializers.py` and causes namespace pollution.

### Settings structure
Single settings file: `core/settings.py`. No base/dev/prod split. Reads env from `core/.env`.

## Testing conventions
Django's built-in `unittest` (no pytest). Test files under `apps/<app>/tests/` as a package. No factory_boy, no coverage config. Tests use Django's `TestCase`.

## Background tasks (Celery)
Tasks defined in `apps/fintech/tasks.py`. Celery app instance is `core.celery.task_app` (not `app`).

Beat schedule runs: credit recalculation (2 AM), installment maintenance (6 AM), status updates (8 AM), payment reminders (9 AM), overdue notifications (10 AM), status every 30 min.

## Important patterns & gotchas
- **`Credit.save()` has recursion protection**: uses `self._saving` flag + `db_transaction.atomic()`. When updating specific fields, always use `save(update_fields=[...])` to avoid triggering the full save logic.
- **`Installment` is flagged for redesign**: the model has a `TODO` comment in `models.py` describing known problems. Avoid adding more complexity to it.
- **Celery import**: always `from core.celery import task_app`, not `from core.celery import app`.
- **Auth backends**: clients authenticate via `FintechAuthenticationBackend` which wraps `apps.fintech.models.User` in a `UserWrapper`. Don't assume `request.user` is always a plain `auth.User` instance.
- **`select_related` on Credit**: `Credit` has FKs to `user`, `seller`, `currency`, `periodicity`, `payment`, `subcategory`. Always add `select_related` when listing credits to avoid N+1.
- **`insights` permissions temporarily disabled**: several `insights` views have `permission_classes = [AllowAny]` (auth disabled for frontend testing). Restore before production.
- **No API documentation**: no Swagger/drf-spectacular configured.

## Files to never modify
- `apps/*/migrations/` — never edit existing migration files; only create new ones.
- `core/.env` — contains production secrets; never commit.
- `celerybeat-schedule.db` — auto-generated by Celery Beat.
