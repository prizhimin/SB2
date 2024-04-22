from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta

from commondata.models import Department
from commondata.forms import DateForm, DateSelectionForm
from .forms import WeeklyReportForm
from .models import WeeklyUserDepartment, WeeklyReport, WeeklyCreatorsSummaryReport
from .utils import friday_of_week
from .decorators import general_weekly_check_user_department, check_general_weekly_summary_report_creator


# from django.apps import apps
# from shutil import copy
# import os
# from openpyxl import load_workbook
# from datetime import timedelta

@login_required
def general_weekly(request):
    """
    Список отчётов
    """
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
        report.user_full_name = f"{report.author.last_name} {report.author.first_name}"
    summary_reports_creators = []
    first_summary_report = WeeklyCreatorsSummaryReport.objects.first()
    if first_summary_report:
        summary_reports_creators = [user.username for user in first_summary_report.creators.all()]
    return render(request, 'general_weekly/report_list.html',
                  {'reports': reports,
                   'form': form,
                   'summary_reports_creators': summary_reports_creators})


@login_required
@general_weekly_check_user_department
def general_weekly_report_details(request, report_id):
    """
    Детализированный отчёт
    :param request:
    :param report_id:
    :return:
    """
    # Получаем объект отчёта по его id
    report = get_object_or_404(WeeklyReport, pk=report_id)
    # Объединяем имя и фамилию пользователя через пробел
    user_full_name = f"{report.author.last_name} {report.author.first_name}"
    return render(request, 'general_weekly/report_details.html', {'report': report, 'user_full_name': user_full_name})


@login_required
def add_general_weekly_report(request):
    """
    Добавление отчёта
    :param request:
    :return:
    """
    if request.method == 'POST':
        # Создаем экземпляр формы ежедневного отчёта, передавая текущего пользователя и данные из POST-запроса
        form = WeeklyReportForm(request.user, request.POST)  # Передаем объект пользователя в форму
        if form.is_valid():  # Проверяем валидность данных формы
            weekly_report = form.save(commit=False)  # Создаем объект ежедневного отчёта, не сохраняя его в базу данных
            weekly_report.author = request.user  # Устанавливаем автора отчёта
            weekly_report.save()  # Сохраняем отчёт в базу данных
            # Перенаправляем пользователя на success_page в случае успешного сохранения отчёта
            return redirect(success_page)
    else:
        # Получаем первое подразделение пользователя, если оно есть
        first_user_department = WeeklyUserDepartment.objects.filter(user=request.user).first()
        if first_user_department:
            first_department = first_user_department.department.first()
        else:
            # Иначе получаем первое подразделение в системе
            first_department = Department.objects.first()
        # Создаем экземпляр формы ежедневного отчёта с начальными данными,
        # передавая текущего пользователя и первое доступное пользователю подразделение
        form = WeeklyReportForm(request.user, initial={
            'department': first_department})  # Передаем объект пользователя и начальные значения в форму
    # Отображаем шаблон add_daily_report.html с переданной формой
    return render(request, 'general_weekly/add_general_weekly_report.html', {'form': form})


@login_required
@general_weekly_check_user_department
def edit_general_weekly_report(request, report_id):
    """
    Редактирование отчёта
    """
    # Получаем отчёт по его идентификатору
    report = get_object_or_404(WeeklyReport, id=report_id)
    # Получаем текущее время в часовом поясе Москвы
    current_time = timezone.now()
    # Проверяем, прошло ли меньше 1 часа с момента создания отчёта
    if current_time - report.created_at > timedelta(hours=1):
        # Если прошло более часа, переходим на страницу с сообщением об ошибке
        return render(request, 'general_weekly/error_edit_report.html')
    if request.method == 'POST':
        # Если запрос метода POST, обрабатываем форму
        form = WeeklyReportForm(request.user, request.POST, instance=report)
        if form.is_valid():
            # Если форма валидна, сохраняем отчёт
            weeklw_report = form.save(commit=False)
            weeklw_report.author = request.user
            weeklw_report.save()
            # Перенаправляем пользователя на страницу успешного завершения
            return redirect(success_page)
    else:
        # Если запрос метода GET, отображаем форму для редактирования
        form = WeeklyReportForm(request.user, instance=report)
    # Возвращаем HTML-страницу с формой для редактирования отчёта
    return render(request, 'general_weekly/edit_general_weekly_report.html', {'form': form, 'report_id': report_id})


@login_required
@check_general_weekly_summary_report_creator
def general_weekly_summary_report(request):
    """
    Сводный отчёт
    """
    if request.method == 'POST':
        # Если запрос метода POST, обрабатываем форму
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            # Если форма действительна, извлекаем выбранную дату из формы
            selected_date = friday_of_week(form.cleaned_data['report_date'])
            # Получаем все отчёты за выбранную дату
            reports = WeeklyReport.objects.filter(report_date=selected_date)
            # Получаем все подразделения
            all_departments = Department.objects.all()
            # Получаем список подразделений, для которых нет отчётов за выбранную дату
            departments_without_reports = (all_departments.exclude(weeklyreport__report_date=selected_date)
                                           .order_by('name'))
            # Возвращаем HTML-страницу с данными отчётов и формой выбора даты
            return render(request, 'general_weekly/summary_report.html',
                          {'form': form, 'reports': reports,
                           'departments_without_reports': departments_without_reports})
    else:
        form = DateSelectionForm(initial={'report_date': friday_of_week(datetime.now())})
        default_date = friday_of_week(datetime.now())
        reports = WeeklyReport.objects.filter(report_date=default_date)
        all_departments = Department.objects.all()
        departments_without_reports = all_departments.exclude(weeklyreport__report_date=default_date).order_by('name')

        return render(request, 'general_weekly/summary_report.html',
                      {'form': form, 'reports': reports,
                       'departments_without_reports': departments_without_reports})


def general_weekly_access_denied_page(request):
    return render(request, 'general_weekly/access_denied_page.html')


@login_required
def success_page(request):
    return render(request, 'general_weekly/success_page.html')


@login_required
@check_general_weekly_summary_report_creator
def generate_general_weekly_summary_report(request):
    """
    Генерация сводного отчёта
    :param request:
    :return:
    """
    return HttpResponse('General weekly')
