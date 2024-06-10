from django.db import models
from django.contrib.auth.models import User


class SemiAnnual2024Company(models.Model):
    name = models.CharField(max_length=255)
    line_number = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.name}"


class SemiAnnual2024UserCompany(models.Model):
    """
    Определяет какой филиал(ы) может редактировать пользователь
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    companies = models.ManyToManyField(SemiAnnual2024Company)

    def __str__(self):
        return f"{self.user.username} - {', '.join([company.name for company in self.companies.all()])}"


class SemiAnnual2024CreatorsSummaryReport(models.Model):
    """
    Список создателей сводного отчёта
    """
    creators = models.ManyToManyField(User, related_name='semi_annual_2024_summary_reports')


class SemiAnnual2024Report(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    company = models.OneToOneField(SemiAnnual2024Company, verbose_name='Компания/Филиал ПАО "Т Плюс"', on_delete=models.CASCADE)

    # ------------------ КАДРЫ
    field_1 = models.PositiveIntegerField(verbose_name="Штатная численность СБ (чел.)", default=0)
    field_2 = models.PositiveIntegerField(verbose_name="Фактическая численность СБ (чел.) на 31.05.2024", default=0)
    # ------------------ УД БЕЗ ДЗ
    field_3 = models.PositiveIntegerField(verbose_name="Направлено заявлений в правоохранительные органы за период с "
                                                       "01.01 по 31.05.2024 (кол-во без дебиторской задолженности)",
                                          default=0)
    field_4 = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Заявленный причиненный ущерб по "
                                                                                "заявлениям из предыдущего столбца ("
                                                                                "млн руб.)", default=0)
    # *осуществлялось в 2024 году сопровождение расследования уголовных дел (с остатком прошлых лет)
    field_5 = models.PositiveIntegerField(verbose_name="158", default=0)
    field_6 = models.PositiveIntegerField(verbose_name="159", default=0)
    field_7 = models.PositiveIntegerField(verbose_name="165", default=0)
    field_8 = models.PositiveIntegerField(verbose_name="160", default=0)
    field_9 = models.PositiveIntegerField(verbose_name="204", default=0)
    field_10 = models.PositiveIntegerField(verbose_name="247", default=0)
    field_11 = models.PositiveIntegerField(verbose_name="др.", default=0)
    # ^^^^^^^^^^^^^^^^^^^
    field_12 = models.PositiveIntegerField(verbose_name="Кол-во оконченых расследованием уд с направлением в суд за "
                                                        "период с 01.01 по 31.05.2024 из сопровождаемых (с остатком "
                                                        "прошлых лет)", default=0)
    field_13 = models.PositiveIntegerField(verbose_name="Кол-во приговоров вступивших в законную силу за период с "
                                                        "01.01 по 31.05.2024 по сопровождаемым уголовным делам (с "
                                                        "остатком прошлых лет)", default=0)
    # *по фактам бездействия правоохранительных органов, в том числе на нарушения процессуальных сроков в надзорные органы в период с 01.01 по 31.05.2024 направлено
    field_14 = models.PositiveIntegerField(verbose_name="Ходатайств", default=0)
    field_15 = models.PositiveIntegerField(verbose_name="Жалоб", default=0)
    # ^^^^^^^^^^^^^^^^^^^
    # *за период с 01.01 по 31.05.2024 по дату отчета возмещен причиненный ущерб по результатам (с учетом заявлений прошлых лет) (млн руб.)
    field_16 = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Уголовного преследования", default=0)
    field_17 = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Доследственных проверок", default=0)
    # ^^^^^^^^^^^^^^^^^^^
    # *на 01.06.2024 осуществляется сопровождение (с остатком прошлых лет)
    field_18 = models.PositiveIntegerField(verbose_name="Уголовных дел", default=0)
    field_19 = models.PositiveIntegerField(verbose_name="Материалов проверок", default=0)
    # ^^^^^^^^^^^^^^^^^^^
    # ------------------ АНТИКОРПОРАТИВ И КОРРУПЦИОННЫЕ
    field_20 = models.PositiveIntegerField(verbose_name="Выявлено фактов с 01.01. по 31.05.2024", default=0)
    field_21 = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="По данным фактам причинен ущерб ("
                                                                                 "млн руб.)", default=0)
    field_22 = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="По данным фактам возмещен ущерб ("
                                                                                 "млн руб.)", default=0)
    field_23 = models.PositiveIntegerField(verbose_name="Привлечено к ответственности", default=0)
    field_24 = models.PositiveIntegerField(verbose_name="В т.ч. руководителей", default=0)
    field_25 = models.PositiveIntegerField(verbose_name="Уволено", default=0)
    # ------------------ ОХРАНА
    field_26 = models.PositiveIntegerField(verbose_name="Проведено проверок несения службы за период с 01.01. по "
                                                        "31.05.2024", default=0)
    # *по результатам проверок выявлено нарушений
    field_27 = models.PositiveIntegerField(verbose_name="Пропускного и внутриобъектового режимов", default=0)
    field_28 = models.PositiveIntegerField(verbose_name="Исполнения работниками охранных предприятий своих "
                                                        "обязанностей", default=0)
    field_29 = models.PositiveIntegerField(verbose_name="др.", default=0)
    # ^^^^^^^^^^^^^^^^^^^
    field_30 = models.PositiveIntegerField(verbose_name="По выявленным нарушениям направлено претензионных писем за "
                                                        "период с 01.01 по 31.05.2024", default=0)
    field_31 = models.PositiveIntegerField(verbose_name="Привлечено к дисциплинарной ответственности", default=0)
    field_32 = models.PositiveIntegerField(verbose_name="Уволено", default=0)
    field_33 = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Удержана неустойка "
                                                                                 "на сумму (млн руб)", default=0)
    # ------------------ ПРОВЕРКА ЮЛ И ФЛ
    field_34 = models.PositiveIntegerField(verbose_name="В период с 01.01 по 31.05.2024 изучено юр. лиц (подрядчики , "
                                                        "субподрядчики), принявшие участие в закупочных процедурах ("
                                                        "кол-во)", default=0)
    field_35 = models.PositiveIntegerField(verbose_name="Из них обоснованно отклонены", default=0)
    field_36 = models.PositiveIntegerField(verbose_name="Изучено физ. лиц , заявившихся к трудоустройству, а также "
                                                        "собственники или руководители потенциальных подрядчиков ("
                                                        "кол-во)", default=0)
    field_37 = models.PositiveIntegerField(verbose_name="Из них обоснованно отклонены", default=0)
    # ------------------ ТРАВМАТИЗМ
    # *пострадало лиц от оперативной деятельности за период с 01.01. по 31.05.2024
    field_38 = models.PositiveIntegerField(verbose_name="Работники компании", default=0)
    field_39 = models.PositiveIntegerField(verbose_name="Подрядчики", default=0)
    field_40 = models.PositiveIntegerField(verbose_name="Сторонние лица", default=0)
    # ^^^^^^^^^^^^^^^^^^^
    # *в том числе с летальным исходом
    field_41 = models.PositiveIntegerField(verbose_name="Работники компании", default=0)
    field_42 = models.PositiveIntegerField(verbose_name="Подрядчики", default=0)
    field_43 = models.PositiveIntegerField(verbose_name="Сторонние лица", default=0)
    # ^^^^^^^^^^^^^^^^^^^
    # ------------------ АВАРИЙНОСТЬ
    # *зафиксировано аварий на оборудовании за период с 01.01. по 31.05.2024
    field_44 = models.PositiveIntegerField(verbose_name="Кол-во", default=0)
    field_45 = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Ущерб (млн руб)", default=0)
    # ^^^^^^^^^^^^^^^^^^^
    # *зафиксировано инцидентов на тепловых сетях за период с 01.01. по 31.05.2024
    field_46 = models.PositiveIntegerField(verbose_name="Кол-во", default=0)
    field_47 = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Ущерб (млн руб)", default=0)
    # ^^^^^^^^^^^^^^^^^^^
    # ------------------ АНАЛИТИКА
    # *направлено в СБ КЦ за период с 01.01. по 31.05.2024 (без сводок)
    field_48 = models.PositiveIntegerField(verbose_name="Тематические сообщения о деятельности СБ", default=0)
    field_49 = models.PositiveIntegerField(verbose_name="Справочные материалы в рамках установленной отчетности",
                                           default=0)
    # ^^^^^^^^^^^^^^^^^^^
    field_50 = models.PositiveIntegerField(verbose_name="Служебные записки руководству по проблемным вопросам, "
                                                        "требующим мер реагирования", default=0)
    field_51 = models.PositiveIntegerField(verbose_name="Инициативные информационные письма, направленные в ФОИВ и "
                                                        "региональные , а также правоохранительные органы о "
                                                        "проблемных вопросах, требующих рассмотрения (не ответы на "
                                                        "запросы)", default=0)

    def __str__(self):
        return f"SemiAnnual2024Report by {self.user.username} on {self.created_at}"
