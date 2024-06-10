from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.apps import apps
from .forms import ReportForm
from .models import (SemiAnnual2024Report, SemiAnnual2024CreatorsSummaryReport, SemiAnnual2024UserCompany,
                     SemiAnnual2024Company)
from shutil import copy
from os import path
from openpyxl import load_workbook

@login_required
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user  # Установите поле user
            report.save()
            return redirect('report_list')
    else:
        form = ReportForm()
    return render(request, 'sixmonths2024/report_form.html', {'form': form})


@login_required
def update_report(request, pk):
    report = get_object_or_404(SemiAnnual2024Report, pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report_list')
    else:
        form = ReportForm(instance=report)
    return render(request, 'sixmonths2024/report_form.html', {'form': form})


@login_required
def delete_report(request, pk):
    report = get_object_or_404(SemiAnnual2024Report, pk=pk)

    if request.method == 'POST':
        report.delete()
        # messages.success(request, 'Отчет успешно удален.')
        return redirect('report_list')

    return render(request, 'sixmonths2024/report_confirm_delete.html', {'report': report})


@login_required
def report_list(request):
    user = request.user

    creators_summary_report = SemiAnnual2024CreatorsSummaryReport.objects.first()
    if creators_summary_report and user in creators_summary_report.creators.all():
        reports = SemiAnnual2024Report.objects.all()
        return render(request, 'sixmonths2024/report_list.html', {'reports': reports})
    else:
        user_company = SemiAnnual2024UserCompany.objects.get(user=user)
        company = user_company.companies.first()

        # Если для этой компании уже есть отчет, получаем его
        report = SemiAnnual2024Report.objects.filter(company=company).first()

        if request.method == 'POST':
            form = ReportForm(request.POST, instance=report)
            if form.is_valid():
                report = form.save(commit=False)
                report.user = request.user  # Устанавливаем текущего пользователя
                report.save()
                return redirect('report_list')
        else:
            form = ReportForm(instance=report, initial={'company': company})
            user_company = SemiAnnual2024UserCompany.objects.filter(user=user).first()
            available_companies = user_company.companies.all()  # Компании, доступные пользователю
            form.fields['company'].queryset = available_companies  # Ограничиваем доступные компании
        return render(request, 'sixmonths2024/report_form.html', {'form': form})


def generate_sixmonths_2024_summary_report(request):
    # Получаем экземпляр класса конфигурации приложения sixmonths2024
    sixmonths2024_config = apps.get_app_config('sixmonths2024')
    # Получаем путь к папке для сохранения отчётов
    path_to_reports = sixmonths2024_config.PATH_TO_SAVE
    # Префикс названия отчёта
    report_name = 'Сводный отчёт за 6 месяцев 2024 г.'
    # Формируем имя файла отчёта на основе выбранной даты
    report_name = path.join(path_to_reports, f'{report_name}')
    print(report_name)
    # Копируем шаблон отчёта
    # copy(path.join(path_to_reports, 'sixmonths2024_blank.xlsx'), report_name)
    # # Загружаем созданный отчёт в Excel
    # report_workbook = load_workbook(report_name)
    # report_sheet = report_workbook.active
    cols ='CD'
    # Получаем список названий всех компаний из модели SemiAnnual2024Company
    company_names = SemiAnnual2024Company.objects.values_list('name', flat=True)
    # Итерируемся по списку названий компаний
    for company_name in company_names:
        # Получаем объект компании по её названию
        company = SemiAnnual2024Company.objects.get(name=company_name)
        # Проверяем, существует ли отчет для этой компании
        if SemiAnnual2024Report.objects.filter(company=company).exists():
            # Если отчет существует, выводим название компании
            print(company_name)
            # Объект отчёт филиал company_name
            report = SemiAnnual2024Report.objects.filter(company=company).first()
            # Начинаем формировать отчёт
            for idx_field in range(1, 52):
                # закладка охрана поля 26..33
                match idx_field:
                    # закладка кадры поля 1,2
                    case 1 | 2:
                        print(idx_field, '1 или 2')
                        cols = 'CD'
                        print(f'Колонка {cols[idx_field - 1]}')
                    # закладка уд и дз поля 3..19
                    case n if 3 <= n <= 19:
                        print(idx_field, 'От 3 до 5')
                        cols = 'CDEFGHIJKMNOPQRST'
                        print(f'Колонка {cols[idx_field - 3]}')
                    # закладка антикорпоратив и коррупционные поля 20..25
                    case n if 20 <= n <= 25:
                        print(idx_field, 'От 20 до 25')
                        cols = 'CDEFGH'
                        print(f'Колонка {cols[idx_field - 20]}')
                    # закладка охрана поля 26..33
                    case n if 26 <= n <= 33:
                        print(idx_field, 'От 26 до 33')
                        cols = 'CDEFHIJK'
                        print(f'Колонка {cols[idx_field - 26]}')
                    # закладка проверка физ. юр. лиц поля 34..37
                    case n if 34 <= n <= 37:
                        print(idx_field, 'От 34 до 37')
                        cols = 'CDEF'
                        print(f'Колонка {cols[idx_field - 34]}')
                    # закладка травматизм поля 38..43
                    case n if 38 <= n <= 43:
                        print(idx_field, 'От 38 до 43')
                        cols = 'CDEGHIJ'
                        print(f'Колонка {cols[idx_field - 38]}')
                    # закладка аварийность поля 44..47
                    case n if 44 <= n <= 47:
                        print(idx_field, 'От 44 до 47')
                        cols = 'CDEGHI'
                        print(f'Колонка {cols[idx_field - 44]}')
                    # закладка аналитика поля 48..51
                    case n if 48 <= n <= 51:
                        print(idx_field, 'От 38 до 43')
                        cols = 'CDEF'
                        print(f'Колонка {cols[idx_field-48]}')
    return HttpResponse('Отчёт нах!')


    #
    #         # Словарь, соотносящий названия подразделений с соответствующими столбцами в Excel
    #         departments_cols = {k: v for k, v in zip(('Марий Эл и Чувашии', 'Ульяновский', 'Удмуртский', 'Свердловский',
    #                                                   'Саратовский', 'Самарский', 'Пермский', 'Оренбургский',
    #                                                   'Нижегородский', 'Мордовский', 'Коми', 'Кировский',
    #                                                   'Владимирский', 'Пензенский'), 'CDEFGHIJKLMNOP')}
    #         weekly_sums = {}
    #         # Считаем суммы за указанный диапазон дат
    #         for department in Department.objects.all():
    #             weekly_sums[department.name] = DailyReport.get_weekly_sums(department, start_date, end_date)
    #         # Копируем посчитанные суммы в сводный отчёт
    #         for department in Department.objects.all():
    #             for idx, line in enumerate(tuple(range(3, 12)) + (16, 17), start=1):
    #                 report_sheet[f'{departments_cols[department.name]}{line}'] = (
    #                     0 if weekly_sums[department.name].get(f'total_field_{idx}') is None
    #                     else weekly_sums[department.name][f'total_field_{idx}']
    #                 )
    #         report_sheet['A16'] = 'Количество проведенных проверок СБ'
    #         report_sheet['A17'] = 'Количество направленных претензионных писем'
    #         # Высота строки
    #         report_sheet.row_dimensions[16].height = 15
    #         report_sheet.row_dimensions[17].height = 15
    #         # Сохраняем изменения в отчёте
    #         report_workbook.save(report_name)
    #         # Возвращаем файл отчёта в HTTP-ответе
    #         response = FileResponse(open(report_name, 'rb'), as_attachment=True,
    #                                 filename=report_name)
    #         return response
    #     else:
    #         return HttpResponse('Invalid form data')  # Сообщение о неверных данных формы
    # else:
    #     return HttpResponse('Only POST requests are allowed')  # Сообщение о неправильном методе запроса