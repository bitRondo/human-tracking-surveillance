from django.db import models
from django.db.models import Sum

class DailyRecord(models.Model):
    record_date = models.DateField()

    total_count = models.IntegerField()

    peak_hour_start = models.TimeField()

    peak_hour_end = models.TimeField()

# Create your models here.
