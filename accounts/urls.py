from django.urls import path

from . import views


urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),

    # DOCTORS
    path("doctors/", views.DoctorListView.as_view(), name="doctor_list"),
    path("doctors/<int:pk>/", views.DoctorDetailView.as_view(), name="doctor_detail"),
    path("doctors/create/", views.DoctorCreateView.as_view(), name="doctor_create"),
    path(
        "doctors/<int:pk>/update/",
        views.DoctorUpdateView.as_view(),
        name="doctor_update",
    ),
    path(
        "doctors/<int:pk>/delete/",
        views.DoctorDeleteView.as_view(),
        name="doctor_delete",
    ),
    path("doctor/dashboard/", views.DoctorDashboardView.as_view(), name="dashboard"),
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
    path("operators/", views.OperatorListView.as_view(), name="operator_list"),
    # OPERATORS
    path(
        "operators/<int:pk>/",
        views.OperatorDetailView.as_view(),
        name="operator_detail",
    ),
    path(
        "operators/create/", views.OperatorCreateView.as_view(), name="operator_create"
    ),
    path(
        "operators/update/<int:pk>/",
        views.OperatorUpdateView.as_view(),
        name="operator_update",
    ),
    path(
        "operators/delete/<int:pk>/",
        views.OperatorDeleteView.as_view(),
        name="operator_delete",
    ),
]
