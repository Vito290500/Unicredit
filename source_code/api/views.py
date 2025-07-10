from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import BankAccount, Card
from accounts.serializers import BankAccountSerializer, CardSerializer
from accounts.models import Accounts

# Create your views here.

class DashboardDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        last_login = user.last_login
        last_login_str = last_login.isoformat() if last_login else None
        # Recupera il primo conto e la prima carta associata
        account = BankAccount.objects.filter(user=user).first()
        card = Card.objects.filter(account=account).first() if account else None
        account_data = BankAccountSerializer(account).data if account else None
        card_data = CardSerializer(card).data if card else None

        # Nome utente: prendi dal modello Accounts associato all'utente loggato
        try:
            user_account = Accounts.objects.get(user=user)
            user_full_name = user_account.name
        except Accounts.DoesNotExist:
            user_full_name = user.email

        # Numero carta completo (pan_hash) come card_number
        card_number = card.pan_hash if card else None
        if card_data is not None:
            card_data['card_number'] = card_number

        return Response({
            'user_full_name': user_full_name,
            'last_login': last_login_str,
            'account': account_data,
            'card': card_data,
        })
