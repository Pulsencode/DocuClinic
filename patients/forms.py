from django import forms

from accounts.models import Patient

from .models import PatientDetail


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "username",
            "email",
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
        }

    address = forms.CharField(
        required=True, widget=forms.Textarea(attrs={"class": "form-control", "rows": 2})
    )


class PatientDetailsForm(forms.ModelForm):
    class Meta:
        model = PatientDetail
        fields = [
            # "condition",
            "age",
            "gender",
            "blood_type",
            "allergies",
            "emergency_contact_name",
            "emergency_contact_number",
        ]
        widgets = {
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            # "condition": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "allergies": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "gender": forms.Select(
                choices=PatientDetail.GENDER_CHOICES, attrs={"class": "form-select"}
            ),
            "blood_type": forms.Select(
                choices=PatientDetail.BLOOD_TYPE_CHOICES,
                attrs={"class": "form-select"},
            ),
            "emergency_contact_name": forms.TextInput(attrs={"class": "form-control"}),
            "emergency_contact_number": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["condition"].required = False
        self.fields["age"].required = True
        self.fields["gender"].required = True
        self.fields["blood_type"].required = False
        self.fields["allergies"].required = False
        self.fields["emergency_contact_name"].required = True
        self.fields["emergency_contact_number"].required = True

        # Validation
        self.fields["age"].validators.append(self.validate_positive_age)

    def validate_positive_age(self, value):
        if value is not None and value < 0:
            raise forms.ValidationError("Age must be a positive number.")
