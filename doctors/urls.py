from django.urls import path

from . import views


urlpatterns = [
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
    path(
        "doctor/dashboard/",
        views.DoctorDashboardView.as_view(),
        name="doctor_dashboard",
    ),
]
