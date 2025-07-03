"""
Views customization for accounts app
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from .models import Accounts
from .serializers import AccountWithProfileSerializer

class MyAccountView(RetrieveAPIView):
    """Api for retrive my account data."""
    serializer_class = AccountWithProfileSerializer
    permission_classes =[IsAuthenticated]

    def get_queryset(self):
        return Accounts.objects.all()

    def get_object(self):
        return self.get_queryset().get(user=self.request.user)

   