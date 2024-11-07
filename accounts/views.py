from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
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
from .models import Nurse, Accountant, Receptionist
from .forms import NurseForm, AccountantForm, ReceptionistForm


@login_required
def user_redirect(request):
    """Redirects users to their respective dashboards based on user class."""

    if request.user.is_superuser:
        return redirect("admin:index")

    if hasattr(request.user, "physician"):
        return redirect("physician_dashboard")
    elif hasattr(request.user, "accountant"):
        return redirect("operator_dashboard")
    elif hasattr(request.user, "administrator"):
        return redirect("admin_dashboard")
    else:
        raise Http404("You are not registered with the system")


class NurseListView(LoginRequiredMixin, ListView):
    model = Nurse
    template_name = "accounts/nurses_list.html"
    context_object_name = "nurses"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Nurse List"
        return context


class NurseDetailView(LoginRequiredMixin, DetailView):
    model = Nurse
    template_name = "accounts/nurse_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Nurse Details"
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


class ReceptionistListView(LoginRequiredMixin, ListView):
    model = Receptionist
    template_name = "accounts/receptionists_list.html"
    context_object_name = "receptionists"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Receptionist List"
        return context


class ReceptionistDetailView(LoginRequiredMixin, DetailView):
    model = Receptionist
    template_name = "accounts/receptionist_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Receptionist Details"
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
        messages.error(self.request, "Failed to create Receptionist. Please check the form for errors.")
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
        messages.error(self.request, "Failed to update Receptionist. Please check the form for errors.")
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


class AccountantListView(LoginRequiredMixin, ListView):
    model = Accountant
    template_name = "accounts/accountants_list.html"
    context_object_name = "accountants"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Accountant List"
        return context


class AccountantDetailView(LoginRequiredMixin, DetailView):
    model = Accountant
    template_name = "accounts/accountant_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Accountant Details"
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
        messages.error(self.request, "Failed to create Accountant. Please check the form for errors.")
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
        messages.error(self.request, "Failed to update Accountant. Please check the form for errors.")
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
