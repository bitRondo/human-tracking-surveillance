from django.shortcuts import render, redirect

from django.http import HttpResponse

from .forms import SystemSettingsForm
import videoAnalysis.videoAnalysis as program

# urlname = system_settings
def system(request):
    mode = program.getMode()
    form = SystemSettingsForm()
    validMode = 2 if mode[0] == 1 else 1

    if request.method == 'POST':
        if request.POST['change_mode']:
            program.setMode(validMode)

    context = {
        'form' : form,
        'mode' : mode[1],
        'validMode' : program.modes.get(validMode),
    }
    return render(request, 'systemManagement/systemSettings.html', context)