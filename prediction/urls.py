from django.urls import path

from . import views

urlpatterns = [
    path('', views.Analysis, name='Prediction'),
    path('getPre/', views.getPre, name='getPre'),
]