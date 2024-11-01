from django import forms

from accounts.models import Doctor, Patient

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["patient", "doctor", "appointment_datetime", "status"]

    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
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
        if not(self.instance and self.instance.pk):
            self.fields.pop("status")
