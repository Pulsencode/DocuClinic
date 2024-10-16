from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from accounts.forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Doctor, Appointment, Patient
from .forms import DoctorForm, AppointmentForm
from django.utils import timezone


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class Dashboard(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Dashboard"  # Set the page title
        return context


class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = "doctors/doctor_list.html"
    context_object_name = "doctors"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Doctor List"  # Set the page title
        return context


class DoctorDetailView(LoginRequiredMixin, DetailView):
    model = Doctor
    template_name = "doctors/doctor_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Doctor Details"
        return context


class DoctorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = "doctors/add_update_doctor.html"
    success_url = reverse_lazy("doctor_list")

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, "Doctor successfully created.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Failed to create doctor. Please check the form for errors."
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Doctor"  # Set the page title
        return context


class DoctorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = "doctors/add_update_doctor.html"

    def get_success_url(self):
        return reverse_lazy("doctor_detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.request.user.is_staff or self.request.user == self.get_object()

    def form_valid(self, form):
        messages.success(self.request, "Doctor successfully updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Failed to update doctor. Please check the form for errors."
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Doctor"
        return context


class DoctorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Doctor
    template_name = "doctor_confirm_delete.html"
    success_url = reverse_lazy("doctor_list")

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Doctor successfully deleted.")
        return super().delete(request, *args, **kwargs)


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "patients/patient_list.html"

    def form_valid(self, form):
        form.instance.patient = Patient.objects.get(pk=self.request.POST["patient"])  # Get patient from form
        self.object = form.save()
        messages.success(self.request, "Appointment created successfully!")  # Add a success message
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("patient_list")


# Doctor's Appointment List View
class DoctorDashboardView(ListView):
    model = Appointment
    template_name = "doctors/doctor_dashboard.html"  # Doctor dashboard template
    context_object_name = "appointments"

    def get_queryset(self):
        # Show only appointments related to the logged-in doctor
        return Appointment.objects.filter(doctor=self.request.user).order_by(
            "appointment_datetime"
        )


# Update Appointment Status View
class AppointmentUpdateView(UpdateView):
    model = Appointment
    fields = ["status"]  # Only the status field should be editable
    template_name = "doctors/appointment_update_form.html"
    success_url = reverse_lazy("dashboard")

    def get_queryset(self):
        # Limit to appointments belonging to the logged-in doctor
        return Appointment.objects.filter(doctor=self.request.user)


class AppointmentDeleteView(DeleteView):
    model = Appointment
    template_name = "patients/appointment_confirm_delete.html"  # Optional: You can create a confirmation template
    success_url = reverse_lazy('dashboard')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Appointment removed successfully!")
        return super().delete(request, *args, **kwargs)