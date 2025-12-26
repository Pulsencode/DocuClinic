from django import forms

from .models import Discount, Prescription, PrescriptionMedicine


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ["percentage"]
        widgets = {
            "percentage": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter discount percentage",
                }
            ),
        }
        labels = {
            "percentage": "Discount Percentage",
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = [
            "notes",
            "diagnosis",
            "follow_up_date",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "diagnosis": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "follow_up_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }


class PrescriptionMedicineForm(forms.ModelForm):
    class Meta:
        model = PrescriptionMedicine
        fields = [
            "medicine",
            "dose",
            "frequency",
            "timing",
            "amount",
            "additional_instructions",
        ]
        widgets = {
            "medicine": forms.Select(attrs={"class": "form-select"}),
            "dose": forms.TextInput(attrs={"class": "form-control"}),
            "frequency": forms.TextInput(attrs={"class": "form-control"}),
            "timing": forms.TextInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "additional_instructions": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
        }
