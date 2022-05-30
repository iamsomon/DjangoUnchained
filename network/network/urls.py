
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_post", views.add_post, name="add_post"),
    # path("likedis_post", views.likedis_post, name="likedis_post"),
    # path("u/<str:username>/likedis_post_prof", views.likedis_post_prof, name="likedis_post_prof"),
    path("u/<str:username>", views.user_profile, name="user_profile"),
    path("u/<str:username>/follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    # path("likedis_post_fol", views.likedis_post_fol, name="likedis_post_fol"),
    # path("edit_post", views.edit_post, name="edit_post"),
    path("edit_post_async", views.edit_post_async, name="edit_post_async"),
    # path("edit_post_prof", views.edit_post_prof, name="edit_post_prof"),
    path("like_post", views.like_post, name="like_post"),
]
