from django.urls import path
from .views import (daily_reports, report_details, add_daily_report, edit_daily_report, summary_report,
                    generate_summary_report, summary_weekly_report)

urlpatterns = [
    path('', daily_reports, name='daily_reports'),  # Маршрут по умолчанию для списка отчётов
    path('report/<int:report_id>/', report_details, name='report_details'),  # Маршрут для деталей отчёта
    path('add_daily_report/', add_daily_report, name='add_daily_report'),
    path('edit_daily_report/<int:report_id>', edit_daily_report, name='edit_daily_report'),
    path('summary_report/', summary_report, name='summary_report'),
    path('generate_summary_report/', generate_summary_report, name='generate_summary_report'),
    path('generate_summay_weekly_report/', summary_weekly_report, name='summary_weekly_report')
]
