from .models import DailyRecord, TimelyRecord

from django.utils import timezone
import datetime

import random

'''
Method: save_all_timely_records
Description: Saves timely records in 30-min intervals on a given day
Params: date{required}: recording date as a 3-tuple (YYYY, MM, DD), initial_count: int, 
        start_time: recording start time as a 2-tuple (HH, MM), end_time = recording stop time as a 2-tuple (HH, MM)
'''
def save_all_timely_records(date, initial_count = 0, start_time = (0, 0), end_time = (23, 30)):
    startTime = datetime.datetime(date[0], date[1], date[2], start_time[0], start_time[1], 0)
    endTime = datetime.datetime(date[0], date[1], date[2], end_time[0], end_time[1], 0)
    for t in range(48):
        time = startTime + datetime.timedelta(minutes = 30*t)
        h = time.hour

        print("Date: " + time.date().strftime("%Y-%m-%d") 
        + "\tTime: " + time.time().strftime("%H:%M") 
        + "\tCount: " + str(initial_count))

        # # Uncomment the following 2 lines to save in the database
        # record = TimelyRecord(record_date = time.date(), record_time = time.time(), record_count = initial_count)
        # record.save()

        if h >= 8 and h < 12:
            initial_count += random.randint(1, 5)
        elif h >= 12 and h < 17:
            initial_count += random.randint(1, 10)
        elif h >= 17 and h < 20:
            initial_count += random.randint(1, 5)
        
        if time == endTime:
            break

'''
Method: save_all_daily_records
Description: Saves daily records on a given month
Params: date{required}: recording start date as a 3-tuple (YYYY, MM, DD), 
        end_date = recording stop date as a 3-tuple (YYYY, MM, DD)
'''
def save_all_daily_records(date, end_date = 0):
    startDate = datetime.datetime(date[0], date[1], date[2])

    if end_date: endDate = datetime.datetime(date[0], date[1], end_date)

    choices = [0, 30]

    for d in range(31):
        current_date = startDate + datetime.timedelta(hours = 24*d)
        if current_date.month > date[1]:
            break
        elif current_date.day > 12 and current_date.day < 25:
            count = random.randint(50, 150)
        else:
            count = random.randint(25, 50)

        peak_start = datetime.time(random.randint(10, 14), random.choice(choices))
        peak_end = datetime.time(peak_start.hour + 1, peak_start.minute)
        print("Date: " + current_date.strftime("%Y-%m-%d") +
                "\tCount: " + str(count) +
                "\tPeak time: " + peak_start.strftime("%H:%M") + " to " + peak_end.strftime("%H:%M"))

        # # Uncomment the following 3 lines to save in the database
        # record = DailyRecord(record_date = current_date, total_count = count, 
        # peak_hour_start = peak_start, peak_hour_end = peak_end)
        # record.save()

        if end_date and current_date == endDate:
            break


'''
Test code for shell:

from statisticsManagement.controllers import save_all_daily_records, save_all_timely_records
save_all_daily_records
save_all_timely_records

'''
