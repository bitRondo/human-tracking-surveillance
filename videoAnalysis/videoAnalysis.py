import threading, time, schedule

import datetime

from django.utils import timezone

from statisticsManagement.models import TimelyRecord

counter = 0
modes = {0 : 'Started', 1 : 'Business', 2 : 'Security', 3 : 'Auto-Switching', 4 : 'Terminated'}
mode = 0
activeTimers = []


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
    print("Mode set to %d"%mode)

def getMode():
    return mode, modes.get(mode)

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
        mode = 4
        endTimers()
        print("Exitting Analyzer")

class Reporter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name = "Reporter")

    def run(self):
        global counter, mode
        print("Starting Reporter")
        while (mode != 4):
            if (mode == 1):
                schedule.run_pending()
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
    schedule.every(1).minutes.do(record)

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

def runMain():
    setMode(1)
    Reporter().start()
    Analyzer().start()

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