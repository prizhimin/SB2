# Generated by Django 5.0.4 on 2024-04-27 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('daily', '0007_alter_dailyreport_department_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dailyreport',
            options={'ordering': ('-report_date',)},
        ),
    ]
