
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:page_id>", views.Profile_page, name="Profile_page"),
    path("follow", views.Follow, name="follow"),
    path("edit", views.edit, name="edit"),
    path("like", views.like, name="like"),
]
