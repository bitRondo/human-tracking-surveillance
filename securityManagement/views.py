from django.shortcuts import render, redirect 
from django.core.mail import send_mail

from django.http import HttpResponse
from .models import Recipient
from  .forms import RecipientAddForm


def Security(request):
    recipient=Recipient.objects.all()
    return render(request,'security.html',{'Recipient':recipient})

def RecipientAdd(request):
    form =RecipientAddForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/securityManagement')
       

    form = RecipientAddForm()
    return render (request, 'recipientAdd.html',{'form':form})

def RecipientRemove(request,pk):
    recipient=Recipient.objects.get(id=pk)
    if request.method=="POST":
        recipient.delete()
        return redirect('/securityManagement')
    contex={'item':recipient}
    return render(request,'recipientRemove.html',contex)


def RecipientEdit(request,pk):
    form =RecipientAddForm()
    return render (request, 'recipientAdd.html',{'form':form})


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