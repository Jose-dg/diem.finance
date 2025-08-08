from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ForecastingConfig(AppConfig):
    name = 'apps.forecasting'
    verbose_name = _('Predicciones y Análisis')
    
    def ready(self):
        # Importar señales
        import apps.forecasting.signals 