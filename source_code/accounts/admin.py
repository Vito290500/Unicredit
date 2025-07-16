"""
ACCOUNTS admin configuration
"""

from django.contrib import admin
from .models import Accounts, Profile, Card, BankAccount

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
