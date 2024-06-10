from django.contrib import admin
from .models import (SemiAnnual2024Company, SemiAnnual2024Report, SemiAnnual2024UserCompany,
                     SemiAnnual2024CreatorsSummaryReport)


@admin.register(SemiAnnual2024Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'line_number')
    search_fields = ('name',)


@admin.register(SemiAnnual2024Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'company')
    list_filter = ('created_at', 'user', 'company')
    search_fields = ('user__username', 'company__name')


admin.site.register(SemiAnnual2024UserCompany)
admin.site.register(SemiAnnual2024CreatorsSummaryReport)
