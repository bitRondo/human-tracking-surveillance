from django.db import models

from django.utils.translation import gettext_lazy as _

class TimelyRecord(models.Model):

    record_date = models.DateField(
        _('Record Date'),
    )

    record_time = models.TimeField(
        _('Record Time'),
    )

    record_count = models.IntegerField(
        _('Count of people'),
    )

class DailyRecord(models.Model):

    record_date = models.DateField(
        _('Record date'),
    )

    total_count = models.IntegerField(
        _('Record count'),
    )

    peak_hour_start = models.TimeField(
        _('Start of Peak hour'),
    )

    peak_hour_end = models.TimeField(
        _('End of Peak hour'),
    )

    @classmethod
    def fetchWithinRange(cls, start_date, end_date):
        return cls.objects.filter(record_date__range = (start_date, end_date))

    @classmethod
    def findPeakWithinRange(cls, start_date, end_date):
        result = cls.objects.filter(record_date__range = (start_date, end_date)).aggregate(models.Max('total_count'))
        peakValue = result['total_count__max']
        return cls.objects.filter(total_count = peakValue)