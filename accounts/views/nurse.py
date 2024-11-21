from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from ..forms import NurseForm
from ..models import Nurse


class NurseDashboard(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard/nurse_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Nurse Dashboard"
        return context


class NurseListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    ordering = ["id"]
    model = Nurse
    template_name = "accounts/list_view.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Nurse List"
        context["user_create"] = "nurse_create"
        context["user_detail"] = "nurse_detail"
        return context


class NurseCreateView(LoginRequiredMixin, CreateView):
    model = Nurse
    form_class = NurseForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("nurse_list")

    def form_valid(self, form):
        messages.success(self.request, "Nurse successfully created.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Failed to create Nurse. Please check the form for errors."
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Nurse"
        return context


class NurseUpdateView(LoginRequiredMixin, UpdateView):
    model = Nurse
    form_class = NurseForm
    template_name = "general_create_update.html"

    def get_success_url(self):
        return reverse_lazy("nurse_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Nurse successfully updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Failed to update Nurse. Please check the form for errors."
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Nurse"
        return context


class NurseDeleteView(LoginRequiredMixin, DeleteView):
    model = Nurse
    success_url = reverse_lazy("nurse_list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Nurse successfully deleted.")
        return super().delete(request, *args, **kwargs)
