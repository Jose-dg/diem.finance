import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.fintech.models import Credit, Transaction, CategoryType, Credit, Expense, AccountMethodAmount
from apps.fintech.serializers import CreditSerializer, CreditSimpleSerializer, TransactionSerializer
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.db.models import Sum, Count, F
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.db.models.functions import Trunc
from pytz import timezone  # Importante para definir la zona horaria

# Vista para obtener clientes con morosidad
class ClientsWithDefaultAPIView(APIView):
    def post(self, request, *args, **kwargs):
        credits = Credit.objects.filter(
            morosidad_level__in=['mild_default', 'moderate_default', 'severe_default', 'recurrent_default', 'critical_default']
        ).distinct('user')

        # Usamos el CreditSerializer para serializar todos los datos
        serializer = CreditSerializer(credits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TransactionsAPIView(APIView):
    """
    Vista para obtener las transacciones dentro de un rango de fechas.
    """

    def post(self, request, *args, **kwargs):
        start_date = parse_date(request.data.get('start_date'))
        end_date = parse_date(request.data.get('end_date'))

        if not start_date or not end_date:
            return Response({"error": "start_date y end_date son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener todas las transacciones dentro del rango de fechas
        transactions = Transaction.objects.filter(
            date__range=[start_date, end_date]
        ).order_by('-date')

        return Response(TransactionSerializer(transactions, many=True).data, status=status.HTTP_200_OK)

class CreditsAPIView(APIView):

    def post(self, request, *args, **kwargs):
        start_date = parse_date(request.data.get('start_date'))
        end_date = parse_date(request.data.get('end_date'))

        if not start_date or not end_date:
            return Response({"error": "start_date y end_date son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener todos los créditos dentro del rango de fechas
        all_credits = Credit.objects.filter(created_at__range=[start_date, end_date])

        # Filtrar créditos con estado "pending"
        pending_credits = all_credits.filter(state="pending").order_by('-created_at')
        
        # Obtener hasta dos créditos con estado "completed"
        completed_credits = all_credits.filter(state="completed").order_by('-created_at')[:2]

        # Combinar ambos queryset
        combined_credits = list(pending_credits) + list(completed_credits)

        return Response(CreditSerializer(combined_credits, many=True).data)

# class SortedCreditsByLabelAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         from datetime import datetime, time
#         from django.utils.timezone import make_aware

#         start_raw = request.data.get('start_date')
#         end_raw = request.data.get('end_date')

#         if not start_raw or not end_raw:
#             return Response(
#                 {"error": "start_date and end_date are required."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         start_date = make_aware(datetime.combine(parse_date(start_raw), time.min))
#         end_date = make_aware(datetime.combine(parse_date(end_raw), time.max))

#         credits = Credit.objects.filter(
#             created_at__range=[start_date, end_date],
#             state="pending"
#         ).select_related('user__label').order_by(
#             F('user__label__name').asc(nulls_last=True),
#             '-created_at'
#         )

#         return Response(CreditSimpleSerializer(credits, many=True).data)

class SortedCreditsByLabelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        from datetime import datetime, time
        from django.utils.timezone import make_aware
        from django.db.models import F

        start_raw = request.data.get('start_date')
        end_raw = request.data.get('end_date')

        if not start_raw or not end_raw:
            return Response(
                {"error": "start_date and end_date are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        start_date = make_aware(datetime.combine(parse_date(start_raw), time.min))
        end_date = make_aware(datetime.combine(parse_date(end_raw), time.max))

        credits = Credit.objects.filter(
            created_at__range=[start_date, end_date],
            state="pending"
        ).select_related(
            'user__label', 'periodicity'
        ).order_by(
            F('periodicity__days').asc(nulls_last=True),
            F('user__label__name').asc(nulls_last=True),
            '-created_at'
        )

        return Response(CreditSimpleSerializer(credits, many=True).data)

class FinanceView(APIView):
    def post(self, request):
        try:
            # Validar datos requeridos
            required_fields = ['start_date', 'end_date']
            missing_fields = [field for field in required_fields if not request.data.get(field)]

            if missing_fields:
                return Response(
                    {
                        "error": f"Los siguientes campos son requeridos: {', '.join(missing_fields)}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Obtener fechas del request
            current_start_date = datetime.strptime(request.data['start_date'], '%Y-%m-%d')
            current_end_date = datetime.strptime(request.data['end_date'], '%Y-%m-%d')

            # Convertir a fechas aware utilizando la zona horaria de Django
            current_start_date = timezone.make_aware(current_start_date)
            current_end_date = timezone.make_aware(current_end_date)

            # Calcular periodicidad automáticamente
            periodicity_days = (current_end_date - current_start_date).days

            # Calcular las fechas del periodo anterior
            previous_start_date = current_start_date - timedelta(days=periodicity_days)
            previous_end_date = current_end_date - timedelta(days=periodicity_days)

            # -------------------- PERIODO ACTUAL --------------------

            current_income = AccountMethodAmount.objects.filter(
                transaction__transaction_type='income',
                transaction__date__range=[current_start_date, current_end_date]
            ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

            current_expense = Expense.objects.filter(
                date__range=[current_start_date, current_end_date]
            ).aggregate(Sum('amount'))['amount__sum'] or 0

            current_remaining = current_income - current_expense

            current_loans = Credit.objects.filter(
                first_date_payment__range=[current_start_date, current_end_date]
            ).aggregate(Sum('price'))['price__sum'] or 0

            current_receivables = Credit.objects.filter(
                first_date_payment__range=[current_start_date, current_end_date],
                pending_amount__gt=0
            ).aggregate(Sum('pending_amount'))['pending_amount__sum'] or 0

            current_earnings = Credit.objects.filter(
                first_date_payment__range=[current_start_date, current_end_date]
            ).aggregate(total=Sum('earnings'))['total'] or 0

            # -------------------- PERIODO ANTERIOR --------------------

            previous_income = AccountMethodAmount.objects.filter(
                transaction__transaction_type='income',
                transaction__date__range=[previous_start_date, previous_end_date]
            ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

            previous_expense = Expense.objects.filter(
                date__range=[previous_start_date, previous_end_date]
            ).aggregate(Sum('amount'))['amount__sum'] or 0

            previous_remaining = previous_income - previous_expense

            previous_loans = Credit.objects.filter(
                first_date_payment__range=[previous_start_date, previous_end_date]
            ).aggregate(Sum('price'))['price__sum'] or 0

            previous_receivables = Credit.objects.filter(
                first_date_payment__range=[previous_start_date, previous_end_date],
                pending_amount__gt=0
            ).aggregate(Sum('pending_amount'))['pending_amount__sum'] or 0

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

class SellerChartDataAPIView(APIView):
    # permission_classes = [IsAuthenticated]  # Desactivado temporalmente

    def post(self, request):
        # Obtener rango de fechas desde el body (últimos 90 días por defecto)
        range_days = int(request.data.get("range", 90))
        seller_id = request.data.get("seller_id")
        subcategory_id = request.data.get("subcategory_id")

        end_date = now().date()
        start_date = end_date - timedelta(days=range_days)

        credit_filters = {'created_at__date__range': (start_date, end_date)}
        if seller_id:
            credit_filters['seller_id'] = seller_id
        if subcategory_id:
            credit_filters['subcategory_id'] = subcategory_id

        credit_qs = (
            Credit.objects.filter(**credit_filters)
            .annotate(date=Trunc('created_at', kind='day', tzinfo=timezone('America/Bogota')))
            .values('date')
            .annotate(
                credits=Count('id'),
                earnings=Sum('earnings'),
            )
        )

        payment_filters = {'transaction__date__date__range': (start_date, end_date)}
        if seller_id:
            payment_filters['credit__seller_id'] = seller_id
        if subcategory_id:
            payment_filters['credit__subcategory_id'] = subcategory_id

        payment_qs = (
            AccountMethodAmount.objects.filter(**payment_filters)
            .annotate(date=Trunc('transaction__date', kind='day', tzinfo=timezone('America/Bogota')))
            .values('date')
            .annotate(
                payments=Sum('amount_paid')
            )
        )

        # Unificar resultados en un solo diccionario agrupado por fecha
        data_dict = {}

        for row in credit_qs:
            key = row['date']
            data_dict.setdefault(key, {'date': key, 'credits': 0, 'payments': 0, 'earnings': 0})
            data_dict[key]['credits'] += row['credits']
            data_dict[key]['earnings'] += float(row['earnings'] or 0)

        for row in payment_qs:
            key = row['date']
            data_dict.setdefault(key, {'date': key, 'credits': 0, 'payments': 0, 'earnings': 0})
            data_dict[key]['payments'] += float(row['payments'] or 0)

        # Convertir a lista ordenada por fecha
        data = sorted(data_dict.values(), key=lambda x: x['date'])
        return Response(data)


# class SellerChartDataAPIView(APIView):
#     # permission_classes = [IsAuthenticated]  # Desactivado temporalmente

#     def post(self, request):
#         # Obtener rango de fechas desde el body (últimos 90 días por defecto)
#         range_days = int(request.data.get("range", 90))
#         seller_id = request.data.get("seller_id")
#         subcategory_id = request.data.get("subcategory_id")

#         end_date = now().date()
#         start_date = end_date - timedelta(days=range_days)

#         credit_filters = {'created_at__date__range': (start_date, end_date)}
#         if seller_id:
#             credit_filters['seller_id'] = seller_id
#         if subcategory_id:
#             credit_filters['subcategory_id'] = subcategory_id

#         credit_qs = (
#             Credit.objects.filter(**credit_filters)
#             .annotate(date=TruncDate('created_at'))
#             .values('date')
#             .annotate(
#                 credits=Count('id'),
#                 earnings=Sum('earnings'),
#             )
#         )

#         payment_filters = {'transaction__date__date__range': (start_date, end_date)}
#         if seller_id:
#             payment_filters['credit__seller_id'] = seller_id
#         if subcategory_id:
#             payment_filters['credit__subcategory_id'] = subcategory_id

#         payment_qs = (
#             AccountMethodAmount.objects.filter(**payment_filters)
#             .annotate(date=TruncDate('transaction__date'))
#             .values('date')
#             .annotate(
#                 payments=Sum('amount_paid')
#             )
#         )

#         # Unificar resultados en un solo diccionario agrupado por fecha
#         data_dict = {}

#         for row in credit_qs:
#             key = row['date']
#             data_dict.setdefault(key, {'date': key, 'credits': 0, 'payments': 0, 'earnings': 0})
#             data_dict[key]['credits'] += row['credits']
#             data_dict[key]['earnings'] += float(row['earnings'] or 0)

#         for row in payment_qs:
#             key = row['date']
#             data_dict.setdefault(key, {'date': key, 'credits': 0, 'payments': 0, 'earnings': 0})
#             data_dict[key]['payments'] += float(row['payments'] or 0)

#         # Convertir a lista ordenada por fecha
#         data = sorted(data_dict.values(), key=lambda x: x['date'])
#         return Response(data)


    # permission_classes = [IsAuthenticated]  # Desactivado temporalmente

    def post(self, request):
        # Obtener rango de fechas desde el body (últimos 90 días por defecto)
        range_days = int(request.data.get("range", 90))
        end_date = now().date()
        start_date = end_date - timedelta(days=range_days)

        # Créditos entregados por vendedor
        credit_qs = (
            Credit.objects.filter(created_at__date__range=(start_date, end_date))
            .annotate(date=TruncDate('created_at'))
            .values('date', 'seller__user__first_name', 'subcategory__name')
            .annotate(
                credits=Count('id'),
                earnings=Sum('earnings'),
            )
        )

        # Pagos realizados por vendedor (corregido: usar transaction__date en lugar de created_at)
        payment_qs = (
            AccountMethodAmount.objects.filter(transaction__date__date__range=(start_date, end_date))
            .annotate(date=TruncDate('transaction__date'))
            .values('date', 'credit__seller__user__first_name', 'credit__subcategory__name')
            .annotate(
                payments=Sum('amount_paid')
            )
        )

        # Unificar resultados en un solo diccionario agrupado por fecha, vendedor y tipo de crédito
        data_dict = {}

        for row in credit_qs:
            key = (row['date'], row['seller__user__first_name'], row['subcategory__name'])
            data_dict.setdefault(key, {'date': row['date'], 'seller': row['seller__user__first_name'], 'credit_type': row['subcategory__name'], 'credits': 0, 'payments': 0, 'earnings': 0})
            data_dict[key]['credits'] = row['credits']
            data_dict[key]['earnings'] = float(row['earnings'] or 0)

        for row in payment_qs:
            key = (row['date'], row['credit__seller__user__first_name'], row['credit__subcategory__name'])
            data_dict.setdefault(key, {'date': row['date'], 'seller': row['credit__seller__user__first_name'], 'credit_type': row['credit__subcategory__name'], 'credits': 0, 'payments': 0, 'earnings': 0})
            data_dict[key]['payments'] = float(row['payments'] or 0)

        # Convertir a lista ordenada por fecha
        data = sorted(data_dict.values(), key=lambda x: x['date'])
        return Response(data)