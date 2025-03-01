import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.fintech.serializers import CreditSerializer, TransactionSerializer
from apps.fintech.models import AccountMethodAmount, CategoryType, Credit, Expense, Transaction
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.db.models import Sum, Count, F
from datetime import datetime, timedelta

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
# class CreditsAPIView(APIView):

#     def post(self, request, *args, **kwargs):
#         # Obtener las fechas del cuerpo
#         start_date = parse_date(request.data.get('start_date'))
#         end_date = parse_date(request.data.get('end_date'))

#         if not start_date or not end_date:
#             return Response({"error": "start_date y end_date son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

#         # Filtrar los créditos financieros en el período
#         credits = Credit.objects.filter(created_at__range=[start_date, end_date]).order_by('-created_at')

#         serialized_data = []
#         for credit in credits:
#             try:
#                 serialized_data.append(CreditSerializer(credit).data)
#             except Exception as e:
#                 print(f"Error serializing credit {credit.id}: {str(e)}")
        
#         return Response(serialized_data)
class CreditsAPIView(APIView):

    def post(self, request, *args, **kwargs):
        # Obtener las fechas del cuerpo
        start_date = parse_date(request.data.get('start_date'))
        end_date = parse_date(request.data.get('end_date'))

        if not start_date or not end_date:
            return Response({"error": "start_date y end_date son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar los créditos financieros en el período con state="pending"
        credits = Credit.objects.filter(
            created_at__range=[start_date, end_date],
            state="pending"  # Filtro agregado
        ).order_by('-created_at')

        serialized_data = []
        for credit in credits:
            try:
                serialized_data.append(CreditSerializer(credit).data)
            except Exception as e:
                print(f"Error serializing credit {credit.uid}: {str(e)}")  # Cambié 'id' por 'uid' ya que Credit usa UUID
        
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
            current_start_date = datetime.timezone.make_aware(current_start_date)
            current_end_date = datetime.timezone.make_aware(current_end_date)

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
        
class CreditsVsRecaudosChart(APIView):
    def post(self, request):
        """
        Endpoint para obtener la suma de créditos y recaudos por día, filtrados por un rango de fechas.
        """
        # 📌 Obtener fechas de la consulta o asignar valores predeterminados
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        # 📌 Si no se envían fechas, usamos últimos 30 días como predeterminado
        if not start_date or not end_date:
            end_date = now().date()
            start_date = end_date - timedelta(days=30)
        else:
            # Convertir los parámetros a formato de fecha
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            except ValueError:
                return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}, status=400)

        # 📌 Validar que `start_date` no sea mayor que `end_date`
        if start_date > end_date:
            return Response({"error": "La fecha de inicio no puede ser mayor que la fecha final."}, status=400)

        # 📌 Créditos por día (suma y cantidad)
        credits_per_day = (
            Credit.objects
            .filter(created_at__date__range=[start_date, end_date])
            .values('created_at__date')
            .annotate(
                total_credits=Sum('price'),
                count_credits=Count('id'),
                total_earnings=Sum(F('price') - F('cost')))
            )

        recaudos_per_day = (
            AccountMethodAmount.objects
            .filter(transaction__transaction_type="income", transaction__date__range=[start_date, end_date])
            .values('transaction__date')
            .annotate(total_recaudos=Sum('amount_paid'), count_recaudos=Count('id'))
        )
        

        # Filtering expenses for 'Operational Expenses' by uid
        operational_expenses_type = CategoryType.objects.get(uid="17f1ad39-eec9-400e-ab03-8a47cd7f68d9")
        expenses_per_day = (
            Expense.objects
            .filter(subcategory__category__category_type=operational_expenses_type, created_at__date__range=[start_date, end_date])
            .values('created_at__date')
            .annotate(total_expenses=Sum('amount'))
        )

        # 📌 Formatear datos en estructura esperada
        chart_data = []
        for credit in credits_per_day:
            date = credit['created_at__date']
            recaudo = next((item for item in recaudos_per_day if item.get('transaction__date') == date), {"total_recaudos": 0, "count_recaudos": 0})
            expense = next((item for item in expenses_per_day if item['created_at__date'] == date), {"total_expenses": 0})

            chart_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "total_credits": float(credit['total_credits']),
                "count_credits": credit['count_credits'],
                "total_earnings": float(credit['total_earnings']),
                "total_recaudos": float(recaudo["total_recaudos"]) if recaudo["total_recaudos"] else 0,
                "count_recaudos": recaudo["count_recaudos"],
                "total_expenses": float(expense["total_expenses"]) if expense["total_expenses"] else 0
            })

        return Response(chart_data)

