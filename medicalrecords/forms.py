from django import forms

from accounts.models import Physician, Patient
from .models import Appointment, PrescriptionMedicine, Prescription, Discount


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "patient",
            "physician",
            "date",
            "time",
            "status",
            "discount",
        ]

    physician = forms.ModelChoiceField(
        queryset=Physician.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
    )

    time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                "type": "time",
                "class": "form-control",
            }
        ),
    )

    status = forms.ChoiceField(
        choices=Appointment.STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )

    discount = forms.ModelChoiceField(
        queryset=Discount.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.instance and self.instance.pk):
            self.fields.pop("status")
        self.fields["discount"].required = False
        self.fields["discount"].empty_label = "Select Discount"


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
