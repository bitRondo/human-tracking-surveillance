from django.contrib.auth.base_user import BaseUserManager

from django.utils.translation import ugettext_lazy as _

class UserManager (BaseUserManager):
    def create_user (self, first_name, username, email, password, **extra_fields):
        if not first_name:
            raise ValueError(_('The first name is required'))
        elif not username:
            raise ValueError(_('Username is required'))
        elif not email:
            raise ValueError(_('The email is required'))

        email = self.normalize_email(email)

        user = self.model(first_name = first_name, username = username, email = email, **extra_fields)
        user.set_password(password)

        user.save()

        return user

    def create_superuser (self, first_name, username, email, password, **extra_fields):

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Super user must have is_superuser = True'))

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Super user must have is_staff = True'))

        return self.create_user(first_name, username, email, password, **extra_fields)