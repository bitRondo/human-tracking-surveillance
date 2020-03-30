from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user = True), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(next_page = '/'), name = 'logout'),
    path('register/', views.register, name = 'register'),
]