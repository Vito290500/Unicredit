"""
ACCOUNTS admin configuration
"""

from django.contrib import admin
from .models import Accounts, Profile, Card, BankAccount, Accredito, EstrattoConto, GoalsSaving, GoalsSavingMovimento

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

@admin.register(GoalsSaving)
class GoalsSavingAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 'bank_account', 'importo_target', 'importo_attuale',
        'data_limite', 'periodicita', 'importo_periodicita', 'attivo', 'created'
    )
    list_filter = ('attivo', 'periodicita', 'created')
    search_fields = ('nome', 'bank_account__iban', 'bank_account__name')
    readonly_fields = ('created', 'updated_at', 'importo_attuale')
    date_hierarchy = 'created'

@admin.register(GoalsSavingMovimento)
class GoalsSavingMovimentoAdmin(admin.ModelAdmin):
    list_display = ('goal', 'tipo', 'importo', 'data_movimento')
    list_filter = ('tipo', 'data_movimento')
    search_fields = ('goal__nome',)
    date_hierarchy = 'data_movimento'