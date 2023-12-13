from django.urls import path
from leave_type import views

urlpatterns=[
    path("list-leave-type",views.list_leave_type,name="list-leave-type"),
    path('create-leavetype', views.create_leavetype, name='create-leavetype'),
    path('update-leavetype/<int:pk>', views.update_leavetype, name='update-leavetype'),
    path('delete-leavetype/<int:pk>', views.delete_leavetype, name='delete-leavetype'),
]