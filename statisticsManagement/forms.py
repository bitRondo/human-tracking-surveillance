from django import forms

from django.utils import timezone

from datetime import timedelta

class DateInput(forms.DateInput):
    input_type = 'date'

class DateRangeSearchForm(forms.Form):
    maxEndDate = (timezone.localtime().today() - timedelta(days = 1)).date()
    maxStartDate = (timezone.localtime().today() - timedelta(days = 2)).date()
    start_date = forms.DateField(
        initial = (timezone.localtime().today() - timedelta(days = 15)).date(),
        widget = DateInput(attrs = {"max" : maxStartDate.isoformat, 'class' : 'form-control'}),
    )

    end_date = forms.DateField(
        initial = maxEndDate,
        widget = DateInput(attrs = {"max" : maxEndDate.isoformat, 'class' : 'form-control'}),
    )

    today = timezone.localtime().today().date()
    

    auto_adjust = forms.BooleanField(
        required = False,
        widget = forms.CheckboxInput,
        initial = True,
    )


class DateForm(forms.Form):
    
    today = timezone.localtime().today().date()
    single_date = forms.DateField(
        widget = DateInput(attrs = {"max" : today.isoformat, 'class' : 'form-control'}),
        initial = today,
    )

    auto_adjust = forms.BooleanField(
        required = False,
        widget = forms.CheckboxInput,
        initial = True,
    )
