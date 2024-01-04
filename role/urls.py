from django.urls import path
from role import views

urlpatterns=[
    path("list-role",views.list_role,name="list-role"),
    path('create-role', views.create_role, name='create-role'),
    path('update-role/<int:pk>', views.update_role, name='update-role'),
    path('delete-role/<int:pk>', views.delete_role, name='delete-role'),
]