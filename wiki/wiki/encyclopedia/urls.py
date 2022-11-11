from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.view, name="view"),
    path("results", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("edit_page", views.edit_page, name="edit_page"),
    path("update_page", views.update_page, name="update_page")
]
