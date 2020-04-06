from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Recipient
from .forms import RecipientForm


def index(request):
    return HttpResponse("Surveillance system to detect and track humans")


def recipient(request):
    form = RecipientForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request,'recipient.html',context)

# Create your views here.
