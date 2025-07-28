import os
from celery import Celery
from celery.schedules import crontab

# Definir la variable de entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Crear instancia de Celery e incluir explícitamente las tareas
task_app = Celery(
    "core",
    include=["apps.fintech.tasks"]  # apunta al módulo tasks.py en apps/fintech
)

# Cargar configuración de CELERY_ desde settings.py
task_app.config_from_object("django.conf:settings", namespace="CELERY")

# Configurar tareas periódicas
task_app.conf.beat_schedule = {
    # Cálculo masivo diario a las 2 AM
    'calculate-installment-fields-daily': {
        'task': 'apps.fintech.tasks.calculate_installment_fields_batch',
        'schedule': crontab(hour=2, minute=0),
    },
    # Cálculo de cuotas vencidas a las 6 AM
    'calculate-overdue-installments-daily': {
        'task': 'apps.fintech.tasks.calculate_overdue_installments',
        'schedule': crontab(hour=6, minute=0),
    },
    # Actualización de estados de créditos a las 8 AM
    'update-credit-statuses-daily': {
        'task': 'apps.fintech.tasks.update_credit_statuses',
        'schedule': crontab(hour=8, minute=0),
    },
    # Cálculo por periodicidad a las 10 AM
    'calculate-periodic-installments-daily': {
        'task': 'apps.fintech.tasks.calculate_periodic_installments',
        'schedule': crontab(hour=10, minute=0),
    },
    # Limpieza de cache semanal
    'clear-old-cache-weekly': {
        'task': 'apps.fintech.tasks.clear_old_cache',
        'schedule': crontab(hour=3, minute=0, day_of_week=1),  # Lunes 3 AM
    },
}

# Autodiscover en INSTALLED_APPS
task_app.autodiscover_tasks()