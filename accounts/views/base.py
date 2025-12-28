from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from accounts.forms import UserLoginForm
from accounts.models import User


@login_required
def user_redirect(request):
    """Redirects users to their respective dashboards based on user class."""

    if request.user.is_superuser:
        return redirect("admin:index")

    if hasattr(request.user, "physician"):
        return redirect("physician_dashboard")
    elif hasattr(request.user, "nurse"):
        return redirect("nurse_dashboard")
    elif hasattr(request.user, "accountant"):
        return redirect("accountant_dashboard")
    elif hasattr(request.user, "receptionist"):
        return redirect("receptionist_dashboard")
    elif hasattr(request.user, "administrator"):
        return redirect("administration_dashboard")
    else:
        raise Http404(
            "You are not registered with the system"
        )  # TODO redirect the user to a 404 Page


def login_user(request):
    """Logs in the users and also is the user is authenticated then they will be redirected to there dashboard"""
    if request.user.is_authenticated:
        return redirect("user_redirect")

    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Authenticate the user
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(
                    request, "You have been logged in!", extra_tags="success-subtle"
                )
                return redirect("user_redirect")
            else:
                messages.error(
                    request, "Invalid username or password!", extra_tags="alert-danger"
                )
                return redirect("login")
        else:
            messages.error(
                request, "Please fill out both fields.", extra_tags="alert-danger"
            )
            return redirect("login")

    # GET request: render the login form
    form = UserLoginForm()
    context = {"page_title": "Login", "form": form}
    return render(request, "registration/login.html", context=context)


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs["username"])
        if hasattr(user, "physician"):
            context["user_role"] = "physician"
            context["user_delete"] = "physician_delete"
            context["user_update"] = "physician_update"
        elif hasattr(user, "nurse"):
            context["user_role"] = "nurse"
            context["user_delete"] = "nurse_delete"
            context["user_update"] = "nurse_update"
        elif hasattr(user, "accountant"):
            context["user_role"] = "accountant"
            context["user_delete"] = "accountant_delete"
            context["user_update"] = "accountant_update"
        elif hasattr(user, "receptionist"):
            context["user_role"] = "receptionist"
            context["user_delete"] = "receptionist_delete"
            context["user_update"] = "receptionist_update"
        elif hasattr(user, "administrator"):
            context["user_role"] = "administrator"
            context["user_delete"] = "administrator_delete"
            context["user_update"] = "administrator_update"
        elif hasattr(user, "patient"):
            context["user_role"] = "patient"
            context["user_delete"] = "patient_delete"
            context["user_update"] = "patient_update"
        else:
            context["user_role"] = "None"
            raise Http404("You are not registered with the system")
        context["user"] = user
        context["page_title"] = "Profile"

        return context
