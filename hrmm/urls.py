# from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path,include,re_path
# from base.admin import hr_admin_site
from rest_framework_swagger.views import get_swagger_view
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView
# schema_view = get_swagger_view(title='Pastebin API')



# schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('auth/',include('djoser.urls')),
    # path('auth/',include('djoser.urls.jwt')),
    path('',include('base.urls')),
    path('',include('department.urls')),
    path('',include('leave.urls')),
    path('',include('leave_type.urls')),
    path('',include('timesheet.urls')),
    path('',include('job.urls')),
    # path('hr_admin/', hr_admin_site.urls),  
    # url("api/", schema_view)
    # path("organization/",include('organization.urls')),
    path("",include('salary.urls')),
    path("api/schema/",SpectacularAPIView.as_view(),name="schema"),
    path("docs/",SpectacularSwaggerView.as_view(url_name="schema")),
    path('project/', include('project.urls')),
    path("",include("role.urls")),

    # path('', schema_view),
]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
