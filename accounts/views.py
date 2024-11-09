from django.contrib.auth import authenticate, login


from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
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
from .models import Nurse, Accountant, Receptionist, User
from .forms import NurseForm, AccountantForm, ReceptionistForm, UserLoginForm


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
    template_name = "accounts/list_view.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Nurse List"
        context["user_create"] = "nurse_create"
        context["user_detail"] = "nurse_detail"
        return context


class NurseDetailView(LoginRequiredMixin, DetailView):
    model = Nurse
    template_name = "accounts/detail_view.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Nurse Details"
        context["user_update"] = "nurse_update"
        context["user_delete"] = "nurse_delete"
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


def login_user(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Username is invalid!",
                    extra_tags="alert-danger",
                )
                return redirect("login")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "You have been logged in!",
                    extra_tags="success-subtle",
                )
                return redirect("user_redirect")
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Password is invalid!",
                    extra_tags="alert-danger",
                )
                return redirect("login")
        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Please fill these two fields",
                extra_tags="alert-danger",
            )
            return redirect("login")
    else:
        form = UserLoginForm()
        context = {"page_title": "Login", "form": form}
        return render(request, "registration/login.html", context=context)
