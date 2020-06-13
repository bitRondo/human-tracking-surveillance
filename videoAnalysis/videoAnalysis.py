import threading, time, schedule

import datetime

from django.utils import timezone

from statisticsManagement.models import TimelyRecord, DailyRecord
from statisticsManagement.controllers import sendMonthlyReport
from securityManagement.controllers import send_security_alert
from systemManagement.controllers import checkEmailConnectivity
from .HumanTrackingSystem import HumanTrackingSystem
from .HumanTrackingSystem import getNew
counter = 0
timelyCounts = {}
modes = {0 : 'Idle', 1 : 'Business', 2 : 'Security', 3 : 'Terminated'}
mode = 0
count=0
autoSwitch = False
autoSwitchingTimes = {'b_start' : None, 's_start' : None, 'b_end' : None, 's_end' : None}

shouldAlert = True

activeTimers = []

autoSwitchingScheduler = schedule.Scheduler()
reportingScheduler = schedule.Scheduler()
reportingJob = None
monthlyScheduler = schedule.Scheduler()

notifications = []

"""
NOTICE: NOW THIS SYSTEM IS SET FOR DEMONSTRATION PURPOSE
changes tagged as [definite] are made
"""

def setMode(n = 1):
    global mode, counter
    counter = 0
    shouldAlert = True
    if n != mode:
        if n in modes.keys():
            mode = n
        else: 
            print("Invalid mode!")
            mode = 3
        if mode == 1: start_timer()
        else : 
            end_timers()
            reportingJob = None # to make sure reportingJob cannot be referenced while in other modes
        print("Mode set to %s at %s"%(modes.get(mode), timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")))

def getMode():
    return modes.get(mode)

def getNextValidMode():
    if mode == 1: return 'Security'
    elif mode == 2: return 'Business'
    else: return 'Business'

def toggleAutoSwitch(condition, times = None):
    global autoSwitch, autoSwitchingTimes, mode
    autoSwitch = condition
    if autoSwitch:
        if times != autoSwitchingTimes:
            set_auto_switching_times(times)
            schedule_auto_switch_mode()
            print("Auto-Switching ON")
    else:
        if mode == 0: setMode() # set default to Business if current mode is Idle

def isAutoSwitching():
    return autoSwitch

def getAutoSwitchingTimes():
    return autoSwitchingTimes

def set_auto_switching_times(times):
    global autoSwitchingTimes
    autoSwitchingTimes.update(times)


class Analyzer(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self,  name = "Analyzer")

    def run(self):
        print("Starting Analyzer")
        global counter, mode
        key = 's'
        while(True):
            counter += getNew()
            time.sleep(1)
        mode = 3
        end_timers()
        print("Exitting Analyzer")

class Reporter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name = "Reporter")

    def run(self):
        global counter, mode, autoSwitch, shouldAlert
        print("Starting Reporter")
        while (mode != 3):
            monthlyScheduler.run_pending()
            if autoSwitch:
                autoSwitchingScheduler.run_pending()
            if (mode == 1):
                reportingScheduler.run_pending()
            elif (mode == 2):
                if counter:
                    print("Alert!")
                    if shouldAlert:
                        send_security_alert()
                        shouldAlert = False
            time.sleep(1)
        print("Exitting Reporter")

def record():
    global counter, timelyCounts
    now = timezone.localtime()
    nowString = now.strftime("%H:%M:%S")

    '''
    the following check is essential because this method is called by 2 instances:
    the reportingScheduler and the scheduled job - get_results_of_the_day
    '''
    if nowString not in timelyCounts:
        # # Uncomment following 6 lines to actually save data into database
        # rec = TimelyRecord(
        #     record_date = now.date(), 
        #     record_time = now.time().replace(microsecond = 0), 
        #     record_count = counter,
        # )
        # rec.save()
        print("Counter = %d"%counter, nowString)
        timelyCounts[nowString] = counter
        counter = 0

def schedule_recording():
    record()
    print("Scheduled at: " + timezone.localtime().strftime("%H:%M:%S"))

    global reportingJob
    reportingJob = reportingScheduler.every(30).seconds.do(record) # change
    reportingScheduler.every().day.at("00:00").do(record_at_end_of_day) # change
    end_timers()

def start_timer():
    end_timers()
    # Calculating the delay in which Scheduling should start at a 'ROUND' time
    now = timezone.localtime()
    if now.minute < 30:     # e.g. if now is 11:16, scheduling should start at 11:30
        hour, minute = now.hour, 30
    else:                   # e.g. if now is 11:34, scheduling should start at 12:00
        hour, minute = (now.hour + 1)%24, 0

    exec_time = datetime.datetime(now.year, now.month, now.day, hour = hour, minute = minute, 
    tzinfo = now.tzinfo)

    # Delaying the Scheduling until the next 'ROUND' time
    nownow = timezone.localtime() # the exact moment after the above calculations
    timer = threading.Timer((exec_time - nownow).total_seconds(), schedule_recording)
    timer.start()
    print("Scheduling will start at: " + exec_time.strftime("%H:%M:%S"))
    activeTimers.append(timer)

def end_timers():
    for timer in activeTimers:
        timer.cancel()

def schedule_auto_switch_mode():
    global autoSwitchingTimes
    if autoSwitchingTimes['b_start']:
        autoSwitchingScheduler.every().day.at(autoSwitchingTimes['b_start']).do(setMode, 1)
        print("Scheduled to set Mode to Business at %s" % autoSwitchingTimes['b_start'])
        if autoSwitchingTimes['b_end'] != autoSwitchingTimes['s_start']:
            autoSwitchingScheduler.every().day.at(autoSwitchingTimes['b_end']).do(setMode, 0)
            print("Scheduled to go Idle at %s" % autoSwitchingTimes['b_end'])
    if autoSwitchingTimes['s_start']:
        autoSwitchingScheduler.every().day.at(autoSwitchingTimes['s_start']).do(setMode, 2)
        print("Scheduled to set Mode to Security at %s" % autoSwitchingTimes['s_start'])
        if autoSwitchingTimes['s_end'] != autoSwitchingTimes['b_start']:
            autoSwitchingScheduler.every().day.at(autoSwitchingTimes['s_end']).do(setMode, 0)
            print("Scheduled to go Idle at %s" % autoSwitchingTimes['s_end'])

def get_results_of_day():
    if reportingJob: reportingJob.run() # to make sure first it records the last timely record of the day

    maxCount = 0
    timeStamps = list(timelyCounts.keys())
    totalCount = timelyCounts[timeStamps[0]]

    for t in range(len(timeStamps) - 1):
        hourlyCount = timelyCounts[timeStamps[t]] + timelyCounts[timeStamps[t + 1]]
        if hourlyCount >= maxCount: 
            maxCount = hourlyCount
            peakHourStart = datetime.time.fromisoformat(timeStamps[t])
        totalCount += timelyCounts[timeStamps[t + 1]]

    # a dummy date is required because timedelta operations can be done only with datetime objects
    dummyDate = datetime.datetime(100, 1, 1, peakHourStart.hour, peakHourStart.minute)

    # adjustments to properly represent the peak hour
    peakHourStart = (dummyDate - datetime.timedelta(seconds=30)).time() # change
    peakHourEnd = (dummyDate + datetime.timedelta(seconds=30)).time() # change

    return totalCount, peakHourStart, peakHourEnd

def record_at_end_of_day():
    totalCount, peakStart, peakEnd = get_results_of_day()
    # decreasing date by 1 day because this is executed past 00:00
    date = (timezone.localtime() - datetime.timedelta(days=1)).date()
    # # Uncomment following 2 lines to actually save data into database
    # rec = DailyRecord(
    #     record_date = date, total_count = totalCount, 
    #     peak_hour_start = peakStart, peak_hour_end = peakEnd
    # )
    # rec.save()
    print(date, totalCount, peakStart, peakEnd)

def send_monthly_report():
    today = datetime.datetime.today()
    if today.day != 2:
        return
    else:
        if checkEmailConnectivity():
            sendMonthlyReport()
        else:
            prevMonth = datetime.date(today.year, today.month - 1, 1)
            message = "Could not send Monthly Report of %s"%(prevMonth.strftime("%B, %Y"))
            addNotification(message)

monthlyScheduler.every().day.at("00:30").do(send_monthly_report) # change

def addNotification(n):
    global notifications
    notifications.append(n)    

def getNotifications():
    return notifications

def removeNotifications():
    global notifications
    notifications = []

def runMain():
    setMode(1)
    humanDetectionSystem=HumanTrackingSystem()
    humanDetectionSystem.start()
    Reporter().start()
    Analyzer().start()

'''
Do the following changes in testing/demonstration process:

function record:
1) Comment out the defined lines

function schedule_recording:
[definite]2) change every(30).minutes to every(30).seconds in reportingJob
3) change "00:00" to a time close to now

monthlyScheduler:
4) change every().day.at("00:30") to a time close to now

function start_timer:
5) add a line just before exec_time having an (hour, minute) tuple with values close to now

function get_results_of_day:
[definite]6) change minutes=30 to seconds=30 in both peakHourStart and peakHourEnd

function recordAtEndOfDay:
7) Comment out the defined lines
'''