import os
import shutil
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import InvestigationForm, AttachedFileForm, DateForm
from .models import Investigation, AttachedFile, InvestigationUserDepartment, InvestigationCreatorsSummaryReport
from .decorators import check_user_department, check_summary_report_creator
from django.utils import timezone


@login_required
def investigation_list(request):
    # Получаем текущего пользователя
    user = request.user
    # Получаем филиалы, к которым пользователь имеет отношение
    user_departments = InvestigationUserDepartment.objects.filter(user=user).values_list('department', flat=True)
    # Получаем СЗ, к которым у пользователя есть доступ
    investigations = Investigation.objects.filter(department__in=user_departments).order_by('-order_date')
    # Если форма была отправлена методом POST, обрабатываем её
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['selected_date']
            # Фильтруем служебные проверки по выбранной дате
            investigations = investigations.filter(order_date=selected_date)
    else:
        # Если форма не отправлена, создаем форму с начальной датой для отчета
        form = DateForm(initial={'selected_date': timezone.now().astimezone(tz=timezone.get_current_timezone())})
    # Получаем список создателей сводных отчетов, если таковые имеются
    summary_reports_creators = []
    first_summary_report = InvestigationCreatorsSummaryReport.objects.first()
    if first_summary_report:
        # Сохраняем имена пользователей, создавших первый сводный отчет
        summary_reports_creators = [user.username for user in first_summary_report.creators.all()]
    paginator = Paginator(investigations, 14)  # X расследования на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'investigations/investigation_list.html',
                  {'page_obj': page_obj,
                   'form': form,
                   'summary_reports_creators': summary_reports_creators})


@login_required
def add_investigation(request):
    if request.method == 'POST':
        form = InvestigationForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('investigations:investigation_list')
    else:
        first_user_department = InvestigationUserDepartment.objects.filter(user=request.user).first()
        form = InvestigationForm(request.user, initial={'department': first_user_department})
    return render(request, 'investigations/add_investigation.html', {'form': form})


@login_required
@check_user_department
def investigation_detail(request, pk):
    investigation = get_object_or_404(Investigation, pk=pk)
    return render(request, 'investigations/investigation_detail.html',
                  {'investigation': investigation})


@login_required
@check_user_department
def edit_investigation(request, pk):
    # Получаем объект по первичному ключу или возвращаем 404 ошибку, если объект не найден
    investigation = get_object_or_404(Investigation, pk=pk)

    # Проверяем, что это POST запрос
    if request.method == "POST":
        # Передаем экземпляр объекта и данные формы
        form = InvestigationForm(request.user, request.POST, instance=investigation)
        if form.is_valid():  # Проверка на валидность данных формы
            investigation = form.save(commit=False)  # Сохраняем объект формы в переменную, но пока не записываем в БД
            investigation.save()  # Теперь сохраняем изменения в БД
            return redirect('investigations:investigation_detail',
                            pk=investigation.pk)  # Перенаправление на страницу детального просмотра
    else:
        form = InvestigationForm(request.user, instance=investigation)  # Создаем форму с начальными данными объекта

    # Отображаем страницу с формой
    return render(request, 'investigations/edit_investigation.html', {'form': form,
                                                                      'investigation_pk': pk,
                                                                      'has_attach': investigation.has_attach})


# Функции для работы с прикрепленными файлами

@login_required
# @check_user_department
def attach_file(request, investigation_id):
    investigation = get_object_or_404(Investigation, id=investigation_id)
    if request.method == 'POST':
        form = AttachedFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(investigation=investigation)
            return redirect('investigations:manage_attach', pk=investigation.pk)
    else:
        form = AttachedFileForm()
    return render(request, 'investigations/attach_file_form.html', {'form': form, 'investigation': investigation})


@login_required
# @check_user_department
def delete_file(request, file_id):
    attached_file = get_object_or_404(AttachedFile, id=file_id)
    investigation_id = attached_file.investigation.id
    if request.method == 'POST':
        attached_file.delete()
        file_path = os.path.join(settings.MEDIA_ROOT, 'invests', str(investigation_id),
                                 os.path.basename(attached_file.file.name))
        if os.path.exists(file_path):
            os.remove(file_path)
        return redirect('investigations:manage_attach', pk=investigation_id)
    return render(request,
                  'investigations/delete_file_confirm.html',
                  {'attached_file': attached_file, 'short_name': os.path.basename(attached_file.file.name)})


@login_required
def download_file(request, file_id):
    attached_file = get_object_or_404(AttachedFile, id=file_id)
    file_path = os.path.join(settings.MEDIA_ROOT, 'invests', str(attached_file.investigation.id),
                             os.path.basename(attached_file.file.name))
    response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                            filename=file_path)
    return response


@login_required
def delete_investigation(request, pk):
    investigation = get_object_or_404(Investigation, pk=pk)
    if request.method == 'POST':
        for attached_file in investigation.attached_files.all():
            file_path = os.path.join(settings.MEDIA_ROOT, 'invests', str(investigation.id),
                                     os.path.basename(attached_file.file.name))
            if os.path.exists(file_path):
                os.remove(file_path)
        investigation_dir = os.path.join(settings.MEDIA_ROOT, 'invests', str(investigation.id))
        if os.path.exists(investigation_dir):
            shutil.rmtree(investigation_dir)
        investigation.delete()
        return redirect('investigations:investigation_list')
    return render(request, 'investigations/investigation_confirm_delete.html', {'investigation': investigation})



@login_required
def manage_attach(request, pk):
    investigation = get_object_or_404(Investigation, id=pk)
    attached_files = AttachedFile.objects.filter(investigation=investigation)
    return render(request, 'investigations/manage_attach.html',
                  {'investigation': investigation,
                   'attached_files': attached_files})


@login_required
def download_attaches_zip(request, investigation_id):
    investigation = get_object_or_404(Investigation, id=investigation_id)
    if investigation.has_attach() > 0:
        attached_files = AttachedFile.objects.filter(investigation=investigation)
        for attached_file in attached_files:
            print(os.path.join(settings.MEDIA_ROOT, str(attached_file.file)))
        return HttpResponse('ZIPZIPZIP!!!')
    else:
        return HttpResponse('Нечего скачивать')


@login_required
@check_summary_report_creator
def summary_report(request):
    return HttpResponse('ЭТО СВОДНЫЙ ОТЧЁТ')