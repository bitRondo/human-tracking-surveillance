from .models import DailyRecord, TimelyRecord

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

def createPDF(firstDay):
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

    lastDay = firstDay.replace(day=calendar.monthrange(firstDay.year, firstDay.month)[1])
    records = DailyRecord.fetchWithinRange(firstDay, lastDay)
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

def sendMonthlyReport():
    today = datetime.datetime.today()
    firstDayOfPastMonth = datetime.date(today.year, today.month - 1, 1)
    createPDF(firstDayOfPastMonth)

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

