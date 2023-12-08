from django.urls import path
from organization import views

urlpatterns=[
    path("view_organization",views.view_organization,name="view-organization"),
    path("update_organization",views.update_organization,name="update-organization"),
]