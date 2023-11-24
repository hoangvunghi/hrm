from django.urls import path
from . import views

urlpatterns=[
    path("login/", views.user_login_view, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.user_register_view, name="register"),
    path('create_employee/', views.add_employee, name='create-employee'),
    path('update_employee/<str:pk>/', views.update_employee, name='update-employee'),
    path('delete_employee/<str:pk>/', views.delete_employee, name='delete-employee'),
]