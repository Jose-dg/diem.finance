from django.test import TestCase
from django.conf import settings

from apps.fintech import catalogs


class CatalogsImportTest(TestCase):
    def test_catalogs_module_importable(self):
        # Ensure the catalogs module exposes expected models
        self.assertTrue(hasattr(catalogs, 'Country'))
        self.assertTrue(hasattr(catalogs, 'Currency'))
        self.assertTrue(hasattr(catalogs, 'Category'))

    def test_country_creation_and_str(self):
        c = catalogs.Country.objects.create(name='Testland', utc_offset=0)
        self.assertEqual(str(c), 'Testland')
