# Generated by Django 4.1.1 on 2022-09-29 11:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workhoursregistry',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 29, 11, 11, 25, 512186, tzinfo=datetime.timezone.utc), verbose_name='Start pracy'),
        ),
    ]
