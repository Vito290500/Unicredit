"""
Transaction Serializers configuration.
"""
from rest_framework import serializers
from .models import Transaction, Category
from accounts.models import BankAccount
from django.utils import timezone
from django.db import transaction as db_transaction
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import BankAccountSerializer

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'account',
            'date',
            'amount',
            'currency',
            'description',
            'category',
            'has_document',
            'created_at',
            'merchant_name',
            'external_id',
            'notes',
        ]
        read_only_fields = ['id', 'created_at']

class TransferSerializer(serializers.Serializer):
    # Nuovi campi per supportare il frontend
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    description = serializers.CharField(allow_blank=True, required=False)
    category = serializers.CharField(allow_blank=True, required=False)
    clause = serializers.CharField(allow_blank=True, required=False)
    pin = serializers.CharField(max_length=6)
    to_name = serializers.CharField(allow_blank=True, required=False)
    to_email = serializers.EmailField(allow_blank=True, required=False)
    to_iban = serializers.CharField(max_length=34)
    to_city = serializers.CharField(allow_blank=True, required=False)

    def validate(self, data):
        user = self.context['request'].user
        # Trova il conto mittente
        from_account = BankAccount.objects.filter(user=user).first()  # type: ignore[attr-defined]
        if not from_account:
            raise serializers.ValidationError("Conto mittente non trovato.")
        # Trova il conto destinatario tramite IBAN
        to_iban = data['to_iban']
        try:
            to_account = BankAccount.objects.get(iban=to_iban)  # type: ignore[attr-defined]
        except BankAccount.DoesNotExist:  # type: ignore[attr-defined]
            raise serializers.ValidationError("Conto destinatario non trovato.")
        if from_account == to_account:
            raise serializers.ValidationError("Il conto mittente e destinatario devono essere diversi.")
        amount = data['amount']
        if amount <= 0:
            raise serializers.ValidationError("L'importo deve essere positivo.")
        if from_account.balance < amount:
            raise serializers.ValidationError("Saldo insufficiente sul conto mittente.")
        # Validazione PIN
        if from_account.pin != data['pin']:
            raise serializers.ValidationError("PIN errato.")
        data['from_account'] = from_account
        data['to_account'] = to_account
        return data

    def create(self, validated_data):
        from_account = validated_data['from_account']
        to_account = validated_data['to_account']
        amount = validated_data['amount']
        description = validated_data.get('description', '')
        category_name = validated_data.get('category', '')
        clause = validated_data.get('clause', '')
        date = timezone.now().date()
        # Trova o crea la categoria
        category_obj = None
        if category_name:
            category_obj, _ = Category.objects.get_or_create(name=category_name)  # type: ignore[attr-defined]
        with db_transaction.atomic():  # type: ignore[attr-defined]
            # Movimento uscita
            tx_out = Transaction.objects.create(  # type: ignore[attr-defined]
                account=from_account,
                date=date,
                amount=-amount,
                currency='EUR',
                description=description,
                category=category_obj,
                notes=clause,
                merchant_name=str(to_account),
            )
            # Movimento entrata
            tx_in = Transaction.objects.create(  # type: ignore[attr-defined]
                account=to_account,
                date=date,
                amount=amount,
                currency='EUR',
                description=description,
                category=category_obj,
                notes=clause,
                merchant_name=str(from_account),
            )
            # Aggiorna saldi
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()
        return {'tx_out': tx_out, 'tx_in': tx_in}
