"""
Transaction model configuration.
"""
import uuid
from django.db import models
from accounts.models import BankAccount

class Category(models.Model):
    """Class that handling category model."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    """Class that handling transaction model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    date = models.DateField(help_text="Data della transazione")
    amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        help_text="Importo positivo per entrate, negativo per uscite"
    )
    currency = models.CharField(
        max_length=3,
        default="EUR",
        help_text="ISO 4217"
    )
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="transactions"
    )
    has_document = models.BooleanField(
        default=False,
        help_text="Se c'è allegato un documento (ricevuta, fattura, ecc.)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp di creazione in DB"
    )
    merchant_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Nome del merchant o controparte"
    )
    external_id = models.CharField(
        max_length=100,
        blank=True, null=True,
        unique=True,
        help_text="ID esterno (es. da importazioni batch)"
    )
    notes = models.TextField(
        blank=True,
        help_text="Annotazioni libere"
    )

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.date} • {self.amount} {self.currency}"