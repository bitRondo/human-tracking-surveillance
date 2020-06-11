from .models import DailyRecord, TimelyRecord
from accountManagement.models import User

import os.path
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker

from django.utils import timezone
import datetime
import calendar

import random

'''
from statisticsManagement.controllers import sendMonthlyReport
sendMonthlyReport()
'''

def createChart(records, peakValue):
    data = [[]]
    for r in records:
        data[0].append((r.record_date.day, r.total_count))

    chart = LinePlot()
    chart.data = data
    chart.x, chart.y = 5, 5
    chart.height, chart.width = 200, 400

    chart.xValueAxis.valueMin = 1
    chart.xValueAxis.valueStep = 1
    chart.yValueAxis.valueMin = 0
    chart.yValueAxis.valueMax = (peakValue//10)*10 + 10
    chart.yValueAxis.valueStep = 10

    chart.lines[0].symbol = makeMarker('Circle')
    chart.lineLabelFormat = "%d"

    drawing = Drawing()
    drawing.add(chart) 

    return drawing

def createTable(records):
    data = [
        ["Date", "Total Count", "Peak Hour"],
    ]

    for r in records:
        date = r.record_date.strftime("%Y-%m-%d")
        peakHour = "%s to %s"%(r.peak_hour_start.strftime("%H:%M"),r.peak_hour_end.strftime("%H:%M"))
        data.append([date, r.total_count, peakHour])

    table = Table(data, colWidths=(1.5*inch, inch, 2*inch))

    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('ALIGN', (0,0), (-1,-1), 'CENTRE')
    ])
    table.setStyle(style)

    return table

"""
returns a PDF containing a graph and a list of statistics for the given month of firstDay
returns None if no data is available for that month
"""
def createPDF(firstDay):
    lastDay = firstDay.replace(day=calendar.monthrange(firstDay.year, firstDay.month)[1])
    records = DailyRecord.fetchWithinRange(firstDay, lastDay)

    if records:
        folder = os.path.join("statisticsManagement", "monthly_reports")
        filename = os.path.join(folder, "HTS_Monthly_Report_%s.pdf"%(firstDay.strftime("%B_%Y")))
        pdf = SimpleDocTemplate(
            filename=filename,
            pagesize=letter,
            rightmargin=72, leftmargin=72, topmargin=72, bottommargin=72
        )

        contents = []
        styles = getSampleStyleSheet()

        title1 = Paragraph("Monthly Report - %s"%(firstDay.strftime("%B, %Y")), styles['Heading1'])
        title2 = Paragraph("Counting Statistics", styles['Heading2'])

        contents.append(title1)
        contents.append(title2)
        noteString = Paragraph("This is a system-generated document.", styles['Normal'])
        contents.append(noteString)
        contents.append(Spacer(1, inch))

        peakDays = DailyRecord.findPeakWithinRange(firstDay, lastDay)
        peakValue = peakDays[0].total_count

        chart = createChart(records, peakValue)

        contents.append(chart)

        contents.append(Spacer(1, inch))

        peakTitleString = "Peak Day" if len(peakDays) == 1 else "Peak Days"
        peakTitleString += "\t(Total Count = %d) :"%(peakValue)
        peakTitle = Paragraph(peakTitleString, styles['Heading3'])

        contents.append(peakTitle)

        for day in peakDays:
            dayString = day.record_date.strftime("%Y-%m-%d")
            peakDay = Paragraph(dayString, styles['Normal'])
            contents.append(peakDay)

        contents.append(PageBreak())

        styles['Heading4'].alignment = 1
        listViewTitle = Paragraph("Daily records in detail", styles['Heading4'])
        contents.append(listViewTitle)
        contents.append(Spacer(1, 0.25*inch))

        table = createTable(records)
        contents.append(table)

        pdf.build(contents)
        return filename
    else: return None

"""
Returns 1 if sent to all recipients, 0 if sending failed, -1 if no data available
That way, we can be sure that no empty reports are sent.
"""
def sendMonthlyReport():
    today = datetime.datetime.today()
    firstDayOfPastMonth = datetime.date(today.year, today.month - 1, 1)
    pdf = [createPDF(firstDayOfPastMonth)]

    if pdf:
        recpients = User.objects.filter(receive_reports = True)
        month = firstDayOfPastMonth.strftime("%B, %Y")
        subject = "Monthly Report - %s"%(month)
        message = ("Please find the attached PDF document containing Counting statistics of %s"%(month))

        sentStatus = 1
        for r in recpients:
            sent = r.email_user_with_attachments(subject, message, pdf)
            if not sent: 
                sentStatus = 0

        return sentStatus
    else: return -1

'''
params: date = 3-tuple (YYYY, MM, DD)
'''
def save_all_timely_records(date):
    timelyCounts = {}
    startTime = datetime.datetime(date[0], date[1], date[2], 0, 0)
    for t in range(48):
        time = startTime + datetime.timedelta(minutes = 30*t)
        h = time.hour
        count = 0
        if h >= 8 and h < 12:
            count = random.randint(1, 5)
        elif h >= 12 and h < 17:
            count = random.randint(1, 10)
        elif h >= 17 and h < 20:
            count = random.randint(1, 5)
        timelyCounts[time.strftime("%H:%M:%S")] = count
    
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
    peakHourStart = (dummyDate - datetime.timedelta(minutes=30)).time()
    peakHourEnd = (dummyDate + datetime.timedelta(minutes=30)).time()

    record_string = ""
    for k in list(timelyCounts.keys()):
        record_string += "%s,%s,%d"%(startTime.strftime("%Y-%m-%d"), k, timelyCounts[k]) + "\n"

    return str(totalCount), peakHourStart.strftime("%H:%M:%S"), peakHourEnd.strftime("%H:%M:%S"), record_string

def save_all_records(startDate, endDate):
    start_date = datetime.datetime(startDate[0], startDate[1], startDate[2], 0, 0)
    end_date = datetime.datetime(endDate[0], endDate[1], endDate[2], 0, 0)

    timely_string = ""
    daily_string = ""

    date = start_date
    while date <= end_date:
        record = save_all_timely_records((date.year, date.month, date.day))
        timely_string += record[3]
        daily_record = "%s,%s,%s,%s"%(date.strftime("%Y-%m-%d"), record[0], record[1], record[2])
        daily_string += daily_record + "\n"
        
        date = date + datetime.timedelta(days=1)

    folder = os.path.join("statisticsManagement", "dummy_data")
    timely_filename = os.path.join(folder, "%s to %s timely.txt"%
    (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
    daily_filename = os.path.join(folder, "%s to %s daily.txt"%
    (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))

    t = open(timely_filename, "w")
    t.write(timely_string.strip())
    t.close()

    d = open(daily_filename, "w")
    d.write(daily_string.strip())
    d.close()

def saveAllToDatabase(timely_filename = None, daily_filename = None):
    folder = os.path.join("statisticsManagement", "dummy_data")
    if timely_filename:
        timely_filename = os.path.join(folder, timely_filename)
        t = open(timely_filename, "r")
        t_lines = t.readlines()
        t.close()
        for line in t_lines:
            if line != '':
                content = line.strip().split(',')
                rec_date = datetime.date.fromisoformat(content[0])
                rec_time = datetime.time.fromisoformat(content[1])
                rec_count = int(content[2])
                record = TimelyRecord(record_date = rec_date, 
                record_time = rec_time, record_count = rec_count)
                record.save()
                print(record)
    if daily_filename:
        daily_filename = os.path.join(folder, daily_filename)
        d = open(daily_filename, "r")
        d_lines = d.readlines()
        d.close()
        for line in d_lines:
            if line != '':
                content = line.strip().split(',')
                rec_date = datetime.date.fromisoformat(content[0])
                rec_count = int(content[1])
                peak_start = datetime.time.fromisoformat(content[2])
                peak_end = datetime.time.fromisoformat(content[3])
                record = DailyRecord(record_date = rec_date, total_count = rec_count, 
                peak_hour_start = peak_start, peak_hour_end = peak_end)
                record.save()
                print(record.total_count)

'''
from statisticsManagement.controllers import save_all_records, saveAllToDatabase
save_all_records((2020,4,1), (2020,4,30))
saveAllToDatabase(timely_filename = "")
'''