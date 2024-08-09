# Generated by Django 5.0.7 on 2024-08-07 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investigations', '0005_alter_investigation_brief_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investigation',
            name='num_employees_discipline_demotion',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Количество работников, привлечённых к дисциплинарной ответственности (депремировано)'),
        ),
        migrations.AlterField(
            model_name='investigation',
            name='num_employees_discipline_fired',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Количество работников, привлечённых к дисциплинарной ответственности (уволено)'),
        ),
        migrations.AlterField(
            model_name='investigation',
            name='num_employees_discipline_reduction',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Количество работников, привлечённых к дисциплинарной ответственности (понижено в должности)'),
        ),
        migrations.AlterField(
            model_name='investigation',
            name='num_employees_discipline_reprimand',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Количество работников, привлечённых к дисциплинарной ответственности (выговор)'),
        ),
        migrations.AlterField(
            model_name='investigation',
            name='num_employees_discipline_warning',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Количество работников, привлечённых к дисциплинарной ответственности (замечание)'),
        ),
    ]