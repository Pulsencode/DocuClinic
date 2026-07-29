from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display

from .models import Discount, Prescription, PrescriptionMedicine

User = get_user_model()


class PrescriptionMedicineInline(TabularInline):
    """
    Add medicines directly inside the prescription form.
    """

    model = PrescriptionMedicine

    extra = 1
    min_num = 0
    can_delete = True
    show_change_link = True

    autocomplete_fields = ("medicine",)

    fields = (
        "medicine",
        "dose",
        "frequency",
        "timing",
        "amount",
        "additional_instructions",
    )


@admin.register(Discount)
class DiscountAdmin(ModelAdmin):
    warn_unsaved_form = True
    save_on_top = True
    list_per_page = 25

    list_display = (
        "percentage_display",
        "created_at",
        "updated_at",
    )

    list_display_links = ("percentage_display",)

    search_fields = ("percentage",)

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Discount Information",
            {
                "fields": ("percentage",),
            },
        ),
        (
            "System Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    @display(
        description="Discount",
        ordering="percentage",
    )
    def percentage_display(self, obj):
        return f"{obj.percentage}%"


@admin.register(Prescription)
class PrescriptionAdmin(ModelAdmin):
    warn_unsaved_form = True
    save_on_top = True
    list_per_page = 25

    inlines = (PrescriptionMedicineInline,)

    list_display = (
        "prescription_information",
        "patient",
        "physician_display",
        "diagnosis_summary",
        "medicine_count",
        "date_prescribed",
        "follow_up_status",
    )

    list_display_links = (
        "prescription_information",
        "patient",
    )

    list_filter = (
        "date_prescribed",
        "prescription_date",
        "follow_up_date",
        "physician",
    )

    search_fields = (
        "patient__first_name",
        "patient__last_name",
        "patient__registration_id",
        "patient__phone_number",
        "physician__username",
        "physician__first_name",
        "physician__last_name",
        "physician__registration_id",
        "diagnosis",
        "notes",
        "medicines__medicine__name",
    )

    autocomplete_fields = (
        "patient",
        "physician",
    )

    readonly_fields = (
        "prescription_date",
        "medicine_summary",
    )

    ordering = ("-date_prescribed",)

    date_hierarchy = "date_prescribed"

    fieldsets = (
        (
            "Prescription Information",
            {
                "classes": ("tab",),
                "fields": (
                    (
                        "patient",
                        "physician",
                    ),
                    (
                        "date_prescribed",
                        "follow_up_date",
                    ),
                ),
            },
        ),
        (
            "Clinical Information",
            {
                "classes": ("tab",),
                "fields": (
                    "diagnosis",
                    "notes",
                ),
            },
        ),
        (
            "Medicine Summary",
            {
                "classes": ("tab",),
                "fields": ("medicine_summary",),
                "description": (
                    "Medicines can be added or edited in the medicine " "section below."
                ),
            },
        ),
        (
            "System Information",
            {
                "classes": ("tab",),
                "fields": ("prescription_date",),
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.select_related(
            "patient",
            "physician",
        ).annotate(
            total_medicines=Count(
                "medicines",
                distinct=True,
            )
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Only active physician users can be selected.
        """

        if db_field.name == "physician":
            kwargs["queryset"] = User.objects.filter(
                role="physician",
                is_active=True,
            ).order_by(
                "first_name",
                "last_name",
                "username",
            )

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs,
        )

    @display(
        description="Prescription",
        ordering="date_prescribed",
    )
    def prescription_information(self, obj):
        return f"Prescription #{obj.pk}"

    @display(
        description="Physician",
        ordering="physician__first_name",
    )
    def physician_display(self, obj):
        full_name = obj.physician.get_full_name()

        return full_name or obj.physician.username

    @display(
        description="Diagnosis",
        ordering="diagnosis",
    )
    def diagnosis_summary(self, obj):
        if not obj.diagnosis:
            return "-"

        maximum_length = 60

        if len(obj.diagnosis) <= maximum_length:
            return obj.diagnosis

        return f"{obj.diagnosis[:maximum_length]}..."

    @display(
        description="Medicines",
        ordering="total_medicines",
    )
    def medicine_count(self, obj):
        return obj.total_medicines

    @display(
        description="Follow-up",
        ordering="follow_up_date",
    )
    def follow_up_status(self, obj):
        if not obj.follow_up_date:
            return "-"

        today = timezone.localdate()

        if obj.follow_up_date < today:
            return format_html(
                '<span class="text-red-600 dark:text-red-400">'
                "{} — Overdue"
                "</span>",
                obj.follow_up_date,
            )

        if obj.follow_up_date == today:
            return format_html(
                '<span class="font-medium text-orange-600 '
                'dark:text-orange-400">'
                "{} — Today"
                "</span>",
                obj.follow_up_date,
            )

        return obj.follow_up_date

    @display(
        description="Prescribed Medicines",
    )
    def medicine_summary(self, obj):
        if not obj or not obj.pk:
            return "Save the prescription before adding medicines."

        medicines = obj.medicines.select_related("medicine").all()

        if not medicines:
            return "No medicines added."

        items = []

        for item in medicines:
            details = [
                item.dose,
                item.frequency,
                item.timing,
            ]

            details = [detail for detail in details if detail]

            items.append(
                format_html(
                    """
                    <li class="mb-3">
                        <div class="font-medium">{}</div>
                        <div class="text-sm text-font-subtle-light
                                    dark:text-font-subtle-dark">
                            {}
                        </div>
                    </li>
                    """,
                    item.medicine,
                    " • ".join(details),
                )
            )

        return format_html(
            '<ul class="list-disc pl-5">{}</ul>',
            format_html("".join(str(item) for item in items)),
        )


@admin.register(PrescriptionMedicine)
class PrescriptionMedicineAdmin(ModelAdmin):
    warn_unsaved_form = True
    save_on_top = True
    list_per_page = 25

    list_display = (
        "medicine",
        "patient_display",
        "physician_display",
        "dose",
        "frequency",
        "timing",
        "amount",
        "date_prescribed",
    )

    list_display_links = (
        "medicine",
        "patient_display",
    )

    list_filter = (
        "medicine",
        "prescription__date_prescribed",
        "prescription__physician",
    )

    search_fields = (
        "medicine__name",
        "prescription__patient__first_name",
        "prescription__patient__last_name",
        "prescription__patient__registration_id",
        "prescription__physician__username",
        "prescription__physician__first_name",
        "prescription__physician__last_name",
        "dose",
        "frequency",
        "timing",
        "additional_instructions",
    )

    autocomplete_fields = (
        "prescription",
        "medicine",
    )

    ordering = (
        "-prescription__date_prescribed",
        "medicine__name",
    )

    fieldsets = (
        (
            "Prescription & Medicine",
            {
                "classes": ("tab",),
                "fields": (
                    "prescription",
                    "medicine",
                ),
            },
        ),
        (
            "Dosage Instructions",
            {
                "classes": ("tab",),
                "fields": (
                    (
                        "dose",
                        "frequency",
                    ),
                    (
                        "timing",
                        "amount",
                    ),
                    "additional_instructions",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "prescription",
                "prescription__patient",
                "prescription__physician",
                "medicine",
            )
        )

    @display(
        description="Patient",
        ordering="prescription__patient__first_name",
    )
    def patient_display(self, obj):
        return str(obj.prescription.patient)

    @display(
        description="Physician",
        ordering="prescription__physician__first_name",
    )
    def physician_display(self, obj):
        physician = obj.prescription.physician
        return physician.get_full_name() or physician.username

    @display(
        description="Prescribed On",
        ordering="prescription__date_prescribed",
    )
    def date_prescribed(self, obj):
        return obj.prescription.date_prescribed
