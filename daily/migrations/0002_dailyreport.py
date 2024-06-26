# Generated by Django 5.0.3 on 2024-03-16 19:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_date', models.DateField(auto_now_add=True, verbose_name='Отчётная дата')),
                ('field_1', models.PositiveSmallIntegerField(default=0, verbose_name='Не закрытие постов охраны')),
                ('field_2', models.PositiveSmallIntegerField(default=0, verbose_name='Отсутствие спец. средств и оружия')),
                ('field_3', models.PositiveSmallIntegerField(default=0, verbose_name='Ненадлежащее проведение досмотра')),
                ('field_4', models.PositiveSmallIntegerField(default=0, verbose_name='Самовольное покидание поста')),
                ('field_5', models.PositiveSmallIntegerField(default=0, verbose_name='Допущение проникновения посторонних лиц')),
                ('field_6', models.PositiveSmallIntegerField(default=0, verbose_name='Допущение прохода по чужому пропуску (без пропуска)')),
                ('field_7', models.PositiveSmallIntegerField(default=0, verbose_name='Нахождение на посту в нетрезвом виде')),
                ('field_8', models.PositiveSmallIntegerField(default=0, verbose_name='Неприбытие ГБР')),
                ('field_9', models.PositiveSmallIntegerField(default=0, verbose_name='Иные значимые нарушения')),
                ('field_10', models.PositiveSmallIntegerField(default=0, verbose_name='Количество проведенных проверок СБ за прошедшие сутки')),
                ('field_11', models.PositiveSmallIntegerField(default=0, verbose_name='Количество направленных претензионных писем за прошедшие сутки')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='daily.department', verbose_name='Филиал')),
            ],
        ),
    ]
