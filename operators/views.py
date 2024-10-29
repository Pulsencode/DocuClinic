from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from accounts.models import Doctor, Operator
from .forms import OperatorForm
from django.utils import timezone
from datetime import datetime
from medicalrecords.models import Appointment


class OperatorListView(LoginRequiredMixin, ListView):
    model = Operator
    template_name = "operators/operator_list.html"
    context_object_name = "operators"

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "operator") and not hasattr(
            request.user, "doctor"
        ):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Operator list"
        return context


class OperatorDetailView(LoginRequiredMixin, DetailView):
    model = Operator
    template_name = "operators/operator_detail.html"
    context_object_name = "operator"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Operator Detail"
        return context


class OperatorCreateView(LoginRequiredMixin, CreateView):
    model = Operator
    form_class = OperatorForm
    template_name = "operators/add_update_operator.html"
    success_url = reverse_lazy("operator_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Operator successfully created.")
        return response

    def form_invalid(self, form):
        messages.error(
            self.request, "Failed to create operator. Please check the form for errors."
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Operator"
        return context


class OperatorUpdateView(LoginRequiredMixin, UpdateView):
    model = Operator
    form_class = OperatorForm
    template_name = "operators/add_update_operator.html"

    def get_success_url(self):
        return reverse_lazy("operator_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Operator successfully updated.")
        return response

    def form_invalid(self, form):
        messages.error(
            self.request, "Failed to update operator. Please check the form for errors."
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Operator"
        return context


class OperatorDeleteView(LoginRequiredMixin, DeleteView):
    model = Operator
    template_name = "operators/operator_confirm_delete.html"
    success_url = reverse_lazy("operator_list")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Operator successfully deleted.")
        return super().delete(request, *args, **kwargs)


class OperatorDashboardView(ListView):
    model = Appointment
    template_name = "operators/operator_dashboard.html"
    context_object_name = "appointments"
    paginate_by = 10  # Pagination for better performance

    def get_queryset(self):
        queryset = (
            Appointment.objects.all()
            .select_related("doctor", "patient")
            .order_by("-appointment_datetime")
        )

        # Get filter parameters from GET request
        doctor_id = self.request.GET.get("doctor")
        status = self.request.GET.get("status")
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")

        # Apply filters
        # if 'clear_filters' in self.request.GET:
        #     return queryset.order_by('appointment_datetime')
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
        context["page_title"] = "Operator Dashboard"

        # Add filter options to context
        context["doctors"] = Doctor.objects.all().order_by("username")
        context["status_choices"] = Appointment.STATUS_CHOICES

        # Preserve filter values in context
        context["selected_doctor"] = self.request.GET.get("doctor", "")
        context["selected_status"] = self.request.GET.get("status", "")
        context["selected_date_from"] = self.request.GET.get("date_from", "")
        context["selected_date_to"] = self.request.GET.get("date_to", "")

        # Add summary statistics
        context["total_appointments"] = self.get_queryset().count()
        context["pending_appointments"] = (
            self.get_queryset().filter(status="Pending").count()
        )
        context["today_appointments"] = (
            self.get_queryset()
            .filter(appointment_datetime__date=timezone.now().date())
            .count()
        )

        return context
