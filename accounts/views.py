from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from accounts.forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class Dashboard(TemplateView):
    template_name = "home.html"
