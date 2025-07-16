"""
Serializers for accounts app
"""
from rest_framework import serializers
from .models import Accounts, Profile, BankAccount, Card, Contact

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
            "currency",
            "created_at",
        ]


class AccountWithProfileSerializer(AccountSerializer):
    """Class that handling account with profile data."""
    profile = ProfileSerializer(read_only=False)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Accounts
        fields = [
            "id",
            "iban",
            "name",
            "currency",
            "created_at",
            "profile",
            "email",
        ]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        instance = super().update(instance, validated_data)
        if profile_data:
            profile = instance.profile
            full_name_before = profile.full_name
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
            # Se il full_name è cambiato e non è vuoto, aggiorna il titolare della carta
            if 'full_name' in profile_data and profile_data['full_name'] and profile_data['full_name'] != full_name_before:
                user = instance.user
                from accounts.models import BankAccount, Card
                bank_accounts = BankAccount.objects.filter(user=user)
                for ba in bank_accounts:
                    Card.objects.filter(account=ba).update(holder_name=profile_data['full_name'])
        return instance


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = [
            "id", "iban", "name", "balance", "currency", "opened_at"
        ]

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            "id", "circuit", "pan_last4", "pan_hash", "pan_real", "expiry_month", "expiry_year", "cvv_hash", "cvv_real", "holder_name", "active"
        ]

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "name", "email", "iban", "city", "created_at"]