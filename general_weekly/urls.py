from django.urls import path
from .views import general_weekly, general_weekly_report_details, general_weekly_access_denied_page, \
    add_general_weekly_report, edit_general_weekly_report, success_page, generate_general_weekly_summary_report

urlpatterns = [
    path('', general_weekly, name='general_weekly'),  # Маршрут по умолчанию
    path('report/<int:report_id>/', general_weekly_report_details, name='general_weekly_report_details'),
    path('add_general_weekly_report/', add_general_weekly_report, name='add_general_weekly_report'),
    path('edit_daily_report/<int:report_id>', edit_general_weekly_report, name='edit_general_weekly_report'),
    path('access_denied_page/', general_weekly_access_denied_page, name='general_weekly_access_denied_page'),
    path('success_page/', success_page, name='success_page'),
    path('generate_summary_report/', generate_general_weekly_summary_report, name='generate_general_weekly_summary_report'),
]

