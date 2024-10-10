from rest_framework import viewsets
from .models import User, Account, Transaction, Credit, Expense
from .serializers import (
    UserSerializer, 
    AccountSerializer, 
    TransactionSerializer, 
    CreditSerializer )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils import timezone  
from .serializers import CreditSerializer, TransactionSerializer
from .models import User, Credit, Transaction, Expense, AccountMethodAmount
from django.utils.dateparse import parse_date

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class CreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer

# Vista para obtener resumen general
class FinanceView(APIView):
    def post(self, request):
        # Obtén las fechas de inicio y fin del periodo actual desde el cuerpo de la solicitud
        current_start_date = request.data.get('start_date')
        current_end_date = request.data.get('end_date')

        # Convertir las fechas de cadena a objetos datetime
        current_start_date = datetime.strptime(current_start_date, '%Y-%m-%d')
        current_end_date = datetime.strptime(current_end_date, '%Y-%m-%d')

        # Convertir a fechas aware utilizando la zona horaria de Django
        current_start_date = timezone.make_aware(current_start_date)
        current_end_date = timezone.make_aware(current_end_date)

        # Obtener la periodicidad en días desde el cuerpo de la solicitud
        periodicity_days = int(request.data.get('periodicity_days', 30))  # Default a 30 días si no se proporciona

        # Calcular las fechas del periodo anterior usando la periodicidad
        previous_start_date = current_start_date - timedelta(days=periodicity_days)
        previous_end_date = current_end_date - timedelta(days=periodicity_days)

        # -------------------- PERIODO ACTUAL --------------------

        # Ingresos (abonos) en el periodo actual
        current_income = AccountMethodAmount.objects.filter(
            transaction__transaction_type='income',
            transaction__date__range=[current_start_date, current_end_date]
        ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0  # Sumatoria de los abonos (amount_paid)

        # Gastos en el periodo actual
        current_expense = Expense.objects.filter(
            date__range=[current_start_date, current_end_date]
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        # Remaining en el periodo actual
        current_remaining = current_income - current_expense

        # Calcular la sumatoria de los créditos dados en el periodo actual
        current_loans = Credit.objects.filter(
            first_date_payment__range=[current_start_date, current_end_date]
        ).aggregate(Sum('price'))['price__sum'] or 0

        # Calcular la sumatoria de los saldos pendientes (receivables) en el periodo actual
        current_receivables = Credit.objects.filter(
            first_date_payment__range=[current_start_date, current_end_date],
            pending_amount__gt=0
        ).aggregate(Sum('pending_amount'))['pending_amount__sum'] or 0

        # Ganancias (earnings) en el periodo actual
        current_earnings = Credit.objects.filter(
            first_date_payment__range=[current_start_date, current_end_date]
        ).aggregate(total=Sum('earnings'))['total'] or 0

        # -------------------- PERIODO ANTERIOR --------------------

        # Calcular los valores para el periodo anterior
        previous_income = AccountMethodAmount.objects.filter(
            transaction__transaction_type='income',
            transaction__date__range=[previous_start_date, previous_end_date]
        ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

        previous_expense = Expense.objects.filter(
            date__range=[previous_start_date, previous_end_date]
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        previous_remaining = previous_income - previous_expense

        # Calcular la sumatoria de los créditos dados en el periodo anterior
        previous_loans = Credit.objects.filter(
            first_date_payment__range=[previous_start_date, previous_end_date]
        ).aggregate(Sum('price'))['price__sum'] or 0

        # Calcular la sumatoria de los saldos pendientes (receivables) en el periodo anterior
        previous_receivables = Credit.objects.filter(
            first_date_payment__range=[previous_start_date, previous_end_date],
            pending_amount__gt=0
        ).aggregate(Sum('pending_amount'))['pending_amount__sum'] or 0

         # Ganancias (earnings) en el periodo anterior
        previous_earnings = Credit.objects.filter(
            first_date_payment__range=[previous_start_date, previous_end_date]
        ).aggregate(total=Sum('earnings'))['total'] or 0

        # -------------------- CAMBIOS PORCENTUALES --------------------


        # Calcular el porcentaje de cambio
        def calculate_percentage_change(current, previous):
            if previous == 0:
                return 100 if current > 0 else 0
            return ((current - previous) / previous) * 100

        income_change = calculate_percentage_change(current_income, previous_income)
        expense_change = calculate_percentage_change(current_expense, previous_expense)
        remaining_change = calculate_percentage_change(current_remaining, previous_remaining)
        loans_change = calculate_percentage_change(current_loans, previous_loans)
        receivables_change = calculate_percentage_change(current_receivables, previous_receivables)
        earnings_change = calculate_percentage_change(current_earnings, previous_earnings)

        return Response({
            'current': {
                'income': current_income,
                'expense': current_expense,
                'remaining': current_remaining,
                'loans': current_loans,
                'receivables': current_receivables,
                 'earnings': float(current_earnings),
            },
            'previous': {
                'income': previous_income,
                'expense': previous_expense,
                'remaining': previous_remaining,
                'loans': previous_loans,
                'receivables': previous_receivables,
                'earnings': float(previous_earnings),
            },
            'change': {
                'income_change': income_change,
                'expense_change': expense_change,
                'remaining_change': remaining_change,
                'loans_change': loans_change,
                'receivables_change': receivables_change,
                'earnings_change': earnings_change,
            }
        }, status=status.HTTP_200_OK)


   
    def post(self, request, *args, **kwargs):
        # Obtener las fechas del cuerpo
        start_date = parse_date(request.data.get('start_date'))
        end_date = parse_date(request.data.get('end_date'))

        if not start_date or not end_date:
            return Response({"error": "start_date y end_date son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar los créditos financieros en el período
        credits = Credit.objects.filter(subcategory='financial_product', created_at__range=[start_date, end_date])

        # Instanciar el paginador
        paginator = CustomOrderPagination()

        # Aplicar paginación a los resultados
        paginated_credits = paginator.paginate_queryset(credits, request)

        # Usar el serializer para todos los datos
        serializer = CreditSerializer(paginated_credits, many=True)

        # Devolver los datos paginados
        return paginator.get_paginated_response(serializer.data)