"""
Views customization for accounts app
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from .models import Accounts
from .serializers import AccountWithProfileSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from users.models import User
import uuid

class MyAccountView(RetrieveUpdateAPIView):
    """Api for retrive and update my account data."""
    serializer_class = AccountWithProfileSerializer
    permission_classes =[IsAuthenticated]

    def get_queryset(self):
        return Accounts.objects.all()

    def get_object(self):
        return self.get_queryset().get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        old_email = instance.user.email
        response = super().update(request, *args, **kwargs)
        new_email = data.get('email')
        if new_email and new_email != old_email:
            user = instance.user
            user.email = new_email
            user.is_active = False
            recovery_code = str(uuid.uuid4())
            user.recovery_code = recovery_code
            user.save()
            response.data['recovery_code'] = recovery_code
        return response

   