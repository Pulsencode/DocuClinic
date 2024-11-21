from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from accounting.models import Account

from .forms import AccountCreateUpdateForm


class AccountListView(ListView):
    paginate_by = 10
    ordering = ["id"]
    model = Account
    template_name = "accounting/list_accounts.html"
    context_object_name = "accounts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Clinic Accounts List"
        return context


class AccountCreateView(CreateView):
    model = Account
    form_class = AccountCreateUpdateForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("list_supplier")


class AccountUpdateView(UpdateView):
    template_name = ""


class AccountDeleteView(DeleteView):
    template_name = ""
