# from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path,include,re_path
from base.admin import hr_admin_site
# from rest_framework_swagger.views import get_swagger_view

# schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('djoser.urls')),
    path('auth/',include('djoser.urls.jwt')),
    path('',include('base.urls')),
    path('',include('department.urls')),
    path('',include('leave.urls')),
    path('',include('leave_type.urls')),
    path('',include('attendance.urls')),
    path('',include('position.urls')),
    path('hr_admin/', hr_admin_site.urls),  

    # path('', schema_view),
]


# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
