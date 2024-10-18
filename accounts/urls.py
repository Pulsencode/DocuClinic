from django.urls import path

from . import views


urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("redirect/", views.user_redirect, name="user_redirect"),
    # APPOINMENTS
    path(
        "appointment/create/",
        views.AppointmentCreateView.as_view(),
        name="appointment_create",
    ),
    path(
        "appointment/update/<int:pk>/",
        views.AppointmentUpdateView.as_view(),
        name="appointment_update",
    ),
    path(
        "appointment/delete/<int:pk>/",
        views.AppointmentDeleteView.as_view(),
        name="appointment_delete",
    ),
]
