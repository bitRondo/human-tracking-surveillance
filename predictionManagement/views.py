from django.shortcuts import render
from django.http import HttpResponse
from .models import DailyRecord
from django.db.models import Sum,Avg



def index(request):
     
     items = DailyRecord.objects.filter(total_count ="150").aggregate(Avg('total_count'))
   

     return render(request,'prediction.html',{'Prediction':items})
    
# Create your  views here.
