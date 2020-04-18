import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect

from .models import Recipient

def send_security_alert():
    all_recipients = Recipient.objects.values_list('email')

    date = datetime.datetime.today().strftime("%Y-%m-%d")
    time = datetime.datetime.now().time().strftime("%H:%M:%S")

    for email in all_recipients:
        send_mail(
        'Securiy Alert from HTS', #subject
        'Human Detected on %s at %s'%(date, time), #message
        settings.EMAIL_HOST_USER, #from
        email, #to
        fail_silently = False
        )