from django.urls import path
from job import views

urlpatterns=[
    path("list-job",views.list_job,name="list-job"),
    path('create-job', views.create_job, name='create-job'),
    path('update-job/<int:pk>', views.update_job, name='update-job'),
    path('delete-job/<int:pk>', views.delete_job, name='delete-job'),
]