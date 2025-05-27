from decimal import Decimal
import uuid
from rest_framework import viewsets

from apps.fintech.utils import recalculate_credit
from .models import ( 
   User, 
   Account, 
   Transaction, 
   Credit )
from .serializers import (
    UserSerializer, 
    AccountSerializer, 
    TransactionSerializer, 
    CreditSerializer )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreditSerializer, TransactionSerializer
from .models import User, Credit, Transaction, AccountMethodAmount, Transaction
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.fintech.serializers import CustomTokenObtainPairSerializer
from django.db.models import Sum

from .models import (
    AccountMethodAmount,
    Credit,
    SubCategory
)

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
        subcategory_name = request.data.get("subcategory_name")  # Nombre de la subcategoría
        payment_type = request.data.get("payment_type")

        # Validar el crédito
        credit = get_object_or_404(Credit, uid=credit_uid)
        if amount <= 0:
            return Response({"detail": "El monto debe ser mayor a 0"}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Buscando subcategoría: {subcategory_name}")

        # Buscar la subcategoría por nombre
        try:
            subcategory = SubCategory.objects.get(name=subcategory_name)
            print(f"Subcategoría encontrada: ID={subcategory.id}, nombre={subcategory.name}")
        except ObjectDoesNotExist:
            return Response(
                {"detail": f"No se encontró una subcategoría con nombre {subcategory_name}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Crear la transacción
        try:
            transaction = Transaction.objects.create(
                transaction_type="income",
                description=description or f"Pago registrado: {payment_type}",
                user_id=user_id,
                category=subcategory,  # Ahora asignamos la subcategoría correctamente
            )
            print(f"Transacción creada: ID={transaction.id}")

            # Crear el abono
            AccountMethodAmount.objects.create(
                payment_method=credit.payment,
                payment_code=str(uuid.uuid4()),
                amount=amount,
                amount_paid=amount,
                currency=credit.currency,
                credit=credit,
                transaction=transaction,
            )
            print("Abono creado exitosamente")
        except Exception as e:
            print(f"Error durante la creación: {e}")
            return Response({"detail": f"Error al registrar la transacción: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"detail": "Transacción y abono registrados exitosamente"}, status=status.HTTP_201_CREATED)

class CreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para devolver un token JWT con datos adicionales del usuario.
    """
    serializer_class = CustomTokenObtainPairSerializer

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
