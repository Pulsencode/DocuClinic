from django import forms

from .models import Account


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
