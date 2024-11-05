from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import CustomUserCreationForm


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


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
