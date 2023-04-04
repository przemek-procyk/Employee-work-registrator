from datetime import timedelta
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.timezone import now as utcnow
from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import ImproperlyConfigured
from employee.enums import WorkDayStatus as wds

from employee.models import WorkhoursRegistry

class RedirectMixin:
    """
    Redirect to redirect_url if the test_func() method returns False.
    """

    redirect_url = None
    error_msg = None

    def get_redirect_url(self):
        """
        Override this method to override the redirect_url attribute.
        """
        redirect_url = self.redirect_url 

        if not redirect_url:
            raise ImproperlyConfigured(
                '{0} is missing the redirect_url attribute. Define {0}.redirect_url or override '
                '{0}.get_redirect_url().'.format(self.__class__.__name__)
            )
        return str(redirect_url)

    def test_func(self):
        raise NotImplementedError(
            '{0} is missing the implementation of the test_func() method.'.format(self.__class__.__name__)
        )

    def get_test_func(self):
        """
        Override this method to use a different test_func method.
        """
        return self.test_func

    def dispatch(self, request, *args, **kwargs):
        test_result = self.get_test_func()()
        if not test_result:
            return redirect(reverse(self.redirect_url, args=(self.error_msg, )))
        return super().dispatch(request, *args, **kwargs)


class RestrictAbsentOrFinishedAccessMixin(RedirectMixin):
    """ if user has already reported absence or ended work, raise custom 403 error message"""

    error_msg = "Zgłosiłeś już nieobecność lub zakończyłeś pracę"
    redirect_url = 'errors'
    
    def test_func(self):       
        today = utcnow().date()
        tomorrow = today + timedelta(days=1)
        workday_absent = WorkhoursRegistry.objects.filter(employee=self.request.user.id, start__date__range=(today, tomorrow)).exclude(status__iexact=wds.WORK).first()
        workday_finished = WorkhoursRegistry.objects.filter(employee=self.request.user.id, start__date__range=(today, tomorrow), status__exact=wds.WORK,).exclude(stop__iexact=None).first()
        if workday_absent or workday_finished:
            return False
        else:
            return True


class RestrictWhenWorkdayAccessMixin(RedirectMixin):
    """ if user has already reported absence, redirect to custom error template"""

    error_msg = "Zgłosiłeś już nieobecność lub rozpocząłeś pracę"
    redirect_url = 'errors'

    def test_func(self):       
        today = utcnow().date()
        tomorrow = today + timedelta(days=1)
        workday = WorkhoursRegistry.objects.filter(employee=self.request.user.id, start__date__range=(today, tomorrow)).first()
        if workday:
            return False
        else:
            return True


class RestrictUnfinishedTaskAccessMixin(RedirectMixin):
    """ if user has any unfinished task for the day, raise custom 403 error message"""

    error_msg = "Masz niezakończone zadania"
    redirect_url = 'errors'

    def test_func(self):       
        today = utcnow().date()
        tomorrow = today + timedelta(days=1)

        yesterday = today - timedelta(days=1)
        workday_yesterday = WorkhoursRegistry.objects.filter(employee=self.request.user.id, start__date__range=(yesterday, today), stop=None, status__exact=wds.WORK).first()
        if workday_yesterday:
            tasks = workday_yesterday.task_set.all()
        else:
            workday = WorkhoursRegistry.objects.filter(employee=self.request.user.id, start__date__range=(today, tomorrow), status__exact=wds.WORK).first()
            tasks = workday.task_set.all()
            
        for task in tasks:
            if task.stop == None:
                return False 
            else:
                return True




################################################################################################################################
# Old 403 errors, do not work on azure                                                                                         #
################################################################################################################################
# class RestrictWhenWorkdayAccessMixin(UserPassesTestMixin):
#     """ if user has already reported absence, raise custom 403 error message"""

#     permission_denied_message = "Zgłosiłeś już nieobecność lub rozpocząłeś pracę"

#     def test_func(self):       
#         today = utcnow().date()
#         tomorrow = today + timedelta(days=1)
#         workday = WorkhoursRegistry.objects.filter(employee=self.request.user.id, start__date__range=(today, tomorrow)).first()
#         if workday:
#             return False
#         else:
#             return True


# class RestrictUnfinishedTaskAccessMixin(UserPassesTestMixin):
#     """ if user has any unfinished task for the day, raise custom 403 error message"""

#     permission_denied_message = "Masz niezakończone zadania"

#     def test_func(self):       
#         today = utcnow().date()
#         tomorrow = today + timedelta(days=1)

#         yesterday = today - timedelta(days=1)
#         workday_yesterday = WorkhoursRegistry.objects.filter(employee=self.request.user.id, start__date__range=(yesterday, today), stop=None, status__exact=wds.WORK).first()
#         if workday_yesterday:
#             tasks = workday_yesterday.task_set.all()
#         else:
#             workday = WorkhoursRegistry.objects.filter(employee=self.request.user.id, start__date__range=(today, tomorrow), status__exact=wds.WORK).first()
#             tasks = workday.task_set.all()
            
#         for task in tasks:
#             if task.stop == None:
#                 return False 
#             else:
#                 return True

# class RestrictAbsentOrFinishedAccessMixin(UserPassesTestMixin):
#     """ if user has already reported absence or ended work, raise custom 403 error message"""

#     permission_denied_message = "Zgłosiłeś już nieobecność lub zakończyłeś pracę"
    
#     def test_func(self):       
#         today = utcnow().date()
#         tomorrow = today + timedelta(days=1)
#         workday_absent = WorkhoursRegistry.objects.filter(employee=self.request.user.id, start__date__range=(today, tomorrow)).exclude(status__iexact=wds.WORK).first()
#         workday_finished = WorkhoursRegistry.objects.filter(employee=self.request.user.id, start__date__range=(today, tomorrow), status__exact=wds.WORK,).exclude(stop__iexact=None).first()
#         if workday_absent or workday_finished:
#             return False
#         else:
#             return True