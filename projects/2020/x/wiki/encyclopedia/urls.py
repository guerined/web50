from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:TITLE>", views.title_display, name="title_display")
]


