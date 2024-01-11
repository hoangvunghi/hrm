from django.urls import path
from timesheet import views

urlpatterns=[
    path('timesheet/list-timesheet', views.list_timesheet, name='list-timesheet'),
    # path('create-timesheet', views.create_timesheet, name='create-timesheet'),
    # path('timesheet/delete-timesheet/<int:pk>', views.delete_timesheet, name='delete-timesheet'),
    path('timesheet/list-timesheet-staff', views.list_timesheet_nv, name='list-timesheet-staff'),
    path('timesheet/check-in', views.check_in, name='check-in'),
    path('timesheet/check-out', views.check_out, name='check-out'),
    
]