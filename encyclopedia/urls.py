from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("wiki/<str:entry_name>/edit/", views.edit_entry, name="edit_entry"),
    path("random_entry", views.random_entry, name="random_entry")

]
