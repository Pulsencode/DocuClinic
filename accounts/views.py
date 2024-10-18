from django.shortcuts import redirect
from django.urls import reverse_lazy
from accounts.forms import CustomUserCreationForm
from django.views.generic import (
    CreateView,
)
from .models import Doctor, Operator
from django.contrib.auth.decorators import login_required


@login_required
def user_redirect(request):
    try:
        Doctor.objects.get(id=request.user.id)
        return redirect("doctor_dashboard")
    except Doctor.DoesNotExist:
        try:
            Operator.objects.get(id=request.user.id)
            return redirect("operator_dashboard")
        except Operator.DoesNotExist:
            return redirect("home")


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
