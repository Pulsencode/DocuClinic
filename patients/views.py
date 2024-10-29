from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from accounts.models import Doctor, Patient

from .forms import PatientDetailsForm, PatientForm
from .models import PatientDetail


class PatientListView(ListView):
    model = Patient
    template_name = "patients/patient_list.html"
    context_object_name = "patients"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PatientForm()
        context["page_title"] = "Patient List"
        context["doctors"] = Doctor.objects.all()
        return context


class PatientCreateUpdateMixin:
    model = Patient
    form_class = PatientForm
    template_name = "patients/add_update_patient.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["details_form"] = PatientDetailsForm(
            instance=getattr(self.object, "patient_details", None)
        )
        return context

    def form_valid(self, form):
        details_form = PatientDetailsForm(
            self.request.POST, instance=getattr(self.object, "patient_details", None)
        )

        if form.is_valid() and details_form.is_valid():
            with transaction.atomic():
                patient = form.save()
                details = details_form.save(commit=False)
                details.patient = patient
                details.save()

            messages.success(
                self.request,
                f"Patient '{patient.username}' {'updated' if self.object else 'created'} successfully!",
            )
            return redirect("patient_detail", pk=patient.pk)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Error occurred. Please check the form and try again."
        )
        return super().form_invalid(form)


class PatientCreateView(PatientCreateUpdateMixin, CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add New Patient"
        return context


class PatientUpdateView(PatientCreateUpdateMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Patient"
        return context


class PatientDetailView(DetailView):
    model = Patient
    template_name = "patients/patient_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patient"] = self.object
        context["page_title"] = "Patient Details"
        context["details"] = PatientDetail.objects.get_or_create(patient=self.object)[0]
        return context


class PatientDeleteView(DeleteView):
    model = Patient
    success_url = reverse_lazy("patient_list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        patient = self.get_object()
        messages.success(request, f"Patient '{patient.username}' deleted successfully!")
        return super().delete(request, *args, **kwargs)
