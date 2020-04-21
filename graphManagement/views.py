from django.shortcuts import render
from django.http import JsonResponse
from statisticsManagement.models import DailyRecord
from statisticsManagement.models import TimelyRecord




def DailyRecordsChart(request):
    
    context=DailyRecord.objects.filter(record_date ='2020-04-01' , record_date ='2020-04-04')
    
    return render(request,'dailyRecords.html',{'context':context})




def TimeRecordsChart(request):
    context=TimelyRecord.objects.filter(record_date='2020-04-03')
    return render(request,'timeRecords.html',{'context':context})


# Create your views here.
