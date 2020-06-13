from django import forms

from .models import Recipient

class RecipientAddForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields= ['register_num', 'name', 'email']

        widgets = {
            'register_num' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'email' : forms.EmailInput(attrs={'class' : 'form-control'}),
        }