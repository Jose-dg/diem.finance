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
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from .models import (
    UserProfile, UserRequest, CreditRequestDetail, InvestmentRequestDetail,
    RequestType, RequestStatus, RequestSource
)
from .serializers import (
    UserRegistrationSerializer, UserProfileSerializer, UserRequestSerializer,
    CreditRequestDetailSerializer, InvestmentRequestDetailSerializer,
    ClientCreditsQuerySerializer, ClientCreditsResponseSerializer
)

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

class UserProfileView(APIView):
    """
    Crea o actualiza el perfil de usuario
    POST /api/user/profile/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Verificar si ya existe un perfil
            profile, created = UserProfile.objects.get_or_create(
                user=request.user,
                defaults={}
            )
            
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Perfil creado/actualizado exitosamente',
                    'profile': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserRequestView(APIView):
    """
    Crea una nueva solicitud de usuario
    POST /api/user/requests/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            with transaction.atomic():
                # Obtener o crear el estado "Pendiente"
                pending_status, _ = RequestStatus.objects.get_or_create(
                    name='Pendiente',
                    defaults={
                        'description': 'Solicitud en espera de revisión',
                        'is_active': True
                    }
                )
                
                # Obtener la fuente "Web" (usar UUID del frontend)
                source_uuid = request.data.get('source')
                if source_uuid:
                    try:
                        source = RequestSource.objects.get(code=source_uuid)
                    except RequestSource.DoesNotExist:
                        # Crear fuente Web si no existe
                        source, _ = RequestSource.objects.get_or_create(
                            name='Web',
                            defaults={
                                'description': 'Solicitud desde aplicación web',
                                'is_active': True
                            }
                        )
                else:
                    source = None
                
                # Obtener el tipo de solicitud
                type_uuid = request.data.get('type')
                if type_uuid:
                    try:
                        request_type = RequestType.objects.get(code=type_uuid)
                    except RequestType.DoesNotExist:
                        return Response(
                            {'error': 'Tipo de solicitud no encontrado'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    request_type = None
                
                # Crear la solicitud
                user_request = UserRequest.objects.create(
                    user=request.user,
                    type=request_type,
                    status=pending_status,
                    source=source,
                    notes=request.data.get('notes', '')
                )
                
                serializer = UserRequestSerializer(user_request)
                return Response({
                    'message': 'Solicitud creada exitosamente',
                    'request_id': user_request.request_id,
                    'request': serializer.data
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreditRequestDetailView(APIView):
    """
    Crea el detalle de una solicitud de crédito
    POST /api/user/requests/credit-detail/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            with transaction.atomic():
                request_id = request.data.get('request')
                
                # Verificar que la solicitud existe y pertenece al usuario
                try:
                    user_request = UserRequest.objects.get(
                        request_id=request_id,
                        user=request.user
                    )
                except UserRequest.DoesNotExist:
                    return Response(
                        {'error': 'Solicitud no encontrada'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # Verificar que no existe ya un detalle de crédito
                if hasattr(user_request, 'credit_detail'):
                    return Response(
                        {'error': 'Ya existe un detalle de crédito para esta solicitud'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Crear el detalle de crédito
                credit_detail = CreditRequestDetail.objects.create(
                    request=user_request,
                    amount=request.data.get('amount'),
                    term_days=request.data.get('term_days'),
                    purpose=request.data.get('purpose')
                )
                
                serializer = CreditRequestDetailSerializer(credit_detail)
                return Response({
                    'message': 'Detalle de crédito creado exitosamente',
                    'credit_detail': serializer.data
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InvestmentRequestDetailView(APIView):
    """
    Crea el detalle de una solicitud de inversión
    POST /api/user/requests/investment-detail/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            with transaction.atomic():
                request_id = request.data.get('request')
                
                # Verificar que la solicitud existe y pertenece al usuario
                try:
                    user_request = UserRequest.objects.get(
                        request_id=request_id,
                        user=request.user
                    )
                except UserRequest.DoesNotExist:
                    return Response(
                        {'error': 'Solicitud no encontrada'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # Verificar que no existe ya un detalle de inversión
                if hasattr(user_request, 'investment_detail'):
                    return Response(
                        {'error': 'Ya existe un detalle de inversión para esta solicitud'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Crear el detalle de inversión
                investment_detail = InvestmentRequestDetail.objects.create(
                    request=user_request,
                    investement_amount=request.data.get('investement_amount'),
                    investment_horizon=request.data.get('investment_horizon'),
                    risk_tolerance=request.data.get('risk_tolerance'),
                    investment_goal=request.data.get('investment_goal')
                )
                
                serializer = InvestmentRequestDetailSerializer(investment_detail)
                return Response({
                    'message': 'Detalle de inversión creado exitosamente',
                    'investment_detail': serializer.data
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RequestConstantsView(APIView):
    """
    Obtiene las constantes necesarias para el frontend
    GET /api/user/requests/constants/
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            # Obtener o crear las constantes necesarias
            source_web, _ = RequestSource.objects.get_or_create(
                name='Web',
                defaults={
                    'description': 'Solicitud desde aplicación web',
                    'is_active': True
                }
            )
            
            type_credit, _ = RequestType.objects.get_or_create(
                name='Solicitud de Crédito',
                defaults={
                    'description': 'Solicitud para obtener un crédito',
                    'requires_approval': True,
                    'is_active': True
                }
            )
            
            type_investment, _ = RequestType.objects.get_or_create(
                name='Solicitud de Inversión',
                defaults={
                    'description': 'Solicitud para realizar una inversión',
                    'requires_approval': True,
                    'is_active': True
                }
            )
            
            status_pending, _ = RequestStatus.objects.get_or_create(
                name='Pendiente',
                defaults={
                    'description': 'Solicitud en espera de revisión',
                    'is_active': True
                }
            )
            
            return Response({
                'SOURCE_WEB': str(source_web.code),
                'TYPE_CREDIT': str(type_credit.code),
                'TYPE_INVESTMENT': str(type_investment.code),
                'STATUS_PENDING': str(status_pending.code)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ClientCreditsView(APIView):
    """
    Consulta todos los créditos asociados a un cliente por documento y/o nombre
    POST /api/client/credits/
    """
    # permission_classes = [IsAuthenticated]
    
    def normalize_document_number(self, document_number):
        """
        Normaliza el número de documento removiendo guiones, espacios y puntos
        """
        if not document_number:
            return ""
        # Remover guiones, espacios, puntos y otros caracteres especiales
        return ''.join(filter(str.isalnum, str(document_number)))
    
    def post(self, request):
        try:
            # Validar datos de entrada
            serializer = ClientCreditsQuerySerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            data = serializer.validated_data
            document_number = data.get('document_number')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            
            # Construir filtros para buscar usuarios
            from django.db.models import Q
            
            # Inicializar filtros
            user_filters = Q()
            
            # Filtro por documento - ahora más simple porque se normaliza automáticamente
            if document_number:
                # Normalizar el documento ingresado
                normalized_document = self.normalize_document_number(document_number)
                user_filters &= Q(document__document_number=normalized_document)
            
            # Filtros por nombre
            if first_name and last_name:
                user_filters &= Q(first_name__icontains=first_name) & Q(last_name__icontains=last_name)
            elif first_name:
                user_filters &= Q(first_name__icontains=first_name)
            elif last_name:
                user_filters &= Q(last_name__icontains=last_name)
            
            # Buscar usuarios que coincidan con los criterios
            users = User.objects.filter(user_filters).select_related('document')
            
            if not users.exists():
                return Response({
                    'message': 'No se encontraron clientes con los criterios proporcionados',
                    'credits': [],
                    'total_credits': 0,
                    'total_pending': 0,
                    'total_paid': 0
                }, status=status.HTTP_200_OK)
            
            # Obtener todos los créditos de los usuarios encontrados
            user_ids = users.values_list('id', flat=True)
            credits = Credit.objects.filter(
                user_id__in=user_ids
            ).select_related(
                'user', 'subcategory', 'currency', 'periodicity'
            ).prefetch_related(
                'payments__payment_method',
                'installments'
            ).order_by('-created_at')
            
            # Serializar los créditos
            credits_serializer = ClientCreditsResponseSerializer(credits, many=True)
            
            # Calcular totales
            total_credits = credits.count()
            total_pending = sum(credit.pending_amount or 0 for credit in credits)
            total_paid = sum(credit.total_abonos or 0 for credit in credits)
            
            # Información de los clientes encontrados
            clients_info = []
            for user in users:
                user_credits = credits.filter(user=user)
                clients_info.append({
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'document_number': user.document.document_number if user.document else None,
                    'document_type': user.document.document_type.description if user.document else None,
                    'credits_count': user_credits.count(),
                    'total_pending': sum(credit.pending_amount or 0 for credit in user_credits),
                    'total_paid': sum(credit.total_abonos or 0 for credit in user_credits)
                })
            
            return Response({
                'message': f'Se encontraron {total_credits} créditos para {len(clients_info)} cliente(s)',
                'clients': clients_info,
                'credits': credits_serializer.data,
                'summary': {
                    'total_credits': total_credits,
                    'total_pending': float(total_pending),
                    'total_paid': float(total_paid),
                    'clients_count': len(clients_info)
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Error al consultar créditos: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)