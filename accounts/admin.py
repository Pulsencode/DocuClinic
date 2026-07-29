from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display

from accounts.models import Patient, User


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    """
    Admin configuration for staff-facing users.

    Patient-role users are excluded because patients are managed separately
    through PatientAdmin.
    """

    warn_unsaved_form = True
    save_on_top = True
    list_per_page = 25

    list_display = (
        "registration_id",
        "username",
        "get_full_name_display",
        "role",
        "email",
        "phone_number",
        "is_active",
        "is_staff",
    )

    list_display_links = (
        "registration_id",
        "username",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "registration_id",
        "phone_number",
    )

    ordering = ("username",)

    readonly_fields = (
        "registration_id",
        "last_login",
        "date_joined",
    )

    fieldsets = (
        (
            "Account",
            {
                "classes": ("tab",),
                "fields": (
                    "username",
                    "password",
                ),
            },
        ),
        (
            "Personal Information",
            {
                "classes": ("tab",),
                "fields": (
                    (
                        "first_name",
                        "last_name",
                    ),
                    "email",
                    (
                        "phone_number",
                        "address",
                    ),
                ),
            },
        ),
        (
            "Role & Registration",
            {
                "classes": ("tab",),
                "fields": (
                    (
                        "role",
                        "registration_id",
                    ),
                ),
            },
        ),
        (
            "Permissions",
            {
                "classes": ("tab",),
                "fields": (
                    (
                        "is_active",
                        "is_staff",
                        "is_superuser",
                    ),
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important Dates",
            {
                "classes": ("tab",),
                "fields": (
                    (
                        "last_login",
                        "date_joined",
                    ),
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            "Account",
            {
                "classes": ("wide", "tab"),
                "fields": (
                    "username",
                    (
                        "password1",
                        "password2",
                    ),
                ),
            },
        ),
        (
            "Personal Information",
            {
                "classes": ("wide", "tab"),
                "fields": (
                    (
                        "first_name",
                        "last_name",
                    ),
                    "email",
                    (
                        "phone_number",
                        "address",
                    ),
                ),
            },
        ),
        (
            "Role & Permissions",
            {
                "classes": ("wide", "tab"),
                "fields": (
                    "role",
                    (
                        "is_active",
                        "is_staff",
                    ),
                    "groups",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        """
        Display only staff-facing users.

        Patients are managed independently through PatientAdmin.
        """
        queryset = super().get_queryset(request)
        return queryset.exclude(role="patient")

    @display(
        description="Full Name",
        ordering="first_name",
    )
    def get_full_name_display(self, obj):
        return obj.get_full_name() or "-"


@admin.register(Patient)
class PatientAdmin(ModelAdmin):
    """
    Admin configuration for patient profiles.
    """

    warn_unsaved_form = True
    save_on_top = True
    list_per_page = 25
    date_hierarchy = "last_updated"

    list_display = (
        "patient_information",
        "registration_id",
        "phone_number",
        "formatted_age",
        "gender_display",
        "blood_type_display",
        "bmi_display",
        "blood_pressure_display",
        "vip_status",
        "active_status",
        "last_updated",
    )

    list_display_links = (
        "patient_information",
        "registration_id",
    )

    list_filter = (
        "is_active",
        "is_vip",
        "gender",
        "blood_type",
        "temperature_method",
        "last_updated",
    )

    search_fields = (
        "first_name",
        "last_name",
        "registration_id",
        "email",
        "phone_number",
        "emergency_contact_name",
        "emergency_contact_number",
    )

    ordering = (
        "-is_vip",
        "first_name",
        "last_name",
    )

    readonly_fields = (
        "registration_id",
        "bmi",
        "bmi_status",
        "formatted_age",
        "formatted_blood_pressure",
        "formatted_pulse",
        "last_updated",
    )

    fieldsets = (
        (
            "Patient Information",
            {
                "classes": ("tab",),
                "fields": (
                    (
                        "first_name",
                        "last_name",
                    ),
                    (
                        "registration_id",
                        "is_vip",
                        "is_active",
                    ),
                    (
                        "date_of_birth",
                        "formatted_age",
                        "gender",
                    ),
                ),
            },
        ),
        (
            "Contact Information",
            {
                "classes": ("tab",),
                "fields": (
                    (
                        "email",
                        "phone_number",
                    ),
                    "address",
                ),
            },
        ),
        (
            "Physical Measurements",
            {
                "classes": ("tab",),
                "fields": (
                    (
                        "height_in_centimeter",
                        "weight_in_kg",
                    ),
                    (
                        "bmi",
                        "bmi_status",
                    ),
                    (
                        "temperature",
                        "temperature_method",
                    ),
                    (
                        "pulse",
                        "formatted_pulse",
                    ),
                ),
            },
        ),
        (
            "Medical Information",
            {
                "classes": ("tab",),
                "fields": (
                    "blood_type",
                    (
                        "blood_pressure_systolic",
                        "blood_pressure_diastolic",
                    ),
                    "formatted_blood_pressure",
                    "allergies",
                ),
            },
        ),
        (
            "Emergency Contact",
            {
                "classes": ("tab",),
                "fields": (
                    (
                        "emergency_contact_name",
                        "emergency_contact_number",
                    ),
                ),
            },
        ),
        (
            "System Information",
            {
                "classes": ("tab",),
                "fields": ("last_updated",),
            },
        ),
    )

    @display(
        description="Patient",
        ordering="first_name",
    )
    def patient_information(self, obj):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        full_name = full_name or "Unnamed Patient"

        if not obj.email:
            return full_name

        return format_html(
            """
            <div>
                <div class="font-medium text-font-important-light
                            dark:text-font-important-dark">
                    {}
                </div>
                <div class="text-xs text-font-subtle-light
                            dark:text-font-subtle-dark">
                    {}
                </div>
            </div>
            """,
            full_name,
            obj.email,
        )

    @display(
        description="Age",
        ordering="date_of_birth",
    )
    def formatted_age(self, obj):
        if obj.age is None:
            return "-"

        return f"{obj.age} years"

    @display(
        description="Gender",
        ordering="gender",
    )
    def gender_display(self, obj):
        if not obj.gender:
            return "-"

        return obj.get_gender_display()

    @display(
        description="Blood Type",
        ordering="blood_type",
    )
    def blood_type_display(self, obj):
        return obj.blood_type or "-"

    @display(
        description="BMI",
        ordering="bmi",
    )
    def bmi_display(self, obj):
        if obj.bmi is None:
            return "-"

        status = obj.bmi_status or "Not classified"
        return f"{obj.bmi:.2f} — {status}"

    @display(
        description="Blood Pressure",
        ordering="blood_pressure_systolic",
    )
    def blood_pressure_display(self, obj):
        return obj.get_blood_pressure()

    @display(
        description="Blood Pressure",
    )
    def formatted_blood_pressure(self, obj):
        return obj.get_blood_pressure()

    @display(
        description="Pulse Rate",
    )
    def formatted_pulse(self, obj):
        return obj.get_pulse_rate()

    @display(
        description="VIP",
        boolean=True,
        ordering="is_vip",
    )
    def vip_status(self, obj):
        return obj.is_vip

    @display(
        description="Active",
        boolean=True,
        ordering="is_active",
    )
    def active_status(self, obj):
        return obj.is_active
