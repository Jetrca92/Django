from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("entries/<str:title>", views.entry, name="entry"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("watchlist_add", views.watchlist_add, name="watchlist_add"),
    path("category_list", views.category_list, name="category_list"),
    path("category/<str:title>", views.display_cat, name="display_cat"),
    path("user/<str:user>", views.user_adds, name="user_adds")
    
]
