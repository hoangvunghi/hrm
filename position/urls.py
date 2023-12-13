from django.urls import path
from position import views

urlpatterns=[
    path("list-position",views.list_position,name="list-position"),
    path('create-position', views.create_position, name='create-position'),
    path('update-position/<int:pk>', views.update_position, name='update-position'),
    path('delete-position/<int:pk>', views.delete_position, name='delete-position'),
]