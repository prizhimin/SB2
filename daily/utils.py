from django.utils import timezone


def get_date_for_report():
    """
    Функция предлагает дату для отчётов исходя из дня недели
    Если сегодня - суббота, воскресенье или понедельник до 09:30, то будет возвращена дата прошлой пятницы
    Если сегодня - понедельник после 09:30, то вернётся текущая дата, иначе вернётся вчерашняя дата
    """
    # Определяем текущую дату и время
    current_datetime = timezone.now().astimezone(tz=timezone.get_current_timezone())
    print(current_datetime)
    # Проверяем, что сейчас суббота, воскресенье или понедельник, и время меньше 09:30
    if current_datetime.weekday() in [5, 6] or (current_datetime.weekday() == 0 and
                                                current_datetime.time() < timezone.datetime.strptime('09:30',
                                                                                                     '%H:%M').time()):
        print('get_date_for_report: Сейчас суббота, воскресенье или понедельник до 09:30')
        # Если условие выполняется, выбираем дату прошлой пятницы
        return (current_datetime.date()
                - timezone.timedelta(days=current_datetime.weekday())
                + timezone.timedelta(days=4, weeks=-1))
    else:
        if current_datetime.weekday() == 0:
            print('get_date_for_report: Сейчас понедельник после 09:30')
            # Если сейчас понедельник и время больше 09:30, то возвращаем сегодняшнюю дату
            return current_datetime.date()
        else:
            # Иначе возвращаем вчерашнюю дату
            print('get_date_for_report: Возвращаем вчерашнюю дату')
            return current_datetime.date() - timezone.timedelta(days=1)
