from django.urls import path
from timesheet import views

urlpatterns=[
    path('list-timesheet', views.list_timesheet, name='list-timesheet'),
    # path('create-timesheet', views.create_timesheet, name='create-timesheet'),
    path('delete-timesheet/<int:pk>', views.delete_timesheet, name='delete-timesheet'),
    path('list-timesheet-staff', views.list_timesheet_nv, name='list-timesheet-staff'),
    path('check-in', views.check_in, name='check-in'),
    path('check-out', views.check_out, name='check-out'),
    
]