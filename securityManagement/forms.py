from django import forms

from .models import Recipient

class RecipientAddForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields= [
            'name',
            'email'
        ]