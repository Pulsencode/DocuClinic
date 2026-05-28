from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin, TabularInline

from accounts.models import PatientProfile, User


class PatientProfileInline(TabularInline):
    model = PatientProfile
    extra = 0
    can_delete = False
    fk_name = "user"

    fieldsets = (
        (
            "Basic Details",
            {
                "fields": (
                    "is_vip",
                    "age",
                    "gender",
                    "blood_type",
                )
            },
        ),
        (
            "Vitals",
            {
                "fields": (
                    "height_in_centimeter",
                    "weight_in_kg",
                    "bmi",
                    "bmi_status",
                    "temperature",
                    "temperature_method",
                    "pulse",
                    "blood_pressure_systolic",
                    "blood_pressure_diastolic",
                )
            },
        ),
        (
            "Emergency Details",
            {
                "fields": (
                    "allergies",
                    "emergency_contact_name",
                    "emergency_contact_number",
                )
            },
        ),
    )

    readonly_fields = (
        "bmi",
        "bmi_status",
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    warn_unsaved_form = True
    list_display = (
        "username",
        "registration_id",
        "role",
        "phone_number",
        "is_active",
        "is_staff",
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
                    "phone_number",
                    "address",
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
                    "phone_number",
                    "address",
                )
            },
        ),
    )

    def get_inline_instances(self, request, obj=None):
        if obj and obj.role == "patient":
            return [PatientProfileInline(self.model, self.admin_site)]
        return []


@admin.register(PatientProfile)
class PatientProfileAdmin(ModelAdmin):
    list_display = (
        "user",
        "is_vip",
        "age",
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

    readonly_fields = (
        "bmi",
        "bmi_status",
        "last_updated",
    )

    fieldsets = (
        (
            "Patient",
            {
                "fields": (
                    "user",
                    "is_vip",
                )
            },
        ),
        (
            "Basic Details",
            {
                "fields": (
                    "age",
                    "gender",
                    "blood_type",
                )
            },
        ),
        (
            "Vitals",
            {
                "fields": (
                    "height_in_centimeter",
                    "weight_in_kg",
                    "bmi",
                    "bmi_status",
                    "temperature",
                    "temperature_method",
                    "pulse",
                    "blood_pressure_systolic",
                    "blood_pressure_diastolic",
                )
            },
        ),
        (
            "Emergency Details",
            {
                "fields": (
                    "allergies",
                    "emergency_contact_name",
                    "emergency_contact_number",
                )
            },
        ),
        (
            "System Info",
            {"fields": ("last_updated",)},
        ),
    )
