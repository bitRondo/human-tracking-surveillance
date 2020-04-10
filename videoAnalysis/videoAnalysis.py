import threading, time, schedule

import datetime

from django.utils import timezone

from statisticsManagement.models import TimelyRecord

counter = 0
modes = {0 : 'Idle', 1 : 'Business', 2 : 'Security', 3 : 'Terminated'}
mode = 0
autoSwitch = False
activeTimers = []

autoSwitchingScheduler = schedule.Scheduler()
reportingScheduler = schedule.Scheduler()


def setMode(n = 1):
    global mode, counter
    counter = 0

    if n in modes.keys():
        mode = n
    else: 
        print("Invalid mode!")
        mode = 4
    if mode == 1: startTimer()
    else : endTimers()
    print("Mode set to %d at %s"%(mode, timezone.localtime().strftime("%Y-%m-%d %H:%M")))

def getMode():
    return mode, modes.get(mode)

def setAutoSwitch(condition = True):
    global autoSwitch
    autoSwitch = condition

class Analyzer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self,  name = "Analyzer")

    def run(self):
        print("Starting Analyzer")
        global counter, mode
        key = 's'
        while(key != 'q'):
            key = input("Increment: ")
            try:
                counter += int(key)
            except:
                if key != 'q': print("Please give a value")
            time.sleep(1)
        mode = 3
        endTimers()
        print("Exitting Analyzer")

class Reporter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name = "Reporter")

    def run(self):
        global counter, mode, autoSwitch
        print("Starting Reporter")
        while (mode != 3):
            if autoSwitch:
                autoSwitchingScheduler.run_pending()
            if (mode == 1):
                reportingScheduler.run_pending()
            elif (mode == 2):
                if counter:
                    print("Alert!")
            time.sleep(1)
        print("Exitting Reporter")

def record():
    now = timezone.now()
    # # Uncomment following lines 52-57 to actually save data into database
    # rec = TimelyRecord(
    #     record_date = now.date(), 
    #     record_time = now.time().replace(microsecond = 0), 
    #     record_count = counter,
    # )
    # rec.save()
    print("Counter = %d"%counter, now.strftime("%H:%M:%S"))

def schedule_recording():
    record()
    print("Scheduled at: " + timezone.now().strftime("%H:%M:%S"))
    reportingScheduler.every(30).seconds.do(record)

def startTimer():
    endTimers()
    # Calculating the delay in which Scheduling should start at a 'ROUND' time
    now = timezone.now()
    if now.minute < 30:     # e.g. if now is 11:16, scheduling should start at 11:30
        hour, minute = now.hour, 30
    else:                   # e.g. if now is 11:34, scheduling should start at 12:00
        hour, minute = now.hour + 1, 0

    exec_time = datetime.datetime(now.year, now.month, now.day, hour = hour, minute = minute, 
    tzinfo = timezone.get_current_timezone())

    # Delaying the Scheduling until the next 'ROUND' time
    nownow = timezone.now() # the exact moment after the above calculations
    timer = threading.Timer((exec_time - nownow).total_seconds(), schedule_recording)
    timer.start()
    print("Scheduling will start at: " + exec_time.strftime("%H:%M:%S"))
    activeTimers.append(timer)

def endTimers():
    for timer in activeTimers:
        timer.cancel()

def switch_mode(business_start, security_start, idle_start):
    autoSwitchingScheduler.every().day.at(business_start).do(setMode, 1)
    autoSwitchingScheduler.every().day.at(security_start).do(setMode, 2)
    autoSwitchingScheduler.every().day.at(idle_start).do(setMode, 0)

def runMain():
    setMode(1)
    Reporter().start()
    Analyzer().start()


# The following 2 classes and runThreads method are not used.
'''
class Business(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("Starting " + self.name)

        global counter, mode
        while (mode != 4):
            if (mode == 1):
                schedule.run_pending()
            time.sleep(1)
        print("Exiting " + self.name)

class Security(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("Starting " + self.name)
        global counter, mode
        while(mode != 4):
            if (mode == 2):
                if counter:
                    print("Alert!")
            time.sleep(1)
        print("Exiting " + self.name)    

def runThreads():
    bthread = Business(1, "Business")
    bthread.start()

    sthread = Security(2, "Security")
    sthread.start()
    
    pthread = Analyzer(0, "Video analyzer")
    pthread.start()

'''

'''
import videoAnalysis.videoAnalysis as v
v.switch_mode()
v.setAutoSwitch()
v.runMain()
'''