from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from accounting.models import (
    Account,
    AccountsReceivable,
    Asset,
    GeneralLedgerEntry,
    AccountsPayable,
    Invoice,
)

from .forms import (
    AccountCreateUpdateForm,
    AccountsPayableForm,
    AccountsReceivableForm,
    AssetForm,
    GeneralLedgerEntryForm,
    InvoiceForm,
)


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
    success_url = reverse_lazy("accounts_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Clinic Accounts Create"
        return context


class AccountUpdateView(UpdateView):
    model = Account
    form_class = AccountCreateUpdateForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("accounts_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Clinic Accounts Update"
        return context


class AccountDeleteView(DeleteView):
    model = Account
    success_url = reverse_lazy("accounts_list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Account deleted")
        return super().delete(request, *args, **kwargs)


class GeneralLedgerEntryListView(ListView):
    model = GeneralLedgerEntry
    template_name = "accounting/list_general_entries.html"
    ordering = ["-date"]
    context_object_name = "general_entries"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "General Entry List"
        return context


class GeneralLedgerEntryCreateView(SuccessMessageMixin, CreateView):
    model = GeneralLedgerEntry
    form_class = GeneralLedgerEntryForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("general_entry_list")
    success_message = "Ledger entry created successfully!"

    def form_invalid(self, form):
        messages.error(self.request, "Error! Couldn't Create.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "General Entry Create"
        return context


class GeneralLedgerEntryUpdateView(SuccessMessageMixin, UpdateView):
    model = GeneralLedgerEntry
    form_class = GeneralLedgerEntryForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("general_entry_list:list")
    success_message = "Ledger entry updated successfully!"

    def form_invalid(self, form):
        messages.error(self.request, "Error! Couldn't Update.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "General Entry Update   "
        return context


class GeneralLedgerEntryDeleteView(SuccessMessageMixin, DeleteView):
    model = GeneralLedgerEntry
    success_url = reverse_lazy("general_entry_list")
    success_message = "Ledger entry deleted successfully!"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class AccountsReceivableListView(ListView):
    model = AccountsReceivable
    template_name = "accounting/list_accounts_receivable.html"
    ordering = ["-due_date"]
    context_object_name = "accounts_receivable"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Accounts Receivable List"
        return context


class AccountsReceivableCreateView(SuccessMessageMixin, CreateView):
    model = AccountsReceivable
    form_class = AccountsReceivableForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("accounts_receivable_list")
    success_message = "Account receivable created successfully!"

    def form_invalid(self, form):
        messages.error(self.request, "Error! Couldn't Create.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create Account Receivable"
        return context


class AccountsReceivableUpdateView(SuccessMessageMixin, UpdateView):
    model = AccountsReceivable
    form_class = AccountsReceivableForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("accounts_receivable_list")
    success_message = "Account receivable updated successfully!"

    def form_invalid(self, form):
        messages.error(self.request, "Error! Couldn't Update.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Account Receivable"
        return context


class AccountsReceivableDeleteView(SuccessMessageMixin, DeleteView):
    model = AccountsReceivable
    success_url = reverse_lazy("accounts_receivable_list")
    success_message = "Account receivable deleted successfully!"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class AccountsPayableListView(ListView):
    model = AccountsPayable
    template_name = "accounting/list_accounts_payable.html"
    ordering = ["-due_date"]
    context_object_name = "accounts_payable"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Accounts Payable List"
        return context


class AccountsPayableCreateView(SuccessMessageMixin, CreateView):
    model = AccountsPayable
    form_class = AccountsPayableForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("accounts_payable_list")
    success_message = "Account payable created successfully!"

    def form_invalid(self, form):
        messages.error(self.request, "Error! Couldn't Create.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create Account Payable"
        return context


class AccountsPayableUpdateView(SuccessMessageMixin, UpdateView):
    model = AccountsPayable
    form_class = AccountsPayableForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("accounts_payable_list")
    success_message = "Account payable updated successfully!"

    def form_invalid(self, form):
        messages.error(self.request, "Error! Couldn't Update.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Account Payable"
        return context


class AccountsPayableDeleteView(SuccessMessageMixin, DeleteView):
    model = AccountsPayable
    success_url = reverse_lazy("accounts_payable_list")
    success_message = "Account receivable deleted successfully!"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class InvoiceListView(ListView):
    model = Invoice
    template_name = "accounting/list_invoice.html"
    ordering = ["-date"]
    context_object_name = "invoices"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Invoice List"
        return context


class InvoiceCreateView(SuccessMessageMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("invoice_list")
    success_message = "Invoice created successfully!"

    def form_invalid(self, form):
        messages.error(self.request, "Error! Couldn't Create.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create Invoice"
        return context


class InvoiceUpdateView(SuccessMessageMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("invoice_list")
    success_message = "Invoice updated successfully!"

    def form_invalid(self, form):
        messages.error(self.request, "Error! Couldn't Update.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Invoice"
        return context


class InvoiceDeleteView(SuccessMessageMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy("invoice_list")
    success_message = "Invoice deleted successfully!"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class AssetListView(ListView):
    model = Asset
    template_name = "accounting/list_asset.html"
    ordering = ["-id"]
    context_object_name = "assets"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Asset List"
        return context


class AssetCreateView(SuccessMessageMixin, CreateView):
    model = Asset
    form_class = AssetForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("asset_list")
    success_message = "Asset created successfully!"

    def form_invalid(self, form):
        messages.error(self.request, "Error! Couldn't Create.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create Asset"
        return context


class AssetUpdateView(SuccessMessageMixin, UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = "general_create_update.html"
    success_url = reverse_lazy("asset_list")
    success_message = "Asset updated successfully!"

    def form_invalid(self, form):
        messages.error(self.request, "Error! Couldn't Update.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Asset"
        return context


class AssetDeleteView(SuccessMessageMixin, DeleteView):
    model = Asset
    success_url = reverse_lazy("asset_list")
    success_message = "Asset deleted successfully!"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
