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
    )

    business_end = forms.TimeField(
        widget = TimeInput,
        label = 'Stop: ',
    )

    security_start = forms.TimeField(
        widget = TimeInput,
        label = 'Start: ',
    )

    security_end = forms.TimeField(
        widget = TimeInput,
        label = 'Stop: ',
    )