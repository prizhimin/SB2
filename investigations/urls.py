from django.urls import path

from . import views

app_name = 'investigations'

urlpatterns = [
    path('', views.investigation_list, name='investigation_list'),
    path('add/', views.add_investigation, name='add_investigation'),
    path('<int:pk>/', views.investigation_detail, name='investigation_detail'),
    path('<int:pk>/edit/', views.edit_investigation, name='edit_investigation'),
    path('<int:pk>/delete/', views.delete_investigation, name='delete_investigation'),
    path('<int:pk>/manage_attach', views.manage_attach, name='manage_attach'),
    path('<int:investigation_id>/attach/', views.attach_file, name='attach_file'),
    path('<int:investigation_id>/zipattach/', views.download_attaches_zip, name='download_attaches_zip'),
    path('file/<int:file_id>/delete/', views.delete_file, name='delete_file'),
    path('file/<int:file_id>/download/', views.download_file, name='download_file'),
    path('summary_report/', views.summary_report, name='summary_report'),
    path('generate_summary_report/<int:operation_id>', views.generate_summary_report, name='generate_summary_report'),
]
