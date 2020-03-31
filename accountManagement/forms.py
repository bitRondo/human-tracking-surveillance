from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

class CustomizedUserCreationForm (UserCreationForm):

    class Meta (UserCreationForm):
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'username', )

class CustomizedUserChangeForm (UserChangeForm):
    
    class Meta (UserChangeForm):
        model = User
        fields = ('first_name', 'email')

