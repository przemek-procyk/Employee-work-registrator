# Generated by Django 4.1.1 on 2022-10-04 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_alter_workhoursregistry_stop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='stop',
            field=models.DateTimeField(null=True, verbose_name='Zakończenie zadania'),
        ),
    ]