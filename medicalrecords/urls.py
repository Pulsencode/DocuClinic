from django.urls import path
from . import views


urlpatterns = [
    path(
        "list/appointment",
        views.AppointmentListView.as_view(),
        name="list_appointments",
    ),
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
    path(
        "prescriptions/", views.PrescriptionListView.as_view(), name="prescription_list"
    ),
    path(
        "prescription/create/",
        views.PrescriptionCreateView.as_view(),
        name="create_prescription",
    ),
    path(
        "prescription/<int:pk>/",
        views.PrescriptionDetailView.as_view(),
        name="prescription_detail",
    ),
    path(
        "prescription/delete/<int:pk>/",
        views.PrescriptionDeleteView.as_view(),
        name="prescription_delete",
    ),
]
