from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.fintech.serializers import CreditSerializer, TransactionSerializer
from apps.fintech.models import Credit, Transaction
from django.utils.dateparse import parse_date

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
        ).distinct('user')

        # Usamos el CreditSerializer para serializar todos los datos
        serializer = CreditSerializer(credits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Vista para obtener creditos de un periodo
class CreditsAPIView(APIView):

    def post(self, request, *args, **kwargs):
        # Obtener las fechas del cuerpo
        start_date = parse_date(request.data.get('start_date'))
        end_date = parse_date(request.data.get('end_date'))

        if not start_date or not end_date:
            return Response({"error": "start_date y end_date son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar los créditos financieros en el período
        credits = Credit.objects.filter(created_at__range=[start_date, end_date]).order_by('-created_at')

        serialized_data = []
        for credit in credits:
            try:
                serialized_data.append(CreditSerializer(credit).data)
            except Exception as e:
                print(f"Error serializing credit {credit.id}: {str(e)}")
        
        return Response(serialized_data)


#Vista para resumen

class FinanceView(APIView):
    def post(self, request):
        try:
            # Validar datos requeridos

            required_fields = ['start_date', 'end_date', 'periodicity_days']
            missing_fields = [field for field in required_fields if not request.data.get(field)]
        
            if missing_fields:
                return Response(
                    {
                        "error": f"Los siguientes campos son requeridos: {', '.join(missing_fields)}"
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Obtener fechas del request
            current_start_date = request.data.get('start_date')
            current_end_date = request.data.get('end_date')
            periodicity_days = int(request.data.get('periodicity_days', 30))

            # Convertir las fechas de cadena a objetos datetime
            current_start_date = datetime.strptime(current_start_date, '%Y-%m-%d')
            current_end_date = datetime.strptime(current_end_date, '%Y-%m-%d')

            # Convertir a fechas aware utilizando la zona horaria de Django
            current_start_date = timezone.make_aware(current_start_date)
            current_end_date = timezone.make_aware(current_end_date)

            # Calcular las fechas del periodo anterior
            previous_start_date = current_start_date - timedelta(days=periodicity_days)
            previous_end_date = current_end_date - timedelta(days=periodicity_days)

            # -------------------- PERIODO ACTUAL --------------------

            # Ingresos (abonos) en el periodo actual
            current_income = AccountMethodAmount.objects.filter(
                transaction__transaction_type='income',
                transaction__date__range=[current_start_date, current_end_date]
            ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

            # Gastos en el periodo actual
            current_expense = Expense.objects.filter(
                date__range=[current_start_date, current_end_date]
            ).aggregate(Sum('amount'))['amount__sum'] or 0

            # Remaining en el periodo actual
            current_remaining = current_income - current_expense

            # Créditos dados en el periodo actual
            current_loans = Credit.objects.filter(
                first_date_payment__range=[current_start_date, current_end_date]
            ).aggregate(Sum('price'))['price__sum'] or 0

            # Saldos pendientes (receivables) en el periodo actual
            current_receivables = Credit.objects.filter(
                first_date_payment__range=[current_start_date, current_end_date],
                pending_amount__gt=0
            ).aggregate(Sum('pending_amount'))['pending_amount__sum'] or 0

            # Ganancias (earnings) en el periodo actual
            current_earnings = Credit.objects.filter(
                first_date_payment__range=[current_start_date, current_end_date]
            ).aggregate(total=Sum('earnings'))['total'] or 0

            # -------------------- PERIODO ANTERIOR --------------------

            # Ingresos del periodo anterior
            previous_income = AccountMethodAmount.objects.filter(
                transaction__transaction_type='income',
                transaction__date__range=[previous_start_date, previous_end_date]
            ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

            # Gastos del periodo anterior
            previous_expense = Expense.objects.filter(
                date__range=[previous_start_date, previous_end_date]
            ).aggregate(Sum('amount'))['amount__sum'] or 0

            previous_remaining = previous_income - previous_expense

            # Créditos del periodo anterior
            previous_loans = Credit.objects.filter(
                first_date_payment__range=[previous_start_date, previous_end_date]
            ).aggregate(Sum('price'))['price__sum'] or 0

            # Receivables del periodo anterior
            previous_receivables = Credit.objects.filter(
                first_date_payment__range=[previous_start_date, previous_end_date],
                pending_amount__gt=0
            ).aggregate(Sum('pending_amount'))['pending_amount__sum'] or 0

            # Earnings del periodo anterior
            previous_earnings = Credit.objects.filter(
                first_date_payment__range=[previous_start_date, previous_end_date]
            ).aggregate(total=Sum('earnings'))['total'] or 0

            # -------------------- CAMBIOS PORCENTUALES --------------------

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
                    'income': float(current_income),
                    'expense': float(current_expense),
                    'remaining': float(current_remaining),
                    'loans': float(current_loans),
                    'receivables': float(current_receivables),
                    'earnings': float(current_earnings),
                },
                'previous': {
                    'income': float(previous_income),
                    'expense': float(previous_expense),
                    'remaining': float(previous_remaining),
                    'loans': float(previous_loans),
                    'receivables': float(previous_receivables),
                    'earnings': float(previous_earnings),
                },
                'change': {
                    'income_change': round(income_change, 2),
                    'expense_change': round(expense_change, 2),
                    'remaining_change': round(remaining_change, 2),
                    'loans_change': round(loans_change, 2),
                    'receivables_change': round(receivables_change, 2),
                    'earnings_change': round(earnings_change, 2),
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


