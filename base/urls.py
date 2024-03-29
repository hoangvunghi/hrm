from django.urls import path
from . import views, models
from django.contrib.auth import views as auth_views
from django.contrib import admin



 
urlpatterns=[
    path('account/refresh-token/', views.refresh_token_view, name='refresh_token'),
    path("login", views.user_login_view, name="login"),
    # path('employee/create-useraccount', views.create_useraccount, name='create-account'),
    path("employee/list-account",views.find_employee,name="list-EmpID"),
    path('employee/create-employee', views.create_employee, name='create-employee'),
    path('employee/update-employee/<str:pk>', views.update_employee, name='update-employee'),
    path('employee/delete-employee/<str:pk>', views.delete_employee, name='delete-employee'),
    # path('change-password/<str:pk>', views.change_password, name='change-password'),
    path('employee/list-username', views.list_user_password, name="list_user_password"),
    path("",views.a),
    path('account/reset-password/<int:pk>', views.reset_employee_password, name='reset_employee_password'),
    path("employee/list-employee",views.list_employee,name="list-employee"), 
    path("account/change-password/<str:pk>", views.change_password,name="change-password"),
    path("account/delete-account/<str:pk>",views.delete_account, name="delete-account"),
    path("account/update-account/<str:pk>", views.update_account,name="update-account"),
    path('forgot/forgot-password', views.forgot_password_view, name='forgot_password'),
    path('forgot/reset-password/<str:token>', views.reset_password_view, name='reset_password'),
    path("employee/birthday",views.get_birthday_employee,name="get-birthday"),
    path("query/employee",views.query_employee,name="query-employee"),
    # path("query/useraccount",views.query_useraccount,name="query-useraccount"),

]

