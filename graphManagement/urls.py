from django.urls import path

from . import views

urlpatterns = [
    
    path('dailyRecordschart', views.DailyRecordsChart, name='DailyRecordsChart'),
    path('timeRecordschart', views.TimeRecordsChart, name='DailyRecordsChart'),
]

