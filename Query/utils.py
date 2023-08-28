import imp
from django.core.mail import EmailMessage
from ClaimAssurance.settings import EMAIL_HOST_USER 
from .models import User
class util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body= data['body'],
            from_email = EMAIL_HOST_USER,
            to = [data['to_email']]
        )
        email.send()