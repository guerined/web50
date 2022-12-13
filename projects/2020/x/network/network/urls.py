
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("edit", views.update, name="updatePost"),
    path("follow/<int:follower_id>/<int:followee_id>", views.follow, name="follow"),
    path("unfollow/<int:follower_id>/<int:followee_id>", views.unfollow, name="unfollow"),
    path("likes", views.like_unlike_post, name="likeview"),
    path("following", views.following, name="following"),
]
