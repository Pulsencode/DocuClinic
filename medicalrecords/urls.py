from django.urls import path

from . import views


urlpatterns = [
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
