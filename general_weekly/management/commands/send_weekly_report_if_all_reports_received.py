import os
import datetime

from django.core.management import BaseCommand
from django.apps import apps
from exchangelib import Credentials, Account, Message, DELEGATE, HTMLBody, FileAttachment

from general_weekly.views import generate_general_weekly_summary_report, get_users_for_department
from general_weekly.utils import friday_of_week
from general_weekly.models import WeeklyReport
from commondata.models import Department


class Command(BaseCommand):
    """
    Команда Django для проверки наличия всех отчётов и отправки сводного отчёта
    по охране, если все отчёты представлены.
    """
    help = 'Проверка наличия всех отчётов и отправка сводного отчёта, если все отчёты представлены.'

    def handle(self, *args, **kwargs):
        """
        Метод для выполнения команды. Проверяет наличие всех отчётов и отправляет
        сводный отчёт по электронной почте, если все отчёты представлены.
        """
        # Получаем учетные данные из переменных окружения
        email_user = os.getenv('SW_EMAIL_USER')
        email_password = os.getenv('SW_EMAIL_PASSWORD')
        if not email_user or not email_password:
            return
        cc_emails = os.getenv('SW_WEEKLY_CC_EMAILS', '').split(';')
        # Получаем дату для отчета
        date_obj = friday_of_week(datetime.datetime.now())
        # Проверяем, все ли отчёты за указанную дату представлены
        departments_with_reports = (WeeklyReport.objects.filter(report_date=date_obj)
                                    .values_list('department', flat=True))
        all_departments = Department.objects.all()
        missing_departments = all_departments.exclude(id__in=departments_with_reports)
        if missing_departments.exists():
            # Создание сообщения с информацией о недостающих данных
            missing_departments_info = [
                f"{department.name}: {', '.join(get_users_for_department(department.name))}"
                for department in missing_departments
            ]
            missing_departments_text = '\n'.join(missing_departments_info)
            # Настройка e-mail клиента и создание сообщения
            credentials = Credentials(email_user, email_password)
            account = Account(email_user, credentials=credentials, autodiscover=True, access_type=DELEGATE)
            # Получаем получателей из строковой переменной
            recipients = os.getenv('SW_WEEKLY_CC_EMAILS', '').split(';')
            subject = f'Не все еженедельные отчёты по эффективности СБ за {date_obj.strftime("%d.%m.%Y")} представлены'
            body = f"""
                <html>
                <body>
                    <p>Здравствуйте!</p>
                    <p>Не все отчёты за {date_obj.strftime('%d.%m.%Y')} представлены</p>
                    <p>Ниже приведён список филиалов и пользователей, которые не внесли данные:</p>
                    {''.join([f'<p>{line}</p>' for line in missing_departments_text.splitlines()])}
                    <p><i>Сообщение создано автоматически, отвечать на него не требуется</i></p>
                </body>
                </html>
            """
            message = Message(
                account=account,
                subject=subject,
                body=HTMLBody(body),
                to_recipients=[email.strip() for email in recipients if email.strip()]
            )

            # Отправка сообщения
            message.send()
            return

        # Создание отчёта и получение пути к файлу
        report_name = generate_general_weekly_summary_report(date_obj, apps.get_app_config('daily').PATH_TO_SAVE)

        # Настройка e-mail клиента и создание сообщения
        credentials = Credentials(email_user, email_password)
        account = Account(email_user, credentials=credentials, autodiscover=True, access_type=DELEGATE)

        # Получаем получателей из строковой переменной
        recipients = os.getenv('SW_WEEKLY_REPORT_RECIPIENTS', '').split(';')

        subject = f'Сводный отчёт по эффективности СБ за {date_obj.strftime("%d.%m.%Y")}'
        body = f"""
            <html>
            <body>
                <p>Уважаемые коллеги, добрый день!</p>
                <p>Направляю вам сводный отчёт по эффективности СБ за {date_obj.strftime('%d.%m.%Y')}</p>
                <p><i>Сообщение создано автоматически, отвечать на него не требуется</i></p>
            </body>
            </html>
        """
        # Создание сообщения
        message = Message(
            account=account,
            subject=subject,
            body=HTMLBody(body),
            to_recipients=[email.strip() for email in recipients if email.strip()],
            cc_recipients=[email for email in cc_emails if email]
        )

        # Добавляем вложение
        with open(report_name, 'rb') as report_file:
            file_attachment = FileAttachment(name=os.path.basename(report_name), content=report_file.read())
            message.attach(file_attachment)

        # Отправка сообщения
        message.send()
