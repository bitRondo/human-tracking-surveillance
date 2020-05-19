from django.urls import path

from . import views

urlpatterns = [
    path('system_settings', views.systemSetting, name = 'system_settings'),
    path('user_settings', views.userSetting, name = 'user_settings')
]