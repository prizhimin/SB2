from django.contrib import admin
from .models import WeeklyReport, WeeklyUserDepartment, WeeklyCreatorsSummaryReport


# Register your models here.
admin.site.register(WeeklyReport)
admin.site.register(WeeklyUserDepartment)
admin.site.register(WeeklyCreatorsSummaryReport)
