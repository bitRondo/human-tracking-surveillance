from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'mainApp/index.html')

def login(request):
    return render(request, 'mainApp/login.html')
