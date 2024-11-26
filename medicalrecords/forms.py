from django import forms

from accounts.models import Patient, Physician, PhysicianAvailability

from .models import Appointment, Discount, Prescription, PrescriptionMedicine


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['percentage']
        widgets = {
            'percentage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter discount percentage'}),
        }
        labels = {
            'percentage': 'Discount Percentage',
        }


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
        required=True,
        widget=forms.Select(
            attrs={"class": "form-control", "id": "id_date", "required": "required"}
        ),
        input_formats=["%Y-%m-%d"],
    )
    time = forms.TimeField(
        required=True,
        widget=forms.Select(
            attrs={"class": "form-control", "id": "id_time", "required": "required"}
        ),
        input_formats=["%H:%M"],
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

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")
        physician = cleaned_data.get("physician")

        if date and time and physician:
            # Validate the selected date and time against physician availability
            try:
                availability = PhysicianAvailability.objects.get(physician=physician)
                weekday = date.strftime("%A")
                if not availability.work_days.filter(name=weekday).exists():
                    raise forms.ValidationError(
                        f"Physician is not available on {weekday}"
                    )

                time_str = time.strftime("%H:%M")
                work_start = availability.work_time_start.strftime("%H:%M")
                work_end = availability.work_time_end.strftime("%H:%M")

                if not (work_start <= time_str <= work_end):
                    raise forms.ValidationError(
                        "Selected time is outside physician's working hours"
                    )
            except PhysicianAvailability.DoesNotExist:
                raise forms.ValidationError("No availability found for this physician")

        return cleaned_data

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
