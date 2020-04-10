from django.urls import path

from . import views

urlpatterns = [
    path('', views.system, name = 'system_settings')
]