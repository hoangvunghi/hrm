from django.urls import path
from position import views

urlpatterns=[
    path("list_position",views.list_position,name="list-position"),
    path('create_position', views.create_position, name='create-position'),
    path('update_position/<int:pk>', views.update_position, name='update-position'),
    path('delete_position/<int:pk>', views.delete_position, name='delete-position'),
]