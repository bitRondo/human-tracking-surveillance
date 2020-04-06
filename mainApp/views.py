from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Surveillance system to detect and track humans")


# Create your views here.
