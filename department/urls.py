from django.urls import path
from department import views
 
urlpatterns=[
    path("list-department",views.list_department,name="list-department"),
    path('create-department', views.create_department, name='create-department'),
    path('update-department/<int:pk>', views.update_department, name='update-department'),
    path('delete-department/<int:pk>', views.delete_department, name='delete-department'),
]