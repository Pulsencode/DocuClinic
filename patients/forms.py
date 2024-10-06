from django import forms
from accounts.models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "username",
            "email",
            "phone_number_country_code",
            "phone_number",
            "address",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your username"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter your email"}
            ),
            # 'phone_number_country_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country code'}),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your phone number",
                }
            ),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }

    phone_number_country_code = forms.CharField(
        required=False,
        max_length=3,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "style": "max-width: 65px;",
                "placeholder": "Country code",
            }
        ),
    )
