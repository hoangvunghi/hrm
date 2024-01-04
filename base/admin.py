from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from .models import Employee, Project, Task,UserAccount
from timesheet.models import TimeSheet
from leave.models import LeaveRequest
from leave_type.models import LeaveType
from salary.models import SalaryHistory
from department.models import Department
from job.models import Job
from role.models import Role

admin.site.register(LeaveType)
admin.site.register(LeaveRequest)
admin.site.register(SalaryHistory)
admin.site.register(UserAccount)
admin.site.register(Job)
admin.site.register(Department)
admin.site.register(TimeSheet)
admin.site.register(Role)


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ["EmpID"]

admin.site.register(Employee, UserAccountAdmin)
