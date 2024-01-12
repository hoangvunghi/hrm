from django.urls import path
from role import views

urlpatterns=[
    path("role/list-role",views.list_role,name="list-role"),
    path('role/create-role', views.create_role, name='create-role'),
    path('role/update-role/<int:pk>', views.update_role, name='update-role'),
    path('role/delete-role/<int:pk>', views.delete_role, name='delete-role'),
    path("query/role",views.query_role,name="query-role"),

]