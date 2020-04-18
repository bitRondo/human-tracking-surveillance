from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

class CustomizedUserCreationForm (UserCreationForm):
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class' : 'form-control'}),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class' : 'form-control'}),
        strip=False,
    )

    class Meta (UserCreationForm):
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 
        'username', 'password1', 'password2','receive_reports')

        widgets = {
            'first_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'last_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'email' : forms.EmailInput(attrs={'class' : 'form-control'}),
            'phone' : forms.TextInput(attrs={'class' : 'form-control'}),
            'username' : forms.TextInput(attrs={'class' : 'form-control'}),   
        }

class CustomizedUserChangeForm (UserChangeForm):
    
    class Meta (UserChangeForm):
        model = User
        fields = ('first_name', 'email')

[]