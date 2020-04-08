from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from django.utils import timezone
import datetime

from .forms import DateRangeSearchForm

from .models import DailyRecord, TimelyRecord

@login_required
def viewStatistics(request):
    timezone.activate('Asia/Colombo')

    if request.method == 'POST':
        form = DateRangeSearchForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            single_date = form.cleaned_data['single_date']
            
            if form.cleaned_data['auto_adjust']:
                dateTuple = calculate_viewable_date_range(
                    form.cleaned_data['single_date'],
                    form.fields['end_date'].initial,
                )
                form = DateRangeSearchForm(
                    {
                        'start_date' : dateTuple[0],
                        'end_date' : dateTuple[1],
                        'single_date' : request.POST['single_date'],
                        'auto_adjust' : request.POST['auto_adjust'],
                    }
                )
                start_date, end_date = dateTuple

    else:
        form = DateRangeSearchForm()
        start_date = form.fields['start_date'].initial
        end_date = form.fields['end_date'].initial
        single_date = form.fields['single_date'].initial
    
    all_results = DailyRecord.fetchWithinRange(start_date = start_date, end_date = end_date)
    results_of_peak_days = DailyRecord.findPeakWithinRange(start_date = start_date, end_date = end_date)
    
    single_date_timely_results = TimelyRecord.getRecordsOnDate(single_date)
    single_date_daily_result = DailyRecord.objects.filter(record_date__exact = single_date)
    single_date_peak_times = ()
    if single_date_daily_result:
        single_date_daily_result = single_date_daily_result[0]
        if single_date_daily_result.peak_hour_start.minute == 30:
            midVal = datetime.time(single_date_daily_result.peak_hour_end.hour, 0)
        else:
            midVal = datetime.time(single_date_daily_result.peak_hour_start.hour, 30)
        single_date_peak_times = (
            single_date_daily_result.peak_hour_start,
            midVal,                
            single_date_daily_result.peak_hour_end
        )

    content = {
        'form' : form,
        'all_results' : all_results,
        'peak_results' : results_of_peak_days,
        'single_date' : single_date,
        'single_date_timely_results' : single_date_timely_results,
        'single_date_daily_result' : single_date_daily_result,
        'single_date_peak_times' : single_date_peak_times,
        'invalid_date_range': start_date >= end_date,
    }
    return render(request, 'statisticsManagement/viewDailyRecords.html', content)

def calculate_viewable_date_range(start_date, end_date):
    start_date = datetime.datetime.fromisoformat(start_date.isoformat())
    end_date = datetime.datetime.fromisoformat(end_date.isoformat())
    rightDifference = (end_date - start_date).days
    
    if rightDifference > 7 :
        maxRight = (start_date + datetime.timedelta(days = 7)).date()
        maxLeft = (start_date - datetime.timedelta(days = 7)).date()
        return (maxLeft, maxRight)

    else:
        if rightDifference < 0:
            rightDifference = 0
    
    maxRight = end_date.date()
    maxLeft = (end_date - datetime.timedelta(days = (14))).date()
    return (maxLeft, maxRight)