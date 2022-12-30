from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:search>",views.entry, name="entry"),
    path("New_Page",views.newPage, name="newPage"),
    path("edit/<str:title>",views.edit, name="edit"),
    path("random",views.randomf, name="random")
]
