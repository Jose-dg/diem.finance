# Catálogos en `apps/fintech`

Este documento explica por qué dejamos los modelos de catálogo dentro de la app `fintech` y cómo referenciarlos correctamente desde otras apps.

Resumen
-------
- Los modelos de catálogo (Country, Currency, Category, SubCategory, Periodicity, DocumentType, Language, ParamsLocation, PhoneNumber, Label) permanecen en `apps/fintech` bajo el submódulo `apps/fintech/catalogs.py`.
- `fintech` actúa como owner de estos datos. Otras apps deben consumirlos, no importarlos para definir su propio estado.

Reglas de uso
--------------
1. Referenciar mediante lazy string cuando declares FKs en otras apps, por ejemplo:

```py
from django.db import models

class MyModel(models.Model):
    country = models.ForeignKey('fintech.Country', on_delete=models.PROTECT)
```

2. Nunca hacer `from apps.fintech.models import Country` en módulos que a su vez son importados por `fintech` (evitar import cycles).

3. Los cambios en los catálogos (migrations) son responsabilidad de `apps/fintech`.

Cómo evolucionar en el futuro
----------------------------
- Si en el futuro los catálogos crecen y varios dominios los necesitan de forma independiente, considerar extraerlos en una app dedicada. Antes de hacerlo, crear una API interna para consumirlos y migrar consumidores gradualmente.

Notas operativas
-----------------
- Las migraciones existentes y nombres de tablas no cambian por este refactor; sólo reorganizamos el código en el repo para mejor mantenibilidad.
