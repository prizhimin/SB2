from django.urls import path
from . import views

app_name = 'daily_reports'

urlpatterns = [
    path('', views.daily_reports, name='daily_reports'),  # Маршрут по умолчанию для списка отчётов
    path('report/<int:report_id>/', views.report_details, name='report_details'),  # Маршрут для деталей отчёта
    path('add_daily_report/', views.add_daily_report, name='add_daily_report'),
    path('edit_daily_report/<int:report_id>', views.edit_daily_report, name='edit_daily_report'),
    path('summary_report/', views.summary_report, name='summary_report'),
    path('generate_summary_report/', views.generate_summary_report, name='generate_summary_report'),
    path('summary_weekly_report/', views.summary_weekly_report, name='summary_weekly_report'),
    path('generate_weekly_summary_report/', views.generate_weekly_summary_report, name='generate_weekly_summary_report'),
]
