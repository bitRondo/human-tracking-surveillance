from django.shortcuts import render
from django.core.mail import send_mail

from django.http import HttpResponse
from .models import Recipient
from  .forms import RecipientAddForm


def index(request):
    return render(request,'security.html')

def RecipientAdd(request):
    form =RecipientAddForm(request.POST)
    if form.is_valid():
        form.save()
       

    form = RecipientAddForm()
    return render (request, 'recipientAdd.html',{'form':form})

def RecipientRemove(request):
    all_recipient=Recipient.objects.all()
    return render(request,'recipientRemove.html',{'Recipient':all_recipient})

def email(request):
   
    all_recipient=Recipient.objects.values_list('email')
    for email in all_recipient:

        send_mail(
        'security Alerts', #subject
        'surveillance system', #message
        'surveillancesystemcse@gmail.com', #from
        email, #to
            fail_silently = False
        )
    return render(request,'email.html')
    
 
  
  #print ( Recipient.objects.all())

    

# Create your 
# views here.