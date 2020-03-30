from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

class CustomizedUserCreationForm (UserCreationForm):

    class Meta (UserCreationForm):
        model = User
        fields = ('first_name', 'email', 'last_name', 'phone', 'username', )

class CustomizedUserChangeForm (UserChangeForm):
    
    class Meta (UserChangeForm):
        model = User
        fields = ('first_name', 'email')

