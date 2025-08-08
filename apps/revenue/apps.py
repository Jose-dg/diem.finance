from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class RevenueConfig(AppConfig):
    name = 'apps.revenue'
    verbose_name = _('Ingresos y Ganancias')
    
    def ready(self):
        # Importar señales
        import apps.revenue.signals 