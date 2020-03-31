from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from datetime import timedelta

from .forms import CustomizedUserCreationForm

from .controllers import send_activation_key

import random

def index(request):
    if request.user.is_authenticated:
        if request.user.activation_key != '':
            return render(request, 'activation/notActivated.html')
    return render(request, 'accountManagement/index.html')

def register(request):

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

    context = {'form' : form}

    return render(request, 'registration/register.html', context)

def activateAccount(request, resend_requested = ''):
    user = request.user

    if user.is_authenticated:

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
            }

            if (resend_requested == 'new'):
                print ("new")
                send_activation_key(user, True)

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
    else:
        return redirect('index')