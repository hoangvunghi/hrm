from django.urls import path
from task import views

urlpatterns = [
    path('creat_task', views.create_task, name='create-task'),
    path('update_task/<str:id>', views.update_task, name='update-task'),
    path('delete_task/<str:id>', views.delete_task, name='delete-task'),
    path('find_task/', views.find_task, name='find-task'),
]
