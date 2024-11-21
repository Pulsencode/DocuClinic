from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.InventoryDashboard.as_view(), name="inventory_dashboard"),
    # Supplier URLs
    path("suppliers/", views.SupplierListView.as_view(), name="list_supplier"),
    path("add/suppliers/", views.SupplierCreateView.as_view(), name="add_supplier"),
    path(
        "update/suppliers/<int:pk>/",
        views.SupplierUpdateView.as_view(),
        name="update_supplier",
    ),
    path(
        "delete/suppliers/<int:pk>/",
        views.SupplierDeleteView.as_view(),
        name="delete_supplier",
    ),
    # RouteOfAdministration URLs
    path(
        "routes/",
        views.RouteOfAdministrationListView.as_view(),
        name="list_route_of_administration",
    ),
    path(
        "add/routes/",
        views.RouteOfAdministrationCreateView.as_view(),
        name="add_route_of_administration",
    ),
    path(
        "update/routes/<int:pk>/",
        views.RouteOfAdministrationUpdateView.as_view(),
        name="update_route_of_administration",
    ),
    path(
        "delete/routes/<int:pk>/",
        views.RouteOfAdministrationDeleteView.as_view(),
        name="delete_route_of_administration",
    ),
    # Medicine URLs
    path("medicine/", views.MedicineListView.as_view(), name="list_medicine"),
    path("add/medicine/", views.MedicineCreateView.as_view(), name="add_medicine"),
    path(
        "update/medicine/<int:pk>/",
        views.MedicineUpdateView.as_view(),
        name="update_medicine",
    ),
    path(
        "delete/medicine/<int:pk>/",
        views.MedicineDeleteView.as_view(),
        name="delete_medicine",
    ),
    # Medicine Supplier URLs
    path(
        "medicine/supplier/",
        views.MedicineSupplierListView.as_view(),
        name="list_medicine_supplier",
    ),
    path(
        "add/medicine/supplier/",
        views.MedicineSupplierCreateView.as_view(),
        name="add_medicine_supplier",
    ),
    path(
        "update/medicine/supplier/<int:pk>/",
        views.MedicineSupplierUpdateView.as_view(),
        name="update_medicine_supplier",
    ),
    path(
        "delete/medicine/supplier/<int:pk>/",
        views.MedicineSupplierDeleteView.as_view(),
        name="delete_medicine_supplier",
    ),
]
