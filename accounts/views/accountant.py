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

from ..forms import AccountantForm
from ..models import Accountant


class AccountantDashboard(TemplateView):
    template_name = "accounts/dashboard/accountant_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Accountant Dashboard"
        return context


class AccountantListView(LoginRequiredMixin, ListView):
    model = Accountant
    template_name = "accounts/list_view.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Accountant List"
        context["user_create"] = "accountant_create"
        context["user_detail"] = "accountant_detail"
        return context


class AccountantDetailView(LoginRequiredMixin, DetailView):
    model = Accountant
    template_name = "accounts/detail_view.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Accountant Details"
        context["user_update"] = "accountant_update"
        context["user_delete"] = "accountant_delete"
        return context


class AccountantCreateView(LoginRequiredMixin, CreateView):
    model = Accountant
    form_class = AccountantForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("accountant_list")

    def form_valid(self, form):
        messages.success(self.request, "Accountant successfully created.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Failed to create Accountant. Please check the form for errors.",
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add Accountant"
        return context


class AccountantUpdateView(LoginRequiredMixin, UpdateView):
    model = Accountant
    form_class = AccountantForm
    template_name = "general_create_update.html"

    def get_success_url(self):
        return reverse_lazy("accountant_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Accountant successfully updated.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Failed to update Accountant. Please check the form for errors.",
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Accountant"
        return context


class AccountantDeleteView(LoginRequiredMixin, DeleteView):
    model = Accountant
    success_url = reverse_lazy("accountant_list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Accountant successfully deleted.")
        return super().delete(request, *args, **kwargs)
