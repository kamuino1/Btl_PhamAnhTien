from django.urls import path
from . import views

urlpatterns = [
    path("add_comment/", views.add_comment, name = "add_comment"),
    path("get_comment/", views.get_comment, name = "get_comment"),
    path("remove_comment/", views.remove_comment, name = "remove_comment"),
]