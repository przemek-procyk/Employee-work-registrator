# Generated by Django 4.1.1 on 2022-09-29 11:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_alter_workhoursregistry_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 29, 11, 55, 56, 297096, tzinfo=datetime.timezone.utc), verbose_name='Początek zadania'),
        ),
        migrations.AlterField(
            model_name='workhoursregistry',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 29, 11, 55, 56, 296082, tzinfo=datetime.timezone.utc), verbose_name='Start pracy'),
        ),
    ]