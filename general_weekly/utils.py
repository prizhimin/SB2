from datetime import datetime, timedelta


def friday_of_week(date_string):
    """
    Функция возвращает дату пятницы
    :param date_string: дата дня недели
    :return: дата пятницы этой недели
    """
    # Преобразуем строку с датой в объект datetime
    date_format = '%d.%m.%Y'
    date = datetime.strptime(date_string, date_format)
    # Вычисляем день недели (0 - понедельник, 6 - воскресенье)
    weekday = date.weekday()
    # Вычисляем смещение для пятницы (если сегодня пятница, то смещение равно 0,
    # если сегодня понедельник, то смещение равно 4 и т.д.)
    friday_offset = (4 - weekday) % 7
    # Вычисляем дату пятницы добавлением смещения к исходной дате
    friday_date = date + timedelta(days=friday_offset)
    # Форматируем дату пятницы в строку с тем же форматом
    return friday_date.strftime(date_format)

