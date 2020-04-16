from .models import User
from django.utils import timezone
from datetime import timedelta

import random

def create_activation_key():
    user_exists = True
    while (user_exists):
        key = random.randint(100000, 999999)
        user_exists = User.objects.filter(activation_key = key).exists()

    return str(key)

def send_activation_key(user, resend = False):
    key = create_activation_key()
    keyString = key[:3] + '-' + key[3:]
    subject = "Account Activation"
    
    if not resend:
        message = ("<h1>Thank you for registering at HumanTrackingSurveillance!</h1>" +
        "<p>Please use the following activation code to activate your account:</p>" +
        "<h2>%s</h2>"%keyString +
        "<p>We hope you enjoy using HumanTrackingSurveillance!</p>" +
        "<small>Please note that the above activation code will be valid only within 24 hours after being sent.</small>")
    else:
        message = ("<h1>New Activation Code</h1>" +
        "<p>Your new activation code is:</p>" +
        "<h2>%s</h2>"%keyString +
        "<p>We hope you enjoy using HumanTrackingSurveillance!</p>" +
        "<small>Please note that the above activation code will be valid only within 24 hours after being sent.</small>")
    
    from_email = "HTS@hts.com"


    user.activation_key = key
    user.key_expiry = timezone.now() + timedelta(hours = 24)
    user.save()

    print (keyString)
    # send_mail(subject, "", from_email, ["disurawaru.17@cse.mrt.ac.lk",], html_message = message)

    user.email_user(subject, "", from_email = from_email, html_message = message)

def checkIsAdmin(user):
    return user.is_staff    

# from accountManagement.controllers import a
def test_mail():
    subject = "Account Activation"
    message = "Please use this email to activate your account"
    from_email = "HTS@hts.com"
    to_email = ["disurawaru.17@cse.mrt.ac.lk",]
    send_mail(subject, message, from_email, to_email)

    from django.core.mail import send_mail
    send_mail("Helo", "Test mail", "HTS@hts.com", ["disurawaru.17@cse.mrt.ac.lk",])