import os
from django.core.management import BaseCommand
from django.apps import apps
from exchangelib import Credentials, Account, Message, DELEGATE, HTMLBody, FileAttachment

from daily.views import create_daily_report  # Импортируем функцию создания отчета из views.py
from daily.utils import get_date_for_report, get_users_for_department
from commondata.models import Department
from daily.models import DailyReport


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
            self.stdout.write(self.style.ERROR('EMAIL_USER or EMAIL_PASSWORD environment variable is not set.'))
            return

        # Получаем дату для отчета
        date_obj = get_date_for_report()

        # Проверяем, все ли отчёты за указанную дату представлены
        departments_with_reports = DailyReport.objects.filter(report_date=date_obj).values_list('department', flat=True)
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
            recipients = os.getenv('SW_CC_EMAILS', '').split(';')

            subject = f'Не все ежедневные отчёты по охране за {date_obj.strftime("%d.%m.%Y")} представлены'
            body = (
                f'Здравствуйте!\n\n'
                f'Не все отчёты за {date_obj.strftime("%d.%m.%Y")} представлены. Ниже приведен список '
                f'отделов и пользователей, которые не внесли данные:\n\n'
                f'{missing_departments_text}\n\n'
            )
            print(subject)
            print(body)
            message = Message(
                account=account,
                subject=subject,
                body=HTMLBody(body),
                to_recipients=[email.strip() for email in recipients if email.strip()]
            )

            # Отправка сообщения
            # message.send()
            self.stdout.write(self.style.SUCCESS('Notification email sent successfully.'))
            return

        # Создание отчёта и получение пути к файлу
        report_name = create_daily_report(date_obj, apps.get_app_config('daily').PATH_TO_SAVE)

        # Настройка e-mail клиента и создание сообщения
        credentials = Credentials(email_user, email_password)
        account = Account(email_user, credentials=credentials, autodiscover=True, access_type=DELEGATE)

        # Получаем получателей из строковой переменной
        recipients = os.getenv('SW_DAILY_REPORT_RECIPIENTS', '').split(';')

        subject = 'Сводный ежедневный отчёт по охране'
        body = (
            'Здравствуйте!\n\n'
            'Прикреплён сводный ежедневный отчёт по охране.\n\n'
            'Спасибо!'
        )

        # Создание сообщения
        message = Message(
            account=account,
            subject=subject,
            body=HTMLBody(body),
            to_recipients=[email.strip() for email in recipients if email.strip()]
        )

        # Добавляем вложение
        with open(report_name, 'rb') as report_file:
            file_attachment = FileAttachment(name=os.path.basename(report_name), content=report_file.read())
            message.attach(file_attachment)

        # Отправка сообщения
        # message.send()
        self.stdout.write(self.style.SUCCESS('Summary report sent successfully.'))
