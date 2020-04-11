from django.urls import path

from . import views

urlpatterns = [
    path('', views.viewStatistics, name = 'daily_records')
]