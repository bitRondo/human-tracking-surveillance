from django import forms

class TimeInput(forms.TimeInput):
    input_type = 'time'

class SystemSettingsForm(forms.Form):
    business_start = forms.TimeField(
        widget = TimeInput,
    )