from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DetailView
from django.shortcuts import reverse, redirect
from django.utils.timezone import now as utcnow

from employee.mixins import RestrictWhenWorkdayAccessMixin, RestrictUnfinishedTaskAccessMixin, RestrictAbsentOrFinishedAccessMixin
from employee.models import WorkhoursRegistry, Task
from employee.enums import WorkDayStatus

from datetime import timedelta


class HomeTemplateView(TemplateView):
    template_name = 'employee\employee_home.html'


class CreateAbsenceView(LoginRequiredMixin, RestrictWhenWorkdayAccessMixin, CreateView):
    model = WorkhoursRegistry
    template_name = 'employee/absence.html'
    fields = ['start', 'status']

    def form_valid(self, form):
        objct = form.save(commit=False)
        objct.employee = self.request.user
        objct.stop = objct.start
        objct.save()
        return redirect('emp_home')


class WorkDayListView(LoginRequiredMixin, RestrictAbsentOrFinishedAccessMixin, ListView):
    model = Task
    template_name = 'employee/work_day_list.html'

    def get_queryset(self):
        today = utcnow().date()
        tomorrow = today + timedelta(days=1)

        yesterday = today - timedelta(days=1)
        workday_yesterday = WorkhoursRegistry.objects.filter(employee=self.request.user.id, start__date__range=(yesterday, today), stop=None, status__exact=WorkDayStatus.WORK).first()
        if workday_yesterday:
            tasks_daybefore = workday_yesterday.task_set.all()
            return tasks_daybefore

        workday = WorkhoursRegistry.objects.filter(employee=self.request.user.id, start__date__range=(today, tomorrow), status__exact=WorkDayStatus.WORK).first()
        if workday:
            tasks = workday.task_set.all()
            return tasks
        else:
            return None

class CreateWorkDayView(LoginRequiredMixin, CreateView):
    model = WorkhoursRegistry
    template_name = 'employee/workday_create.html'
    fields = ['start']

    def form_valid(self, form):
        today = utcnow().date()
        tomorrow = today + timedelta(days=1)
        workday = WorkhoursRegistry.objects.filter(employee=self.request.user.id, start__date__range=(today, tomorrow), status__exact=WorkDayStatus.WORK).first()
        if workday:
            return redirect('workdaylist')
        else:
            objct = form.save(commit=False)
            objct.employee = self.request.user
            objct.stop = None
            objct.status = WorkDayStatus.WORK
            objct.save()
            return redirect('workdaylist')


class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'employee/task_create.html'
    fields = ['start', 'location', 'project', 'work_mode']

    def form_valid(self, form):
        objct = form.save(commit=False)
        today = utcnow().date()
        tomorrow = today + timedelta(days=1)

        yesterday = today - timedelta(days=1)
        workday_yesterday = WorkhoursRegistry.objects.filter(employee=self.request.user.id, start__date__range=(yesterday, today), stop=None, status__exact=WorkDayStatus.WORK).first()

        if workday_yesterday:
            objct.work_day = workday_yesterday
        else:
            workday = WorkhoursRegistry.objects.filter(employee=self.request.user.id, start__date__range=(today, tomorrow), status__exact=WorkDayStatus.WORK).first()
            objct.work_day = workday
        
        objct.stop = None
        objct.save()
        return redirect('workdaylist')

class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'employee/task_update.html'
    fields = ['location', 'project', 'work_mode']

    def get_success_url(self):
        return reverse('workdaylist')


class EndTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'employee/task_end.html'
    fields = ['location']

    def form_valid(self, form):
        objct = form.save(commit=False)
        objct.stop = utcnow()
        objct.save()
        return redirect('workdaylist')


class EndWorkDayView(LoginRequiredMixin, RestrictUnfinishedTaskAccessMixin, UpdateView):
    model = WorkhoursRegistry
    template_name = 'employee/workday_end.html'
    fields = ['status']

    def form_valid(self, form):
        objct = form.save(commit=False)
        objct.stop = utcnow()
        objct.save()
        return redirect('emp_home')


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'employee/emp_detail.html' 