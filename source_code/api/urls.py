"""
API urls endpoint configuration.
"""
from rest_framework.routers import DefaultRouter
from transactions.views import TransactionViewSet, TransferView
from django.urls import path
from .views import DashboardDataAPIView
from api.views import UserBankAccountListView, CategoryListView

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = router.urls + [
    path('dashboard-data/', DashboardDataAPIView.as_view(), name='dashboard-data'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('accounts/', UserBankAccountListView.as_view(), name='user-accounts'),
    path('categories/', CategoryListView.as_view(), name='categories'),
]