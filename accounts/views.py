from django.shortcuts import redirect
from django.urls import reverse_lazy
from accounts.forms import CustomUserCreationForm
from django.contrib import messages
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Doctor, Appointment, Patient, Operator
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required


@login_required
def user_redirect(request):
    try:
        Doctor.objects.get(id=request.user.id)
        return redirect("doctor_dashboard")
    except Doctor.DoesNotExist:
        try:
            Operator.objects.get(id=request.user.id)
            return redirect("operator_dashboard")
        except Operator.DoesNotExist:
            return redirect("home")


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "patients/patient_list.html"

    def form_valid(self, form):
        form.instance.patient = Patient.objects.get(
            pk=self.request.POST["patient"]
        )  # Get patient from form
        self.object = form.save()
        messages.success(
            self.request, "Appointment created successfully!"
        )  # Add a success message
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("patient_list")


# Update Appointment Status View
class AppointmentUpdateView(UpdateView):
    model = Appointment
    fields = ["status"]  # Only the status field should be editable
    template_name = "doctors/appointment_update_form.html"

    def get_queryset(self):
        user = self.request.user
        # Check if the user is a doctor or an operator
        if hasattr(user, "operator"):
            return Appointment.objects.all()  # Operators can update any appointment
        elif hasattr(user, "doctor"):
            return Appointment.objects.filter(
                doctor=user
            )  # Doctors can only update their own appointments
        else:
            return Appointment.objects.none()

    def get_success_url(self):
        user = self.request.user
        # Redirect to the appropriate dashboard based on the user's role
        if hasattr(user, "operator"):
            return reverse_lazy("operator_dashboard")  # Redirect to operator dashboard
        else:
            return reverse_lazy("doctor_dashboard")  # Redirect to doctor/dashboard


class AppointmentDeleteView(DeleteView):
    model = Appointment
    template_name = "patients/appointment_confirm_delete.html"  # Optional: You can create a confirmation template

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Appointment removed successfully!")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        user = self.request.user
        # Redirect to the appropriate dashboard based on the user's role
        if hasattr(user, "operator"):
            return reverse_lazy("operator_dashboard")  # Redirect to operator dashboard
        else:
            return reverse_lazy("doctor_dashboard")
