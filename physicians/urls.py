from django.urls import path

from . import views


urlpatterns = [
    path("list/", views.PhysicianListView.as_view(), name="physician_list"),
    path("<int:pk>/", views.PhysicianDetailView.as_view(), name="physician_detail"),
    path("create/", views.PhysicianCreateView.as_view(), name="physician_create"),
    path(
        "update/<int:pk>/",
        views.PhysicianUpdateView.as_view(),
        name="physician_update",
    ),
    path(
        "delete/<int:pk>/",
        views.PhysicianDeleteView.as_view(),
        name="physician_delete",
    ),
    path(
        "dashboard/",
        views.PhysicianDashboardView.as_view(),
        name="physician_dashboard",
    ),
]
