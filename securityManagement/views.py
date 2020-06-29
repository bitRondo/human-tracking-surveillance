from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import user_passes_test

from django.http import HttpResponse

from accountManagement.controllers import checkIsAdmin
from .models import Recipient
from .forms import RecipientAddForm

@user_passes_test(checkIsAdmin, login_url='index')
def Security(request):
    recipients = Recipient.objects.all()
    return render(request,'security.html', {'Recipient':recipients} )

@user_passes_test(checkIsAdmin, login_url='index')
def RecipientAdd(request):
    form = RecipientAddForm()
    
    if request.method == 'POST':
        form = RecipientAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/securityManagement')
       
    return render (request, 'recipientAdd.html',{'form':form})



@user_passes_test(checkIsAdmin, login_url='index')
def RecipientRemove(request,pk):
    recipient = Recipient.objects.get(id = pk)
    if request.method=="POST":
        recipient.delete()
        return redirect('/securityManagement')
    context = {'item' : recipient}
    return render(request, 'recipientRemove.html', context)



@user_passes_test(checkIsAdmin, login_url='index') 
def RecipientEdit(request,pk):
    recipient = Recipient.objects.get(id=pk)
    form = RecipientAddForm(instance=recipient)

    if request.method == 'POST':
        form = RecipientAddForm(request.POST , instance=recipient)
        if form.is_valid():
            form.save()
            return redirect('/securityManagement')
       
    
    return render (request, 'recipientAdd.html',{'form':form})

# def alert(request):
#     return render(request, 'alert.html')