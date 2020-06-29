from django.urls import path

from . import views

urlpatterns = [
    path('dailyRecord', views.DailyRecords, name = 'DailyRecords'),
    path('timelyRecord', views.TimelyRecords, name = 'TimelyRecords')
]