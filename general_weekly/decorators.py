from functools import wraps
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import WeeklyCreatorsSummaryReport, WeeklyUserDepartment, WeeklyReport


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
        user_department_ids = user_departments.values_list('department__id', flat=True)
        if report_department.id in user_department_ids:
            return view_func(request, report_id, *args, **kwargs)
        else:
            messages.error(request, "У вас нет доступа к этому отчёту.")
            return redirect('general_weekly_access_denied_page')
    return wrapper
