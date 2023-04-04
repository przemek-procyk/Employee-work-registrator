from django.db import models

class WorkDayStatus(models.TextChoices):
    WORK = 'P', 'Praca'
    HOLIDAY = 'U', 'Urlop'
    SICK_LEAVE = 'C', 'Choroba'
    CHILD_CARE = 'O', 'Opieka'


class WorkModeStatus(models.TextChoices):
    HOME_OFFICE = 'HO', 'Home office'
    ON_SITE = 'F', 'W Firmie'
    DELEGATION = 'D', 'Delegacja'
    MAINTENANCE=  'S', 'Serwis'