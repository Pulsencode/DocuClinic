import os
from pathlib import Path

from django.urls import reverse_lazy
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG", default=False)


INSTALLED_APPS = [
    "unfold",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Add External Apps Here
EXTERNAL_APPS = [
    "accounts.apps.AccountsConfig",
    "inventory.apps.InventoryConfig",
    "medicalrecords.apps.MedicalrecordsConfig",
    "accounting.apps.AccountingConfig",
    "clinic.apps.ClinicConfig",
    "appointments.apps.AppointmentsConfig",
    "dashboard.apps.DashboardConfig",
]

INSTALLED_APPS += EXTERNAL_APPS

AUTH_USER_MODEL = "accounts.User"

LOGIN_REDIRECT_URL = "user_redirect"
LOGOUT_REDIRECT_URL = "login"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

MEDIA_URL = "/media/"

STATIC_ROOT = BASE_DIR / "assets"

MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email configuration
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
EMAIL_DEBUG = os.getenv("EMAIL_DEBUG")

UNFOLD = {
    "SITE_TITLE": "DocuClinic",
    "SITE_HEADER": "DocuClinic",
    "SITE_SUBHEADER": "Administration",
    "SIDEBAR": {
        "show_search": True,
        "navigation": [
            {
                "title": ("Clinic"),
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": ("Clinic Settings"),
                        "icon": "local_hospital",
                        "link": reverse_lazy("admin:clinic_clinic_changelist"),
                    },
                ],
            },
            {
                "title": ("Users"),
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": ("Admin"),
                        "icon": "supervisor_account",
                        "link": reverse_lazy("admin:accounts_administrator_changelist"),
                    },
                    {
                        "title": ("Physicians"),
                        "icon": "stethoscope",
                        "link": reverse_lazy("admin:accounts_physician_changelist"),
                    },
                    {
                        "title": ("Nurses"),
                        "icon": "medical_services",
                        "link": reverse_lazy("admin:accounts_nurse_changelist"),
                    },
                    {
                        "title": ("Accountants"),
                        "icon": "calculate",
                        "link": reverse_lazy("admin:accounts_accountant_changelist"),
                    },
                    {
                        "title": ("Patients"),
                        "icon": "patient_list",
                        "link": reverse_lazy("admin:accounts_patient_changelist"),
                    },
                ],
            },
            {
                "title": ("Appointments"),
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": ("Appointments"),
                        "icon": "calendar_month",
                        "link": reverse_lazy(
                            "admin:appointments_appointment_changelist"
                        ),
                    },
                    {
                        "title": ("Physician Availability"),
                        "icon": "event_available",
                        "link": reverse_lazy(
                            "admin:appointments_physicianavailability_changelist"
                        ),
                    },
                    {
                        "title": ("Weekdays"),
                        "icon": "date_range",
                        "link": reverse_lazy("admin:appointments_weekday_changelist"),
                    },
                ],
            },
            {
                "title": ("Medical Records"),
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": ("Prescriptions"),
                        "icon": "prescriptions",
                        "link": reverse_lazy(
                            "admin:medicalrecords_prescription_changelist"
                        ),
                    },
                    {
                        "title": ("Prescription Medicines"),
                        "icon": "medication",
                        "link": reverse_lazy(
                            "admin:medicalrecords_prescriptionmedicine_changelist"
                        ),
                    },
                    {
                        "title": ("Discount"),
                        "icon": "percent",
                        "link": reverse_lazy(
                            "admin:medicalrecords_discount_changelist"
                        ),
                    },
                ],
            },
            {
                "title": ("Inventory"),
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": ("Medicine"),
                        "icon": "vaccines",
                        "link": reverse_lazy("admin:inventory_medicine_changelist"),
                    },
                    {
                        "title": ("Route Of Administration"),
                        "icon": "route",
                        "link": reverse_lazy(
                            "admin:inventory_routeofadministration_changelist"
                        ),
                    },
                    {
                        "title": ("Suppliers"),
                        "icon": "local_shipping",
                        "link": reverse_lazy(
                            "admin:inventory_medicinesupplier_changelist"
                        ),
                    },
                ],
            },
            {
                "title": ("Accounting"),
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": ("Invoices"),
                        "icon": "receipt_long",
                        "link": reverse_lazy("admin:accounting_invoice_changelist"),
                    },
                    {
                        "title": ("Accounts"),
                        "icon": "account_balance",
                        "link": reverse_lazy("admin:accounting_account_changelist"),
                    },
                    {
                        "title": ("Accounts Payable"),
                        "icon": "payments",
                        "link": reverse_lazy(
                            "admin:accounting_accountspayable_changelist"
                        ),
                    },
                    {
                        "title": ("Accounts Receivable"),
                        "icon": "request_quote",
                        "link": reverse_lazy(
                            "admin:accounting_accountsreceivable_changelist"
                        ),
                    },
                    {
                        "title": ("Assets"),
                        "icon": "real_estate_agent",
                        "link": reverse_lazy("admin:accounting_asset_changelist"),
                    },
                    {
                        "title": ("General Ledger Entry"),
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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "general.log",
            "formatter": "verbose",
        },
        "test_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "test_logs.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
        "test": {
            "handlers": ["test_file"],
            "level": "DEBUG",
            "propagate": False,  # Ensure logs don't propagate to the root or other loggers
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}
