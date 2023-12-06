from django.urls import path
from . import views, models

from django.contrib import admin


urlpatterns=[
    path("login", views.user_login_view, name="login"),
    # path("logout/", views.logout_user, name="logout"),
    # path("register", views.user_register_view, name="register"),
    path('employee/create_employee', views.create_employee, name='create-employee'),
    path('employee/update_employee/<str:pk>', views.update_employee, name='update-employee'),
    path('employee/delete_employee/<str:pk>', views.delete_employee, name='delete-employee'),
    path('change_password/<str:pk>', views.change_password, name='change-password'),
    path('find_employee/', views.find_employee, name='find_employee'),
    path("",views.a),
    path("employees",views.list_employee)
]


