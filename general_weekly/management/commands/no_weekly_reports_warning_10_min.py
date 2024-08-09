import os
import datetime
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from commondata.models import Department
from general_weekly.models import WeeklyUserDepartment, WeeklyCreatorsSummaryReport, WeeklyReport
from general_weekly.utils import friday_of_week

from exchangelib import Credentials, Account, Message, DELEGATE, HTMLBody


class Command(BaseCommand):
    """
    Команда Django для отправки напоминаний пользователям о внесении данных в
    ежедневный отчёт по охране за 10 минут до окончания рабочего дня.
    """
    help = 'Напоминание за 10 минут о внесении данных для еженедельного отчёта по эффективности СБ'

    def handle(self, *args, **kwargs):
        """
        Метод для выполнения команды. Получает e-mail пользователей, чьи отделы
        не заполнили отчёт, и отправляет им напоминания по e-mail.
        """
        # Получаем учетные данные из переменных окружения
        email_user = os.getenv('SW_EMAIL_USER')
        email_password = os.getenv('SW_EMAIL_PASSWORD')
        # Получаем список адресов для копий из переменных окружения
        cc_emails = os.getenv('SW_WEEKLY_CC_EMAILS', '').split(';')
        # Получаем дату для отчета
        date_obj = friday_of_week(datetime.datetime.now())
        # Получаем e-mail пользователей, чьи отделы не заполнили отчёт
        emails = self.get_emails_of_users_without_reports(date_obj)
        # Если список пустой, то возврат
        if not emails:
            return

        # Настройка e-mail клиента
        credentials = Credentials(email_user, email_password)
        account = Account(email_user, credentials=credentials,
                          autodiscover=True, access_type=DELEGATE)

        # Создание и отправка сообщения
        subject = "Напоминание о внесении данных для еженедельного отчёта по эффективности СБ"
        body = f"""
            <html>
            <body>
                <p>Здравствуйте!</p>
                <p>Пожалуйста, внесите данные для еженедельного отчёта по эффективности СБ</p>
                <p>Спасибо!</p>
                <p><i>Сообщение создано автоматически, отвечать на него не требуется</i></p>
            </body>
            </html>        
        """

        message = Message(
            account=account,
            subject=subject,
            body=HTMLBody(body),
            to_recipients=[email for email in emails.split('; ') if email],
            cc_recipients=[email for email in cc_emails if email]
        )

        # Отправка сообщения
        message.send()

    @staticmethod
    def get_emails_of_users_without_reports(date):
        """
        Возвращает строку с e-mail пользователей, чьи отделы не заполнили отчёт
        за указанную дату.

        :param date: Дата отчета (тип datetime.date).
        :return: Строка с e-mail, разделенными точкой с запятой.
        """
        # Филиалы, которые создали отчёты
        departments_with_reports = WeeklyReport.objects.filter(report_date=date).values_list('department', flat=True)
        # Филиалы, которые не создали отчёты
        departments_without_reports = Department.objects.exclude(id__in=departments_with_reports)
        # Пользователи, связанные с этими филиалами
        users_without_reports = User.objects.filter(
            weeklyuserdepartment__department__in=departments_without_reports
        ).distinct()
        # Исключаем пользователей, которые числятся в WeeklyCreatorsSummaryReport
        creators_summary_report_users = WeeklyCreatorsSummaryReport.objects.values_list('creators', flat=True)
        users = users_without_reports.exclude(id__in=creators_summary_report_users)
        # Собираем e-mail пользователей
        emails = [user.email for user in users]
        # Возвращаем e-mail через точку с запятой
        return '; '.join(emails)
