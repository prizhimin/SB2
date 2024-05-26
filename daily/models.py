from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from commondata.models import Department
from datetime import timedelta


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
    created_at = models.DateTimeField('Время создания', auto_now_add=True, editable=False)
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
    field_11 = models.PositiveSmallIntegerField('Количество направленных претензионных писем за прошедшие сутки',
                                                default=0)

    class Meta:
        ordering = ('-report_date',)
        # constraints = [
        #     models.UniqueConstraint(fields=['report_date', 'department'], name='unique_report_date_department')
        # ]

    def __str__(self):
        return (f"{self.report_date.strftime('%d.%m.%Y')} - {self.department.name} - {self.author.last_name} "
                f"{self.author.first_name}")

    @staticmethod
    def get_daily_reports_by_date(date):
        return DailyReport.objects.filter(report_date=date)

    @classmethod
    def get_weekly_sums(cls, department, monday_date):
        end_date = monday_date + timedelta(days=6)
        return cls.objects.filter(
            department=department,
            report_date__range=(monday_date, end_date)).aggregate(
            total_field_1=Sum('field_1'),
            total_field_2=Sum('field_2'),
            total_field_3=Sum('field_3'),
            total_field_4=Sum('field_4'),
            total_field_5=Sum('field_5'),
            total_field_6=Sum('field_6'),
            total_field_7=Sum('field_7'),
            total_field_8=Sum('field_8'),
            total_field_9=Sum('field_9'),
            total_field_10=Sum('field_10'),
            total_field_11=Sum('field_11'),
        )


class CreatorsSummaryReport(models.Model):
    """
    Список создателей сводного отчёта
    """
    creators = models.ManyToManyField(User, related_name='summary_reports')
