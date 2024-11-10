from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from ..forms import UserLoginForm


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
