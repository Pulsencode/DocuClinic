from django import forms

from .models import Account, AccountsReceivable, GeneralLedgerEntry


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
            "description": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter description"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
        }
