from django import forms

from .models import Account, AccountsPayable, AccountsReceivable, Asset, GeneralLedgerEntry, Invoice


class AccountCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["name", "type"]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter account name"}
            ),
            "type": forms.Select(
                attrs={"class": "form-control", "placeholder": "Select account type"}
            ),
        }


class GeneralLedgerEntryForm(forms.ModelForm):
    class Meta:
        model = GeneralLedgerEntry
        fields = ["date", "description", "debit_account", "credit_account", "amount"]
        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "debit_account": forms.Select(attrs={"class": "form-select"}),
            "credit_account": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
        }


class AccountsReceivableForm(forms.ModelForm):
    class Meta:
        model = AccountsReceivable
        fields = ["name", "amount", "due_date", "description", "status"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter name"}
            ),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter amount"}
            ),
            "due_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter description", "rows": 2}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class AccountsPayableForm(forms.ModelForm):
    class Meta:
        model = AccountsPayable
        fields = ["name", "amount", "due_date", "description", "status"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter name"}
            ),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter amount"}
            ),
            "due_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter description", "rows": 2}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = "__all__"
        widgets = {
            "invoice_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Invoice Number"}
            ),
            "organization_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Organization Name"}
            ),
            "date": forms.DateInput(
                attrs={"class": "form-control", "type": "date", "placeholder": "Select Date"}
            ),
            "total_amount": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter Total Amount"}
            ),
        }


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Asset Name"}
            ),
            "purchase_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date", "placeholder": "Select Purchase Date"}
            ),
            "purchase_value": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter Purchase Value"}
            ),
            "current_value": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter Current Value"}
            ),
            "current_value_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date", "placeholder": "Select Current Value Date"}
            ),
            "depreciation_rate": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter Depreciation Rate"}
            ),
        }
