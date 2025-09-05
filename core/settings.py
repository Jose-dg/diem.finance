from pathlib import Path
from datetime import timedelta
import os
import environ
from celery.schedules import crontab

env = environ.Env()
environ.Env.read_env()

ENVIROMENT = env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = 'django-insecure-s%=f4!f-89o#gm3e%t2ss4$81xyk*e*%a#*)6#xi)o%_^rxo)x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
]

PROJECT_APPS = [
    'apps.fintech',
    'apps.dashboard'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'apps.fintech',
    'apps.dashboard',

    'apps.revenue',
    'apps.forecasting',
    'apps.insights',  # Nueva aplicación
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    "default": env.db("DATABASE_URL"),
}

DATABASES["default"]["ATOMIC_REQUESTS"] = True

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'finance',
#         'USER': 'postgres',
#         'PASSWORD': '7508',
#         'HOST': 'localhost', 
#         'PORT': '5432', 
#     }
# }

CORS_ALLOW_ALL_ORIGINS = True

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:3001',
    'https://finance-app-one-navy.vercel.app'
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:3001',
    'https://finance-app-one-navy.vercel.app'
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Bogota'

USE_I18N = False  

USE_TZ = False

LANGUAGES = [
    ('en', 'English'),
]

LOCALE_PATHS = []


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'apps/fintech/static'),
]

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'build/static')
# ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cache configuration for installment calculations
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 3600,  # 1 hora
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

# Celery Configuration
# Configuración que usa REDIS_URL si está disponible, sino usa localhost
REDIS_URL = os.environ.get('REDIS_URL')

# Debug: Imprimir la configuración de Redis para verificar
import logging
logger = logging.getLogger(__name__)
logger.info(f"REDIS_URL configurado: {REDIS_URL}")
logger.info(f"REDIS_URL desde env: {os.environ.get('REDIS_URL', 'NO_ENCONTRADO')}")

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_EAGER_PROPAGATES = True

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Configuración de duración de resultados en Redis
CELERY_TASK_RESULT_EXPIRES = 86400  # 24 horas en segundos
CELERY_TASK_SOFT_TIME_LIMIT = 3600  # 1 hora límite suave
CELERY_TASK_TIME_LIMIT = 7200       # 2 horas límite duro

# Configuración de retención de resultados
CELERY_TASK_IGNORE_RESULT = False   # Guardar resultados
CELERY_TASK_STORE_EAGER_RESULT = True  # Guardar resultados inmediatamente

# Configuración de monitoreo
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True

CELERY_BEAT_SCHEDULE = {
    'recalc-credits-nightly': {
        'task': 'apps.fintech.tasks.batch_recalculate_credits',
        'schedule': crontab(hour=2, minute=0),
    },
    'installment-daily-maintenance': {
        'task': 'apps.fintech.tasks.installment_daily_maintenance',
        'schedule': crontab(hour=6, minute=0),  # 6:00 AM
    },
    'update-installment-statuses': {
        'task': 'apps.fintech.tasks.update_installment_statuses',
        'schedule': crontab(minute='*/30'),  # Cada 30 minutos
    },
    'send-payment-reminders': {
        'task': 'apps.fintech.tasks.send_payment_reminders',
        'schedule': crontab(hour=9, minute=0),  # 9:00 AM
    },
    'send-overdue-notifications': {
        'task': 'apps.fintech.tasks.send_overdue_notifications',
        'schedule': crontab(hour=10, minute=0),  # 10:00 AM
    },
}

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

SIMPLE_JWT = {
    # Token de acceso válido por 8 horas (tiempo de trabajo típico)
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    # Token de refresh válido por 7 días (una semana)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    # Rotar refresh tokens para mayor seguridad
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,  # Actualizar último login para auditoría
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    # Sliding tokens también actualizados
    'SLIDING_TOKEN_LIFETIME': timedelta(hours=7),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
}



# Revisarla forma en como se buscan las personas en el sistema desde transactions para hacer lo mismo en credits