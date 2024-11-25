from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    DetailView,
)

from accounts.models import Physician, PhysicianAvailability
from medicalrecords.models import Appointment

from ..forms import PhysicianAvailabilityForm, PhysicianForm


class PhysicianListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    ordering = ["id"]
    model = Physician
    template_name = "accounts/physician/physicians_list.html"
    context_object_name = "physicians"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Physician List"
        return context


class PhysicianCreateView(LoginRequiredMixin, CreateView):
    model = Physician
    form_class = PhysicianForm
    template_name = "accounts/physician/create_update_physician.html"
    success_url = reverse_lazy("physician_list")

    def form_valid(self, form):
        messages.success(self.request, "Physician successfully created.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Failed to create Physician. Please check the form for errors.",
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Physician"
        return context


class PhysicianUpdateView(LoginRequiredMixin, UpdateView):
    model = Physician
    form_class = PhysicianForm
    template_name = "accounts/physician/create_update_physician.html"

    def get_success_url(self):
        return reverse_lazy("physician_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Physician successfully updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Failed to update Physician. Please check the form for errors.",
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Physician"
        return context


class PhysicianDeleteView(LoginRequiredMixin, DeleteView):
    model = Physician
    success_url = reverse_lazy("physician_list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Physician successfully deleted.")
        return super().delete(request, *args, **kwargs)


class PhysicianDashboardView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = (
        "accounts/dashboard/physician_dashboard.html"  # Physician dashboard template
    )
    context_object_name = "appointments"

    def get_queryset(self):
        # Show only appointments related to the logged-in Physician
        return Appointment.objects.filter(physician=self.request.user).order_by(
            "-date", "-time"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Physicians Dashboard"  # Set the page title
        return context


class PhysicianAvailabilityCreateView(CreateView):
    model = PhysicianAvailability
    form_class = PhysicianAvailabilityForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("user_redirect")

    def form_valid(self, form):
        messages.success(self.request, "Physician availability successfully created.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error creating the physician availability. Please check the form.",
        )
        return self.render_to_response(self.get_context_data(form=form))


class PhysicianAvailabilityUpdateView(UpdateView):
    model = PhysicianAvailability
    form_class = PhysicianAvailabilityForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("user_redirect")

    def form_valid(self, form):
        messages.success(self.request, "Physician availability successfully updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error updating the physician availability. Please check the form.",
        )
        return self.render_to_response(self.get_context_data(form=form))


class PhysicianAvailabilityDeleteView(DeleteView):
    model = PhysicianAvailability
    template_name = "general_create_update.html"
    success_url = reverse_lazy("user_redirect")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Physician availability successfully deleted.")
        return super().delete(request, *args, **kwargs)


class PhysicianAvailabilityDetailView(DetailView):
    model = PhysicianAvailability
    template_name = "physicianavailability_detail.html"
