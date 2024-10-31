from django.urls import path

from . import views


urlpatterns = [
    path("list/", views.OperatorListView.as_view(), name="operator_list"),
    # OPERATORS
    path(
        "detail/<int:pk>/",
        views.OperatorDetailView.as_view(),
        name="operator_detail",
    ),
    path(
        "create/", views.OperatorCreateView.as_view(), name="operator_create"
    ),
    path(
        "update/<int:pk>/",
        views.OperatorUpdateView.as_view(),
        name="operator_update",
    ),
    path(
        "delete/<int:pk>/",
        views.OperatorDeleteView.as_view(),
        name="operator_delete",
    ),
    path(
        "dashboard/",
        views.OperatorDashboardView.as_view(),
        name="operator_dashboard",
    ),
]
