"""
Serializers for accounts app
"""
from rest_framework import serializers
from .models import Accounts, Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "full_name",
            "phone_number",
            "birth_date",
            "fiscal_code",
            "city",
            "postal_code",
            "updated_at",
        ]


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = [
            "id",
            "iban",
            "name",
            "balance",
            "currency",
            "created_at",
        ]


class AccountWithProfileSerializer(AccountSerializer):
    """Class that handling account with profile data."""
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Accounts
        fields = [
            "id",
            "iban",
            "name",
            "balance",
            "currency",
            "created_at",
            "profile",
        ]