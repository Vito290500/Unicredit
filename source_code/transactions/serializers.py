"""
Transaction Serializers configuration.
"""
from rest_framework import serializers
from .models import Transaction

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
