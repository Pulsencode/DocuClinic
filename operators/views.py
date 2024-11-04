# from django.urls import reverse_lazy
# from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import (
#     ListView,
#     DetailView,
#     CreateView,
#     UpdateView,
#     DeleteView,
# )
# # from accounts.models import Operator
# from .forms import OperatorForm
# from django.utils import timezone
# from medicalrecords.models import Appointment


# class OperatorListView(LoginRequiredMixin, ListView):
#     model = Operator
#     template_name = "operators/operator_list.html"
#     context_object_name = "operators"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["page_title"] = "Operator list"
#         return context


# class OperatorDetailView(LoginRequiredMixin, DetailView):
#     model = Operator
#     template_name = "operators/operator_detail.html"
#     context_object_name = "operator"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["page_title"] = "Operator Detail"
#         return context


# class OperatorCreateView(LoginRequiredMixin, CreateView):
#     model = Operator
#     form_class = OperatorForm
#     template_name = "operators/add_update_operator.html"
#     success_url = reverse_lazy("operator_list")

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         messages.success(self.request, "Operator successfully created.")
#         return response

#     def form_invalid(self, form):
#         messages.error(
#             self.request, "Failed to create operator. Please check the form for errors."
#         )
#         return super().form_invalid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["page_title"] = "Add Operator"
#         return context


# class OperatorUpdateView(LoginRequiredMixin, UpdateView):
#     model = Operator
#     form_class = OperatorForm
#     template_name = "operators/add_update_operator.html"

#     def get_success_url(self):
#         return reverse_lazy("operator_detail", kwargs={"pk": self.object.pk})

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         messages.success(self.request, "Operator successfully updated.")
#         return response

#     def form_invalid(self, form):
#         messages.error(
#             self.request, "Failed to update operator. Please check the form for errors."
#         )
#         return super().form_invalid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["page_title"] = "Update Operator"
#         return context


# class OperatorDeleteView(LoginRequiredMixin, DeleteView):
#     model = Operator
#     template_name = "operators/operator_confirm_delete.html"
#     success_url = reverse_lazy("operator_list")

#     def delete(self, request, *args, **kwargs):
#         messages.success(request, "Operator successfully deleted.")
#         return super().delete(request, *args, **kwargs)


# class OperatorDashboardView(ListView):
#     model = Appointment
#     template_name = "operators/operator_dashboard.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["page_title"] = "Operator Dashboard"
#         context["appointments"] = Appointment.objects.filter(
#             appointment_datetime=timezone.now().date()
#         )

#         # Add summary statistics
#         context["total_appointments"] = self.model.objects.all().count()
#         context["pending_appointments"] = self.model.objects.filter(
#             status="Pending"
#         ).count()
#         context["today_appointments"] = self.model.objects.filter(
#             appointment_datetime__date=timezone.now().date()
#         ).count()

#         return context
