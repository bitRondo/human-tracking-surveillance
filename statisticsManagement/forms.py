from django import forms

from django.utils import timezone

from datetime import timedelta

class DateInput(forms.DateInput):
    input_type = 'date'

class DateRangeSearchForm(forms.Form):
    start_date = forms.DateField(
        widget = DateInput,
        initial = (timezone.now() - timedelta(days = 14)).date(),
    )

    end_date = forms.DateField(
        widget = DateInput,
        initial = (timezone.now() - timedelta(days = 1)).date(),
    )

    single_date = forms.DateField(
        widget = DateInput,
        initial = timezone.now().today().date(),
    )

    auto_adjust = forms.BooleanField(
        required = False,
        widget = forms.CheckboxInput,
        initial = True,
    )