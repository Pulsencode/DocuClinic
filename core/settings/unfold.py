from django.templatetags.static import static
from django.urls import reverse_lazy


def can_view_model(app_label, model_name):
    # Unfold calls this inner function for the current request, not at startup.
    def has_permission(request):
        user = request.user
        if not user.is_active or not user.is_staff:
            return False

        # Django also allows users with change permission to view a model's list.
        return (
            user.is_superuser
            or user.has_perm(f"{app_label}.view_{model_name}")
            or user.has_perm(f"{app_label}.change_{model_name}")
        )

    return has_permission


UNFOLD = {
    "DASHBOARD_CALLBACK": "dashboard.views.dashboard_callback",
    "SITE_TITLE": "DocuClinic",
    "SITE_HEADER": "DocuClinic",
    "SITE_SUBHEADER": "Administration",
    "SCRIPTS": [
        lambda request: static("js/custom_time_shortcuts.js"),
    ],
    "SIDEBAR": {
        "show_search": True,
        "navigation": [
            {
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                        # The admin home is available to every active staff user.
                        "permission": lambda request: request.user.is_active
                        and request.user.is_staff,
                    },
                ],
            },
            {
                "items": [
                    {
                        "title": "Clinic Settings",
                        "icon": "local_hospital",
                        "link": reverse_lazy("admin:clinic_clinic_changelist"),
                        "permission": can_view_model("clinic", "clinic"),
                    },
                ],
            },
            {
                "items": [
                    {
                        "title": "Patients",
                        "icon": "personal_injury",
                        "link": reverse_lazy("admin:accounts_patient_changelist"),
                        "permission": can_view_model("accounts", "patient"),
                    },
                ],
            },
            {
                "items": [
                    {
                        "title": "All Users",
                        "icon": "groups",
                        "link": reverse_lazy("admin:accounts_user_changelist"),
                        "permission": can_view_model("accounts", "user"),
                    },
                ],
            },
            {
                "title": "Appointments",
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": "Appointments",
                        "icon": "calendar_month",
                        "link": reverse_lazy(
                            "admin:appointments_appointment_changelist"
                        ),
                        "permission": can_view_model("appointments", "appointment"),
                    },
                    {
                        "title": "Physician Availability",
                        "icon": "event_available",
                        "link": reverse_lazy(
                            "admin:appointments_physicianavailability_changelist"
                        ),
                        "permission": can_view_model(
                            "appointments", "physicianavailability"
                        ),
                    },
                    {
                        "title": "Weekdays",
                        "icon": "date_range",
                        "link": reverse_lazy("admin:appointments_weekday_changelist"),
                        "permission": can_view_model("appointments", "weekday"),
                    },
                ],
            },
            {
                "title": "Medical Records",
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": "Prescriptions",
                        "icon": "prescriptions",
                        "link": reverse_lazy(
                            "admin:medicalrecords_prescription_changelist"
                        ),
                        "permission": can_view_model("medicalrecords", "prescription"),
                    },
                    {
                        "title": "Prescription Medicines",
                        "icon": "medication",
                        "link": reverse_lazy(
                            "admin:medicalrecords_prescriptionmedicine_changelist"
                        ),
                        "permission": can_view_model(
                            "medicalrecords", "prescriptionmedicine"
                        ),
                    },
                    {
                        "title": "Discounts",
                        "icon": "percent",
                        "link": reverse_lazy(
                            "admin:medicalrecords_discount_changelist"
                        ),
                        "permission": can_view_model("medicalrecords", "discount"),
                    },
                ],
            },
            {
                "title": "Inventory",
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": "Medicines",
                        "icon": "vaccines",
                        "link": reverse_lazy("admin:inventory_medicine_changelist"),
                        "permission": can_view_model("inventory", "medicine"),
                    },
                    {
                        "title": "Routes of Administration",
                        "icon": "route",
                        "link": reverse_lazy(
                            "admin:inventory_routeofadministration_changelist"
                        ),
                        "permission": can_view_model(
                            "inventory", "routeofadministration"
                        ),
                    },
                    {
                        "title": "Suppliers",
                        "icon": "local_shipping",
                        "link": reverse_lazy(
                            "admin:inventory_medicinesupplier_changelist"
                        ),
                        # This link opens medicine-supplier records, not Supplier.
                        "permission": can_view_model("inventory", "medicinesupplier"),
                    },
                ],
            },
            # NOTE this app not needed for the first version of the app, and can be added in later versions if needed
            # {
            #     "title": "Accounting",
            #     "collapsible": True,
            #     "separator": True,
            #     "items": [
            #         {
            #             "title": "Invoices",
            #             "icon": "receipt_long",
            #             "link": reverse_lazy("admin:accounting_invoice_changelist"),
            #         },
            #         {
            #             "title": "Accounts",
            #             "icon": "account_balance",
            #             "link": reverse_lazy("admin:accounting_account_changelist"),
            #         },
            #         {
            #             "title": "Accounts Payable",
            #             "icon": "payments",
            #             "link": reverse_lazy(
            #                 "admin:accounting_accountspayable_changelist"
            #             ),
            #         },
            #         {
            #             "title": "Accounts Receivable",
            #             "icon": "request_quote",
            #             "link": reverse_lazy(
            #                 "admin:accounting_accountsreceivable_changelist"
            #             ),
            #         },
            #         {
            #             "title": "Assets",
            #             "icon": "real_estate_agent",
            #             "link": reverse_lazy("admin:accounting_asset_changelist"),
            #         },
            #         {
            #             "title": "General Ledger Entries",
            #             "icon": "menu_book",
            #             "link": reverse_lazy(
            #                 "admin:accounting_generalledgerentry_changelist"
            #             ),
            #         },
            #     ],
            # },
        ],
    },
}
