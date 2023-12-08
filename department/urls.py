from django.urls import path
from department import views

urlpatterns=[
    path("list_department",views.list_department,name="list-department"),
    path('create_department', views.create_department, name='create-department'),
    path('update_department/<int:pk>', views.update_department, name='update-department'),
    path('delete_department/<int:pk>', views.delete_department, name='delete-department'),
]