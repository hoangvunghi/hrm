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
from django.http import HttpResponse

def export_to_txt(modeladmin, request, queryset):
    content = "\n".join([f"{field}: {getattr(obj, field)}" for obj in queryset for field in obj.__dict__])

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=exported_data.txt'

    return response

export_to_txt.short_description = "Export selected objects to txt"

# admin.site.register(LeaveType)
admin.site.register(SalaryHistory)
# admin.site.register(UserAccount)
# admin.site.register(Job)

# admin.site.register(TimeSheet)
admin.site.register(Role)

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ["EmpID"]

admin.site.register(UserAccount, UserAccountAdmin)

class TimeSheetInline(admin.TabularInline):
    model = TimeSheet
class EmployeeAdmin(admin.ModelAdmin):
    inlines = [TimeSheetInline]
    list_display = ["EmpName", "get_dep_name",]
    raw_id_fields = ["DepID", "JobID","RoleID"]
    # list_editable = ["EmpStatus"]
    # fieldsets = [
    #     ('Main Information', {
    #         'fields': ['EmpName', 'Phone', 'HireDate', 'BirthDate', 'Address', 'PhotoPath', 'Email', 'Gender', 'RoleID', 'TaxCode', 'CCCD', 'BankAccountNumer', 'BankName', 'EmpStatus','DepID', 'JobID'],
    #     }),
    #     ('Department and Job Information', {
    #         'fields': [],
    #         'classes': ['collapse'],
    #     }),
    # ]

    def get_dep_name(self, obj):
        return obj.DepID.DepName if obj.DepID else ''

    get_dep_name.short_description = 'Department Name'

admin.site.register(Employee, EmployeeAdmin)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["DepID", "DepName","ManageID"]

admin.site.register(Department, DepartmentAdmin)

class JobAdmin(admin.ModelAdmin):
    list_display = ["JobID", "JobName",]
    raw_id_fields = ["DepID",]

admin.site.register(Job, JobAdmin)



class LeaveAdmin(admin.ModelAdmin):
    list_display = ["get_name", "LeaveStatus", "LeaveTypeID", "LeaveStartDate", "LeaveEndDate"]
    raw_id_fields = ["LeaveTypeID"]

    def get_name(self, obj):
        return obj.EmpID.EmpName if obj.EmpID else ''

    get_name.short_description = 'Employee Name'

admin.site.register(LeaveRequest, LeaveAdmin)

class LeaveTypeAdmin(admin.ModelAdmin):
    list_display=["LeaveTypeID","LeaveTypeName"]
admin.site.register(LeaveType,LeaveTypeAdmin)





class TimeAdmin(admin.ModelAdmin):
    list_display = ["get_name", "TimeIn", "TimeOut","TimeStatus",]
    raw_id_fields = ["EmpID"]
    actions = [export_to_txt,]
    def get_name(self, obj):
        return obj.EmpID.EmpName if obj.EmpID else ''

    get_name.short_description = "Employee Name"

admin.site.register(TimeSheet, TimeAdmin)


