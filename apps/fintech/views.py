from rest_framework import viewsets
from .models import User, Category, Account, Transaction, Credit, Expense
from .serializers import (
    UserSerializer,
    AccountSerializer,
    TransactionSerializer,
    CreditSerializer
)


import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils import timezone  
from .pagination import CustomOrderPagination
from .serializers import CreditDetailSerializer, CreditSerializer, TransactionSerializer
from .models import User, Credit, Transaction, Expense, AccountMethodAmount
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class CreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer

# class ExpenseViewSet(viewsets.ModelViewSet):
#     queryset = Expense.objects.all()
#     serializer_class = ExpenseSerializer




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

class CreditsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        start_date = parse_date(request.data.get('start_date'))
        end_date = parse_date(request.data.get('end_date'))

        if not start_date or not end_date:
            return Response({"error": "start_date y end_date son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar los créditos creados en el período
        credits = Credit.objects.filter(created_at__range=[start_date, end_date]).order_by('created_at')

        # Instanciar el paginador
        paginator = CustomOrderPagination()

        # Aplicar paginación a los resultados
        paginated_credits = paginator.paginate_queryset(credits, request)

        # Serializar los créditos paginados
        serializer = CreditSerializer(paginated_credits, many=True)

        # Devolver los datos paginados
        return paginator.get_paginated_response(serializer.data)


class PendingCreditsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        start_date = parse_date(request.data.get('start_date'))
        end_date = parse_date(request.data.get('end_date'))

        if not start_date or not end_date:
            return Response({"error": "start_date y end_date son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar los créditos con saldo pendiente en el período
        credits = Credit.objects.filter(pending_amount__gt=0, created_at__range=[start_date, end_date])

        # Instanciar el paginador
        paginator = CustomOrderPagination()

        # Aplicar paginación a los resultados
        paginated_credits = paginator.paginate_queryset(credits, request)

        # Serializar los créditos paginados
        serializer = CreditSerializer(paginated_credits, many=True)

        # Devolver los datos paginados
        return paginator.get_paginated_response(serializer.data)

# Vista para obtener transacciones en un período
class TransactionsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        start_date = parse_date(request.data.get('start_date'))
        end_date = parse_date(request.data.get('end_date'))

        if not start_date or not end_date:
            return Response({"error": "start_date y end_date son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar las transacciones en el período
        transactions = Transaction.objects.filter(date__range=[start_date, end_date])

        # Usamos el serializer para todos los datos
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Vista para obtener clientes con morosidad
class ClientsWithDefaultAPIView(APIView):
    def post(self, request, *args, **kwargs):
        credits = Credit.objects.filter(
            morosidad_level__in=['mild_default', 'moderate_default', 'severe_default', 'recurrent_default', 'critical_default']
        ).distinct('client')

        # Usamos el CreditSerializer para serializar todos los datos
        serializer = CreditSerializer(credits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Vista para obtener créditos de productos en un período
class ProductCreditsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        start_date = parse_date(request.data.get('start_date'))
        end_date = parse_date(request.data.get('end_date'))

        if not start_date or not end_date:
            return Response({"error": "start_date y end_date son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar los créditos de productos en el período
        credits = Credit.objects.filter(credit_type='personal', created_at__range=[start_date, end_date])

        # Usamos el CreditSerializer para serializar todos los datos
        serializer = CreditSerializer(credits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreditDetailAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Obtener el UUID del crédito desde el cuerpo de la solicitud
        credit_uuid = request.data.get('credit_id')
        print(f"Recibido credit_uuid desde el cuerpo: {credit_uuid}")  # Verificar que se recibe correctamente

        # Verificar que el UUID es válido
        try:
            credit_uuid = uuid.UUID(credit_uuid)
        except (ValueError, TypeError):
            return Response({"error": "ID de crédito no válido o no proporcionado."}, status=status.HTTP_400_BAD_REQUEST)

          # Consultar el crédito usando el UUID
        credit = get_object_or_404(Credit, uid=credit_uuid)
        print(f"Crédito encontrado: {credit}")

        # Obtener el cliente asociado al crédito
        client = credit.client
        print(f"Cliente asociado: {client}")

        # Serializar los detalles del crédito y sus abonos
        serializer = CreditDetailSerializer(credit)
        print(f"Datos serializados del crédito: {serializer.data}")

        # Devolver los datos tal como están, en formato JSON crudo
        return Response(serializer.data, status=status.HTTP_200_OK)

class FinancialCreditsAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Obtener las fechas del cuerpo
        start_date = parse_date(request.data.get('start_date'))
        end_date = parse_date(request.data.get('end_date'))

        if not start_date or not end_date:
            return Response({"error": "start_date y end_date son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar los créditos financieros en el período
        credits = Credit.objects.filter(credit_type='financial_product', created_at__range=[start_date, end_date])

        # Instanciar el paginador
        paginator = CustomOrderPagination()

        # Aplicar paginación a los resultados
        paginated_credits = paginator.paginate_queryset(credits, request)

        # Usar el serializer para todos los datos
        serializer = CreditSerializer(paginated_credits, many=True)

        # Devolver los datos paginados
        return paginator.get_paginated_response(serializer.data)