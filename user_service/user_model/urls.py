from django.urls import path
from . import views

urlpatterns = [
    path("userregistration/", views.registration_req, name = "userregistration"),
]