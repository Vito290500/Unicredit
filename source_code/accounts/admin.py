"""
ACCOUNTS admin configuration
"""

from django.contrib import admin
from .models import Accounts, Profile, Card, BankAccount, Accredito, EstrattoConto

@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    list_display = ("user", "iban", "name", "currency", "created_at")
    search_fields = ("user__email", "iban", "name")
    list_filter = ("currency",)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("account", "full_name", "phone_number", "birth_date", "fiscal_code", "city", "postal_code", "updated_at")
    search_fields = ("full_name", "fiscal_code", "city", "account__iban")
    list_filter = ("city",)

admin.site.register(Card)
admin.site.register(BankAccount)

@admin.register(Accredito)
class AccreditoAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'date', 'amount', 'currency', 'source', 'created_at')
    search_fields = ('account__iban', 'source', 'description')
    list_filter = ('currency', 'date', 'source')

@admin.register(EstrattoConto)
class EstrattoContoAdmin(admin.ModelAdmin):
    list_display = ('user', 'mese', 'anno', 'saldo_iniziale', 'saldo_finale', 'data_creazione')
    list_filter = ('anno', 'mese', 'user')