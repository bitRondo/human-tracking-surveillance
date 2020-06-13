from django.urls import path

from . import views

urlpatterns = [
    path('', views.Analysis, name='Prediction'),
    path('training/', views.training, name='training'),
    path('training/getPre/', views.getPre, name='getPre'),
]