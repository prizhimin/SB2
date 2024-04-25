from django.contrib import admin
from .models import WeeklyReport, WeeklyUserDepartment, WeeklyCreatorsSummaryReport


# Register your models here.

class WeeklyReportAdmin(admin.ModelAdmin):
    list_filter = ('report_date', 'author', 'department')


admin.site.register(WeeklyReport, WeeklyReportAdmin)
admin.site.register(WeeklyUserDepartment)
admin.site.register(WeeklyCreatorsSummaryReport)
