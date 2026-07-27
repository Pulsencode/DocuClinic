from django.urls import path

from public_interface import views

urlpatterns = [
    path("", views.home, name="home"),
]
