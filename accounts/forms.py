from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Appointment, Patient, User, Doctor, Operator


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter your password"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm your password"}
        )
    )

    class Meta:
        model = User
        fields = ("username", "email", "phone_number")
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your username"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter your email"}
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your phone number",
                }
            ),
        }


class DoctorForm(UserCreationForm):
    class Meta:
        model = Doctor
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "specialization",
            "license_number",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your username"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter your email"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your first name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your last name"}
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your phone number",
                }
            ),
            "specialization": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter specialization"}
            ),
            "license_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter license number"}
            ),
        }

    address = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Enter your address",
            }
        ),
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter password"}
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm password"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["password1"].required = False
            self.fields["password2"].required = False

    def clean(self):
        if not self.instance and not self.instance.pk:
            cleaned_data = super().clean()
            password1 = cleaned_data.get("password1")
            password2 = cleaned_data.get("password2")

            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")

            return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # Allow current user to retain their username without validation error
        if self.instance and self.instance.pk:
            existing_user = Doctor.objects.filter(username=username).exclude(pk=self.instance.pk)
            if existing_user.exists():
                raise forms.ValidationError("User with this username already exists.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class AppointmentForm(forms.ModelForm):
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

    class Meta:
        model = Appointment
        fields = ["patient", "doctor", "appointment_datetime"]


class OperatorForm(UserCreationForm):
    class Meta:
        model = Operator
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
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
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your first name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your last name"}
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your phone number",
                }
            ),
        }

    address = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Enter your address",
            }
        ),
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter password"}
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm password"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["password1"].required = False
            self.fields["password2"].required = False

    def clean(self):
        if not self.instance and not self.instance.pk:
            cleaned_data = super().clean()
            password1 = cleaned_data.get("password1")
            password2 = cleaned_data.get("password2")

            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")

            return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # Allow current user to retain their username without validation error
        if self.instance and self.instance.pk:
            existing_user = Operator.objects.filter(username=username).exclude(pk=self.instance.pk)
            if existing_user.exists():
                raise forms.ValidationError("User with this username already exists.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
