from django import forms
from .models import Clinic


class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = [
            "name",
            "address",
            "email",
            "contact_number",
            "gst_number",
            "license_number",
            "logo",
            "consultation_duration",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter clinic name"}
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter clinic address",
                    "rows": 2,
                }
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter email address"}
            ),
            "contact_number": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter contact number"}
            ),
            "gst_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter GST number"}
            ),
            "license_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter license number"}
            ),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "consultation_duration": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter consultation duration (minutes)",
                }
            ),
        }

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get("contact_number")
        if contact_number and len(str(contact_number)) < 10:
            raise forms.ValidationError("Contact number must be at least 10 digits.")
        return contact_number
