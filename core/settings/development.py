from .base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Database
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": os.getenv("NAME"),  # noqa: F405
#         "USER": os.getenv("USER"),  # noqa: F405
#         "PASSWORD": os.getenv("PASSWORD"),  # noqa: F405
#         "HOST": os.getenv("HOST"),  # noqa: F405
#         "PORT": os.getenv("PORT"),  # noqa: F405
#         "OPTIONS": {
#             "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

DATA_GENERATOR_EXCLUDE_APPS = ["accounts"]

DATA_GENERATOR_EXCLUDE_MODELS = [
    "patients.PatientDetail",
    "medicalrecords.Appointment",
    "medicalrecords.Prescription",
    "medicalrecords.PrescriptionMedicine",
]

DATA_GENERATOR_CUSTOM_FIELD_VALUES = {
    "auth.User": {"first_name": "sample", "email": "sample@example.com"}
}
