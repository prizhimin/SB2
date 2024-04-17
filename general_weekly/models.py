from django.db import models
from django.contrib.auth.models import User
from commondata.models import Department


class WeeklyReport(models.Model):
    """
    Еженедельный отчёт филиалов
    """
    created_at = models.DateTimeField('Время создания', auto_now_add=True,
                                      editable=False)  # Нередактируемое поле с временем создания
    report_date = models.DateField('Отчётная дата')
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    field1 = models.DecimalField('Экономический эффект (сумма, в млн. руб. без НДС)', max_digits=10, decimal_places=3)
    field2 = models.CharField('Наиболее значимый пример', max_length=1000, blank=True)
    field3 = models.DecimalField('Выявлено неучтённых ТМЦ (сумма, в млн. руб. без НДС)', max_digits=10,
                                 decimal_places=3)
    field4 = models.CharField('Наиболее значимый пример', max_length=1000, blank=True)
    field5 = models.DecimalField('Входной контроль (сумма, в млн. руб. без НДС)', max_digits=10, decimal_places=3)
    field6 = models.CharField('Наиболее значимый пример', max_length=1000, blank=True)
    field7 = models.PositiveIntegerField('Количество запросов, актов реагирования от\n'
                                         'контрольно-надзорых и правоохранительных органов,\n'
                                         'поступивших в отчётном периоде', default=0)
    field8 = models.CharField('Наиболее значимый пример', max_length=1000, blank=True)
    field9 = models.PositiveIntegerField('Количество запросов, актов реагирования, поручений\n'
                                         'из территориальных органов власти, поступивших\n'
                                         'в отчётном периоде', default=0)
    field10 = models.CharField('Наиболее значимый пример', max_length=1000, blank=True)
    field11 = models.PositiveIntegerField('Направлено заявлений в правоохранительные органы\n'
                                          'для защиты интересова Компании', default=0)
    field12 = models.CharField('Наиболее значимый пример', max_length=1000, blank=True)
    field13 = models.PositiveIntegerField('Проведено встреч, рабочих групп с сотрудниками\n'
                                          'правоохратиельных органов, контрольно-нажзорных органов', default=0)
    field14 = models.CharField('Наиболее значимый пример', max_length=1000, blank=True)
    field15 = models.PositiveIntegerField('Выявлено фактов антикорпоративных проявлений', default=0)
    field16 = models.CharField('Наиболее значимый пример', max_length=1000, blank=True)
    field17 = models.PositiveIntegerField('Инициировано служеюных проверок', default=0)
    field18 = models.CharField('Наиболее значимый пример', max_length=1000, blank=True)
    field19 = models.CharField('Значимая информация, факты, события, риски и т.д.', max_length=2000, blank=True)

