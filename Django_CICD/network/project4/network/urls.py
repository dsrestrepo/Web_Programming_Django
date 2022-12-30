
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profiles", views.profiles, name="profiles"),
    path("following", views.following, name="following"),
        # API Routes
    path("newPost", views.newPost, name="newPost"),
    path("users/<str:username>", views.users, name="users"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("like/<int:post_id>", views.like, name="like"),
    path("follow/<str:username>", views.follow, name="follow")
]
