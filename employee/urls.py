from django.urls import path
from django.views.generic import TemplateView

from employee.views import HomeTemplateView, CreateAbsenceView, CreateWorkDayView, WorkDayListView, CreateTaskView, UpdateTaskView, EndTaskView, EndWorkDayView, EmployeeDetailView

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='emp_home'),
    path('absence/', CreateAbsenceView.as_view(), name='absence'),
    path('workdaylist/', WorkDayListView.as_view(), name='workdaylist'),
    path('workdaycreate/', CreateWorkDayView.as_view(), name='workdaycreate'),
    path('taskcreate/', CreateTaskView.as_view(), name='taskcreate'),
    path('taskupdate/<int:pk>', UpdateTaskView.as_view(), name='taskupdate'),
    path('taskend/<int:pk>', EndTaskView.as_view(), name='taskend'),
    path('workdayend/<int:pk>', EndWorkDayView.as_view(), name='workdayend'),
    path('emp_detail/<int:pk>', EmployeeDetailView.as_view(), name='emp_detail'),
    path('errors/<str:msg>',TemplateView.as_view(template_name='employee/errors.html'), name='errors'),
]