from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.utils import timezone

from .forms import SystemSettingsForm
import videoAnalysis.videoAnalysis as program

modeDict = {'Business' : 1, 'Security' : 2}

# urlname = system_settings
def system(request):
    mode = program.getMode()
    is_auto_switching = program.isAutoSwitching()
    auto_switch = 'on' if is_auto_switching else 'off'

    autoSwitchingTimes = program.getAutoSwitchingTimes()

    form = SystemSettingsForm(
        initial = {
            'auto_switching' : auto_switch,
            'business_start' : autoSwitchingTimes['b_start'],
            'security_start' : autoSwitchingTimes['s_start'],
            'business_end' : autoSwitchingTimes['b_end'],
            'security_end' :autoSwitchingTimes['s_end'],
        }
    )


    if request.method == 'POST':
        form = SystemSettingsForm(request.POST)

        if 'change_mode' in request.POST.keys():
            program.toggleAutoSwitch(False)
            program.setMode(modeDict.get(request.POST['change_mode']))
            mode = program.getMode()
        elif 'auto_switch' in request.POST.keys():
            if request.POST['auto_switching'] == 'on':
                if form.is_valid():
                    times = {
                        'b_start' : request.POST['business_start'],
                        's_start' : request.POST['security_start'],
                        'b_end' : request.POST['business_end'],
                        's_end' : request.POST['security_end']
                    } 
                    program.toggleAutoSwitch(True, times)
            else:
                program.toggleAutoSwitch(False)

    context = {
        'form' : form,
        'mode' : mode,
        'validMode' : program.getNextValidMode(),
        'auto_switching_disabled' : not is_auto_switching
    }
    return render(request, 'systemManagement/systemSettings.html', context)