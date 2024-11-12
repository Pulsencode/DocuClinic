from datetime import datetime

from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from accounts.models import Patient, Physician
from inventory.models import Medicine

from .forms import AppointmentForm, PrescriptionForm, PrescriptionMedicineForm
from .models import Appointment, Prescription, PrescriptionMedicine


class AppointmentListView(ListView):
    model = Appointment
    template_name = "medicalrecords/list_appointments.html"
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
    template_name = "medicalrecords/appointments_detail.html"
    context_object_name = "appointments"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Appointment Details"
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
        return reverse_lazy("list_appointments")


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
        elif hasattr(user, "physician"):
            return Appointment.objects.filter(physician=user)
        else:
            return Appointment.objects.none()

    def get_success_url(self):
        return reverse_lazy("list_appointments")


class AppointmentDeleteView(DeleteView):
    model = Appointment

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Appointment removed successfully!")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("list_appointments")


class PrescriptionListView(ListView):
    model = Prescription
    template_name = "medicalrecords/list_prescription.html"
    context_object_name = "prescriptions"
    ordering = ["-prescription_date"]
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Prescription List"
        return context

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

        # Retrieve the appointment using the appointment_id from the URL
        appointment_id = self.kwargs.get('appointment_id')

        appointment = get_object_or_404(Appointment, id=appointment_id)

        # Set patient and physician information from the appointment
        context["patient"] = appointment.patient
        context["physician"] = (
            appointment.physician
        )  # No need to show this in the template

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
                "additional_instructions",
            ),
            can_delete=True,
        )

        # Determine formset handling for GET or POST
        if self.request.POST:
            context["medicine_formset"] = PrescriptionMedicineFormSet(self.request.POST)
        else:
            context["medicine_formset"] = PrescriptionMedicineFormSet(
                queryset=PrescriptionMedicine.objects.none()
            )

        context["page_title"] = "Create Prescription"
        context["medicines"] = Medicine.objects.all()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        medicine_formset = context["medicine_formset"]

        if form.is_valid() and medicine_formset.is_valid():
            # Get the appointment ID and fetch the related Patient and Physician
            appointment_id = self.kwargs.get('appointment_id')

            appointment = get_object_or_404(Appointment, id=appointment_id)

            # Save the prescription, linking to patient and physician from the appointment
            prescription = form.save(commit=False)
            prescription.patient = appointment.patient
            prescription.physician = appointment.physician
            prescription.date_prescribed = timezone.now().date()
            prescription.save()

            # Save each medicine form linked to the prescription
            for medicine_form in medicine_formset:
                if medicine_form.cleaned_data and not medicine_form.cleaned_data.get(
                    "DELETE", False
                ):
                    medicine = medicine_form.save(commit=False)
                    medicine.prescription = prescription
                    medicine.save()
                elif medicine_form.cleaned_data.get("DELETE", False):
                    if medicine_form.instance.pk:
                        medicine_form.instance.delete()

            return super().form_valid(form)
        else:
            return self.form_invalid(form, medicine_formset)

    def form_invalid(self, form, medicine_formset=None):
        print(form.errors, "invalid")
        if medicine_formset is None:
            medicine_formset = self.get_context_data()["medicine_formset"]
        return self.render_to_response(
            self.get_context_data(form=form, medicine_formset=medicine_formset)
        )


class PrescriptionDetailView(DetailView):
    model = Prescription
    template_name = "medicalrecords/prescription_detail.html"
    context_object_name = "prescription"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Print Prescription"
        context["clinic_name"] = "Hospital Name"
        context["clinic_address"] = "Address or description"
        return context


class PrescriptionDeleteView(DeleteView):
    model = Prescription

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Prescription removed successfully!")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("prescription_list")
