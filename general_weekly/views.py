from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import WeeklyUserDepartment, WeeklyReport, WeeklyCreatorsSummaryReport
from .utils import friday_of_week
from commondata.forms import DateForm
from datetime import datetime
# from django.apps import apps
# from shutil import copy
# import os
# from openpyxl import load_workbook
# from datetime import timedelta

@login_required
def general_weekly(request):
    # Получаем текущего пользователя
    user = request.user
    # Получаем филиалы, к которым пользователь имеет отношение
    user_departments = WeeklyUserDepartment.objects.filter(user=user).values_list('department', flat=True)
    # Получаем все отчёты, связанные с этими филиалами, и сортируем их по дате отчёта
    reports = WeeklyReport.objects.filter(department__in=user_departments).order_by('-report_date')
    # Если форма отправлена методом POST
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['selected_date']
            # Фильтруем отчёты по выбранной дате
            reports = reports.filter(report_date=friday_of_week(selected_date))
    else:
        form = DateForm(initial={'selected_date': friday_of_week(datetime.now())})
    for report in reports:
        report.user_full_name = f"{report.author.first_name} {report.author.last_name}"
    summary_reports_creators = []
    first_summary_report = WeeklyCreatorsSummaryReport.objects.first()
    if first_summary_report:
        summary_reports_creators = [user.username for user in first_summary_report.creators.all()]
    return render(request, 'general_weekly/report_list.html',
                  {'reports': reports,
                   'form': form,
                   'summary_reports_creators': summary_reports_creators})
