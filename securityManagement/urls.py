from django.urls import path

from . import views

urlpatterns = [
    path('', views.Security, name='Security'),
    path('recipientadd/',views.RecipientAdd,name='RecipientAdd'),
    path('email/',views.email,name='email'),
    path('recipientremove/<str:pk>/',views.RecipientRemove,name='RecipientRemove'),
    path('recipientedit/<str:pk>/',views.RecipientEdit,name='RecipientEdit')
]
