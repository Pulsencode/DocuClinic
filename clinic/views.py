from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .models import Clinic
from .forms import ClinicForm


class ClinicCreateView(CreateView):
    model = Clinic
    form_class = ClinicForm
    template_name = "general_create_update.html"

    def get_success_url(self):
        return reverse('clinic_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create Clinic"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Clinic created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "There were errors in the form. Please check your input."
        )
        return super().form_invalid(form)


class ClinicUpdateView(UpdateView):
    model = Clinic
    form_class = ClinicForm
    template_name = "general_create_update.html"

    def get_success_url(self):
        return reverse('clinic_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Clinic"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Clinic updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "There were errors in the form. Please check your input."
        )
        return super().form_invalid(form)


class ClinicDetailView(DetailView):
    model = Clinic
    template_name = (
        "clinic/clinic_detail.html"
    )
    context_object_name = "clinic"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Clinic Details"
        return context


class ClinicDeleteView(DeleteView):
    model = Clinic
    template_name = "clinic_confirm_delete.html"
    success_url = reverse_lazy("clinic_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Delete Clinic"
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Clinic deleted successfully!")
        return super().delete(request, *args, **kwargs)
