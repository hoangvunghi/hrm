from django.urls import path
from salary import views

urlpatterns=[
    path("salary/list-salary",views.list_salary,name="list-salary"),
    path('salary/create-salary', views.create_salary, name='create-salary'),
    path('salary/update-salary/<int:pk>/<str:gk>', views.update_salary, name='update-salary'),
    path('salary/delete-salary/<int:pk>', views.delete_salary, name='delete-salary'),
]