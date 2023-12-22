from django.urls import path
from . import views, models

from django.contrib import admin

 
urlpatterns=[
    path("login", views.user_login_view, name="login"),
    # path("logout/", views.logout_user, name="logout"),
    # path("register", views.user_register_view, name="register"),
    path('employee/create-useraccount', views.create_useraccount, name='create-account'),
    path("employee/list-account",views.find_employee,name="list-EmpID"),
    path('employee/create-employee', views.create_employee, name='create-employee'),
    path('employee/update-employee/<str:pk>', views.update_employee, name='update-employee'),
    path('employee/delete-employee/<str:pk>', views.delete_employee, name='delete-employee'),
    path('change-password/<str:pk>', views.change_password, name='change-password'),
    path('find-employee', views.find_employee, name='find_employee'),
    path("",views.a),
    path("employee/list-employee",views.list_employee,name="list-employee"), 
]


