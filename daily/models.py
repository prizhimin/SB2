from django.db import models
from django.contrib.auth.models import User
from commondata.models import Department


class UserDepartment(models.Model):
    """
    Список пользователей и филиалов, к которым они относятся
    Один пользователь может относиться к нескольким филиалам
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ManyToManyField(Department)

    def __str__(self):
        return f"{self.user.username}'s departments"


class DailyReport(models.Model):
    """
    Ежедневный отчёт филиалов
    """
    created_at = models.DateTimeField('Время создания', auto_now_add=True, editable=False)  # Нередактируемое поле с временем создания
    report_date = models.DateField('Отчётная дата')
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, verbose_name='Филиал', on_delete=models.CASCADE)
    field_1 = models.PositiveSmallIntegerField('Незакрытие постов охраны', default=0)
    field_2 = models.PositiveSmallIntegerField('Отсутствие спец. средств и оружия', default=0)
    field_3 = models.PositiveSmallIntegerField('Ненадлежащее проведение досмотра', default=0)
    field_4 = models.PositiveSmallIntegerField('Самовольное покидание поста', default=0)
    field_5 = models.PositiveSmallIntegerField('Допущение проникновения посторонних лиц', default=0)
    field_6 = models.PositiveSmallIntegerField('Допущение прохода по чужому пропуску (без пропуска)', default=0)
    field_7 = models.PositiveSmallIntegerField('Нахождение на посту в нетрезвом виде', default=0)
    field_8 = models.PositiveSmallIntegerField('Неприбытие ГБР', default=0)
    field_9 = models.PositiveSmallIntegerField('Иные значимые нарушения', default=0)
    field_10 = models.PositiveSmallIntegerField('Количество проведенных проверок СБ за прошедшие сутки', default=0)
    field_11 = models.PositiveSmallIntegerField('Количество направленных претензионных писем за прошедшие сутки', default=0)

    def __str__(self):
        return f"{self.report_date.strftime('%d.%m.%Y')} - {self.department.name} - {self.author.last_name} {self.author.first_name}"

    @staticmethod
    def get_daily_reports_by_date(date):
        return DailyReport.objects.filter(report_date=date)


class CreatorsSummaryReport(models.Model):
    """
    Список создателей сводного отчёта
    """
    creators = models.ManyToManyField(User, related_name='summary_reports')
