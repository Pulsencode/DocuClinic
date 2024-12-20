from django import forms

from accounts.models import (
    Accountant,
    Nurse,
    Patient,
    PatientDetail,
    Physician,
    Receptionist,
)


class BaseUserForm(forms.ModelForm):
    # Common fields for all user types
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
            self.fields["password1"].widget = forms.HiddenInput()
            self.fields["password2"].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username")
        model = self.Meta.model  # Dynamically set the model
        if self.instance and self.instance.pk:
            existing_user = model.objects.filter(username=username).exclude(
                pk=self.instance.pk
            )
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


class NurseForm(BaseUserForm):
    class Meta:
        model = Nurse
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
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your first name",
                    "required": "required",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your last name",
                    "required": "required",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your phone number",
                }
            ),
        }


class ReceptionistForm(BaseUserForm):
    class Meta:
        model = Receptionist
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
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your first name",
                    "required": "required",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your last name",
                    "required": "required",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your phone number",
                }
            ),
        }


class AccountantForm(BaseUserForm):
    class Meta:
        model = Accountant
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
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your first name",
                    "required": "required",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your last name",
                    "required": "required",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your phone number",
                }
            ),
        }


class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=75, widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your first name",
                    "required": "required",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your last name",
                    "required": "required",
                }
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

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name and last_name:
            if Patient.objects.filter(
                first_name=first_name,
                last_name=last_name
            ).exists():
                raise forms.ValidationError(
                    "A patient with this first and last name already exists."
                )
        return cleaned_data


class PatientDetailsForm(forms.ModelForm):
    class Meta:
        model = PatientDetail
        fields = [
            "age",
            "gender",
            "height_in_centimeter",
            "weight_in_kg",
            "temperature",
            "temperature_method",
            "pulse",
            "blood_type",
            "blood_pressure_systolic",
            "blood_pressure_diastolic",
            "allergies",
            "emergency_contact_name",
            "emergency_contact_number",
        ]
        widgets = {
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            "height_in_centimeter": forms.NumberInput(attrs={"class": "form-control"}),
            "weight_in_kg": forms.NumberInput(attrs={"class": "form-control"}),
            "gender": forms.Select(
                choices=PatientDetail.GENDER_CHOICES, attrs={"class": "form-select"}
            ),
            "temperature": forms.NumberInput(attrs={"class": "form-control"}),
            "temperature_method": forms.TextInput(attrs={"class": "form-control"}),
            "pulse": forms.NumberInput(attrs={"class": "form-control"}),
            "blood_type": forms.Select(
                choices=PatientDetail.BLOOD_TYPE_CHOICES, attrs={"class": "form-select"}
            ),
            "blood_pressure_systolic": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "blood_pressure_diastolic": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "allergies": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "emergency_contact_name": forms.TextInput(attrs={"class": "form-control"}),
            "emergency_contact_number": forms.TextInput(
                attrs={"class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["age"].required = True
        self.fields["gender"].required = True
        self.fields["height_in_centimeter"].required = True
        self.fields["weight_in_kg"].required = True
        self.fields["temperature"].required = False
        self.fields["temperature_method"].required = False
        self.fields["pulse"].required = False
        self.fields["blood_type"].required = False
        self.fields["blood_pressure_systolic"].required = False
        self.fields["blood_pressure_diastolic"].required = False
        self.fields["allergies"].required = False
        self.fields["emergency_contact_name"].required = True
        self.fields["emergency_contact_number"].required = True

        # Validation
        self.fields["age"].validators.append(self.validate_positive_age)

    def validate_positive_age(self, value):
        if value is not None and value < 0:
            raise forms.ValidationError("Age must be a positive number.")


class PhysicianForm(forms.ModelForm):
    class Meta:
        model = Physician
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "specialization",
            "license_number",
            "fee_per_consultation",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter your username"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter your email"}
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your first name",
                    "required": "required",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your last name",
                    "required": "required",
                }
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
            "fee_per_consultation": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter consultation fee"}
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
            existing_user = Physician.objects.filter(username=username).exclude(
                pk=self.instance.pk
            )
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
