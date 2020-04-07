import threading, time, schedule

import datetime

from django.utils import timezone

from statisticsManagement.models import TimelyRecord

counter = 0
mode = True

class Analyzer(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("Starting " + self.name)
        global counter, mode
        key = input("Press S to start, Q to stop.\n")
        while(key != 'q'):
            try:
                key = int(input("Increment: "))
                counter += key
            except:
                print("Please give a value")
            time.sleep(1)
        mode = False
        print("Exiting " + self.name)

class Recorder(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("Starting " + self.name)
        global counter, mode
        while(mode):
            schedule.run_pending()
            time.sleep(1)
        print("Exiting " + self.name)

pthread = Analyzer(1, "Video analyzer")
cthread = Recorder(2, "Recorder")

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
    schedule.every(10).minutes.do(record)

def runThreads():
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
    threading.Timer((exec_time - nownow).total_seconds(), schedule_recording).start()

    print("Timer started at: " + nownow.strftime("%H:%M:%S"))
    
    pthread.start()
    cthread.start()