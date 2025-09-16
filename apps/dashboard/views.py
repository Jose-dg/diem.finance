from collections import defaultdict
from apps.fintech.filter import CreditFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.utils.dateparse import parse_date
from django.utils.timezone import now, make_aware

from django.db.models import Sum
from django.db.models.functions import Trunc, TruncMonth

from django.utils import timezone
from datetime import datetime, timedelta, time
import pytz

from apps.fintech.models import Credit, Transaction, Expense, AccountMethodAmount
from apps.fintech.serializers import StandardResultsSetPagination
from apps.fintech.serializers import CreditSerializer, CreditFilterSerializer

# Import del servicio con manejo de errores
try:
    from apps.fintech.services.credit import CreditQueryService
except ImportError:
    print("⚠️ Error importando CreditQueryService, usando lógica directa")
    CreditQueryService = None

from apps.fintech.services.analytics import KPIService
from datetime import datetime

class FinanceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
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
            .annotate(date=Trunc('created_at', kind='day', tzinfo=pytz.timezone('America/Bogota')))
            .values('date')
            .annotate(
                credits=Sum('price'),  # ✅ suma total del valor de los créditos
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
            .annotate(date=Trunc('transaction__date', kind='day', tzinfo=pytz.timezone('America/Bogota')))
            .values('date')
            .annotate(
                payments=Sum('amount_paid')
            )
        )

        data_dict = {}

        for row in credit_qs:
            key = row['date']
            data_dict.setdefault(key, {'date': key, 'credits': 0, 'payments': 0, 'earnings': 0})
            data_dict[key]['credits'] += float(row['credits'] or 0)
            data_dict[key]['earnings'] += float(row['earnings'] or 0)

        for row in payment_qs:
            key = row['date']
            data_dict.setdefault(key, {'date': key, 'credits': 0, 'payments': 0, 'earnings': 0})
            data_dict[key]['payments'] += float(row['payments'] or 0)

        data = sorted(data_dict.values(), key=lambda x: x['date'])
        return Response(data)
    
class MonthlyChartDataAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Obtener parámetros del request
            range_months = int(request.data.get("months", 6))
            seller_id = request.data.get("seller_id")
            subcategory_id = request.data.get("subcategory_id")

            # Calcular fechas aware
            # tz = timezone("America/Bogota")
            tz = pytz.timezone("America/Bogota")
            end_date = make_aware(datetime.combine(now().date(), time.max), timezone=tz)
            start_date = make_aware(
                datetime.combine(end_date.date() - timedelta(days=range_months * 30), time.min),
                timezone=tz,
            )

            # Filtros para créditos
            credit_filters = {"created_at__range": (start_date, end_date)}
            if seller_id:
                credit_filters["seller_id"] = seller_id
            if subcategory_id:
                credit_filters["subcategory_id"] = subcategory_id

            credits = (
                Credit.objects.filter(**credit_filters)
                .annotate(month=TruncMonth("created_at", tzinfo=tz))
                .values("month")
                .annotate(
                    total_credit=Sum("price"),
                    earnings=Sum("earnings"),
                )
            )

            # Filtros para pagos
            payment_filters = {"transaction__date__range": (start_date, end_date)}
            if seller_id:
                payment_filters["credit__seller_id"] = seller_id
            if subcategory_id:
                payment_filters["credit__subcategory_id"] = subcategory_id

            payments = (
                AccountMethodAmount.objects.filter(**payment_filters)
                .annotate(month=TruncMonth("transaction__date", tzinfo=tz))
                .values("month")
                .annotate(
                    payments=Sum("amount_paid")
                )
            )

            # Agrupar datos por mes
            data_dict = defaultdict(lambda: {"month": "", "credits": 0, "payments": 0, "earnings": 0})

            for row in credits:
                month_str = row["month"].strftime("%Y-%m")
                data_dict[month_str]["month"] = month_str
                data_dict[month_str]["credits"] += float(row["total_credit"] or 0)
                data_dict[month_str]["earnings"] += float(row["earnings"] or 0)

            for row in payments:
                month_str = row["month"].strftime("%Y-%m")
                data_dict[month_str]["month"] = month_str
                data_dict[month_str]["payments"] += float(row["payments"] or 0)

            # Devolver los datos ordenados por mes
            data = sorted(data_dict.values(), key=lambda x: x["month"])
            return Response(data)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from datetime import datetime, timedelta
import json

from apps.fintech.models import Credit, Transaction, AccountMethodAmount
from apps.fintech.serializers import CreditSerializer
from apps.fintech.filter import CreditFilter
from apps.fintech.services.analytics import KPIService
from apps.fintech.services.credit import CreditQueryService

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

@method_decorator(csrf_exempt, name='dispatch')

class CreditsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get(self, request):
        """Endpoint para obtener créditos con filtros opcionales"""
        try:
            # Parámetros de consulta - primero de URL, luego de body
            start_date = request.GET.get('start_date') or request.data.get('start_date')
            end_date = request.GET.get('end_date') or request.data.get('end_date')
            status_filter = request.GET.get('status') or request.data.get('status')
            user_filter = request.GET.get('user') or request.data.get('user')
            
            print(f"🔍 CreditsAPIView - Usuario: {request.user.username}")
            print(f"🔍 Parámetros: start_date={start_date}, end_date={end_date}, status={status_filter}, user={user_filter}")
            print(f"🔍 Body data: {request.data}")
            
            # Validar fechas
            if start_date and end_date:
                try:
                    start_aware = datetime.strptime(start_date, '%Y-%m-%d')
                    end_aware = datetime.strptime(end_date, '%Y-%m-%d')
                except ValueError:
                    return Response(
                        {'error': 'Formato de fecha inválido. Use YYYY-MM-DD'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                # Usar CreditQueryService con filtro de fecha
                base_qs = CreditQueryService.get_user_credits_by_date_range(
                    request.user, 
                    start_aware.date(), 
                    end_aware.date()
                ).order_by('-created_at')
            else:
                # Sin filtro de fecha - obtener todos los créditos del usuario
                base_qs = CreditQueryService.get_user_credits(request.user).order_by('-created_at')
            
            # Log del tipo de usuario para debugging
            user_type = "super_admin" if request.user.is_superuser else \
                       "admin" if request.user.is_staff else \
                       "seller" if hasattr(request.user, 'seller_profile') else "client"
            print(f"🔍 Usuario {request.user.username} ({user_type}) - Créditos encontrados: {base_qs.count()}")
            
            # Filtros opcionales
            if status_filter:
                base_qs = base_qs.filter(status=status_filter)
                print(f"🔍 Filtro por status: {status_filter}")
            
            if user_filter:
                base_qs = base_qs.filter(user__username__icontains=user_filter)
                print(f"🔍 Filtro por usuario: {user_filter}")
            
            # Eager loading para optimizar consultas
            base_qs = base_qs.select_related(
                'user', 'seller', 'currency', 'periodicity', 'subcategory', 'payment'
            ).prefetch_related('payments', 'adjustments', 'installments')
            
            # Paginación
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(base_qs, request)
            
            if page is not None:
                serializer = CreditSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            
            serializer = CreditSerializer(base_qs, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            print(f"❌ Error en CreditsAPIView: {str(e)}")
            return Response(
                {'error': f'Error interno del servidor: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        """Endpoint para filtrar créditos con parámetros en el body (compatible con frontend)"""
        try:
            data = request.data
            print(f"🔍 CreditsAPIView POST - Usuario: {request.user.username}")
            print(f"🔍 Datos recibidos: {data}")
            
            # Extraer parámetros del body
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            status_filter = data.get('status')
            user_filter = data.get('user')
            
            print(f"🔍 Parámetros extraídos: start_date={start_date}, end_date={end_date}, status={status_filter}, user={user_filter}")
            
            # Validar fechas requeridas
            if not start_date or not end_date:
                return Response(
                    {'error': 'start_date y end_date son requeridos'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validar formato de fechas
            try:
                start_aware = datetime.strptime(start_date, '%Y-%m-%d')
                end_aware = datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return Response(
                    {'error': 'Formato de fecha inválido. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Usar CreditQueryService con filtro de fecha
            base_qs = CreditQueryService.get_user_credits_by_date_range(
                request.user, 
                start_aware.date(), 
                end_aware.date()
            ).order_by('-created_at')
            
            # Log del tipo de usuario para debugging
            user_type = "super_admin" if request.user.is_superuser else \
                       "admin" if request.user.is_staff else \
                       "seller" if hasattr(request.user, 'seller_profile') else "client"
            print(f"🔍 Usuario {request.user.username} ({user_type}) - Créditos encontrados: {base_qs.count()}")
            
            # Filtros opcionales
            if status_filter:
                base_qs = base_qs.filter(status=status_filter)
                print(f"🔍 Filtro por status: {status_filter}")
            
            if user_filter:
                base_qs = base_qs.filter(user__username__icontains=user_filter)
                print(f"🔍 Filtro por usuario: {user_filter}")
            
            # Eager loading para optimizar consultas
            base_qs = base_qs.select_related(
                'user', 'seller', 'currency', 'periodicity', 'subcategory', 'payment'
            ).prefetch_related('payments', 'adjustments', 'installments')
            
            # Paginación
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(base_qs, request)
            
            if page is not None:
                serializer = CreditSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            
            serializer = CreditSerializer(base_qs, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            print(f"❌ Error en CreditsAPIView POST: {str(e)}")
            return Response(
                {'error': f'Error interno del servidor: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _filter_and_respond(self, request, params):
        """Método auxiliar para filtrar y responder"""
        try:
            # 1) Validar fechas
            start_date = params.get('start_date')
            end_date = params.get('end_date')
            
            try:
                start_aware = datetime.strptime(start_date, '%Y-%m-%d')
                end_aware = datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                return Response(
                    {'error': 'Formato de fecha inválido. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 2) Usar CreditQueryService para obtener créditos según rol
            base_qs = CreditQueryService.get_user_credits_by_date_range(
                request.user, 
                start_aware.date(), 
                end_aware.date()
            ).order_by('-created_at')  # Agregar ordenamiento
            
            # Log del tipo de usuario para debugging
            user_type = "super_admin" if request.user.is_superuser else \
                       "admin" if request.user.is_staff else \
                       "seller" if hasattr(request.user, 'seller_profile') else "client"
            print(f"🔍 Usuario {request.user.username} ({user_type}) - Créditos encontrados: {base_qs.count()}")
            
            # 3) Filtros opcionales
            status_filter = params.get('status')
            if status_filter:
                base_qs = base_qs.filter(status=status_filter)
                print(f"🔍 Filtro por status: {status_filter}")
            
            user_filter = params.get('user')
            if user_filter:
                base_qs = base_qs.filter(user__username__icontains=user_filter)
                print(f"🔍 Filtro por usuario: {user_filter}")
            
            # 4) Eager loading para optimizar consultas
            base_qs = base_qs.select_related(
                'user', 'seller', 'currency', 'periodicity', 'subcategory', 'payment'
            ).prefetch_related('payments', 'adjustments', 'installments')
            
            # 5) Paginación
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(base_qs, request)
            
            if page is not None:
                serializer = CreditSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            
            serializer = CreditSerializer(base_qs, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            print(f"❌ Error en _filter_and_respond: {str(e)}")
            return Response(
                {'error': f'Error interno del servidor: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_exempt, name='dispatch')
class CreditFilterAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def post(self, request, *args, **kwargs):
        """Endpoint para filtrar créditos usando django-filter"""
        try:
            data = request.data
            print(f"🔍 CreditFilterAPIView - Usuario: {request.user.username}")
            print(f"🔍 Datos recibidos: {data}")
            
            # Crear filterset con los datos recibidos
            filterset = CreditFilter(data=data)
            
            if not filterset.is_valid():
                return Response(
                    {'error': 'Parámetros de filtro inválidos', 'details': filterset.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Usar CreditQueryService para obtener créditos según rol
            base_qs = CreditQueryService.get_user_credits(request.user).order_by('-created_at')  # Agregar ordenamiento
            
            # Log del tipo de usuario para debugging
            user_type = "super_admin" if request.user.is_superuser else \
                       "admin" if request.user.is_staff else \
                       "seller" if hasattr(request.user, 'seller_profile') else "client"
            print(f"🔍 Usuario {request.user.username} ({user_type}) - Créditos encontrados: {base_qs.count()}")
            
            # Aplicar filtros del filterset
            qs = filterset.qs
            
            # Eager loading para optimizar consultas
            qs = qs.select_related(
                'user', 'seller', 'currency', 'periodicity', 'subcategory', 'payment'
            ).prefetch_related('payments', 'adjustments', 'installments')
            
            # Paginación
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(qs, request)
            
            if page is not None:
                serializer = CreditSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            
            serializer = CreditSerializer(qs, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            print(f"❌ Error en CreditFilterAPIView: {str(e)}")
            return Response(
                {'error': f'Error interno del servidor: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_exempt, name='dispatch')
class CreditKPIView(APIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Endpoint para obtener KPIs de créditos"""
        try:
            # Parámetros de consulta
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            
            print(f"🔍 CreditKPIView - Usuario: {request.user.username}")
            print(f"🔍 Parámetros: start_date={start_date}, end_date={end_date}")
            
            # Validar fechas
            if not start_date or not end_date:
                return Response(
                    {'error': 'start_date y end_date son requeridos'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Formato de fecha inválido. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Obtener KPIs usando el servicio
            kpi_data = KPIService.get_credit_kpi_summary(
                start_date=start_date,
                end_date=end_date,
                user=request.user  # Pasar usuario para filtrado por rol
            )
            
            return Response(kpi_data)
            
        except Exception as e:
            print(f"❌ Error en CreditKPIView: {str(e)}")
            return Response(
                {'error': f'Error interno del servidor: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
