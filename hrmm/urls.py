# from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path,include,re_path
from base.admin import hr_admin_site
from rest_framework_swagger.views import get_swagger_view
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView
# schema_view = get_swagger_view(title='Pastebin API')



# schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('djoser.urls')),
    path('auth/',include('djoser.urls.jwt')),
    path('',include('base.urls')),
    path('department/',include('department.urls')),
    path('leave/',include('leave.urls')),
    path('leave_type/',include('leave_type.urls')),
    path('attendance/',include('attendance.urls')),
    path('position/',include('position.urls')),
    path('hr_admin/', hr_admin_site.urls),  
    # url("api/", schema_view)
    path("organization/",include('organization.urls')),
    path("api/schema/",SpectacularAPIView.as_view(),name="schema"),
    path("docs/",SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/schema",SpectacularAPIView.as_view(),name="schema"),
    path("docs",SpectacularSwaggerView.as_view(url_name="schema")),
    path('', include('project.urls')),

    # path('', schema_view),
]


# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
