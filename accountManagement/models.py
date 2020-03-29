from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .managers import UserManager

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
    
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_admin = models.BooleanField(
        _('admin status'),
        default = False,
        help_text = _(
            'Designates whether this user has admin privileges'
        )
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default = False,
        help_text = _(
            'Designates whether this user has access to admin site'
        )
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'email']

    def __str__ (self):
        return self.username