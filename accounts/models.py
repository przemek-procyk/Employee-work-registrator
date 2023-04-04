from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.timezone import now as utcnow

from employee import models as emp_models
from employee.enums import WorkDayStatus

class AccountManagerCustom(BaseUserManager):

    def create_user(self,
                    email,
                    first_name,
                    last_name,
                    mobile_nr,
                    pesel,
                    password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not mobile_nr:
            raise ValueError("User must have a phone number")
        if not pesel:
            raise ValueError("User must have a PESEL number")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile_nr=mobile_nr,
            pesel=pesel,)

        user.is_staff = True

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         email,
                         first_name,
                         last_name,
                         mobile_nr,
                         pesel,
                         password):

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile_nr=mobile_nr,
            pesel=pesel)

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.set_password(password)
        user.save(using=self.db)
        return user


class UserCustom(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email", max_length=50, unique=True)
    last_login = models.DateTimeField(verbose_name="Ostatnie logowanie", auto_now=True)

    first_name = models.CharField(verbose_name="Imie", max_length=30)
    last_name = models.CharField(verbose_name="Nazwisko", max_length=50)
    mobile_nr = models.CharField(verbose_name="Nr telefonu", max_length=15)
    pesel = models.CharField(verbose_name="Nr PESEL", max_length=11) # PESEL is polish type of ID https://en.wikipedia.org/wiki/PESEL

    is_admin = models.BooleanField(verbose_name="Administrator", default=False)
    is_staff = models.BooleanField(verbose_name="Pracownik", default=False)
    is_superuser = models.BooleanField(verbose_name="Glowny administrator", default=False)
    is_active = models.BooleanField(verbose_name="Aktywny", default=True)

    holiday_allowance = models.IntegerField(verbose_name="Wymiar urlopu", default=0)

    objects = AccountManagerCustom()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name',
                       'last_name',                    
                       'mobile_nr',
                       'pesel'
                       ]

    class Meta:
        verbose_name = "Pracownik"
        verbose_name_plural = "Pracownicy"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def get_remaining_holiday(self):
        current_year = utcnow().year
        used_up_holiday_qs = emp_models.WorkhoursRegistry.objects.filter(employee=self.pk, start__year=current_year, status=WorkDayStatus.HOLIDAY)
        used_up_holiday = used_up_holiday_qs.count()
        remaining_holiday = self.holiday_allowance - used_up_holiday
        return remaining_holiday