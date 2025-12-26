from django.urls import path

from appointments import views

urlpatterns = [
    path(
        "list/appointment",
        views.AppointmentListView.as_view(),
        name="list_appointments",
    ),
    path(
        "appointment/detail/<int:pk>/",
        views.AppointmentDetailView.as_view(),
        name="appointments_detail",
    ),
    path(
        "check-patient-vip/", views.check_patient_vip_status, name="check_patient_vip"
    ),
    path("get_available_dates/", views.get_available_dates, name="get_available_dates"),
    path(
        "create/appointment",
        views.AppointmentCreateView.as_view(),
        name="create_appointment",
    ),
    path(
        "update/appointment/<int:pk>/",
        views.AppointmentUpdateView.as_view(),
        name="update_appointment",
    ),
    path(
        "delete/appointment/<int:pk>/",
        views.AppointmentDeleteView.as_view(),
        name="delete_appointment",
    ),
]
