from django.contrib import admin


from .models import DailyRecord
from .models import TimelyRecord

admin.site.register(DailyRecord)
admin.site.register(TimelyRecord)

# Register your models here.
