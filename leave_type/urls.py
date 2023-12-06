from django.urls import path
from leave_type import views

urlpatterns=[

    path('create_leavetype', views.create_leavetype, name='create-leavetype'),
    path('update_leavetype/<int:pk>', views.update_leavetype, name='update-leavetype'),
    path('delete_leavetype/<int:pk>', views.delete_leavetype, name='delete-leavetype'),
]