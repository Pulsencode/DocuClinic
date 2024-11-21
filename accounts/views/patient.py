from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from accounts.models import Patient

from ..forms import PatientDetailsForm, PatientForm


class PatientListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    ordering = ["id"]
    model = Patient
    template_name = "accounts/patient/patient_list.html"
    context_object_name = "patients"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PatientForm()
        context["page_title"] = "Patient List"
        context["patient"] = Patient.objects.all()
        return context


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("patient_list")

    def form_valid(self, form):
        # Save Patient form data
        patient = form.save()

        # Save PatientDetails form data
        details_form = PatientDetailsForm(self.request.POST)
        if details_form.is_valid():
            details = details_form.save(commit=False)
            details.patient = patient  # link PatientDetails to the patient
            details.save()

        messages.success(self.request, "Patient successfully created.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Failed to create Patient. Please check the form for errors.",
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Patient"
        context["details_form"] = PatientDetailsForm()
        return context


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = "general_create_update.html"

    def get_success_url(self):
        return reverse_lazy("user_profile", kwargs={"username": self.object.username})

    def form_valid(self, form):
        # Save the Patient form data
        patient = form.save()

        # Save PatientDetails form data
        details_form = PatientDetailsForm(
            self.request.POST, instance=self.object.patient_details
        )
        if details_form.is_valid():
            details = details_form.save(commit=False)
            details.patient = patient  # Ensure the correct patient is linked
            details.save()

        messages.success(self.request, "Patient successfully updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Failed to update Patient. Please check the form for errors.",
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Patient"
        context["details_form"] = PatientDetailsForm(
            instance=self.object.patient_details
        )
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
