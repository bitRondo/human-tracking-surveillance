from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .forms import CustomizedUserCreationForm, CustomizedUserChangeForm
from .models import User

class CustomizedUserAdmin (UserAdmin):
    add_form = CustomizedUserCreationForm
    form = CustomizedUserChangeForm
    model = User
    list_display = ('first_name', 'username', 'email', 'is_staff', 'is_active',)
    list_filter = ('first_name', 'username', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email',)
    ordering = ('username', 'email',)

admin.site.register(User, CustomizedUserAdmin)
