from django.urls import path
from .views import general_weekly, general_weekly_report_details, general_weekly_access_denied_page, \
    add_general_weekly_report

urlpatterns = [
    path('', general_weekly, name='general_weekly'),  # Маршрут по умолчанию
    path('report/<int:report_id>/', general_weekly_report_details, name='general_weekly_report_details'),
    path('add_general_weekly_report/', add_general_weekly_report, name='add_general_weekly_report'),
    path('access_denied_page/', general_weekly_access_denied_page, name='general_weekly_access_denied_page'),
]

