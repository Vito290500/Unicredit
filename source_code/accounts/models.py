"""
Accounts models customization
"""
import uuid
from django.db import models
from django.conf import settings
from users.models import User

class Accounts(models.Model):
    """
    Accounts model  
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iban = models.CharField(max_length=34, unique=True)
    name = models.CharField(max_length=120)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.iban}"

        
class Profile(models.Model):
    """
    Profile Model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField(Accounts, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=120,blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    fiscal_code = models.CharField(max_length=16,blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.account.name}"




class BankAccount(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    iban        = models.CharField(max_length=34, unique=True)
    name        = models.CharField(max_length=120)             
    balance     = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency    = models.CharField(max_length=3, default='EUR')
    opened_at   = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.iban})"


class Card(models.Model):
    class Circuit(models.TextChoices):
        VISA   = "VISA",  "Visa"
        MAST   = "MC",    "Mastercard"
        AMEX   = "AMEX",  "American Express"

    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account       = models.ForeignKey('accounts.BankAccount', on_delete=models.CASCADE, related_name='cards')
    circuit       = models.CharField(max_length=5, choices=Circuit.choices)
    pan_last4     = models.CharField(max_length=4)                
    pan_hash      = models.CharField(max_length=128)              
    expiry_month  = models.PositiveSmallIntegerField()
    expiry_year   = models.PositiveSmallIntegerField()
    cvv_hash      = models.CharField(max_length=128)              
    holder_name   = models.CharField(max_length=60)
    issued_at     = models.DateField(auto_now_add=True)
    active        = models.BooleanField(default=True)

    class Meta:
        unique_together = ("account", "pan_hash")  

    def __str__(self):
        return f"{self.circuit} **** {self.pan_last4}"
