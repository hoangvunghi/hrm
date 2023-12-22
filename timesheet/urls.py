from django.urls import path
from timesheet import views

urlpatterns=[
    path('list-timesheet', views.list_timesheet, name='list-timesheet'),
    path('create-timesheet', views.create_timesheet, name='create-timesheet'),
    # path('update_attendance/<int:pk>/', views.update_attendance, name='update-attendance'),
    path('delete-timesheet/<int:pk>', views.delete_timesheet, name='delete-timesheet'),
]