from django.urls import path
from project import views

urlpatterns = [
    path('create_project', views.create_project, name='create-project'),
    path('update_project/<str:id>', views.update_project, name='update-project'),
    path('delete_project/<str:id>', views.delete_project, name='delete-project'),
    path('find_project/', views.find_project, name='find-project'),
]
