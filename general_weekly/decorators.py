from functools import wraps
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from .models import WeeklyCreatorsSummaryReport, WeeklyUserDepartment, WeeklyReport


def general_weekly_check_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Проверяем принадлежность пользователя к подразделению
        user_departments = WeeklyUserDepartment.objects.filter(user=request.user)
        if user_departments.count():
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'general_weekly/access_denied_page.html')
    return wrapper



def general_weekly_check_user_department(view_func):
    """
    Проверка прав пользователя на доступ к отчётам выбранного подразделения
    """
    @wraps(view_func)
    def wrapper(request, report_id, *args, **kwargs):
        # Получаем объект отчёта по его идентификатору
        report = get_object_or_404(WeeklyReport, id=report_id)
        # Получаем подразделение отчёта
        report_department = report.department
        # Проверяем принадлежность пользователя к подразделению
        user_departments = WeeklyUserDepartment.objects.filter(user=request.user)
        if user_departments.count() == 0:
            return render(request, 'general_weekly/access_denied_page.html')
        user_department_ids = user_departments.values_list('department__id', flat=True)
        if report_department.id in user_department_ids:
            return view_func(request, report_id, *args, **kwargs)
        else:
            messages.error(request, "У вас нет доступа к этому отчёту.")
            return render(request, 'general_weekly/access_denied_page.html')
    return wrapper


def check_general_weekly_summary_report_creator(view_func):
    """"
    Проверка прав пользователя на создание сводного отчёта
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Получаем список создателей сводных отчётов
        summary_reports_creators = WeeklyCreatorsSummaryReport.objects.first().creators.all()
        # Проверяем, имеет ли пользователь права на создание сводного отчёта
        if request.user in summary_reports_creators:
            return view_func(request, *args, **kwargs)
        else:
            # Если пользователь не является создателем, перенаправляем его на страницу доступа запрещен
            messages.error(request, "Доступ запрещен")
            return redirect('access_denied_page')
    return wrapper
