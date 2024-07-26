from django.urls import path
from . import views

app_name = 'sixmonths2024'

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('create/', views.create_report, name='create_report'),
    path('update/<int:pk>/', views.update_report, name='update_report'),
    path('report/delete/<int:pk>/', views.delete_report, name='delete_report'),
    path('generate_sixmonths_2024_summary_report/', views.generate_sixmonths_2024_summary_report,
         name='generate_sixmonths_2024_summary_report')
]