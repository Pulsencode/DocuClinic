from django.urls import path

from . import views


urlpatterns = [
    path("list/", views.DoctorListView.as_view(), name="doctor_list"),
    path("<int:pk>/", views.DoctorDetailView.as_view(), name="doctor_detail"),
    path("create/", views.DoctorCreateView.as_view(), name="doctor_create"),
    path(
        "update/<int:pk>/",
        views.DoctorUpdateView.as_view(),
        name="doctor_update",
    ),
    path(
        "delete/<int:pk>/",
        views.DoctorDeleteView.as_view(),
        name="doctor_delete",
    ),
    path(
        "dashboard/",
        views.DoctorDashboardView.as_view(),
        name="doctor_dashboard",
    ),
]
