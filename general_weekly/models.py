from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from commondata.models import Department
from .utils import friday_of_week


class WeeklyReport(models.Model):
    """
    Еженедельный отчёт филиалов
    """
    created_at = models.DateTimeField('Время создания', auto_now_add=True,
                                      editable=False)  # Нередактируемое поле с временем создания
    report_date = models.DateField('Отчётная дата', null=False, blank=False)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    field1 = models.DecimalField('Экономический эффект (сумма, в млн. руб. без НДС)', max_digits=10, decimal_places=3)
    field2 = models.TextField('Наиболее значимый пример', max_length=1000, blank=True)
    field3 = models.DecimalField('Выявлено неучтённых ТМЦ (сумма, в млн. руб. без НДС)', max_digits=10,
                                 decimal_places=3)
    field4 = models.TextField('Наиболее значимый пример', max_length=1000, blank=True)
    field5 = models.DecimalField('Входной контроль (сумма, в млн. руб. без НДС)', max_digits=10, decimal_places=3)
    field6 = models.TextField('Наиболее значимый пример', max_length=1000, blank=True)
    field7 = models.PositiveIntegerField('Количество запросов, актов реагирования от\n'
                                         'контрольно-надзорых и правоохранительных органов,\n'
                                         'поступивших в отчётном периоде', default=0)
    field8 = models.TextField('Наиболее значимый пример', max_length=1000, blank=True)
    field9 = models.PositiveIntegerField('Количество запросов, актов реагирования, поручений\n'
                                         'из территориальных органов власти, поступивших\n'
                                         'в отчётном периоде', default=0)
    field10 = models.TextField('Наиболее значимый пример', max_length=1000, blank=True)
    field11 = models.PositiveIntegerField('Направлено заявлений в правоохранительные органы\n'
                                          'для защиты интересова Компании', default=0)
    field12 = models.TextField('Наиболее значимый пример', max_length=1000, blank=True)
    field13 = models.PositiveIntegerField('Проведено встреч, рабочих групп с сотрудниками\n'
                                          'правоохратиельных органов, контрольно-нажзорных органов', default=0)
    field14 = models.TextField('Наиболее значимый пример', max_length=1000, blank=True)
    field15 = models.PositiveIntegerField('Выявлено фактов антикорпоративных проявлений', default=0)
    field16 = models.TextField('Наиболее значимый пример', max_length=1000, blank=True)
    field17 = models.PositiveIntegerField('Инициировано служебных проверок', default=0)
    field18 = models.TextField('Наиболее значимый пример', max_length=1000, blank=True)
    field19 = models.TextField('Значимая информация, факты, события, риски и т.д.', max_length=2000, blank=True)

    def save(self, *args, **kwargs):
        # Получаем дату пятницы для даты отчета
        friday_date = datetime.strptime(friday_of_week(self.report_date.strftime('%d.%m.%Y')), "%d.%m.%Y")
        self.report_date = friday_date.strftime("%Y-%m-%d")
        super().save(*args, **kwargs)

    def __str__(self):
        return (f"{self.report_date.strftime('%d.%m.%Y')} - {self.department.name} - {self.author.last_name} "
                f"{self.author.first_name}")


class WeeklyUserDepartment(models.Model):
    """
    Список пользователей и филиалов, к которым они относятся
    Один пользователь может относиться к нескольким филиалам
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ManyToManyField(Department)

    def __str__(self):
        return f"{self.user.username}'s departments"


class WeeklyCreatorsSummaryReport(models.Model):
    """
    Список создателей сводного отчёта
    """
    creators = models.ManyToManyField(User, related_name='weekly_summary_reports')
