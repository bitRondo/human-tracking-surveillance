from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipientadd/',views.RecipientAdd,name='RecipientAdd'),
    path('email/',views.email,name='email'),
    path('recipientremove/',views.RecipientRemove,name='RecipientRemove')
]
