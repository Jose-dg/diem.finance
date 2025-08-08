from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InsightsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.insights'
    verbose_name = _('Análisis e Insights')

    def ready(self):
        import apps.insights.signals
