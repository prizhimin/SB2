import os

from django.apps import apps
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum

from commondata.models import Department
from commondata.forms import DateForm, DateSelectionForm
from .forms import WeeklyReportForm
from .models import WeeklyUserDepartment, WeeklyReport, WeeklyCreatorsSummaryReport
from .utils import friday_of_week
from .decorators import general_weekly_check_user_department, check_general_weekly_summary_report_creator

from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.cell.text import InlineFont
from openpyxl.cell.rich_text import TextBlock, CellRichText

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
    Генерация сводного еженедельного отчёта
    """

    # описание структуры готового отчёта
    report_structure = (
        # 1 значение - строка, "Номер подпункта"
        # 2 значение - строка, "Название раздела"
        # 3 тип - булевая, True - суммируем числовые значения, False - формируем строковое описание
        ('1', 'Экономический эффект (сумма, млн. руб без НДС)', True),
        ('1.1', 'Наиболее значимый пример:', False),
        ('2', 'Выявлено неучтенным ТМЦ (сумма, млн. руб без НДС)', True),
        ('2.1', 'Наиболее значимый пример:', False),
        ('3', 'Входной контроль (сумма, млн. руб без НДС)', True),
        ('3.1', 'Наиболее значимый пример:', False),
        ('4', 'Количество запросов, актов реагирования от контрольно-надзорных и правоохранительных органов, '
              'поступивших в отчетном периоде', True),
        ('4.1', 'Наиболее значимый пример:', False),
        ('5', 'Количество запросов, актов реагирования, поручений поступивших из территориальных органов '
              'власти, поступивших в отчетном периоде', True),
        ('5.1', 'Наиболее значимый пример:', False),
        ('6', 'Направлено заявлений в правоохранительные органы для защиты интересов Компании', True),
        ('6.1', 'Наиболее значимый пример:', False),
        ('7', 'Проведено встреч, рабочих групп с сотрудниками правоохранительных, контрольно-надзорными органов', True),
        ('7.1', 'Наиболее значимый пример:', False),
        ('8', 'Выявлено фактов антикорпоративных проявлений', True),
        ('8.1', 'Наиболее значимый пример:', False),
        ('9', 'Инициировано служебных проверок', True),
        ('9.1', 'Наиболее значимый пример:', False),
        ('10', 'Значимая информация, факты, события, риски и т.д.', False)
    )

    def get_last_saturday_and_current_friday_dates():
        # Получить текущую дату
        current_date = datetime.now()
        # Определить день недели (0 - понедельник, 6 - воскресенье)
        current_weekday = current_date.weekday()
        # Вычислить дату прошлой субботы
        _last_saturday = current_date - timedelta(days=current_weekday + 2)
        # Вычислить дату текущей пятницы
        _current_friday = current_date + timedelta(days=(4 - current_weekday))
        # Преобразовать даты обратно в строки в формате '%d.%m.%Y'
        last_saturday_str = _last_saturday.strftime('%d.%m.%Y')
        current_friday_str = _current_friday.strftime('%d.%m.%Y')
        # Вернуть кортеж из строк с датами
        return last_saturday_str, current_friday_str

    if request.method == 'POST':
        # Получаем данные формы
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            # Извлекаем выбранную дату из формы
            selected_date = friday_of_week(form.cleaned_data['report_date'])
            # Получаем экземпляр класса конфигурации приложения general_weekly
            general_weekly_config = apps.get_app_config('general_weekly')
            # Получаем путь к папке для сохранения отчётов
            path_to_reports = general_weekly_config.PATH_TO_SAVE
            # Префикс названия отчёта
            prefix_report_name = 'Еженедельный отчёт филиалов'
            # Формируем имя файла отчёта на основе выбранной даты
            report_name = os.path.join(path_to_reports, f'{prefix_report_name} за '
                                                        f'{selected_date.strftime('%d.%m.%Y')}.xlsx')
            # Создаём xlsx-файл отчёта
            wb = Workbook()
            sheet = wb.active
            sheet.title = f'Отчёт {selected_date.strftime('%d.%m.%Y')}'
            # Заполняем отчёт
            # Масштаб 55%
            sheet.page_setup.scale = 55 # НЕ РАБОТАЕТ!!!
            border = Border(left=Side(style='thin'), right=Side(style='thin'),
                            top=Side(style='thin'), bottom=Side(style='thin'))
            # Форматируем 1 строку
            sheet.merge_cells(f'A1:C1')
            sheet.column_dimensions['A'].width = 15
            sheet.column_dimensions['B'].width = 59
            sheet.column_dimensions['C'].width = 247
            sheet.row_dimensions[1].height = 100
            last_saturday, current_friday = get_last_saturday_and_current_friday_dates()
            sheet['A1'].value = f'Еженедельный отчёт\n'\
                                f'эффективности работы СБ филиалов\n'\
                                f'c {last_saturday} г. по {current_friday} г.'
            sheet['A1'].font = Font(name='Tahoma', bold=True, size=24)
            sheet['A1'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            sheet['C1'].border = border
            # Получаем все отчёты за выбранную дату, отсортированные по названию филиала
            reports = WeeklyReport.objects.filter(report_date=selected_date).order_by('department__name')
            current_row = 2
            # стиль границ ячейки

            for num, paragraph in enumerate(report_structure, start=1):
                if paragraph[2]:
                    # суммируем значения
                    sheet[f'A{current_row}'] = paragraph[0]
                    sheet[f'B{current_row}'] = paragraph[1]
                    sheet[f'C{current_row}'] = reports.aggregate(total_field_sum=Sum(f'field{num}'))[f'total_field_sum']
                    sheet[f'A{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
                    sheet[f'B{current_row}'].alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
                    sheet[f'C{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
                    sheet[f'A{current_row}'].font = Font(name='Tahoma', size=24)
                    sheet[f'B{current_row}'].font = Font(name='Tahoma', size=24)
                    sheet[f'B{current_row}'].fill = PatternFill(fill_type='solid', start_color='ffff00', end_color='ffff00')
                    sheet[f'C{current_row}'].font = Font(name='Tahoma', size=24)
                    sheet[f'A{current_row}'].border = border
                    sheet[f'B{current_row}'].border = border
                    sheet[f'C{current_row}'].border = border
                    current_row += 1
                else:
                    # формируем строковое описание
                    start_row = current_row
                    sheet[f'A{current_row}'] = paragraph[0]
                    sheet[f'B{current_row}'] = paragraph[1]
                    sheet[f'A{current_row}'].font = Font(name='Tahoma', size=24)
                    sheet[f'B{current_row}'].font = Font(name='Tahoma', size=24)
                    sheet[f'A{current_row}'].border = border
                    sheet[f'B{current_row}'].border = border
                    sheet[f'A{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
                    sheet[f'B{current_row}'].alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
                    for report in reports:
                        if getattr(report, f'field{num}').strip():
                            sheet[f'C{current_row}'] = CellRichText(
                                TextBlock(InlineFont(rFont='Tahoma', sz=24, b=True), report.department.name),
                                ' ',
                                TextBlock(InlineFont(rFont='Tahoma', sz=24), getattr(report, f'field{num}').strip()),
                            )
                            sheet[f'C{current_row}'].font = Font(name='Tahoma', size=24)
                            sheet[f'C{current_row}'].border = border
                            sheet[f'C{current_row}'].alignment = Alignment(horizontal='left', vertical='center',
                                                                           wrap_text=True)
                            sheet.row_dimensions[current_row].height = 'auto'
                            current_row += 1
                    if start_row < current_row:
                        sheet.merge_cells(f'A{start_row}:A{current_row-1}')
                        sheet.merge_cells(f'B{start_row}:B{current_row-1}')
            wb.save(report_name)
            return FileResponse(open(report_name, 'rb'), as_attachment=True,
                                filename=report_name)
