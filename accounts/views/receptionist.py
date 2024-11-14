from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    TemplateView,
)

from ..forms import ReceptionistForm
from ..models import Receptionist


class ReceptionistDashboard(TemplateView):
    template_name = "accounts/dashboard/receptionist_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Receptionist Dashboard"
        return context


class ReceptionistListView(LoginRequiredMixin, ListView):
    model = Receptionist
    template_name = "accounts/list_view.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Receptionist List"
        context["user_create"] = "receptionist_create"
        context["user_detail"] = "receptionist_detail"
        return context


class ReceptionistDetailView(LoginRequiredMixin, DetailView):
    model = Receptionist
    template_name = "accounts/detail_view.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Receptionist Details"
        context["user_update"] = "receptionist_update"
        context["user_delete"] = "receptionist_delete"
        return context


class ReceptionistCreateView(LoginRequiredMixin, CreateView):
    model = Receptionist
    form_class = ReceptionistForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("receptionist_list")

    def form_valid(self, form):
        messages.success(self.request, "Receptionist successfully created.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Failed to create Receptionist. Please check the form for errors.",
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Receptionist"
        return context


class ReceptionistUpdateView(LoginRequiredMixin, UpdateView):
    model = Receptionist
    form_class = ReceptionistForm
    template_name = "general_create_update.html"

    def get_success_url(self):
        return reverse_lazy("receptionist_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Receptionist successfully updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Failed to update Receptionist. Please check the form for errors.",
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Receptionist"
        return context


class ReceptionistDeleteView(LoginRequiredMixin, DeleteView):
    model = Receptionist
    success_url = reverse_lazy("receptionist_list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Receptionist successfully deleted.")
        return super().delete(request, *args, **kwargs)
