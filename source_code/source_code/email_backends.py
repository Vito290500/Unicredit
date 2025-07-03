from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings

class DualBackend:
    """
    Invia le email a due backend SMTP:
    1) MailHog (locale)
    2) Gmail (reale)
    """

    def __init__(self, *args, **kwargs):
        # Backend MailHog (usa le impostazioni EMAIL_…)
        self.mhog = EmailBackend(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
            fail_silently=False,
        )
        # Backend Gmail (usa le impostazioni GMAIL_EMAIL_…)
        self.gmail = EmailBackend(
            host=settings.GMAIL_EMAIL_HOST,
            port=settings.GMAIL_EMAIL_PORT,
            username=settings.GMAIL_EMAIL_HOST_USER,
            password=settings.GMAIL_EMAIL_HOST_PASSWORD,
            use_tls=settings.GMAIL_EMAIL_USE_TLS,
            fail_silently=False,
        )

    def send_messages(self, email_messages):
        sent = 0
        # prima invia a MailHog
        try:
            mh = self.mhog.send_messages(email_messages)
            sent += mh or 0
        except Exception:
            pass  # puoi loggare se vuoi
        # poi invia anche a Gmail
        try:
            gm = self.gmail.send_messages(email_messages)
            sent += gm or 0
        except Exception:
            pass
        return sent
