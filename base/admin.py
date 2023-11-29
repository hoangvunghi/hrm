from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from .models import Attendance,Positions,UserAccount,Department,Leave,Leave_Type
from django.contrib.contenttypes.models import ContentType

class HRAdminSite(AdminSite):
    """HR admin page definition"""
    site_header = "HR Admin"
    site_title = "HR Admin"
    index_title = "Welcome to the HR Admin"

hr_admin_site = HRAdminSite(name='hr_admin')

admin.site.register(UserAccount)
admin.site.register(Positions)
admin.site.register(Attendance)
admin.site.register(Leave)
admin.site.register(Leave_Type)
admin.site.register(Department)

@admin.register(UserAccount, site=hr_admin_site)
class HRUserAdmin(UserAdmin):
    pass

@admin.register(Positions, site=hr_admin_site)
class HRPositionsAdmin(admin.ModelAdmin):
    pass

@admin.register(Attendance, site=hr_admin_site)
class HRAttendanceAdmin(admin.ModelAdmin):
    pass


from django.contrib import admin
from django.contrib.auth.models import Group, Permission



hr_admin_group, created = Group.objects.get_or_create(name='HRAdminGroup')

content_type = ContentType.objects.get_for_model(UserAccount)
can_view_permission, created = Permission.objects.get_or_create(
    codename='can_view_hr_admin',
    name='Can view HR admin',
    content_type=content_type,
)

can_change_permission, created = Permission.objects.get_or_create(
    codename='can_change_useraccount',
    name='Can change User Account',
    content_type=content_type,
)

hr_admin_group.permissions.add(can_view_permission, can_change_permission)



