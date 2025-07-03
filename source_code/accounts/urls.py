"""
URLS configuration for accounts app
"""
from django.urls import path
from .views import MyAccountView

urlpatterns = [
    path('me/', MyAccountView.as_view(), name='my-account'),
]
