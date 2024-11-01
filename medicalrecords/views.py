from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from medicalrecords.models import Appointment
from accounts.models import Patient
from .forms import AppointmentForm


class AppointmentListView(ListView):
    model = Appointment
    template_name = "medicalrecords/list_appointments.html"
    context_object_name = "all_appointments"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Appointment List"
        return context


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "medicalrecords/create_update_appointments.html"

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
