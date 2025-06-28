from django.urls import path
from .views import (
    UserRegistrationView,
    UserProfileView,
    UserRequestView,
    CreditRequestDetailView,
    InvestmentRequestDetailView,
    RequestConstantsView,
    RecalculateCreditView,
    UserViewSet,
    AccountViewSet,
    TransactionViewSet,
    CreditViewSet,
    CustomTokenObtainPairView,
    ClientCreditsView
)

urlpatterns = [

    # Registro de usuario
    path('api/auth/register/', UserRegistrationView.as_view(), name='user-register'),
    
    # Perfil de usuario
    path('api/user/profile/', UserProfileView.as_view(), name='user-profile'),
    
    # Solicitudes
    path('api/user/requests/', UserRequestView.as_view(), name='user-requests'),
    path('api/user/requests/credit-detail/', CreditRequestDetailView.as_view(), name='credit-request-detail'),
    path('api/user/requests/investment-detail/', InvestmentRequestDetailView.as_view(), name='investment-request-detail'),
    path('api/user/requests/constants/', RequestConstantsView.as_view(), name='request-constants'),
    
    # Consulta de créditos por cliente
    path('api/client/credits/', ClientCreditsView.as_view(), name='client-credits'),
    
    # Rutas para ViewSets
    path('clients/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='client-list'),
    path('clients/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='client-detail'),
        
    path('accounts/', AccountViewSet.as_view({'get': 'list', 'post': 'create'}), name='account-list'),
    path('accounts/<int:pk>/', AccountViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='account-detail'),
    
    path('transactions/', TransactionViewSet.as_view({'get': 'list', 'post': 'create'}), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='transaction-detail'),
    
    path('credits/', CreditViewSet.as_view({'get': 'list', 'post': 'create'}), name='credit-list'),
    path('credits/<int:pk>/', CreditViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='credit-detail'),
    
    path('recalculate-credit/', RecalculateCreditView.as_view(), name='recalculate_credit'),

]




