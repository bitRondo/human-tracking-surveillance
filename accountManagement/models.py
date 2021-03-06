'''
Copyright: CSE Group 28 - 2020
(Module Project - Surveillance System to Detect and Track humans)
Written by: Disura Warusawithana
'''
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django.conf import settings

from django.core.mail import send_mail, EmailMessage

from .managers import UserManager

'''
Model: User
Extends: AbstractBaseUser, PermissionsMixin
This is customized User model which is made to contain system-specific attrbibutes of a user.
'''
class User (AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        _('first name'),
        max_length = 20,
        help_text = _('Required')
    )

    username = models.CharField(
        _('username'),
        max_length = 150,
        unique = True,
        help_text = _('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages = {
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        _('email'),
        max_length = 150,
        unique = True,
        help_text = _('Required'),
        error_messages = {
            'unique' : _("That email is already being used by another user."),
        },
    )

    last_name = models.CharField(max_length = 50, blank = True)

    phone = models.CharField(max_length = 10, blank = True)

    is_active = models.BooleanField(
        _('active'),
        default = True,
        help_text = _(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    activation_key = models.CharField(
        _('activation key'),
        max_length = 10,
        help_text = _(
            'This saves the activation key sent at the creation of the account.'
            'When logged in, if this is True, the user is asked to activate the account.'
        ),
        blank = True,
    )
    
    key_expiry = models.DateTimeField(
        _('key expiry'),
        null = True,
        default = None,
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default = False,
        help_text = _(
            'Designates whether this user has access to admin site'
        )
    )

    receive_reports = models.BooleanField(
        _('reception of Monthly Reports'),
        default = True,
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'email']

    def __str__ (self):
        return self.username

    def activate_user(self):
        self.activation_key = ''
        self.key_expiry = None
        self.save()

    def is_account_activated(self):
        return True if self.activation_key == '' else False

    def email_user(self, subject, message, **kwargs):
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [self.email,], **kwargs)
            return True
        except:
            return False

    def email_user_with_attachments(self, subject, message, attachments = []):
        emailObject = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.email],
        )
        for a in attachments:
            emailObject.attach_file(a)

        try:
            emailObject.send()
            return True
        except:
            return False
