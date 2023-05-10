from django.urls import path
from . import views

urlpatterns = [
    path("add_to_cart/", views.add_product_to_cart, name = "add_to_cart"),
    path("get_cart/", views.get_cart, name = "get_cart"),
    path("remove_cart/", views.remove_cart, name = "remove_cart"),
]