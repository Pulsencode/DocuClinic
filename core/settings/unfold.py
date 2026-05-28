from django.urls import reverse_lazy

UNFOLD = {
    "DASHBOARD_CALLBACK": "dashboard.views.dashboard_callback",
    "SITE_TITLE": "DocuClinic",
    "SITE_HEADER": "DocuClinic",
    "SITE_SUBHEADER": "Administration",
    "SIDEBAR": {
        "show_search": True,
        "navigation": [
            {
                "title": "Clinic",
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": "Clinic Settings",
                        "icon": "local_hospital",
                        "link": reverse_lazy("admin:clinic_clinic_changelist"),
                    },
                ],
            },
            {
                "title": "Users & Patients",
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": "All Users",
                        "icon": "groups",
                        "link": reverse_lazy("admin:accounts_user_changelist"),
                    },
                    {
                        "title": "Patient Profiles",
                        "icon": "personal_injury",
                        "link": reverse_lazy(
                            "admin:accounts_patientprofile_changelist"
                        ),
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
                    },
                    {
                        "title": "Physician Availability",
                        "icon": "event_available",
                        "link": reverse_lazy(
                            "admin:appointments_physicianavailability_changelist"
                        ),
                    },
                    {
                        "title": "Weekdays",
                        "icon": "date_range",
                        "link": reverse_lazy("admin:appointments_weekday_changelist"),
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
                    },
                    {
                        "title": "Prescription Medicines",
                        "icon": "medication",
                        "link": reverse_lazy(
                            "admin:medicalrecords_prescriptionmedicine_changelist"
                        ),
                    },
                    {
                        "title": "Discounts",
                        "icon": "percent",
                        "link": reverse_lazy(
                            "admin:medicalrecords_discount_changelist"
                        ),
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
                    },
                    {
                        "title": "Routes of Administration",
                        "icon": "route",
                        "link": reverse_lazy(
                            "admin:inventory_routeofadministration_changelist"
                        ),
                    },
                    {
                        "title": "Suppliers",
                        "icon": "local_shipping",
                        "link": reverse_lazy(
                            "admin:inventory_medicinesupplier_changelist"
                        ),
                    },
                ],
            },
            {
                "title": "Accounting",
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": "Invoices",
                        "icon": "receipt_long",
                        "link": reverse_lazy("admin:accounting_invoice_changelist"),
                    },
                    {
                        "title": "Accounts",
                        "icon": "account_balance",
                        "link": reverse_lazy("admin:accounting_account_changelist"),
                    },
                    {
                        "title": "Accounts Payable",
                        "icon": "payments",
                        "link": reverse_lazy(
                            "admin:accounting_accountspayable_changelist"
                        ),
                    },
                    {
                        "title": "Accounts Receivable",
                        "icon": "request_quote",
                        "link": reverse_lazy(
                            "admin:accounting_accountsreceivable_changelist"
                        ),
                    },
                    {
                        "title": "Assets",
                        "icon": "real_estate_agent",
                        "link": reverse_lazy("admin:accounting_asset_changelist"),
                    },
                    {
                        "title": "General Ledger Entries",
                        "icon": "menu_book",
                        "link": reverse_lazy(
                            "admin:accounting_generalledgerentry_changelist"
                        ),
                    },
                ],
            },
        ],
    },
}
