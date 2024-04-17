from django.contrib import admin
from .models import UserDepartment, DailyReport, CreatorsSummaryReport


admin.site.register(UserDepartment)


class DailyReportAdmin(admin.ModelAdmin):
    list_display = (
        'report_date', 'author', 'department', 'field_1', 'field_2', 'field_3', 'field_4', 'field_5', 'field_6',
        'field_7', 'field_8', 'field_9', 'field_10', 'field_11')
    list_filter = ('report_date', 'author', 'department')


admin.site.register(DailyReport, DailyReportAdmin)
admin.site.register(CreatorsSummaryReport)
