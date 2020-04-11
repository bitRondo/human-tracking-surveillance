from django.shortcuts import render

from django.http import HttpResponse
from .models import Recipient
from  .forms import RecipientAddForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def RecipientAdd(request):
    form =RecipientAddForm(request.POST)
    if form.is_valid():
        form.save()
       

    form = RecipientAddForm()
    return render (request, 'recipientAdd.html',{'form':form})
# Create your views here.