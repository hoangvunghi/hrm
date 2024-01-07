from django.urls import path
from job import views

urlpatterns=[
    path("job/list-job",views.list_job,name="list-job"),
    path('job/create-job', views.create_job, name='create-job'),
    path('job/update-job/<int:pk>', views.update_job, name='update-job'),
    path('job/delete-job/<int:pk>', views.delete_job, name='delete-job'),
    path("query/job",views.query_job,name="query-job"),

]