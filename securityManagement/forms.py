from django import forms

from .models import Recipient

class RecipientAddForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields= [
            'register_num',
            'name',
            'email'
            
        ]