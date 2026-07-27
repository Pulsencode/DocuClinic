from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin, StackedInline

from accounts.models import PatientProfile, User


class PatientProfileInline(StackedInline):
    warn_unsaved_form = True
    model = PatientProfile
    extra = 0
    max_num = 1
    can_delete = False

    readonly_fields = (
        "bmi",
        "bmi_status",
        "last_updated",
    )  # calculated fields shouldn't be editable

    fieldsets = (
        (
            None,
            {
                "fields": ("is_vip",),
            },
        ),
        (
            "Demographics",
            {
                "fields": (("date_of_birth", "gender"), "blood_type"),
            },
        ),
        (
            "Vitals",
            {
                "fields": (
                    ("height_in_centimeter", "weight_in_kg"),
                    ("bmi", "bmi_status"),
                    ("temperature", "temperature_method"),
                    ("pulse",),
                    ("blood_pressure_systolic", "blood_pressure_diastolic"),
                ),
            },
        ),
        (
            "Emergency & Allergies",
            {
                "fields": (
                    "allergies",
                    ("emergency_contact_name", "emergency_contact_number"),
                ),
            },
        ),
        (
            "Meta",
            {
                "fields": ("last_updated",),
                "classes": ("collapse",),  # collapsible section, saves space
            },
        ),
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # inlines = [PatientProfileInline]
    warn_unsaved_form = True
    list_filter_sheet = False  # TODO: confirm this is a valid Unfold ModelAdmin attribute for your installed version

    list_display = (
        "registration_id",
        "role",
        "username",
        "phone_number",
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

    readonly_fields = (
        "registration_id",
        "last_login",
        "date_joined",
    )

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Role & Registration",
            {
                "fields": (
                    "role",
                    "registration_id",
                    ("phone_number", "address"),
                )
            },
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Role & Contact Details",
            {
                "fields": (
                    "role",
                    ("phone_number", "address"),
                )
            },
        ),
    )

    def get_inline_instances(self, request, obj=None):
        inlines = super().get_inline_instances(request, obj)
        if obj and obj.role == "patient":
            inlines = list(inlines) + [
                PatientProfileInline(self.model, self.admin_site)
            ]
        return inlines

    def get_queryset(self, request):
        # "All Users" should only show staff-facing roles.
        # Patients are managed separately via PatientProfileAdmin.
        qs = super().get_queryset(request)
        return qs.exclude(role="patient")


@admin.register(PatientProfile)
class PatientProfileAdmin(ModelAdmin):
    warn_unsaved_form = True
    list_display = (
        "user",
        "is_vip",
        "date_of_birth",
        "gender",
        "blood_type",
        "bmi",
        "bmi_status",
        "last_updated",
    )

    list_filter = (
        "is_vip",
        "gender",
        "blood_type",
        "bmi_status",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__registration_id",
        "user__phone_number",
    )

    readonly_fields = ("bmi", "bmi_status", "last_updated", "age")

    fieldsets = (
        (
            "Patient",
            {
                "fields": (
                    ("user", "date_of_birth"),
                    ("is_vip", "age"),
                )
            },
        ),
        (
            "Basic Details",
            {"fields": (("gender", "blood_type"),)},
        ),
        (
            "Vitals",
            {
                "fields": (
                    ("bmi", "bmi_status"),
                    (
                        "height_in_centimeter",
                        "weight_in_kg",
                        "temperature",
                        "temperature_method",
                    ),
                    ("pulse", "blood_pressure_systolic", "blood_pressure_diastolic"),
                )
            },
        ),
        (
            "Emergency Details",
            {
                "fields": (
                    "allergies",
                    ("emergency_contact_name", "emergency_contact_number"),
                )
            },
        ),
        (
            "System Info",
            {
                "fields": ("last_updated",),
                "classes": ("collapse",),
            },
        ),
    )
