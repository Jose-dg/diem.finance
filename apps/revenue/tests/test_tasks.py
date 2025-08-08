from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch

from apps.fintech.models import Credit
from ..models import CreditEarnings, RevenueMetrics, EarningsSnapshot
from ..tasks import (
    update_credit_earnings,
    calculate_revenue_metrics,
    generate_earnings_snapshots,
    analyze_earnings_trends,
    validate_earnings_consistency
)

class TasksTests(TestCase):
    def setUp(self):
        self.credit = Credit.objects.create(
            price=Decimal('1000.00'),
            cost=Decimal('800.00'),
            interest=Decimal('100.00')
        )
        
        self.earnings = CreditEarnings.objects.create(
            credit=self.credit,
            theoretical=Decimal('300.00'),
            realized=Decimal('100.00'),
            pending=Decimal('200.00')
        )

    @patch('apps.revenue.tasks.EarningsService.recalculate_earnings')
    def test_update_credit_earnings(self, mock_recalculate):
        """Prueba la tarea de actualización de ganancias"""
        mock_recalculate.return_value = self.earnings
        
        result = update_credit_earnings.apply(args=[self.credit.id])
        
        self.assertTrue(result.successful())
        self.assertEqual(result.get()['status'], 'success')
        mock_recalculate.assert_called_once_with(self.earnings)

    @patch('apps.revenue.tasks.RevenueService.calculate_period_metrics')
    def test_calculate_revenue_metrics(self, mock_calculate):
        """Prueba la tarea de cálculo de métricas"""
        metrics = RevenueMetrics.objects.create(
            period_start=timezone.now(),
            period_end=timezone.now() + timezone.timedelta(days=30),
            total_theoretical=Decimal('1000.00'),
            total_realized=Decimal('600.00'),
            total_pending=Decimal('400.00')
        )
        mock_calculate.return_value = metrics
        
        result = calculate_revenue_metrics.apply()
        
        self.assertTrue(result.successful())
        self.assertEqual(result.get()['status'], 'success')
        self.assertEqual(result.get()['metrics_id'], metrics.id)

    def test_generate_earnings_snapshots(self):
        """Prueba la tarea de generación de snapshots"""
        result = generate_earnings_snapshots.apply(kwargs={'batch_size': 10})
        
        self.assertTrue(result.successful())
        self.assertEqual(result.get()['status'], 'success')
        self.assertEqual(
            EarningsSnapshot.objects.filter(credit_earnings=self.earnings).count(),
            1
        )

    @patch('apps.revenue.tasks.EarningsService.get_earnings_trends')
    def test_analyze_earnings_trends(self, mock_trends):
        """Prueba la tarea de análisis de tendencias"""
        mock_trends.return_value = {
            'period_start': timezone.now(),
            'period_end': timezone.now() + timezone.timedelta(days=30),
            'initial_realized': Decimal('100.00'),
            'final_realized': Decimal('200.00'),
            'change': Decimal('100.00'),
            'snapshot_count': 5
        }
        
        result = analyze_earnings_trends.apply(kwargs={'days': 30})
        
        self.assertTrue(result.successful())
        self.assertEqual(result.get()['status'], 'success')
        self.assertEqual(len(result.get()['results']), 1)

    @patch('apps.revenue.tasks.EarningsService.validate_earnings_state')
    def test_validate_earnings_consistency(self, mock_validate):
        """Prueba la tarea de validación de consistencia"""
        mock_validate.return_value = True
        
        result = validate_earnings_consistency.apply(kwargs={'batch_size': 10})
        
        self.assertTrue(result.successful())
        self.assertEqual(result.get()['status'], 'success')
        self.assertEqual(result.get()['inconsistencies_found'], 0)
        mock_validate.assert_called_once_with(self.earnings)

    def test_task_retry_on_error(self):
        """Prueba que las tareas reintenten en caso de error"""
        with patch('apps.revenue.tasks.EarningsService.recalculate_earnings') as mock:
            mock.side_effect = Exception('Test error')
            
            task = update_credit_earnings.s(self.credit.id)
            result = task.apply()
            
            self.assertTrue(result.failed())
            self.assertEqual(mock.call_count, 1)  # Primera llamada
            
            # La tarea debería programar un reintento
            self.assertTrue(result.retried())

    def test_task_atomic_transaction(self):
        """Prueba que las tareas usen transacciones atómicas"""
        with patch('apps.revenue.tasks.transaction.atomic') as mock_atomic:
            update_credit_earnings.apply(args=[self.credit.id])
            
            mock_atomic.assert_called_once()

    def test_task_logging(self):
        """Prueba que las tareas registren información importante"""
        with self.assertLogs('apps.revenue.tasks', level='INFO') as logs:
            update_credit_earnings.apply(args=[self.credit.id])
            
            self.assertTrue(any(
                'Updating credit earnings' in log 
                for log in logs.output
            )) 