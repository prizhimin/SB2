# Generated by Django 5.0.4 on 2024-04-22 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_weekly', '0006_alter_weeklyreport_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeklyreport',
            name='field5',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True, verbose_name='Входной контроль (сумма, в млн. руб. без НДС)'),
        ),
    ]
