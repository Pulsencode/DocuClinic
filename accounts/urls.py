from django.urls import path

from . import views


urlpatterns = [
    # path("signup/", views.SignUpView.as_view(), name="signup"),
    path("redirect/", views.user_redirect, name="user_redirect"),
    # Nurse Crud
    path("list/nurse/", views.NurseListView.as_view(), name="nurse_list"),
    path(
        "detail/nurse/<int:pk>/", views.NurseDetailView.as_view(), name="nurse_detail"
    ),
    path("create/nurse/", views.NurseCreateView.as_view(), name="nurse_create"),
    path(
        "update/nurse/<int:pk>/",
        views.NurseUpdateView.as_view(),
        name="nurse_update",
    ),
    path(
        "delete/nurse/<int:pk>/",
        views.NurseDeleteView.as_view(),
        name="nurse_delete",
    ),
    # Receptionist
    path(
        "list/receptionist/",
        views.ReceptionistListView.as_view(),
        name="receptionist_list",
    ),
    path(
        "detail/receptionist/<int:pk>/",
        views.ReceptionistDetailView.as_view(),
        name="receptionist_detail",
    ),
    path(
        "create/receptionist/",
        views.ReceptionistCreateView.as_view(),
        name="receptionist_create",
    ),
    path(
        "update/receptionist/<int:pk>/",
        views.ReceptionistUpdateView.as_view(),
        name="receptionist_update",
    ),
    path(
        "delete/receptionist/<int:pk>/",
        views.ReceptionistDeleteView.as_view(),
        name="receptionist_delete",
    ),
    # accountant
    path(
        "list/accountant/", views.AccountantListView.as_view(), name="accountant_list"
    ),
    path(
        "detail/accountant/<int:pk>/",
        views.AccountantDetailView.as_view(),
        name="accountant_detail",
    ),
    path(
        "create/accountant/",
        views.AccountantCreateView.as_view(),
        name="accountant_create",
    ),
    path(
        "update/accountant/<int:pk>/",
        views.AccountantUpdateView.as_view(),
        name="accountant_update",
    ),
    path(
        "delete/accountant/<int:pk>/",
        views.AccountantDeleteView.as_view(),
        name="accountant_delete",
    ),
]
