from django.urls import path

from .views import (
    SignUpView,
    Dashboard
    )


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
]
