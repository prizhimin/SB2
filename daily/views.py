from django.shortcuts import render, get_object_or_404, redirect
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.utils import timezone
from django.apps import apps
from .models import DailyReport, CreatorsSummaryReport, Department, UserDepartment
from .forms import DateForm, DailyReportForm, DateSelectionForm
from .decorators import check_summary_report_creator, check_user_department
from .utils import get_date_for_report
from shutil import copy
import os
from openpyxl import load_workbook


@login_required
def daily_reports(request):
    # Получаем текущего пользователя
    user = request.user
    # Получаем филиалы, к которым пользователь имеет отношение
    user_departments = UserDepartment.objects.filter(user=user).values_list('department', flat=True)
    # Получаем отчеты, относящиеся к пользователю
    # reports = DailyReport.objects.filter(author=user).order_by('-report_date')
    # Получаем все отчеты, связанные с этими филиалами, и сортируем их по дате отчета
    reports = DailyReport.objects.filter(department__in=user_departments).order_by('-report_date')
    # Если форма отправлена методом POST
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['selected_date']
            # Фильтруем отчеты по выбранной дате
            reports = reports.filter(report_date=selected_date)
    else:
        form = DateForm(initial={'selected_date': get_date_for_report()})

    for report in reports:
        report.user_full_name = f"{report.author.first_name} {report.author.last_name}"
    summary_reports_creators = [user.username for user in CreatorsSummaryReport.objects.first().creators.all()]
    return render(request, 'daily/reports_list.html',
                  {'reports': reports,
                   'form': form,
                   'summary_reports_creators': summary_reports_creators})


@login_required
@check_user_department
def report_details(request, report_id):
    # Получаем объект отчета по его id
    report = get_object_or_404(DailyReport, pk=report_id)
    # Объединяем имя и фамилию пользователя через пробел
    user_full_name = f"{report.author.last_name} {report.author.first_name}"
    return render(request, 'daily/report_details.html', {'report': report, 'user_full_name': user_full_name})


@login_required
def add_daily_report(request):
    if request.method == 'POST':
        # Создаем экземпляр формы ежедневного отчета, передавая текущего пользователя и данные из POST-запроса
        form = DailyReportForm(request.user, request.POST)  # Передаем объект пользователя в форму
        if form.is_valid():  # Проверяем валидность данных формы
            daily_report = form.save(commit=False)  # Создаем объект ежедневного отчета, не сохраняя его в базу данных
            daily_report.author = request.user  # Устанавливаем автора отчета
            daily_report.save()  # Сохраняем отчет в базу данных
            return redirect(
                success_page)  # Перенаправляем пользователя на success_page в случае успешного сохранения отчета
    else:
        # Получаем первое подразделение пользователя, если оно есть
        first_user_department = UserDepartment.objects.filter(user=request.user).first()
        if first_user_department:
            first_department = first_user_department.department.first()
        else:
            # Иначе получаем первое подразделение в системе
            first_department = Department.objects.first()
        # Создаем экземпляр формы ежедневного отчета с начальными данными,
        # передавая текущего пользователя и первое доступное пользователю подразделение
        form = DailyReportForm(request.user, initial={
            'department': first_department})  # Передаем объект пользователя и начальные значения в форму
    # Отображаем шаблон add_daily_report.html с переданной формой
    return render(request, 'daily/add_daily_report.html', {'form': form})


@login_required
@check_user_department
def edit_daily_report(request, report_id):
    # Получаем отчет по его идентификатору
    report = get_object_or_404(DailyReport, id=report_id)
    # Получаем текущее время в часовом поясе Москвы
    current_time = timezone.now()
    # Проверяем, прошло ли меньше 1 часа с момента создания отчета
    if current_time - report.created_at > timedelta(hours=1):
        # Если прошло более часа, переходим на страницу с сообщением об ошибке
        return render(request, 'daily/error_edit_report.html')

    if request.method == 'POST':
        # Если запрос метода POST, обрабатываем форму
        form = DailyReportForm(request.user, request.POST, instance=report)
        if form.is_valid():
            # Если форма валидна, сохраняем отчет
            daily_report = form.save(commit=False)
            daily_report.author = request.user
            daily_report.save()
            # Перенаправляем пользователя на страницу успешного завершения
            return redirect(success_page)
    else:
        # Если запрос метода GET, отображаем форму для редактирования
        form = DailyReportForm(request.user, instance=report)
    # Возвращаем HTML-страницу с формой для редактирования отчета
    return render(request, 'daily/edit_daily_report.html', {'form': form, 'report_id': report_id})


@login_required
@check_summary_report_creator
def summary_report(request):
    if request.method == 'POST':
        # Если запрос метода POST, обрабатываем форму
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            # Если форма действительна, извлекаем выбранную дату из формы
            selected_date = form.cleaned_data['report_date']
            # Получаем все отчеты за выбранную дату
            reports = DailyReport.objects.filter(report_date=selected_date)
            # Получаем все подразделения
            all_departments = Department.objects.all()
            # Получаем список подразделений, для которых нет отчетов за выбранную дату
            departments_without_reports = all_departments.exclude(dailyreport__report_date=selected_date)
            # Возвращаем HTML-страницу с данными отчетов и формой выбора даты
            return render(request, 'daily/summary_report.html',
                          {'form': form, 'reports': reports,
                           'departments_without_reports': departments_without_reports})
    else:
        form = DateSelectionForm(initial={'report_date': get_date_for_report()})
    return render(request, 'daily/summary_report.html', {'form': form})


@login_required
@check_summary_report_creator
def generate_summary_report(request):
    if request.method == 'POST':
        # Получаем данные формы
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            # Извлекаем выбранную дату из формы
            selected_date = form.cleaned_data['report_date']
            # Получаем экземпляр класса конфигурации приложения daily
            daily_config = apps.get_app_config('daily')
            # Получаем путь к папке для сохранения отчетов
            path_to_reports = daily_config.PATH_TO_SAVE
            # Формируем имя файла отчета на основе выбранной даты
            report_name = os.path.join(path_to_reports, f'Ежедневный отчёт по охране за {selected_date}.xlsx')
            # Копируем шаблон отчета
            copy(os.path.join(path_to_reports, 'daily_summary_report_blank.xlsx'), report_name)
            # Получаем все отчеты за выбранную дату, отсортированные по дате
            reports = DailyReport.objects.filter(report_date=selected_date).order_by('-report_date')
            # Загружаем созданный отчет в Excel
            report_workbook = load_workbook(report_name)
            report_sheet = report_workbook.active
            # Словарь, соотносящий названия подразделений с соответствующими столбцами в Excel
            departments_cols = {k: v for k, v in zip(('Марий Эл и Чувашии', 'Ульяновский', 'Удмуртский', 'Свердловский',
                                                      'Саратовский', 'Самарский', 'Пермский', 'Оренбургский',
                                                      'Нижегородский', 'Мордовский', 'Коми', 'Кировский',
                                                      'Владимирский', 'Пензенский'), 'CDEFGHIJKLNOP')}
            # Копируем данные из отчетов филиалов в сводный отчет
            for report in reports:
                for idx, line in enumerate(tuple(range(3, 12)) + (16, 17), start=1):
                    report_sheet[f'{departments_cols[report.department.name]}{line}'] = getattr(report,
                                                                                                f'field_{idx}')
            # Сохраняем изменения в отчете
            report_workbook.save(report_name)
            # Возвращаем файл отчета в HTTP-ответе
            response = FileResponse(open(report_name, 'rb'), as_attachment=True,
                                    filename=f'Ежедневный отчёт по охране за {selected_date}.xlsx')
            return response


@login_required
def success_page(request):
    return render(request, 'daily/success_page.html')


def access_denied_page(request):
    return render(request, 'daily/access_denied_page.html')
