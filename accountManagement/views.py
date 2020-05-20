from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test

from django.utils import timezone
from datetime import timedelta

from .forms import CustomizedUserCreationForm

from .controllers import send_activation_key, checkIsAdmin

from systemManagement.controllers import checkEmailConnectivity
import videoAnalysis.videoAnalysis as va

from .models import User
import random

def index(request):
    if request.user.is_authenticated:
        context = {'notif' : []}
        if request.user.activation_key != '':
            return render(request, 'activation/notActivated.html')
        if request.user.is_staff:
            context['notif'] = va.getNotifications()
            va.removeNotifications()
        return render(request, 'accountManagement/index.html', context)
    return redirect('login')

@login_required
def allUsers(request):
    all_users=User.objects.all()
    return render(request,'registration/allUsers.html',{'all_users':all_users})

@user_passes_test(checkIsAdmin, login_url='index')
def register(request):
    if checkEmailConnectivity():
        if request.method == 'POST':
            form = CustomizedUserCreationForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                form.save()

                user = authenticate(username = username, password = password)

                send_activation_key(user)
                login(request, user)
                return redirect('activate')

        else:
            form = CustomizedUserCreationForm()

        context = {'form' : form, 'connectivity' : True}
    else:
        context = {'connectivity' : False}

    return render(request, 'registration/register.html', context)

@login_required
def activateAccount(request, resend_requested = ''):
    user = request.user
    if user.activation_key == '':
        return redirect('index')

    else:
        context = { 
            'user_email' : user.email,
            'invalid' : False,
            'expired' : False,
            'resend' : False,
            'resend_requested' : resend_requested,
            'empty' : False,
            'connectivity' : True,
        }

        if (resend_requested == 'new'):
            print ("new")
            if checkEmailConnectivity():
                send_activation_key(user, True)
            else:
                context['connectivity'] = False

        if request.method == 'POST':
            key_given = request.POST['key_given']
            keyString = ''.join(key_given.strip().split('-'))

            if keyString == user.activation_key:    
                difference = timezone.now() - user.key_expiry
                if (difference <= timedelta(hours = 24)):
                    print("OK")
                    user.activate_user()
                    return redirect('index')

                else:
                    context['expired'] = True
                    context['resend'] = True
                    print("code expired")

            elif keyString == '':
                context['empty'] = True

            else:
                context['invalid'] = True
                context['resend'] = True
                print("invalid code")

        return render(request, 'activation/activationForm.html', context)

@login_required
def account(request):

    context = {
        'user' : request.user
    }

    if request.method == 'POST':
        condition = request.POST['receive_reports']
        if condition == 'on':
            reception = True
        else:
            reception = False
        request.user.receive_reports = reception
        request.user.save()
        return redirect('account')

    return render(request, 'registration/account.html', context)

@login_required
def userRemove(request,pk):
    u = User.objects.get(id = pk)
    if request.method=="POST":
        u.delete()
        return redirect('/allusers')
    context = {'item' : u}
    return render(request, 'registration/userRemove.html', context)