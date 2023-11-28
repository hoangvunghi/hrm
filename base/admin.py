from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from .models import Attendance,Positions,UserAccount,Department,Leave,Leave_Type


class HRAdminSite(AdminSite):
    """HR admin page definition"""
    site_header = "HR Admin"
    site_title = "HR Admin"
    index_title = "Welcome to the HR Admin"

hr_admin_site = HRAdminSite(name='hr_admin')

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




# from django.shortcuts import redirect

# from django.urls import reverse,path

# class CustomAdminMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Nếu là superuser, chuyển hướng đến trang admin
#         if request.path.startswith(reverse('admin:index')) and request.user.is_superuser:
#             return self.get_response(request)
#         # Nếu là nhân viên (staff), chuyển hướng đến trang HR admin
#         elif request.path.startswith(reverse('hr_admin:index')) and request.user.is_staff:
#             return self.get_response(request)
#         # Ngược lại, chuyển hướng về trang admin
#         else:
#             return redirect(reverse('admin:index'))
