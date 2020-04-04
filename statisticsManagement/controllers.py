from .models import DailyRecord, TimelyRecord

from django.utils import timezone
import datetime

import random

def save_timely_record():
    date = timezone.now().date()
    time = timezone.now().time().replace(microsecond = 0)
    count = random.randint(0,20)

    record = TimelyRecord(record_date = date, record_time = time, record_count = count)
    record.save()

def save_all_timely_records(date, initial_count):
    startTime = datetime.datetime(date[0], date[1], date[2], 0, 0, 0)
    for h in range(48):
        time = startTime + datetime.timedelta(minutes = 30*h)
        print("Date: " + time.date().strftime("%Y-%m-%d") 
        + "\tTime: " + time.time().strftime("%H:%M") 
        + "\tCount: " + str(initial_count))

        record = TimelyRecord(record_date = time.date(), record_time = time.time(), record_count = initial_count)
        record.save()

        if h > 16 and h < 24:
            initial_count += random.randint(1, 5)
        elif h >= 24 and h < 34:
            initial_count += random.randint(1, 10)
        elif h >= 34 and h < 40:
            initial_count += random.randint(1, 5)

def save_all_daily_records(date):
    startDate = datetime.datetime(date[0], date[1], date[2])
    choices = [0, 30]
    for d in range(31):
        current_date = startDate + datetime.timedelta(hours = 24*d)
        if current_date.month > date[1]:
            break
        elif current_date.day > 12 and current_date.day < 25:
            count = random.randint(50, 150)
        else:
            count = random.randint(25, 50)

        sample_date = datetime.datetime(2020, 4, 4, random.randint(10, 14), random.choice(choices))
        peak_start = sample_date.time()
        peak_end = (sample_date + datetime.timedelta(hours = 1)).time()
        print("Date: " + current_date.strftime("%Y-%m-%d") +
                "\tCount: " + str(count) +
                "\tPeak time: " + peak_start.strftime("%H:%M") + " to " + peak_end.strftime("%H:%M"))

        record = DailyRecord(record_date = current_date, total_count = count, 
        peak_hour_start = peak_start, peak_hour_end = peak_end)
        record.save()

'''
from statisticsManagement.controllers import save_all_daily_records
save_all_daily_records
'''
