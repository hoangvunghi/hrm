from django.urls import path
from salary import views

urlpatterns=[
    path("list-salary",views.list_salary,name="list-salary"),
    path('create-salary', views.create_salary, name='create-salary'),
    path('update-salary/<int:pk>/<str:gk>', views.update_salary, name='update-salary'),
    path('delete-salary/<int:pk>', views.delete_salary, name='delete-salary'),
]