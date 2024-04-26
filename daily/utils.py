from django.utils import timezone
from .models import UserDepartment, CreatorsSummaryReport


def get_date_for_report():
    """
    Функция предлагает дату для отчётов исходя из дня недели
    Если сегодня - суббота, воскресенье или понедельник до 09:30, то будет возвращена дата последней пятницы
    Если сегодня - понедельник после 09:30, то вернётся текущая дата, иначе вернётся вчерашняя дата
    """
    # Определяем текущую дату и время МСК
    current_datetime = timezone.now().astimezone(tz=timezone.get_current_timezone())
    match current_datetime.weekday():
        case 5 | 6:
            # суббота или воскресенье - возращаем дату пятницы этой недели
            return (current_datetime.date()
                    - timezone.timedelta(days=current_datetime.weekday())
                    + timezone.timedelta(days=4))
        case 0:
            # понедельник
            if current_datetime.time() < timezone.datetime.strptime('09:30', '%H:%M').time():
                # время меньше 09:30 МСК
                # возвращаем дату пятницы прошлой недели
                return (current_datetime.date()
                        - timezone.timedelta(days=current_datetime.weekday())
                        + timezone.timedelta(days=4, weeks=-1))
            else:
                # Если сейчас понедельник и время больше 09:30, то возвращаем сегодняшнюю дату
                return current_datetime.date()
        case _:
            # Возвращаем вчерашнюю дату
            return current_datetime.date() - timezone.timedelta(days=1)


def get_users_for_department(department: str) -> list:
    """
    department: строковое название филиала
    users: модель, хранящая отношения пользователя и филиалы
    return: список пользователей для данного филиала
    """
    # return [user for user in users if department in user.department]
    users = UserDepartment.objects.filter(department__name=department)
    # Получаем всех создателей сводного отчета
    creators = CreatorsSummaryReport.objects.values_list('creators', flat=True)
    # Исключаем создателей из списка пользователей
    users = users.exclude(user__in=creators)
    # Извлекаем всех пользователей из найденных записей
    users = [f'{user.user.last_name} {user.user.first_name}' for user in users]
    return users
