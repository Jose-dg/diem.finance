from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    ClientViewSet,
    CategoryViewSet,
    AccountViewSet,
    TransactionViewSet,
    CreditViewSet,
    ExpenseViewSet
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'credits', CreditViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]