from django.urls import path
from .views import (daily_reports, report_details, add_daily_report, edit_daily_report,
                    success_page, summary_report, access_denied_page, generate_summary_report)

urlpatterns = [
    path('', daily_reports, name='daily_reports'),  # Маршрут по умолчанию для списка отчётов
    path('report/<int:report_id>/', report_details, name='report_details'),  # Маршрут для деталей отчёта
    path('add_daily_report/', add_daily_report, name='add_daily_report'),
    path('edit_daily_report/<int:report_id>', edit_daily_report, name='edit_daily_report'),
    path('success_page/', success_page, name='success_page'),
    path('summary_report/', summary_report, name='summary_report'),
    path('access_denied_page/', access_denied_page, name='access_denied_page'),
    path('generate_summary_report/', generate_summary_report, name='generate_summary_report'),
]
