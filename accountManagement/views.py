from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login

from .forms import CustomizedUserCreationForm

def index(request):
    return render(request, 'accountManagement/index.html')

def register(request):

    if request.method == 'POST':
        form = CustomizedUserCreationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            form.save()

            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('index')

    else:
        form = CustomizedUserCreationForm()

    context = {'form' : form}

    return render(request, 'registration/register.html', context)
