from django.urls import path
from department import views
 
urlpatterns=[
    path("department/list-department",views.list_department,name="list-department"),
    path('department/create-department', views.create_department, name='create-department'),
    path('department/update-department/<int:pk>', views.update_department, name='update-department'),
    path('department/delete-department/<int:pk>', views.delete_department, name='delete-department'),
    path("query/department",views.query_department,name="query-department"),
]