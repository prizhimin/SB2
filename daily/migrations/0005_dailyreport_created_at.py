# Generated by Django 5.0.3 on 2024-03-21 08:16

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily', '0004_creatorssummaryreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyreport',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Время создания'),
            preserve_default=False,
        ),
    ]
