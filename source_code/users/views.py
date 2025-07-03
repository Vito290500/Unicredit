"""
Users Views customization
"""

from django.db import transaction
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from django.conf import settings
from djoser import utils
from django.contrib.auth.tokens import default_token_generator

from rest_framework import status
from rest_framework.response import Response
from users.email import ActivationEmail

import logging
logger = logging.getLogger(__name__)

User = get_user_model()

class CustomUserViewSet(DjoserUserViewSet):
    """Class for overwrite Djoser create()."""

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """atomic function for handling create email."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
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


