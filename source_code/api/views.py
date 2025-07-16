"""
API views configuration.
"""

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import BankAccount, Card
from accounts.serializers import BankAccountSerializer, CardSerializer
from accounts.models import Accounts
from rest_framework.generics import ListAPIView
from transactions.models import Category
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination


class DashboardDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        last_login = user.last_login
        last_login_str = last_login.isoformat() if last_login else None
        account = BankAccount.objects.filter(user=user).first()

        card = Card.objects.filter(account=account).first() if account else None
        account_data = BankAccountSerializer(account).data if account else None
        card_data = CardSerializer(card).data if card else None
        card_iban = card.account.iban if card and card.account else ''

        if card_data is not None:
            card_data['iban'] = card_iban
        else:
            card_data = {'iban': ''}

        try:
            user_account = Accounts.objects.get(user=user)
            profile = getattr(user_account, 'profile', None)

            if profile and profile.full_name:
                user_full_name = profile.full_name
            else:
                user_full_name = user.email

        except Accounts.DoesNotExist:
            user_full_name = user.email


        card_number = card.pan_real if card and card.pan_real else ''
        cvv_real = card.cvv_real if card and card.cvv_real else ''
        holder_name = card.holder_name if card and card.holder_name else ''

        if card_data is not None:
            card_data['card_number'] = card_number
            card_data['cvv'] = cvv_real
            card_data['holder_name'] = holder_name
        else:
            card_data = {'card_number': '', 'cvv': '', 'holder_name': ''}

        return Response({
            'user_full_name': user_full_name,
            'last_login': last_login_str,
            'account': account_data,
            'card': card_data,
        })


class UserBankAccountListView(ListAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # Disabilita la paginazione per debug
    ordering = ['-created_at']
    ordering_fields = ['created_at', 'opened_at']

    def get_ordering(self):
        return ['-created_at']

    def get(self, request, *args, **kwargs):
        print("QUERY PARAMS:", request.query_params)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Category.objects.all()
