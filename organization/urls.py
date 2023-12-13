from django.urls import path
from organization import views

urlpatterns=[
    path("view-organization",views.view_organization,name="view-organization"),
    path("update-organization",views.update_organization,name="update-organization"),
]