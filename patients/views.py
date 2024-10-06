from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)
from .forms import PatientForm
from django.contrib import messages
from accounts.models import Patient


# List all patients (ListView)
class PatientListView(ListView):
    model = Patient
    template_name = "patients/patient_list.html"
    context_object_name = "patients"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PatientForm()  # Pass the form instance here
        return context


# Create your views here.
class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "patients/patient_detail.html"
    success_url = reverse_lazy(
        "patient_list"
    )  # Redirect to patient list after creation

    def form_valid(self, form):
        patient = form.save()  # Save the patient instance
        messages.success(
            self.request, "Patient created successfully!"
        )  # Show success message
        return redirect(
            "patient_detail", pk=patient.pk
        )  # Redirect to the detail view of the newly created patient

    def form_invalid(self, form):
        error_details = form.errors.as_text()
        messages.error(self.request, f"Error ocurred: {error_details}")

        return self.render_to_response({"form": form, "form_errors": form.errors})


# View a single patient's details (DetailView)
class PatientDetailView(DetailView):
    model = Patient
    template_name = "patients/patient_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PatientForm(instance=self.object)
        context["patient"] = self.object
        return context


class PatientUpdateView(UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = "patients/patient_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PatientForm(instance=self.object)
        context["patient"] = self.object
        return context

    def form_valid(self, form):
        patient = form.save()
        messages.success(
            self.request, f"Patient '{patient.username}' updated successfully!"
        )
        return redirect("patient_detail", pk=patient.pk)

    def form_invalid(self, form):
        error_details = form.errors.as_text()
        messages.error(self.request, f"Error ocurred: {error_details}")
        return self.render_to_response(self.get_context_data(form=form))


# Delete a patient (DeleteView)
class PatientDeleteView(DeleteView):
    model = Patient
    template_name = "patient_confirm_delete.html"
    success_url = reverse_lazy("patient_list")
