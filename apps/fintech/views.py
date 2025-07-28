from decimal import Decimal
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from django.db.models import Sum, Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from apps.fintech.models import Installment
from apps.fintech.services.installment_calculator import InstallmentCalculator
from apps.fintech.serializers import InstallmentSerializer

from apps.fintech.utils.root import recalculate_credit
from apps.fintech.services.credit_service import CreditService
from apps.fintech.services.kpi_service import KPIService
from apps.fintech.services.client_service import ClientService

from .models import (
    User, Account, Transaction, Credit, AccountMethodAmount, SubCategory,
)
from .serializers import (
    UserSerializer, AccountSerializer, TransactionSerializer, CreditSerializer,
    UserRegistrationSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.fintech.serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para devolver un token JWT con datos adicionales del usuario.
    """
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        print("Datos recibidos en el backend:", request.data)

        # Extraer datos del request
        credit_uid = request.data.get("credit_uid")
        amount = Decimal(request.data.get("amount"))
        description = request.data.get("description")
        user_id = request.data.get("user_id")
        subcategory_name = request.data.get("subcategory_name")
        payment_type = request.data.get("payment_type")

        # Use service layer for business logic
        success, result, status_code = CreditService.create_transaction_from_payment(
            credit_uid, amount, description, user_id, subcategory_name, payment_type
        )
        
        if not success:
            return Response({"detail": result}, status=status_code)
        
        # Serialize the result
        serializer = TransactionSerializer(result)
        return Response(serializer.data, status=status_code)

class CreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer

class RecalculateCreditView(APIView):
    """
    Recalcula abonos, pendientes y morosidad de un crédito específico.
    """
    def post(self, request, *args, **kwargs):
        uid = request.data.get('uid')

        if not uid:
            return Response(
                {"error": "Debes proporcionar un UUID en el body."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            credit = Credit.objects.get(uid=uid)
            recalculate_credit(credit)
            return Response(
                {"message": f"✅ Crédito {credit.uid} recalculado exitosamente."},
                status=status.HTTP_200_OK
            )
        except Credit.DoesNotExist:
            return Response(
                {"error": "Crédito no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error al recalcular: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserRegistrationView(APIView):
    """
    Registra un nuevo usuario
    POST /api/auth/register/
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    'message': 'Usuario creado exitosamente',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def due_today_installments(request):
    """Vista para cuotas que vencen hoy"""
    today = timezone.now().date()
    
    installments = Installment.objects.filter(
        due_date=today,
        status='pending'
    ).select_related('credit__user').order_by('due_date')
    
    # Agregar campos calculados
    for installment in installments:
        installment.remaining_amount_calc = InstallmentCalculator.get_remaining_amount(installment)
        installment.days_overdue_calc = InstallmentCalculator.get_days_overdue(installment)
        installment.late_fee_calc = InstallmentCalculator.get_late_fee(installment)
        installment.total_amount_due = InstallmentCalculator.get_total_amount_due(installment)
    
    serializer = InstallmentSerializer(installments, many=True)
    
    return Response({
        'count': installments.count(),
        'date': today,
        'installments': serializer.data
    })


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def due_tomorrow_installments(request):
    """Vista para cuotas que vencen mañana"""
    tomorrow = timezone.now().date() + timedelta(days=1)
    
    installments = Installment.objects.filter(
        due_date=tomorrow,
        status='pending'
    ).select_related('credit__user').order_by('due_date')
    
    # Agregar campos calculados
    for installment in installments:
        installment.remaining_amount_calc = InstallmentCalculator.get_remaining_amount(installment)
        installment.days_overdue_calc = InstallmentCalculator.get_days_overdue(installment)
        installment.late_fee_calc = InstallmentCalculator.get_late_fee(installment)
        installment.total_amount_due = InstallmentCalculator.get_total_amount_due(installment)
    
    serializer = InstallmentSerializer(installments, many=True)
    
    return Response({
        'count': installments.count(),
        'date': tomorrow,
        'installments': serializer.data
    })


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def upcoming_installments(request):
    """Vista para cuotas que vencen en los próximos días"""
    today = timezone.now().date()
    days_ahead = request.GET.get('days', 7)  # Por defecto 7 días
    
    try:
        days_ahead = int(days_ahead)
    except ValueError:
        days_ahead = 7
    
    end_date = today + timedelta(days=days_ahead)
    
    installments = Installment.objects.filter(
        due_date__range=[today, end_date],
        status='pending'
    ).select_related('credit__user').order_by('due_date')
    
    # Agregar campos calculados
    for installment in installments:
        installment.remaining_amount_calc = InstallmentCalculator.get_remaining_amount(installment)
        installment.days_overdue_calc = InstallmentCalculator.get_days_overdue(installment)
        installment.late_fee_calc = InstallmentCalculator.get_late_fee(installment)
        installment.total_amount_due = InstallmentCalculator.get_total_amount_due(installment)
    
    serializer = InstallmentSerializer(installments, many=True)
    
    return Response({
        'count': installments.count(),
        'start_date': today,
        'end_date': end_date,
        'days_ahead': days_ahead,
        'installments': serializer.data
    })


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def overdue_installments(request):
    """Vista para cuotas vencidas"""
    today = timezone.now().date()
    
    installments = Installment.objects.filter(
        due_date__lt=today,
        status__in=['pending', 'partial']
    ).select_related('credit__user').order_by('due_date')
    
    # Agregar campos calculados
    for installment in installments:
        installment.remaining_amount_calc = InstallmentCalculator.get_remaining_amount(installment)
        installment.days_overdue_calc = InstallmentCalculator.get_days_overdue(installment)
        installment.late_fee_calc = InstallmentCalculator.get_late_fee(installment)
        installment.total_amount_due = InstallmentCalculator.get_total_amount_due(installment)
    
    serializer = InstallmentSerializer(installments, many=True)
    
    return Response({
        'count': installments.count(),
        'date': today,
        'installments': serializer.data
    })


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def collector_dashboard(request):
    """Dashboard completo para cobradores"""
    today = timezone.now().date()
    
    # Cuotas que vencen hoy
    due_today = Installment.objects.filter(
        due_date=today,
        status='pending'
    ).select_related('credit__user').count()
    
    # Cuotas que vencen mañana
    due_tomorrow = Installment.objects.filter(
        due_date=today + timedelta(days=1),
        status='pending'
    ).select_related('credit__user').count()
    
    # Cuotas vencidas
    overdue = Installment.objects.filter(
        due_date__lt=today,
        status__in=['pending', 'partial']
    ).select_related('credit__user').count()
    
    # Total de cuotas pendientes
    total_pending = Installment.objects.filter(
        status='pending'
    ).count()
    
    return Response({
        'summary': {
            'due_today': due_today,
            'due_tomorrow': due_tomorrow,
            'overdue': overdue,
            'total_pending': total_pending,
        },
        'date': today
    })
