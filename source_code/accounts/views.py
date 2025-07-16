"""
Views customization for accounts app
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from .models import Accounts, Contact
from .serializers import AccountWithProfileSerializer, ContactSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from users.models import User
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

class ContactListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contacts = Contact.objects.filter(user=request.user)  # type: ignore[attr-defined]
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            Contact.objects.create(user=request.user, **serializer.validated_data)  # type: ignore[attr-defined]
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            contact = Contact.objects.get(pk=pk, user=request.user)  # type: ignore[attr-defined]
            contact.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contact.DoesNotExist:  # type: ignore[attr-defined]
            return Response({'detail': 'Contatto non trovato.'}, status=status.HTTP_404_NOT_FOUND)

   