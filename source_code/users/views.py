"""
Users Views customization
"""

from django.db import transaction
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from django.conf import settings
from djoser import utils
from django.contrib.auth.tokens import default_token_generator
from accounts.models import Accounts, Profile, BankAccount, Card
import uuid
import hashlib
import random
import string
import datetime

from rest_framework import status
from rest_framework.response import Response
from users.email import ActivationEmail

import logging
logger = logging.getLogger(__name__)

User = get_user_model()

def generate_iban():
    """Generate a fake, formatted Italian IBAN"""
    country_code = "IT"
    check_digits = "60"
    abi = "05428"
    cab = "11101"
    account_number = ''.join(random.choices(string.digits, k=12))
    iban = f"{country_code}{check_digits}{abi}{cab}{account_number}"
    return ' '.join([iban[i:i+4] for i in range(0, len(iban), 4)])

def generate_card_data():
    """Generate fake card data for demo purposes"""
    pan_real = ''.join(random.choices(string.digits, k=16))
    pan_last4 = pan_real[-4:]
    pan_hash = hashlib.sha256(pan_real.encode()).hexdigest()

    current_year = datetime.datetime.now().year
    expiry_year = random.randint(current_year + 3, current_year + 5)
    expiry_month = random.randint(1, 12)

    cvv_real = ''.join(random.choices(string.digits, k=3))
    cvv_hash = hashlib.sha256(cvv_real.encode()).hexdigest()
 
    circuit_choices = ['VISA', 'MC', 'AMEX']
    circuit = random.choice(circuit_choices)
    return {
        'pan_last4': pan_last4,
        'pan_hash': pan_hash,
        'pan_real': pan_real,
        'expiry_month': expiry_month,
        'expiry_year': expiry_year,
        'cvv_hash': cvv_hash,
        'cvv_real': cvv_real,
        'circuit': circuit,
        'holder_name': 'TITOLARE CARTA'
    }

def create_user_accounts(user):
    """Create all necessary account instances for a new user"""
    try:
        account_iban = generate_iban()
        account = Accounts.objects.create(
            user=user,
            iban=account_iban,
            name=f"Conto {user.email.split('@')[0]}",
            balance=0,
            currency='EUR'
        )
        
        profile = Profile.objects.create(
            account=account,
            full_name='',
            phone_number='',
            birth_date=None,
            fiscal_code='',
            city='',
            postal_code=''
        )
        
        bank_account_iban = generate_iban()
        bank_account = BankAccount.objects.create(
            user=user,
            iban=bank_account_iban,
            name=f"Conto Bancario {user.email.split('@')[0]}",
            balance=0,
            currency='EUR'
        )
        
        card_data = generate_card_data()
        Card.objects.create(
            account=bank_account,
            circuit=card_data['circuit'],
            pan_last4=card_data['pan_last4'],
            pan_hash=card_data['pan_hash'],
            pan_real=card_data['pan_real'],
            expiry_month=card_data['expiry_month'],
            expiry_year=card_data['expiry_year'],
            cvv_hash=card_data['cvv_hash'],
            cvv_real=card_data['cvv_real'],
            holder_name=profile.full_name or card_data['holder_name'],
            active=True
        )
        
        logger.info(f"✅ Created account instances for user {user.email}")
        
    except Exception as e:
        logger.error(f"❌ Error creating account instances for user {user.email}: {str(e)}")
        raise

class CustomUserViewSet(DjoserUserViewSet):
    """Class for overwrite Djoser create()."""

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """atomic function for handling create email."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        try:
            create_user_accounts(user)
        except Exception as e:
            logger.exception("❌ Errore creando istanze account")
            transaction.set_rollback(True)
            return Response(
                {"detail": "Errore durante la creazione dell'account, riprova."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        context = self.get_email_context(user)

        try:
            ActivationEmail(request=request, context=context).send([user.email])
            
        except Exception as e:
            logger.exception("❌ Errore inviando email di attivazione")
            transaction.set_rollback(True)
            return Response(
                {"detail": "Impossibile inviare email di attivazione, riprova."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_email_context(self, user):
        """Function that retrive email context."""
        
        context = {
            "user": user,
            "domain": settings.DJOSER["DOMAIN"],
            "site_name": settings.DJOSER["SITE_NAME"],
            "uid": utils.encode_uid(user.pk),
            "token": default_token_generator.make_token(user),
            "protocol": "https" if settings.SECURE_SSL_REDIRECT else "http",
        }
        context["url"] = settings.DJOSER["ACTIVATION_URL"].format(**context)
        return context


