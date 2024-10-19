from django.urls import path

from . import views


urlpatterns = [
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
    path(
        "operator/dashboard/",
        views.OperatorDashboardView.as_view(),
        name="operator_dashboard",
    ),
]
