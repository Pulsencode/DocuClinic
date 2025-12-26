from django.urls import path

from medicalrecords import views

urlpatterns = [
    path(
        "prescriptions/", views.PrescriptionListView.as_view(), name="prescription_list"
    ),
    path(
        "prescription/create/<int:appointment_id>",
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
    path(
        "patient/prescriptions/<int:patient_id>/",
        views.PatientPrescriptionsView.as_view(),
        name="patient_prescriptions",
    ),
    # Discount
    path("discount/add/", views.DiscountCreateView.as_view(), name="discount_add"),
    path(
        "discount/update/<int:pk>/",
        views.DiscountUpdateView.as_view(),
        name="discount_edit",
    ),
    path(
        "discount/delete/<int:pk>/",
        views.DiscountDeleteView.as_view(),
        name="discount_delete",
    ),
]
