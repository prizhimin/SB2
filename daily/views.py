from django.shortcuts import render, get_object_or_404, redirect
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.utils import timezone
from django.apps import apps
from .models import DailyReport, CreatorsSummaryReport, UserDepartment
from commondata.models import Department
from commondata.forms import DateForm, DateSelectionForm
from .forms import DailyReportForm
from .decorators import check_summary_report_creator, check_user_department, check_daily_user
from .utils import get_date_for_report
from shutil import copy
import os
from openpyxl import load_workbook


@login_required
@check_daily_user
def daily_reports(request):
    # Получаем текущего пользователя
    user = request.user
    # Получаем филиалы, к которым пользователь имеет отношение
    user_departments = UserDepartment.objects.filter(user=user).values_list('department', flat=True)
    # Получаем все отчёты, связанные с этими филиалами, и сортируем их по дате отчёта
    reports = DailyReport.objects.filter(department__in=user_departments).order_by('-report_date')
    # Если форма отправлена методом POST
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['selected_date']
            # Фильтруем отчёты по выбранной дате
            reports = reports.filter(report_date=selected_date)
    else:
        form = DateForm(initial={'selected_date': get_date_for_report()})

    for report in reports:
        report.user_full_name = f"{report.author.last_name} {report.author.first_name}"
    summary_reports_creators = []
    first_summary_report = CreatorsSummaryReport.objects.first()
    if first_summary_report:
        summary_reports_creators = [user.username for user in first_summary_report.creators.all()]
    return render(request, 'daily/reports_list.html',
                  {'reports': reports,
                   'form': form,
                   'summary_reports_creators': summary_reports_creators})


@login_required
@check_user_department
def report_details(request, report_id):
    # Получаем объект отчёта по его id
    report = get_object_or_404(DailyReport, pk=report_id)
    # Объединяем имя и фамилию пользователя через пробел
    user_full_name = f"{report.author.last_name} {report.author.first_name}"
    return render(request, 'daily/report_details.html', {'report': report, 'user_full_name': user_full_name})


@login_required
def add_daily_report(request):
    if request.method == 'POST':
        # Создаем экземпляр формы ежедневного отчёта, передавая текущего пользователя и данные из POST-запроса
        form = DailyReportForm(request.user, request.POST)  # Передаем объект пользователя в форму
        if form.is_valid():  # Проверяем валидность данных формы
            daily_report = form.save(commit=False)  # Создаем объект ежедневного отчёта, не сохраняя его в базу данных
            daily_report.author = request.user  # Устанавливаем автора отчёта
            # Проверяем наличие отчёта для выбранного филиала и даты
            if (DailyReport.objects.filter(department=daily_report.department)
                    .filter(report_date=daily_report.report_date).exists()):
                return render(request, 'daily/denied_add_report.html',
                              {'department': daily_report.department.name,
                               'report_date': daily_report.report_date.strftime('%d.%m.%Y')})
            daily_report.save()  # Сохраняем отчёт в базу данных
            return redirect(
                success_page)  # Перенаправляем пользователя на success_page в случае успешного сохранения отчёта
    else:
        # Получаем первое подразделение пользователя, если оно есть
        first_user_department = UserDepartment.objects.filter(user=request.user).first()
        if first_user_department:
            first_department = first_user_department.department.first()
        else:
            # Иначе получаем первое подразделение в системе
            first_department = Department.objects.first()
        # Создаем экземпляр формы ежедневного отчёта с начальными данными,
        # передавая текущего пользователя и первое доступное пользователю подразделение
        form = DailyReportForm(request.user, initial={
            'department': first_department})  # Передаем объект пользователя и начальные значения в форму
    # Отображаем шаблон add_daily_report.html с переданной формой
    return render(request, 'daily/add_daily_report.html', {'form': form})


@login_required
@check_user_department
def edit_daily_report(request, report_id):
    # Получаем отчёт по его идентификатору
    report = get_object_or_404(DailyReport, id=report_id)
    # Получаем текущее время в часовом поясе Москвы
    current_time = timezone.now()
    # Проверяем, прошло ли меньше 1 часа с момента создания отчёта
    if current_time - report.created_at > timedelta(hours=1):
        # Если прошло более часа, переходим на страницу с сообщением об ошибке
        return render(request, 'daily/error_edit_report.html')

    if request.method == 'POST':
        # Если запрос метода POST, обрабатываем форму
        form = DailyReportForm(request.user, request.POST, instance=report)
        if form.is_valid():
            # Если форма валидна, сохраняем отчёт
            daily_report = form.save(commit=False)
            daily_report.author = request.user
            daily_report.save()
            # Перенаправляем пользователя на страницу успешного завершения
            return redirect(success_page)
    else:
        # Если запрос метода GET, отображаем форму для редактирования
        form = DailyReportForm(request.user, instance=report)
    # Возвращаем HTML-страницу с формой для редактирования отчёта
    return render(request, 'daily/edit_daily_report.html', {'form': form, 'report_id': report_id})


@login_required
@check_summary_report_creator
def summary_report(request):
    if request.method == 'POST':
        # Если запрос метода POST, обрабатываем форму
        form = DateForm(request.POST)
        if form.is_valid():
            # Если форма действительна, извлекаем выбранную дату из формы
            selected_date = form.cleaned_data['report_date']
            # Получаем все отчёты за выбранную дату
            reports = DailyReport.objects.filter(report_date=selected_date)
            # Получаем все подразделения
            all_departments = Department.objects.all()
            # Получаем список подразделений, для которых нет отчётов за выбранную дату
            departments_without_reports = (all_departments.exclude(dailyreport__report_date=selected_date)
                                           .order_by('name'))
            # Возвращаем HTML-страницу с данными отчётов и формой выбора даты
            return render(request, 'daily/summary_report.html',
                          {'form': form, 'reports': reports,
                           'departments_without_reports': departments_without_reports})
    else:
        form = DateSelectionForm(initial={'report_date': get_date_for_report()})
        default_date = get_date_for_report()
        reports = DailyReport.objects.filter(report_date=default_date)
        all_departments = Department.objects.all()
        departments_without_reports = all_departments.exclude(dailyreport__report_date=default_date).order_by('name')

        return render(request, 'daily/summary_report.html',
                      {'form': form, 'reports': reports,
                       'departments_without_reports': departments_without_reports})


@login_required
@check_summary_report_creator
def generate_summary_report(request):
    """
    Генерация сводного еженедельного отчёта
    """
    if request.method == 'POST':
        # Получаем данные формы
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            # Извлекаем выбранную дату из формы
            selected_date = form.cleaned_data['report_date']
            # Получаем экземпляр класса конфигурации приложения daily
            daily_config = apps.get_app_config('daily')
            # Получаем путь к папке для сохранения отчётов
            path_to_reports = daily_config.PATH_TO_SAVE
            # Префикс названия отчёта
            prefix_report_name = 'Ежедневный отчёт по охране'
            # Формируем имя файла отчёта на основе выбранной даты
            report_name = os.path.join(path_to_reports, f'{prefix_report_name} за '
                                                        f'{selected_date.strftime('%d.%m.%Y')}.xlsx')
            # Копируем шаблон отчёта
            copy(os.path.join(path_to_reports, 'daily_summary_report_blank.xlsx'), report_name)
            # Получаем все отчёты за выбранную дату, отсортированные по дате
            reports = DailyReport.objects.filter(report_date=selected_date).order_by('-report_date')
            # Загружаем созданный отчёт в Excel
            report_workbook = load_workbook(report_name)
            report_sheet = report_workbook.active
            # Словарь, соотносящий названия подразделений с соответствующими столбцами в Excel
            departments_cols = {k: v for k, v in zip(('Марий Эл и Чувашии', 'Ульяновский', 'Удмуртский', 'Свердловский',
                                                      'Саратовский', 'Самарский', 'Пермский', 'Оренбургский',
                                                      'Нижегородский', 'Мордовский', 'Коми', 'Кировский',
                                                      'Владимирский', 'Пензенский'), 'CDEFGHIJKLMNOP')}
            # Копируем данные из отчётов филиалов в сводный отчёт
            for report in reports:
                for idx, line in enumerate(tuple(range(3, 12)) + (16, 17), start=1):
                    report_sheet[f'{departments_cols[report.department.name]}{line}'] = getattr(report,
                                                                                                f'field_{idx}')
            # Сохраняем изменения в отчёте
            report_workbook.save(report_name)
            # Возвращаем файл отчёта в HTTP-ответе
            response = FileResponse(open(report_name, 'rb'), as_attachment=True,
                                    filename=report_name)
            return response


@login_required
def success_page(request):
    return render(request, 'daily/success_page.html')



def denied_add_daily_report(request, department, report_date):
    return render(request, 'daily/denied_add_report.html', {'department': department,
                                                            'report_date': report_date})
