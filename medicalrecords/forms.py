from django import forms

from accounts.models import Physician, Patient
from .models import Appointment, PrescriptionMedicine, Prescription


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["patient", "doctor", "appointment_datetime", "status"]

    doctor = forms.ModelChoiceField(
        queryset=Physician.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    appointment_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        ),
    )

    status = forms.ChoiceField(
        choices=Appointment.STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.instance and self.instance.pk):
            self.fields.pop("status")


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = [
            "patient",
            "notes",
            "diagnosis",
            "follow_up_date",
        ]
        widgets = {
            "patient": forms.Select(attrs={"class": "form-select"}),
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
