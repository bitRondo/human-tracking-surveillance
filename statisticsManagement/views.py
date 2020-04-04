from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.utils import timezone
import datetime

from .forms import DateRangeSearchForm

from .models import DailyRecord

def viewDailyRecords(request):
    timezone.activate('Asia/Colombo')

    if request.method == 'POST':
        form = DateRangeSearchForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
    else:
        form = DateRangeSearchForm()
        start_date = form.fields['start_date'].initial
        end_date = form.fields['end_date'].initial
    
    all_results = DailyRecord.fetchWithinRange(start_date = start_date, end_date = end_date)
    results_of_peak_days = DailyRecord.findPeakWithinRange(start_date = start_date, end_date = end_date)

    content = {
        'form' : form,
        'all_results' : all_results,
        'peak_results' : results_of_peak_days,
    }
    return render(request, 'statisticsManagement/viewDailyRecords.html', content)
