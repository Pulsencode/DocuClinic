from django.urls import path

from .views import (
    accountant,
    administration,
    base,
    nurse,
    patient,
    physician,
    receptionist,
)

urlpatterns = [
    path("redirect/", base.user_redirect, name="user_redirect"),
    # Physician
    path("list/physician/", physician.PhysicianListView.as_view(), name="physician_list"),
    path("detail/physician/<int:pk>/", physician.PhysicianDetailView.as_view(), name="physician_detail"),
    path("create/physician/", physician.PhysicianCreateView.as_view(), name="physician_create"),
    path(
        "update/physician/<int:pk>/",
        physician.PhysicianUpdateView.as_view(),
        name="physician_update",
    ),
    path(
        "delete/physician/<int:pk>/",
        physician.PhysicianDeleteView.as_view(),
        name="physician_delete",
    ),
    path(
        "physician/dashboard/",
        physician.PhysicianDashboardView.as_view(),
        name="physician_dashboard",
    ),
    # Patient
    path("list/patient/", patient.PatientListView.as_view(), name="patient_list"),
    path("add/patient/", patient.PatientCreateView.as_view(), name="patient_create"),
    path(
        "detail/patient/<int:pk>/", patient.PatientDetailView.as_view(), name="patient_detail"
    ),
    path(
        "update/patient/<int:pk>/", patient.PatientUpdateView.as_view(), name="patient_update"
    ),
    path(
        "delete/patient/<int:pk>/", patient.PatientDeleteView.as_view(), name="patient_delete"
    ),
    # Administration
    path(
        "administration/dashboard/",
        administration.AdminDashboard.as_view(),
        name="administration_dashboard",
    ),
    path("list/groups/", administration.GroupListView.as_view(), name="group_list"),
    path("add/groups/", administration.GroupCreateView.as_view(), name="group_add"),
    path(
        "update/groups/<int:pk>/",
        administration.GroupUpdateView.as_view(),
        name="group_update",
    ),
    path(
        "delete/groups/<int:pk>/",
        administration.GroupDeleteView.as_view(),
        name="group_delete",
    ),
    path(
        "groups/permissions/<int:group_id>/",
        administration.group_permissions,
        name="group_permissions",
    ),
    # Nurse
    path(
        "nurse/dashboard/",
        nurse.NurseDashboard.as_view(),
        name="nurse_dashboard",
    ),
    path("list/nurse/", nurse.NurseListView.as_view(), name="nurse_list"),
    path(
        "detail/nurse/<int:pk>/", nurse.NurseDetailView.as_view(), name="nurse_detail"
    ),
    path("create/nurse/", nurse.NurseCreateView.as_view(), name="nurse_create"),
    path(
        "update/nurse/<int:pk>/",
        nurse.NurseUpdateView.as_view(),
        name="nurse_update",
    ),
    path(
        "delete/nurse/<int:pk>/",
        nurse.NurseDeleteView.as_view(),
        name="nurse_delete",
    ),
    # Receptionist
    path(
        "receptionist/dashboard/",
        receptionist.ReceptionistDashboard.as_view(),
        name="receptionist_dashboard",
    ),
    path(
        "list/receptionist/",
        receptionist.ReceptionistListView.as_view(),
        name="receptionist_list",
    ),
    path(
        "detail/receptionist/<int:pk>/",
        receptionist.ReceptionistDetailView.as_view(),
        name="receptionist_detail",
    ),
    path(
        "create/receptionist/",
        receptionist.ReceptionistCreateView.as_view(),
        name="receptionist_create",
    ),
    path(
        "update/receptionist/<int:pk>/",
        receptionist.ReceptionistUpdateView.as_view(),
        name="receptionist_update",
    ),
    path(
        "delete/receptionist/<int:pk>/",
        receptionist.ReceptionistDeleteView.as_view(),
        name="receptionist_delete",
    ),
    # accountant
    path(
        "accountant/dashboard/",
        accountant.AccountantDashboard.as_view(),
        name="accountant_dashboard",
    ),
    path(
        "list/accountant/",
        accountant.AccountantListView.as_view(),
        name="accountant_list",
    ),
    path(
        "detail/accountant/<int:pk>/",
        accountant.AccountantDetailView.as_view(),
        name="accountant_detail",
    ),
    path(
        "create/accountant/",
        accountant.AccountantCreateView.as_view(),
        name="accountant_create",
    ),
    path(
        "update/accountant/<int:pk>/",
        accountant.AccountantUpdateView.as_view(),
        name="accountant_update",
    ),
    path(
        "delete/accountant/<int:pk>/",
        accountant.AccountantDeleteView.as_view(),
        name="accountant_delete",
    ),
]
