from django.apps import AppConfig

class InteractionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.interactions'
    verbose_name = 'Interactions & Geolocation'

    def ready(self):
        import apps.interactions.signals
