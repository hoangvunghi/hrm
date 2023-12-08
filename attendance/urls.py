from django.urls import path
from attendance import views

urlpatterns=[
    path('list_attendance', views.list_attendance, name='list-attendance'),

    path('create_attendance', views.create_attendance, name='create-attendance'),
    # path('update_attendance/<int:pk>/', views.update_attendance, name='update-attendance'),
    path('delete_attendance/<int:pk>', views.delete_attendance, name='delete-attendance'),
]