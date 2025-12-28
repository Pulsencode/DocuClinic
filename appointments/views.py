from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import make_aware
from django.views.decorators.http import require_http_methods
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from accounts.models import Patient, PatientDetail, Physician, PhysicianAvailability
from appointments.forms import AppointmentForm
from appointments.models import Appointment
from clinic.models import Clinic


class AppointmentListView(ListView):
    paginate_by = 10
    ordering = ["id"]
    model = Appointment
    template_name = "appointments/list_appointments.html"
    context_object_name = "all_appointments"

    def get_queryset(self):
        queryset = (
            Appointment.objects.all()
            .select_related("physician", "patient")
            .order_by("date", "time")
        )

        # Get filter parameters from GET request
        physician_id = self.request.GET.get("physician")
        status = self.request.GET.get("status")
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")

        # Apply filters
        if "clear_filters" in self.request.GET:
            return queryset.order_by("date", "time")
        if physician_id:
            queryset = queryset.filter(physician_id=physician_id)
        if status:
            queryset = queryset.filter(status=status)
        if date_from:
            try:
                date_from = datetime.strptime(date_from, "%Y-%m-%d")
                queryset = queryset.filter(date__gte=date_from)
            except ValueError:
                pass
        if date_to:
            try:
                date_to = datetime.strptime(date_to, "%Y-%m-%d")
                queryset = queryset.filter(date__lte=date_to)
            except ValueError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Appointment List"
        # Add filter options to context
        context["physician"] = Physician.objects.all().order_by("username")
        context["status_choices"] = Appointment.STATUS_CHOICES

        # Preserve filter values in context
        context["selected_physician"] = self.request.GET.get("physician", "")
        context["selected_status"] = self.request.GET.get("status", "")
        context["selected_date_from"] = self.request.GET.get("date_from", "")
        context["selected_date_to"] = self.request.GET.get("date_to", "")

        context["total_appointments"] = self.get_queryset().count()
        context["pending_appointments"] = self.model.objects.filter(
            status="Pending"
        ).count()
        context["today_appointments"] = self.model.objects.filter(
            date=timezone.now().date()
        ).count()
        return context


class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = "appointments/appointments_detail.html"
    context_object_name = "appointments"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Appointment Details"
        return context


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/create_update_appointments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Appointment"
        context["action"] = "Add"
        context["model"] = "Appointment"
        return context

    def form_valid(self, form):
        form.instance.patient = Patient.objects.get(pk=self.request.POST["patient"])
        physician = form.cleaned_data["physician"]
        base_fee = physician.fee_per_consultation
        if form.cleaned_data.get("discount"):
            discount = form.cleaned_data["discount"]
            discount_amount = (base_fee * Decimal(discount.percentage)) / Decimal("100")
            consultation_fee = base_fee - discount_amount
        else:
            consultation_fee = base_fee
        form.instance.consultation_fee = consultation_fee
        self.object = form.save()
        messages.success(self.request, "Appointment created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "error occurred couldn't create appointment")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("list_appointments")


# TODO This can be a util so that other modules can use it too - will need to refactor if app goes live
@require_http_methods(["GET"])
def check_patient_vip_status(request):
    patient_id = request.GET.get("patient_id")
    try:
        # Get the patient's detail through the relationship
        patient_detail = PatientDetail.objects.get(patient_id=patient_id)
        return JsonResponse(
            {
                "is_vip": patient_detail.is_vip,
            }
        )
    except PatientDetail.DoesNotExist:
        return JsonResponse(
            {
                "is_vip": False,  # Default to non-VIP if no details exist
                "error": "Patient details not found",
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def get_available_dates(request):
    physician_id = request.GET.get("physician_id")

    if not physician_id:
        return JsonResponse({"error": "Physician ID not provided."}, status=400)

    try:
        physician_availability = PhysicianAvailability.objects.filter(
            physician_id=physician_id
        ).first()

        if not physician_availability:
            return JsonResponse(
                {"error": "No availability found for this physician."}, status=404
            )

        # Get the consultation duration from the first clinic (assuming single clinic system)
        clinic = Clinic.objects.first()
        consultation_duration = clinic.consultation_duration if clinic else 30

        work_days = physician_availability.work_days.all()

        # Convert day names to weekday integers (0 = Monday, 6 = Sunday)
        day_mapping = {
            "MONDAY": 0,
            "TUESDAY": 1,
            "WEDNESDAY": 2,
            "THURSDAY": 3,
            "FRIDAY": 4,
            "SATURDAY": 5,
            "SUNDAY": 6,
        }
        work_days_indices = [
            day_mapping[str(day.name).strip().upper()]
            for day in work_days
            if str(day.name).strip().upper() in day_mapping
        ]

        work_start = physician_availability.work_time_start
        work_end = physician_availability.work_time_end
        lunch_start = physician_availability.lunch_start
        lunch_end = physician_availability.lunch_end

        time_slots = []
        current_time = work_start

        while current_time < work_end:
            # Calculate next time slot based on clinic's consultation duration
            current_datetime = datetime.combine(datetime.today(), current_time)
            next_datetime = current_datetime + timedelta(minutes=consultation_duration)
            next_time = next_datetime.time()

            # If the next time would go beyond work_end, break the loop
            if next_time > work_end:
                break

            if lunch_start and lunch_end:
                lunch_start_time = make_aware(
                    datetime.combine(datetime.today(), lunch_start)
                )
                lunch_end_time = make_aware(
                    datetime.combine(datetime.today(), lunch_end)
                )

                current_slot_start = make_aware(
                    datetime.combine(datetime.today(), current_time)
                )
                current_slot_end = make_aware(
                    datetime.combine(datetime.today(), next_time)
                )

                # Skip time slots overlapping with lunch
                if (
                    current_slot_end > lunch_start_time
                    and current_slot_start < lunch_end_time
                ):
                    current_time = next_time
                    continue

            time_slots.append(
                {
                    "start": current_time.strftime("%H:%M"),
                    "end": next_time.strftime("%H:%M"),
                }
            )
            current_time = next_time

        today = datetime.now().date()
        available_dates = []

        for i in range(30):  # Next 30 days
            day = today + timedelta(days=i)
            if day.weekday() in work_days_indices:
                available_slots_for_day = [
                    slot
                    for slot in time_slots
                    if not Appointment.objects.filter(
                        physician_id=physician_id,
                        date=day,
                        time=slot["start"],
                    ).exists()
                ]

                if available_slots_for_day:
                    available_dates.append(
                        {
                            "date": day.strftime("%Y-%m-%d"),
                            "times": available_slots_for_day,
                        }
                    )

        return JsonResponse(
            {
                "available_dates": available_dates,
                "consultation_duration": consultation_duration,
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "appointments/create_update_appointments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Appointment"
        context["action"] = "Update"
        context["model"] = "Appointment"
        return context

    def form_valid(self, form):
        form.instance.patient = Patient.objects.get(pk=self.request.POST["patient"])
        physician = form.cleaned_data["physician"]
        base_fee = physician.fee_per_consultation
        if form.cleaned_data.get("discount"):
            discount = form.cleaned_data["discount"]
            discount_amount = (base_fee * Decimal(discount.percentage)) / Decimal("100")
            consultation_fee = base_fee - discount_amount
        else:
            consultation_fee = base_fee
        form.instance.consultation_fee = consultation_fee
        self.object = form.save()
        messages.success(self.request, "Appointment update successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "error occurred couldn't update appointment")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("list_appointments")


class AppointmentDeleteView(DeleteView):
    model = Appointment

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Appointment removed successfully!")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("list_appointments")
