
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile_page, name="profile_page"),
    path("unfollow/<str:username>", views.unfollow, name="unfollow"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("following", views.following, name="following")
]
