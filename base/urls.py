from django.urls import path
from . import views

urlpatterns=[
    path("login/", views.user_login_view, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.user_register_view, name="register"),
]