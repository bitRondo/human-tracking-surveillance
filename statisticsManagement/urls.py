from django.urls import path

from . import views

urlpatterns = [
    path('dailyrecords', views.viewDailyRecords, name = 'daily_records')
]