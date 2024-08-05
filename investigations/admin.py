from django.contrib import admin
from investigations.models import Department, InvestigationUserDepartment, InvestigationCreatorsSummaryReport
from investigations.models import Investigation

class DepartmentAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    ordering = ('name',)
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Department, DepartmentAdmin)
admin.site.register(InvestigationCreatorsSummaryReport)
admin.site.register(InvestigationUserDepartment)
admin.site.register(Investigation)
