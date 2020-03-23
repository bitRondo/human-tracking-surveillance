from django.contrib import admin

from .models import User, UserCredential

admin.site.register(User)
admin.site.register(UserCredential)