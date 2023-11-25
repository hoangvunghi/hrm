from django.urls import path
from leave import views

urlpatterns=[

    path('create_leave/', views.create_leave, name='create-leave'),
    path('update_leave/<int:pk>/', views.update_leave, name='update-leave'),
    path('delete_leave/<int:pk>/', views.delete_leave, name='delete-leave'),
]