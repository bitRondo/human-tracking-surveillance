from django import forms

import videoAnalysis.videoAnalysis as program

class TimeInput(forms.TimeInput):
    input_type = 'time'

class SystemSettingsForm(forms.Form):

    auto_switching_choices = [('on', 'On'), ('off', 'Off')]

    auto_switching = forms.ChoiceField(
        choices = auto_switching_choices,
        widget = forms.RadioSelect(attrs = {'oninput':'toggleAutoSwitching()'}),
    )

    business_start = forms.TimeField(
        widget = TimeInput,
        label = 'Start: ',
        required = False,
    )

    business_end = forms.TimeField(
        widget = TimeInput,
        label = 'Stop: ',
        required = False,
    )

    security_start = forms.TimeField(
        widget = TimeInput,
        label = 'Start: ',
        required = False,
    )

    security_end = forms.TimeField(
        widget = TimeInput,
        label = 'Stop: ',
        required = False,
    )