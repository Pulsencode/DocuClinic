import logging

from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from accounts.models import Patient
from appointments.models import Appointment
from inventory.models import Medicine

from .forms import DiscountForm, PrescriptionForm, PrescriptionMedicineForm
from .models import Discount, Prescription, PrescriptionMedicine

logger = logging.getLogger(__name__)


class PrescriptionListView(ListView):
    paginate_by = 10
    ordering = ["id"]
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
        appointment_id = self.kwargs.get("appointment_id")

        appointment = get_object_or_404(Appointment, id=appointment_id)

        # Set patient and physician information from the appointment
        context["patient"] = appointment.patient
        context[
            "physician"
        ] = appointment.physician  # No need to show this in the template

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
            appointment_id = self.kwargs.get("appointment_id")

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


class PatientPrescriptionsView(View):
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)

        prescriptions = patient.prescriptions.all()

        return render(
            request,
            "medicalrecords/patient_prescriptions.html",
            {"patient": patient, "prescriptions": prescriptions},
        )


class DiscountCreateView(CreateView):
    model = Discount
    form_class = DiscountForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("discount_list")
    success_message = "Discount added successfully!"

    def form_valid(self, form):
        messages.success(self.request, "Discount added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error adding the discount.")
        return super().form_invalid(form)


class DiscountUpdateView(UpdateView):
    model = Discount
    form_class = DiscountForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("discount_list")

    def form_valid(self, form):
        messages.success(self.request, "Discount updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the discount.")
        return super().form_invalid(form)


class DiscountDeleteView(DeleteView):
    model = Discount
    success_url = reverse_lazy("discount_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Discount deleted successfully!")
        return super().delete(request, *args, **kwargs)
