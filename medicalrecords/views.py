from django.forms import modelformset_factory
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    FormView,
    DetailView,
)

from inventory.models import Medicine
from .models import Appointment, Prescription, PrescriptionMedicine
from accounts.models import Physician, Patient
from .forms import AppointmentForm, PrescriptionForm, PrescriptionMedicineForm
from datetime import datetime
from django.utils import timezone


class AppointmentListView(ListView):
    model = Appointment
    template_name = "medicalrecords/list_appointments.html"
    context_object_name = "all_appointments"

    def get_queryset(self):
        queryset = (
            Appointment.objects.all()
            .select_related("doctor", "patient")
            .order_by("appointment_datetime")
        )

        # Get filter parameters from GET request
        doctor_id = self.request.GET.get("doctor")
        status = self.request.GET.get("status")
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")

        # Apply filters
        if "clear_filters" in self.request.GET:
            return queryset.order_by("appointment_datetime")
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        if status:
            queryset = queryset.filter(status=status)
        if date_from:
            try:
                date_from = datetime.strptime(date_from, "%Y-%m-%d")
                queryset = queryset.filter(appointment_datetime__date__gte=date_from)
            except ValueError:
                pass
        if date_to:
            try:
                date_to = datetime.strptime(date_to, "%Y-%m-%d")
                queryset = queryset.filter(appointment_datetime__date__lte=date_to)
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
        context["selected_doctor"] = self.request.GET.get("doctor", "")
        context["selected_status"] = self.request.GET.get("status", "")
        context["selected_date_from"] = self.request.GET.get("date_from", "")
        context["selected_date_to"] = self.request.GET.get("date_to", "")

        context["total_appointments"] = self.get_queryset().count()
        context["pending_appointments"] = self.model.objects.filter(
            status="Pending"
        ).count()
        context["today_appointments"] = self.model.objects.filter(
            appointment_datetime__date=timezone.now().date()
        ).count()
        return context


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "medicalrecords/create_update_appointments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Appointment"
        context["action"] = "Add"
        context["model"] = "Appointment"
        return context

    def form_valid(self, form):
        form.instance.patient = Patient.objects.get(pk=self.request.POST["patient"])
        self.object = form.save()
        messages.success(self.request, "Appointment created successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("user_redirect")


# Update Appointment Status View
class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "medicalrecords/create_update_appointments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Appointment"
        context["action"] = "Update"
        context["model"] = "Appointment"
        return context

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "operator"):
            return Appointment.objects.all()
        elif hasattr(user, "doctor"):
            return Appointment.objects.filter(doctor=user)
        else:
            return Appointment.objects.none()

    def get_success_url(self):
        return reverse_lazy("user_redirect")


class AppointmentDeleteView(DeleteView):
    model = Appointment

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Appointment removed successfully!")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("user_redirect")


class PrescriptionListView(ListView):
    model = Prescription
    template_name = "medicalrecords/list_prescription.html"
    context_object_name = "prescriptions"
    ordering = ["-prescription_date"]
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            if hasattr(self.request.user, "physician"):
                queryset = queryset.filter(physician=self.request.user.physician)
        return queryset


class PrescriptionCreateView(FormView):
    template_name = "medicalrecords/create_prescription.html"
    form_class = PrescriptionForm

    def get_success_url(self):
        return reverse("prescription_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Initialize the PrescriptionMedicine formset
        PrescriptionMedicineFormSet = modelformset_factory(
            PrescriptionMedicine,
            form=PrescriptionMedicineForm,
            extra=1,
            fields=(
                "medicine",
                "dose",
                "frequency",
                "timing",
                "amount",
                "additional_instructions",
            ),
        )
        context["medicine_formset"] = PrescriptionMedicineFormSet(
            queryset=PrescriptionMedicine.objects.none()
        )

        # Add other context variables
        context["physician"] = self.request.user.physician
        context["medicines"] = Medicine.objects.all()

        return context

    def form_valid(self, form):
        # Get medicine formset from POST data
        medicine_formset = self.get_context_data()["medicine_formset"]
        medicine_formset = medicine_formset.__class__(self.request.POST)

        if form.is_valid() and medicine_formset.is_valid():
            # Save the prescription instance
            prescription = form.save(commit=False)
            prescription.physician = self.request.user.physician
            prescription.date_prescribed = (
                self.request.POST.get("date_prescribed") or timezone.now().date()
            )
            prescription.save()

            # Save each valid medicine form linked to the prescription
            for medicine_form in medicine_formset:
                if medicine_form.cleaned_data:
                    medicine = medicine_form.save(commit=False)
                    medicine.prescription = prescription
                    medicine.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form, medicine_formset)

    def form_invalid(self, form, medicine_formset=None):
        if not medicine_formset:
            medicine_formset = self.get_context_data()["medicine_formset"](
                self.request.POST
            )
        # Render invalid form and formset with errors
        return self.render_to_response(
            self.get_context_data(form=form, medicine_formset=medicine_formset)
        )


class PrescriptionDetailView(DetailView):
    model = Prescription
    template_name = "medicalrecords/prescription_detail.html"
    context_object_name = "prescription"
