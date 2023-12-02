from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from .models import Attendance,Positions,UserAccount,Department,Leave,Leave_Type
# from django.contrib.auth.models import User

# from import_export.admin import ImportExportActionModelAdmin
# from .admin import DjangoQLSearchMixin

class HRAdminSite(AdminSite):
    """HR admin page definition"""
    site_header = "HR Neuron Admin"
    site_title = "HR Admin"
    index_title = "Welcome to the HR Neuron Admin"
hr_admin_site = HRAdminSite(name='hr_admin')


admin.site.register(Leave_Type)

@admin.register(UserAccount, site=hr_admin_site)
class HRUserAdmin(UserAdmin):
    pass

@admin.register(Positions, site=hr_admin_site)
class HRPositionsAdmin(admin.ModelAdmin):
    pass

@admin.register(Attendance, site=hr_admin_site)
class HRAttendanceAdmin(admin.ModelAdmin):
    pass


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'is_active', 'is_staff',"status","user_id"]

admin.site.register(UserAccount, UserAccountAdmin)
class DepartmentAdmin(admin.ModelAdmin):
    list_display=["department_id",'department_name']
admin.site.register(Department,DepartmentAdmin)


class PositionAdmin(admin.ModelAdmin):
    list_display=["position_id",'position_name']
admin.site.register(Positions,PositionAdmin)


class LeaveAdmin(admin.ModelAdmin):
    list_display=["employee","status",]
admin.site.register(Leave,LeaveAdmin)



class AttendanceAdmin(admin.ModelAdmin):
    list_display=["employee_id",]
admin.site.register(Attendance,AttendanceAdmin)




