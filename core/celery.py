import os
from celery import Celery

# Definir la variable de entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Crear instancia de Celery e incluir explícitamente las tareas
task_app = Celery(
    "core",
    include=["apps.fintech.tasks"]  # apunta al módulo tasks.py en apps/fintech
)

# Cargar configuración de CELERY_ desde settings.py
task_app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover en INSTALLED_APPS
task_app.autodiscover_tasks()