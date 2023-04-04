from contextlib import nullcontext
import django_filters


from django.shortcuts import render
from django_filters.views import FilterView
from django_filters.widgets import SuffixedMultiWidget
from django.views.generic import ListView, TemplateView
from django.utils.timezone import now as utcnow
from django.contrib.auth import get_user_model
from django import forms

from datetime import timedelta

from accounts.models import UserCustom
from employee.models import Projects, Task, WorkhoursRegistry, OvertimeParameters
from employee.enums import WorkDayStatus, WorkModeStatus
from management.utilities import seconds_to_hours_from_timedelta
from management.widgets import OurDateRangeWidget

# Create your views here.


class WorkDayFilter(django_filters.FilterSet):

    class Meta:
        model = WorkhoursRegistry
        fields = ['employee']


class WorkDayListView(FilterView):
    model = WorkhoursRegistry
    template_name= 'management/today_info.html'
    filterset_class = WorkDayFilter

    def get_context_data(self, *args, **kwargs):
        _request_copy = self.request.GET.copy()
        parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
        context = super().get_context_data(*args, **kwargs)
        context['parameters'] = parameters
        return context
    
    def get_queryset(self):
        today = utcnow().date()
        tomorrow = today + timedelta(days=1)
        workdays = WorkhoursRegistry.objects.filter(start__date__range=(today, tomorrow)).all()
        return workdays


class WorkDayTaskListView(ListView):
    model = Task
    template_name = 'management/task_list.html'

    def get_queryset(self):
        workday = WorkhoursRegistry.objects.filter(id=self.kwargs['pk']).first()
        if workday:
            tasks = workday.task_set.all()
            return tasks
        else:
            return None


class ProjectTodayFilter(django_filters.FilterSet):

    class Meta:
        model = Task
        fields = ['project']
        

class ProjectTodayListView(FilterView):
    model = Task
    template_name= 'management/today_project.html'
    filterset_class = ProjectTodayFilter

    def get_context_data(self, *args, **kwargs):
        _request_copy = self.request.GET.copy()
        parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
        context = super().get_context_data(*args, **kwargs)
        context['parameters'] = parameters
        return context
    
    def get_queryset(self):
        today = utcnow().date()
        tomorrow = today + timedelta(days=1)
        tasks = Task.objects.filter(start__date__range=(today, tomorrow)).all()
        return tasks


class ProjectHoursListView(ListView):
    model = Projects
    template_name='management/pick_project.html'


class ProjectHoursView(TemplateView):
    template_name = 'management/project_hours.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(project=self.kwargs['pk']).exclude(stop__iexact=None).order_by('start')
        hours = 0
        minutes = 0
        for task in tasks:
            task_timedelta_object = task.stop - task.start
            task_time_dict = seconds_to_hours_from_timedelta(task_timedelta_object)
            hours += task_time_dict.get('full_hours')
            minutes += task_time_dict.get('clock_minutes')
    
        hours_total = hours + round(minutes / 60)   
        context['tasks'] = tasks
        context['hours'] = hours_total
        return context
        
class PickEmployeeView(ListView):
    model = get_user_model()
    template_name='management/pick_employee.html'


class OvertimeView(TemplateView):
    template_name = 'management/overtime.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = utcnow().date()
        
        # month is from 10-th to 10-th so some adjustments were needed:
        if today.day < 10:
            today = today.replace(month=(today.month -1))

        if today.month != 12: # No December no problems
            next_month = today.month + 1
            year = today.year
        else:   # because december
            next_month = 1 #January
            year = today.year + 1
        
        tenth = today.replace(day=10)
        next_tenth = tenth.replace(month=next_month, year=year)

        # get queryset with finished workdays from a monthly period
        workdays = WorkhoursRegistry.objects.filter(employee=self.kwargs['pk'], status=WorkDayStatus.WORK, start__date__range=(tenth, next_tenth)).exclude(stop__iexact=None).order_by('start')
        overtime_total = 0
        # overtime is every hour past whatever int is in parameter
        overtime_after = OvertimeParameters.objects.last().overtime_after 
        # every workhour from whichever day is in the parameter will count as overtime (1=Mon, 7=Sun)
        overtime_day = OvertimeParameters.objects.last().overtime_days

        for workday in workdays:
            workday_timedelta_object = workday.stop - workday.start
            task_time_dict = seconds_to_hours_from_timedelta(workday_timedelta_object)
            hours = task_time_dict.get('full_hours')
            
            if hours < overtime_after and workday.start.isoweekday() != overtime_day:
                continue
            
            minutes = task_time_dict.get('clock_minutes')

            if workday.start.isoweekday() == overtime_day:
                overtime_total += hours
            else:
                overtime_total += (hours - overtime_after)
            
            if minutes >= 30: # overtime counts as full hour if it`s longer than or equal to 30 minutes
                overtime_total += 1
     
        context['workdays'] = workdays
        context['overtime'] = overtime_total
        return context


class FilterPicKView(TemplateView):
    template_name = 'management/filters.html'



class WorkDayAllFilter(django_filters.FilterSet):
    start = django_filters.DateFromToRangeFilter(widget=OurDateRangeWidget())
    employee = django_filters.ModelChoiceFilter(queryset=UserCustom.objects.all(), widget=forms.Select(attrs={'style': 'font-size: 1.5em; width:100%'}))
    status = django_filters.ChoiceFilter(choices=WorkDayStatus.choices, widget=forms.Select(attrs={'style': 'font-size: 1.5em; width:100%',}))

    class Meta:
        model = WorkhoursRegistry
        fields = ['start', 'employee', 'status']
        


class WorkDayAllFilterView(FilterView):
    model = WorkhoursRegistry
    template_name= 'management/workday_all_filter.html'
    filterset_class = WorkDayAllFilter
    ordering = ['start']

    def get_context_data(self, *args, **kwargs):
        _request_copy = self.request.GET.copy()
        parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
        context = super().get_context_data(*args, **kwargs)
        context['parameters'] = parameters
        return context


class ProjectAllFilter(django_filters.FilterSet):
    project_queryset = Projects.objects.all()

    project_list_name = [(project.name, project.name) for project in project_queryset]
    name = django_filters.ChoiceFilter(choices=project_list_name, widget=forms.Select(attrs={'style': 'font-size: 1.5em; width:100%',}))


    project_list_client = [(project.client_company, project.client_company) for project in project_queryset]
    client_company = django_filters.ChoiceFilter(choices=project_list_client, widget=forms.Select(attrs={'style': 'font-size: 1.5em; width:100%',}))

    project_list_location = [(project.location, project.location) for project in project_queryset]
    location = django_filters.ChoiceFilter(choices=project_list_location, widget=forms.Select(attrs={'style': 'font-size: 1.5em; width:100%',}))

    finished = django_filters.BooleanFilter(widget=forms.NullBooleanSelect(attrs={'style': 'font-size: 1.5em; width:100%',}))

    class Meta:
        model = Projects
        fields = ['name', 'client_company', 'location', 'finished']
        


class ProjectAllFilterView(FilterView):
    model = Projects
    template_name= 'management/project_all_filter.html'
    filterset_class = ProjectAllFilter
    ordering = ['name']

    def get_context_data(self, *args, **kwargs):
        _request_copy = self.request.GET.copy()
        parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
        context = super().get_context_data(*args, **kwargs)
        context['parameters'] = parameters
        return context


class TaskAllFilter(django_filters.FilterSet):

    start = django_filters.DateFromToRangeFilter(widget=OurDateRangeWidget())
    task_queryset = Task.objects.all()
    task_list_location = set([(task.location, task.location) for task in task_queryset])
    location = django_filters.ChoiceFilter(choices=task_list_location, widget=forms.Select(attrs={'style': 'font-size: 1.5em; width:100%',}))
    project = django_filters.ModelChoiceFilter(queryset=Projects.objects.all(), widget=forms.Select(attrs={'style': 'font-size: 1.5em; width:100%'}))
    work_mode = django_filters.ChoiceFilter(choices=WorkModeStatus.choices, widget=forms.Select(attrs={'style': 'font-size: 1.5em; width:100%',}))

    class Meta:
        model = Task
        fields = ['start', 'location', 'project', 'work_mode']


class TaskAllFilterView(FilterView):
    model = Task
    template_name= 'management/task_all_filter.html'
    filterset_class = TaskAllFilter
    ordering = ['start']

    def get_context_data(self, *args, **kwargs):
        _request_copy = self.request.GET.copy()
        parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
        context = super().get_context_data(*args, **kwargs)
        context['parameters'] = parameters
        return context


class WorkerAllFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='startswith', widget=forms.TextInput(attrs={'style': 'font-size: 1.2em; width:100%',}))
    last_name = django_filters.CharFilter(lookup_expr='startswith', widget=forms.TextInput(attrs={'style': 'font-size: 1.2em; width:100%',}))
    is_active = django_filters.BooleanFilter(widget=forms.NullBooleanSelect(attrs={'style': 'font-size: 1.2em; width:100%',}))
    

    class Meta:
        model = UserCustom
        fields = ['first_name', 'last_name', 'is_active']


class WorkerAllFilterView(FilterView):
    model = UserCustom
    template_name= 'management/worker_all_filter.html'
    filterset_class = WorkerAllFilter
    ordering = ['first_name']

    def get_context_data(self, *args, **kwargs):
        _request_copy = self.request.GET.copy()
        parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
        context = super().get_context_data(*args, **kwargs)
        context['parameters'] = parameters
        return context
