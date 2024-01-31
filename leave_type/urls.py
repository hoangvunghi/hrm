from django.urls import path
from leave_type import views

urlpatterns=[
    path("leavetype/list-leave-type",views.list_leave_type,name="list-leave-type"),
    path('leavetype/create-leave-type', views.create_leavetype, name='create-leavetype'),
    path('leavetype/update-leave-type/<int:pk>', views.update_leavetype, name='update-leavetype'),
    path('leavetype/delete-leave-type/<int:pk>', views.delete_leavetype, name='delete-leavetype'),
    path("query/leavetype",views.query_leavetype,name="query-leavetype"),

]