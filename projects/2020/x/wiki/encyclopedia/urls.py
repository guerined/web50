from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:TITLE>", views.title_display, name="title_display"),
    path("function/search", views.search, name="search"),
    path("function/randomwiki", views.randomwiki, name="randomwiki"),
    path("function/add", views.add, name="add"),
    path("function/editwiki/<str:TITLE>", views.editentry, name="editentry"),
    path("<str:TITLE>", views.title_display, name="title_display2")
]


