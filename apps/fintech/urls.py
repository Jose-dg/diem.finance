from django.urls import path
from .views import (
    RecalculateCreditMorosityView,
    RecalculateCreditPendingAmountView,
    RecalculateCreditView,
    UserViewSet,
    AccountViewSet,
    TransactionViewSet,
    CreditViewSet
)

urlpatterns = [
    # Rutas para ViewSets
    path('clients/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='client-list'),
    path('clients/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='client-detail'),
        
    path('accounts/', AccountViewSet.as_view({'get': 'list', 'post': 'create'}), name='account-list'),
    path('accounts/<int:pk>/', AccountViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='account-detail'),
    
    path('transactions/', TransactionViewSet.as_view({'get': 'list', 'post': 'create'}), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='transaction-detail'),
    
    path('credits/', CreditViewSet.as_view({'get': 'list', 'post': 'create'}), name='credit-list'),
    path('credits/<int:pk>/', CreditViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='credit-detail'),
    
    path('recalculate_cm/<uuid:credit_uid>/', RecalculateCreditMorosityView.as_view(), name='recalculate_credit_morosity'),
    path('recalculate_pending/', RecalculateCreditPendingAmountView.as_view(), name='recalculate_credit_pending_amount'),

    path('recalculate-credit/', RecalculateCreditView.as_view(), name='recalculate_credit'),

]




