from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, date
from apps.insights.services.credit_analysis_service import CreditAnalysisService

class CreditAnalysisViewsTestCase(TestCase):
    """Tests para las vistas de análisis de créditos"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
        # Crear usuario admin
        self.admin_user = get_user_model().objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        
        # Crear usuario normal
        self.normal_user = get_user_model().objects.create_user(
            username='user_test',
            email='user@test.com',
            password='testpass123'
        )
        
        # Fechas de prueba
        self.start_date = date(2025, 5, 1)
        self.end_date = date(2025, 12, 31)
    
    def test_credit_analysis_view_requires_authentication(self):
        """Test que la vista requiere autenticación"""
        url = reverse('insights:credit_analysis')
        response = self.client.get(url, {
            'start_date': '2025-05-01',
            'end_date': '2025-12-31'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_credit_analysis_view_requires_admin_permission(self):
        """Test que la vista requiere permisos de admin"""
        self.client.force_authenticate(user=self.normal_user)
        url = reverse('insights:credit_analysis')
        response = self.client.get(url, {
            'start_date': '2025-05-01',
            'end_date': '2025-12-31'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_credit_analysis_view_missing_parameters(self):
        """Test que la vista requiere parámetros obligatorios"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('insights:credit_analysis')
        
        # Sin parámetros
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('start_date y end_date son parámetros requeridos', response.data['error'])
        
        # Solo start_date
        response = self.client.get(url, {'start_date': '2025-05-01'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Solo end_date
        response = self.client.get(url, {'end_date': '2025-12-31'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_credit_analysis_view_invalid_date_format(self):
        """Test que la vista valida el formato de fecha"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('insights:credit_analysis')
        
        response = self.client.get(url, {
            'start_date': 'invalid-date',
            'end_date': '2025-12-31'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Formato de fecha inválido', response.data['error'])
    
    def test_credit_analysis_view_invalid_date_range(self):
        """Test que la vista valida el rango de fechas"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('insights:credit_analysis')
        
        response = self.client.get(url, {
            'start_date': '2025-12-31',
            'end_date': '2025-05-01'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('start_date debe ser menor o igual a end_date', response.data['error'])
    
    def test_credit_analysis_view_success(self):
        """Test que la vista funciona correctamente con parámetros válidos"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('insights:credit_analysis')
        
        response = self.client.get(url, {
            'start_date': '2025-05-01',
            'end_date': '2025-12-31'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        # Verificar estructura de respuesta
        data = response.data['data']
        self.assertIn('summary', data)
        self.assertIn('clients_table', data)
        self.assertIn('payments_analysis', data)
        self.assertIn('default_analysis', data)
        
        # Verificar parámetros
        params = response.data['parameters']
        self.assertEqual(params['start_date'], '2025-05-01')
        self.assertEqual(params['end_date'], '2025-12-31')
    
    def test_credit_analysis_view_with_limit(self):
        """Test que la vista respeta el parámetro limit"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('insights:credit_analysis')
        
        response = self.client.get(url, {
            'start_date': '2025-05-01',
            'end_date': '2025-12-31',
            'limit': '1'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        clients_table = response.data['data']['clients_table']
        # Si hay datos, verificar que respeta el límite
        if clients_table:
            self.assertLessEqual(len(clients_table), 1)
    
    def test_credit_analysis_view_invalid_limit(self):
        """Test que la vista valida el parámetro limit"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('insights:credit_analysis')
        
        response = self.client.get(url, {
            'start_date': '2025-05-01',
            'end_date': '2025-12-31',
            'limit': 'invalid'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('limit debe ser un número entero positivo', response.data['error'])
    
    def test_credit_analysis_summary_view(self):
        """Test de la vista de resumen"""
        self.client.force_authenticate(user=self.normal_user)  # No requiere admin
        url = reverse('insights:credit_analysis_summary')
        
        response = self.client.get(url, {
            'start_date': '2025-05-01',
            'end_date': '2025-12-31'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        # Verificar que solo incluye el resumen
        data = response.data['data']
        self.assertIn('summary', data)
        self.assertNotIn('clients_table', data)
        self.assertNotIn('payments_analysis', data)
        self.assertNotIn('default_analysis', data)
    
    def test_credit_analysis_clients_view(self):
        """Test de la vista específica de clientes"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('insights:credit_analysis_clients')
        
        response = self.client.get(url, {
            'start_date': '2025-05-01',
            'end_date': '2025-12-31'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        # Verificar estructura de respuesta
        data = response.data['data']
        self.assertIn('clients', data)
        self.assertIn('total_clients', data)
    
    def test_credit_analysis_clients_view_invalid_risk_level(self):
        """Test de validación de nivel de riesgo"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('insights:credit_analysis_clients')
        
        response = self.client.get(url, {
            'start_date': '2025-05-01',
            'end_date': '2025-12-31',
            'risk_level': 'INVALID'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('risk_level debe ser LOW, MEDIUM o HIGH', response.data['error'])
    
    def test_credit_analysis_clients_view_with_risk_filter(self):
        """Test de filtrado por nivel de riesgo"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('insights:credit_analysis_clients')
        
        # Filtrar por riesgo alto
        response = self.client.get(url, {
            'start_date': '2025-05-01',
            'end_date': '2025-12-31',
            'risk_level': 'HIGH'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que todos los clientes tienen riesgo alto (si hay datos)
        clients = response.data['data']['clients']
        for client in clients:
            self.assertEqual(client['risk_level'], 'HIGH')
    
    def test_credit_analysis_clients_view_with_sorting(self):
        """Test de ordenamiento de clientes"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('insights:credit_analysis_clients')
        
        response = self.client.get(url, {
            'start_date': '2025-05-01',
            'end_date': '2025-12-31',
            'sort_by': 'total_requested'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que está ordenado por total_requested (descendente) si hay datos
        clients = response.data['data']['clients']
        if len(clients) > 1:
            self.assertGreaterEqual(clients[0]['total_requested'], clients[1]['total_requested'])
    
    def test_credit_analysis_service_integration(self):
        """Test de integración con el servicio"""
        # Test del servicio directamente
        summary = CreditAnalysisService.get_credit_analysis_summary(self.start_date, self.end_date)
        self.assertIn('summary', summary)
        self.assertIn('total_credits', summary['summary'])
        
        clients_table = CreditAnalysisService.get_detailed_clients_table(self.start_date, self.end_date)
        self.assertIsInstance(clients_table, list)
        
        # Verificar que los clientes tienen la información esperada (si hay datos)
        for client in clients_table:
            self.assertIn('client_id', client)
            self.assertIn('username', client)
            self.assertIn('full_name', client)
            self.assertIn('total_credits', client)
            self.assertIn('total_requested', client)
            self.assertIn('total_paid', client)
            self.assertIn('total_pending', client)
            self.assertIn('payment_percentage', client)
            self.assertIn('risk_level', client)
    
    def test_credit_analysis_data_structure(self):
        """Test de la estructura de datos retornada"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('insights:credit_analysis')
        
        response = self.client.get(url, {
            'start_date': '2025-05-01',
            'end_date': '2025-12-31'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        summary = response.data['data']['summary']['summary']
        
        # Verificar que los campos existen
        self.assertIn('total_credits', summary)
        self.assertIn('total_requested', summary)
        self.assertIn('total_paid', summary)
        self.assertIn('total_pending', summary)
        self.assertIn('unique_clients', summary)
        self.assertIn('clients_without_payments', summary)
        self.assertIn('clients_in_default', summary)
        self.assertIn('payment_percentage', summary)
        
        # Verificar que los valores son del tipo correcto
        self.assertIsInstance(summary['total_credits'], int)
        self.assertIsInstance(summary['total_requested'], float)
        self.assertIsInstance(summary['total_paid'], float)
        self.assertIsInstance(summary['total_pending'], float)
        self.assertIsInstance(summary['unique_clients'], int)
        self.assertIsInstance(summary['clients_without_payments'], int)
        self.assertIsInstance(summary['clients_in_default'], int)
        self.assertIsInstance(summary['payment_percentage'], (int, float))
