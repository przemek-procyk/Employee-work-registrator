from django.contrib import admin
from employee.models import WorkhoursRegistry, Task, Projects, OvertimeParameters


# Register your models here.

admin.site.register(WorkhoursRegistry)
admin.site.register(Task)
admin.site.register(Projects)
admin.site.register(OvertimeParameters)