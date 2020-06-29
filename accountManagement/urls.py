from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user = True), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(next_page = '/'), name = 'logout'),
    path('register/', views.register, name = 'register'),
    path('activate/', views.activateAccount, name = 'activate'),
    path('activate/<resend_requested>', views.activateAccount, name = 'resend_code'),
    path('allusers/', views.allUsers, name='all_users'),
    path('account/', views.account, name = 'account'),
    path('userremove/<str:pk>/', views.userRemove, name='user_remove'),


    path('password_change/', 
    auth_views.PasswordChangeView.as_view(template_name = 'password/password_change.html'), 
    name = 'password_change'),

    path('password_change/done',
    auth_views.PasswordChangeDoneView.as_view(template_name = 'registration/account.html'),
    name = 'password_change_done')
]