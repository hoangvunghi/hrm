from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from .models import Employee, Project, Task,UserAccount
from timesheet.models import TimeSheet
from leave.models import Leave
from leave_type.models import LeaveType
from salary.models import SalaryHistory
from department.models import Department
from job.models import Job

admin.site.register(LeaveType)
admin.site.register(Leave)
admin.site.register(SalaryHistory)
admin.site.register(UserAccount)
admin.site.register(Job)
admin.site.register(Department)
admin.site.register(TimeSheet)


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ["EmpID"]

admin.site.register(Employee, UserAccountAdmin)
