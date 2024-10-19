from django.urls import path

from . import views


urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("redirect/", views.user_redirect, name="user_redirect"),
]
