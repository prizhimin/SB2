import os
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator


def invests_directory_path(instance, filename):
    # Файлы будут загружаться в MEDIA_ROOT/invests/<note_id>/<filename>
    return f'invests/{instance.investigation.id}/{filename}'


class Department(models.Model):
    # Название филиала
    name = models.CharField(verbose_name="Филиал", max_length=100)

    def __str__(self):
        return self.name


class InvestigationUserDepartment(models.Model):
    """
    Список пользователей и филиалов, к которым они относятся
    Один пользователь может относиться к нескольким филиалам
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ManyToManyField(Department)

    def __str__(self):
        return f"{self.user.username}'s departments"


class Investigation(models.Model):
    # Возможные статусы проверки
    STATUS_CHOICES = [
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
        ('suspended', 'Приостановлена'),
    ]

    # Название проверки
    title = models.CharField(verbose_name='Заголовок', max_length=200)
    # Филиал (включая полное название головного ЮЛ)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Филиал')
    # Дата приказа
    order_date = models.DateField(verbose_name="Дата приказа")
    # Номер приказа
    order_num = models.CharField(verbose_name="Номер приказа", max_length=100)
    # Краткая фабула проверки
    brief_summary = models.TextField(verbose_name="Краткая фабула проверки")
    # Инициатор проверки
    initiator = models.CharField(verbose_name="Инициатор проверки", max_length=200)
    # Дата окончания проверки
    end_date = models.DateField(verbose_name="Дата окончания проверки")
    # Дата окончания при продлении, может быть пустым
    extended_end_date = models.DateField(
        verbose_name="Дата окончания при продлении",
        null=True, blank=True
    )
    # Текущее состояние проверки с выбором из предопределенных статусов
    status = models.CharField(
        verbose_name="Текущее состояние по проверке",
        max_length=20, choices=STATUS_CHOICES, default='in_progress'
    )
    # Ущерб в миллионах рублей, значение должно быть не меньше 0
    damage_amount = models.DecimalField(
        verbose_name="Ущерб (млн. руб.)",
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0), ],
        default=0
    )
    # Возмещенная или предотвращенная сумма в миллионах рублей,
    # значение должно быть не меньше 0
    recovered_amount = models.DecimalField(
        verbose_name="Возмещено/предотвращено (млн. руб)",
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    # Краткое описание итогов проверки
    outcome_summary = models.TextField(verbose_name="Краткое описание итогов")
    # Количество работников, привлечённых к дисциплинарной ответственности,
    # значение должно быть не меньше 0
    num_employees_discipline = models.IntegerField(
        verbose_name="Количество работников, привлечённых к дисциплинарной "
                     "ответственности (в т.ч. депремировано)",
        validators=[MinValueValidator(0)],
        default=0
    )

    def __str__(self):
        return (self.title + ' ' +
                self.department.name + ' ' +
                str(self.order_date.strftime('%d.%m.%Y')) + ' ' + self.get_status_display())

    def has_attach(self):
        investigation_dir = os.path.join(settings.MEDIA_ROOT, 'invests', str(self.pk))
        if os.path.isdir(investigation_dir):
            return len(os.listdir(investigation_dir))
        return 0


class AttachedFile(models.Model):
    investigation = models.ForeignKey(Investigation, related_name='attached_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to=invests_directory_path)

    def get_filename(self):
        return os.path.basename(self.file.name)



class InvestigationCreatorsSummaryReport(models.Model):
    """
    Список создателей сводного отчёта
    """
    creators = models.ManyToManyField(User, related_name='investigations_summary_reports')
