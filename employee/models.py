# from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.timezone import now as utcnow
from django.contrib.auth import get_user_model

from employee.enums import WorkDayStatus, WorkModeStatus


class WorkhoursRegistry(models.Model):
    """
    DateTimeField auto_now_add replaced with default=timezone.now(),
    Because auto_now_add is no longer fully supported.
    """
    start = models.DateTimeField(verbose_name="Start pracy", default=utcnow)
    stop = models.DateTimeField(verbose_name="Koniec pracy", null=True)
    employee = models.ForeignKey(get_user_model(), verbose_name="Pracownik", on_delete=models.PROTECT)
    status = models.CharField(verbose_name="Status", choices=WorkDayStatus.choices, default=WorkDayStatus.WORK, max_length=20)

    class Meta:
        verbose_name = "Dzień Pracy"
        verbose_name_plural = "Dni Pracy"

    def __str__(self):
        label = f'{self.employee} dzień {self.start.astimezone()}'
        len_label = len(label)
        len_strip = 6
        return label[0:(len_label-len_strip):] # removes 6 ending characters as in +02:00


class Projects(models.Model):
    name = models.CharField(verbose_name="Nazwa projektu", max_length=100)
    client_company = models.CharField(verbose_name="Nazwa firmy", max_length=50)
    location = models.CharField(verbose_name="Lokalizacja firmy", max_length=50)
    finished = models.BooleanField(verbose_name="Projekt ukończony", default=False)
    
    class Meta:
        verbose_name = "Projekt"
        verbose_name_plural = "Projekty"

    def __str__(self):
        return f'{self.name} dla {self.client_company}'


class Task(models.Model):
    start = models.DateTimeField(verbose_name="Początek zadania", default=utcnow)
    stop = models.DateTimeField(verbose_name="Zakończenie zadania", null=True)
    location = models.CharField(verbose_name="Miejsce pracy", max_length=50)
    project = models.ForeignKey(Projects, verbose_name="Projekt", on_delete=models.PROTECT)
    work_mode = models.CharField(verbose_name="Tryb pracy", choices=WorkModeStatus.choices, max_length=20)
    work_day = models.ForeignKey(WorkhoursRegistry, verbose_name="Dzień pracy", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Zadanie"
        verbose_name_plural = "Zadania"

    def __str__(self):
        work_mode_read = WorkModeStatus(self.work_mode).label
        label = f'{work_mode_read} {self.work_day.employee} {self.project} dnia {self.start.astimezone()}'
        len_label = len(label)
        len_strip = 6
        return label[0:(len_label-len_strip):]

class OvertimeParameters(models.Model):

    overtime_after = models.IntegerField(verbose_name="Nadgodziny po")
    # overtime_days = ArrayField(models.IntegerField(verbose_name="Dni nadgodzin #"))
    overtime_days = models.IntegerField(verbose_name="Dzien nadgodzin")

    class Meta:
        verbose_name = "Parametr Nadgodzin"
        verbose_name_plural = "Parametry Nadgodzin"
    
    def __str__(self):
        return f"Nadgodziny po {self.overtime_after} godzinach pracy w dni: {self.overtime_days}"
