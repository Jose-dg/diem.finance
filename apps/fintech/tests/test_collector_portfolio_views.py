from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.fintech.models import (
    Account,
    Category,
    Credit,
    Currency,
    Installment,
    Periodicity,
    Role,
    Seller,
    SubCategory,
)


User = get_user_model()


class MyCollectorPortfolioViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.collector_user = User.objects.create_user(
            username='collector',
            email='collector@example.com',
            password='testpass123',
        )
        role = Role.objects.create(name='collector')
        self.seller = Seller.objects.create(
            role=role,
            user=self.collector_user,
        )

        self.borrower = User.objects.create_user(
            username='borrower',
            email='borrower@example.com',
            password='testpass123',
            first_name='Ana',
            last_name='Garcia',
        )
        self.currency = Currency.objects.create(
            id_currency='COP',
            currency='Peso',
            exchange_rate=Decimal('1.0000'),
        )
        self.periodicity = Periodicity.objects.create(
            name='Daily',
            days=1,
        )
        self.payment_account = Account.objects.create(
            name='Caja',
            account_number='123',
            balance=Decimal('0.00'),
            currency=self.currency,
        )
        category = Category.objects.create(name='Creditos')
        self.subcategory = SubCategory.objects.create(
            name='Prestamo',
            category=category,
        )

        today = timezone.now().date()
        self.credit = Credit.objects.create(
            registered_by=self.collector_user,
            seller=self.seller,
            user=self.borrower,
            subcategory=self.subcategory,
            cost=Decimal('80000.00'),
            price=Decimal('100000.00'),
            currency=self.currency,
            first_date_payment=today,
            second_date_payment=today,
            credit_days=30,
            periodicity=self.periodicity,
            payment=self.payment_account,
            pending_amount=Decimal('100000.00'),
        )
        self.installment = Installment.objects.create(
            credit=self.credit,
            number=1,
            due_date=today,
            amount=Decimal('100000.00'),
            amount_paid=Decimal('0.00'),
            remaining_amount=Decimal('100000.00'),
            status='pending',
        )

    def test_my_portfolio_returns_authenticated_seller_schedule(self):
        self.client.force_authenticate(user=self.collector_user)

        response = self.client.get(reverse('collector-my-portfolio'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['seller']['id'], self.seller.id)
        self.assertEqual(response.data['summary']['total_installments_pending'], 1)

        date_key = self.installment.due_date.isoformat()
        self.assertIn(date_key, response.data['schedule'])
        self.assertEqual(response.data['schedule'][date_key][0]['installment_id'], self.installment.id)
        self.assertEqual(response.data['schedule'][date_key][0]['due_date'], date_key)
        self.assertEqual(response.data['schedule'][date_key][0]['credit_periodicity_name'], 'Daily')
        self.assertEqual(response.data['schedule'][date_key][0]['credit_periodicity_days'], 1)
        self.assertEqual(response.data['schedule'][date_key][0]['total_due'], '100000.00')
        self.assertEqual(
            response.data['summary']['installments_by_periodicity'],
            [
                {
                    'periodicity_days': 1,
                    'periodicity_name': 'Daily',
                    'installments_count': 1,
                    'total_remaining_amount': '100000.00',
                    'total_due': '100000.00',
                }
            ],
        )

    def test_my_portfolio_rejects_user_without_seller_profile(self):
        user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('collector-my-portfolio'))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['detail'],
            'El usuario autenticado no tiene un perfil de cobrador asociado.',
        )
