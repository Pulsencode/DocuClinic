from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from medicalrecords.models import Appointment
from accounts.models import Doctor, Patient
from .forms import AppointmentForm
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
        context["doctors"] = Doctor.objects.all().order_by("username")
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
