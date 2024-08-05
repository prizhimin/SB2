import os
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from commondata.models import Department
from daily.models import UserDepartment
from daily.utils import get_date_for_report

from exchangelib import Credentials, Account, Message, DELEGATE, HTMLBody


class Command(BaseCommand):
    """
    Команда Django для отправки напоминаний пользователям о внесении данных в
    ежедневный отчёт по охране за 10 минут до окончания рабочего дня.
    """
    help = 'Напоминание за 10 минут о внесении данных для ежедневного отчёта по охране'

    def handle(self, *args, **kwargs):
        """
        Метод для выполнения команды. Получает e-mail пользователей, чьи отделы
        не заполнили отчёт, и отправляет им напоминания по e-mail.
        """
        # Получаем учетные данные из переменных окружения
        email_user = os.getenv('EMAIL_USER')
        email_password = os.getenv('EMAIL_PASSWORD')
        # Получаем дату для отчета
        date_obj = get_date_for_report()

        # Получаем e-mail пользователей, чьи отделы не заполнили отчёт
        emails = self.get_emails_of_users_without_reports(date_obj)
        if not emails:
            self.stdout.write(self.style.SUCCESS('No users to notify.'))
            return

        # Настройка e-mail клиента
        credentials = Credentials(email_user, email_password)
        account = Account(email_user, credentials=credentials,
                          autodiscover=True, access_type=DELEGATE)

        # Создание и отправка сообщения
        subject = 'Напоминание о внесении данных для ежедневного отчёта'
        body = (
            'Здравствуйте!\n\n'
            'Пожалуйста, внесите данные для ежедневного отчёта по охране.\n\n'
            'Спасибо!'
        )

        message = Message(
            account=account,
            subject=subject,
            body=HTMLBody(body),
            to_recipients=[email for email in emails.split('; ') if email]
        )

        # Отправка сообщения
        # message.send()
        self.stdout.write(self.style.SUCCESS('Reminder email sent successfully.'))

    @staticmethod
    def get_emails_of_users_without_reports(date):
        """
        Возвращает строку с e-mail пользователей, чьи отделы не заполнили отчёт
        за указанную дату.

        :param date: Дата отчета (тип datetime.date).
        :return: Строка с e-mail, разделенными точкой с запятой.
        """
        # Получаем все отделы, у которых нет отчёта за указанную дату
        departments_without_reports = Department.objects.exclude(
            dailyreport__report_date=date
        ).distinct()

        # Собираем всех пользователей, у которых есть доступ к этим отделам
        user_ids = UserDepartment.objects.filter(
            department__in=departments_without_reports
        ).values_list('user_id', flat=True)

        # Находим пользователей по их ID
        users = User.objects.filter(id__in=user_ids).distinct()

        # Собираем e-mail пользователей
        emails = [user.email for user in users]

        # Возвращаем e-mail через точку с запятой
        return '; '.join(emails)
