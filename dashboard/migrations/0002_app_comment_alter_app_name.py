# Generated by Django 5.0.3 on 2024-03-19 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='comment',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='app',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
