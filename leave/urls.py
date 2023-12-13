from django.urls import path
from leave import views

urlpatterns=[
    path("list-leave",views.list_leave,name="list-leave"),
    path('create-leave', views.create_leave, name='create-leave'),
    path('update-leave/<int:pk>', views.update_leave, name='update-leave'),
    path('delete-leave/<int:pk>', views.delete_leave, name='delete-leave'),
]