from django import forms

import videoAnalysis.videoAnalysis as program

class TimeInput(forms.TimeInput):
    input_type = 'time'

class SystemSettingsForm(forms.Form):

    auto_switching_choices = [('on', 'On'), ('off', 'Off')]

    auto_switching = forms.ChoiceField(
        choices = auto_switching_choices,
        widget = forms.RadioSelect(
            attrs = {
                'oninput':'toggleAutoSwitching()', 
                'class':'form-check-input',
                'style' : 'margin-left: 20px'
            }
        ),
    )

    business_start = forms.TimeField(
        widget = TimeInput(
            attrs = {'class' : 'form-control col-sm-3', 'style' : 'margin-right: 10px; margin-left: 5px;'}
        ),
        label = 'Start: ',
        required = False,
    )

    business_end = forms.TimeField(
        widget = TimeInput(
            attrs = {'class' : 'form-control col-sm-3', 'style' : 'margin-right: 10px; margin-left: 5px;'}
        ),
        label = 'Stop: ',
        required = False,
    )

    security_start = forms.TimeField(
        widget = TimeInput(
            attrs = {'class' : 'form-control col-sm-3', 'style' : 'margin-right: 10px; margin-left: 5px;'}
        ),
        label = 'Start: ',
        required = False,
    )

    security_end = forms.TimeField(
        widget = TimeInput(
            attrs = {'class' : 'form-control col-sm-3', 'style' : 'margin-right: 10px; margin-left: 5px;'}
        ),
        label = 'Stop: ',
        required = False,
    )