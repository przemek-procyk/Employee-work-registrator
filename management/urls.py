from django.urls import path
from django.views.generic import TemplateView

from management.views import WorkDayListView, WorkDayTaskListView, ProjectTodayListView, ProjectHoursListView, ProjectHoursView, PickEmployeeView, OvertimeView, FilterPicKView, WorkDayAllFilterView, ProjectAllFilterView, TaskAllFilterView, WorkerAllFilterView



urlpatterns = [
    path('', TemplateView.as_view(template_name='management/base_manage.html'), name='manage'),
    path('todayinfo/', WorkDayListView.as_view(), name='today_info'),
    path('todayproject/',ProjectTodayListView.as_view(), name='today_project'),
    path('pickproject/',ProjectHoursListView.as_view(), name='pick_project'),
    path('projecthours/<int:pk>', ProjectHoursView.as_view(), name='project_hours'),
    path('pickemployee/',PickEmployeeView.as_view(), name='pick_employee'),
    path('overtime/<int:pk>',OvertimeView.as_view(template_name='management/overtime.html'), name='overtime'),
    path('filters/',FilterPicKView.as_view(), name='filters'),
    path('tasklist/<int:pk>', WorkDayTaskListView.as_view(), name='tasklist'),
    path('workdayfilter', WorkDayAllFilterView.as_view(), name='workdayfilter'),
    path('projectfilters', ProjectAllFilterView.as_view(), name='projectfilter'),
    path('taskfilter', TaskAllFilterView.as_view(), name='taskfilter'),
    path('workerfilter', WorkerAllFilterView.as_view(), name='workerfilter'),
]