from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from .models import TimeSheet,Position,Employee,Department,Leave,LeaveType,UserAccount, Project, Task
# from django.contrib.auth.models import User
from organization.models import Organization

# from import_export.admin import ImportExportActionModelAdmin
# from .admin import DjangoQLSearchMixin

# class HRAdminSite(AdminSite):
#     """HR admin page definition"""
#     site_header = "HR Neuron Admin"
#     site_title = "HR Admin"
#     index_title = "Welcome to the HR Neuron Admin"
# hr_admin_site = HRAdminSite(name='hr_admin')

# admin.site.register(Employee,UserAccount)
admin.site.register(LeaveType)
admin.site.register(Leave)
admin.site.register(Employee)
admin.site.register(UserAccount)
admin.site.register(Position)
admin.site.register(Department)

# admin.site.register(Organization)

# @admin.register(Employee, site=hr_admin_site)
# class HRUserAdmin(UserAdmin):
#     pass

# @admin.register(Position, site=hr_admin_site)
# class HRPositionsAdmin(admin.ModelAdmin):
#     pass
  
# @admin.register(TimeSheet, site=hr_admin_site)
# class HRAttendanceAdmin(admin.ModelAdmin):
#     pass


# class UserAccountAdmin(admin.ModelAdmin):
#     list_display = ['email', 'username', 'is_active', 'is_staff',"Status","EmpID"]

# admin.site.register(Employee, UserAccountAdmin)
# class DepartmentAdmin(admin.ModelAdmin):
#     list_display=["department_id",'department_name']
# admin.site.register(Department,DepartmentAdmin)


# class PositionAdmin(admin.ModelAdmin):
#     list_display=["PosID",'PosName']
# admin.site.register(Position,PositionAdmin)


# class LeaveAdmin(admin.ModelAdmin):
#     list_display=["employee","status",]
# admin.site.register(Leave,LeaveAdmin)



# class AttendanceAdmin(admin.ModelAdmin):
#     list_display=["employee_id","check_in_time","check_out_time","attendance_date"]
# admin.site.register(TimeSheet,AttendanceAdmin)

# admin.site.register(Project)
# admin.site.register(Task)


