"""
URL api endpoint
"""

from rest_framework.routers import DefaultRouter
from transactions.views import TransactionViewSet
from django.urls import path
from .views import DashboardDataAPIView

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = router.urls + [
    path('dashboard-data/', DashboardDataAPIView.as_view(), name='dashboard-data'),
]