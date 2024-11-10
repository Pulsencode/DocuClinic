from django import forms

from .models import Medicine, MedicineSupplier, RouteOfAdministration, Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "contact_details", "email", "address"]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter supplier name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter supplier email"}
            ),
            "contact_details": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter supplier contact details",
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


class RouteOfAdministrationForm(forms.ModelForm):
    class Meta:
        model = RouteOfAdministration
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter name"}
            ),
        }


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = [
            "name",
            "generic_name",
            "brand_name",
            "route_of_administration",
            "description",
            "quantity",
            "expiration_date",
            "purchase_date",
            "minimum_stock_level",
            "maximum_stock_level",
            "storage_location",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter medicine name"}
            ),
            "generic_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter generic name"}
            ),
            "brand_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter brand name"}
            ),
            "route_of_administration": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter description",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter quantity"}
            ),
            "expiration_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "purchase_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "minimum_stock_level": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter minimum stock level",
                }
            ),
            "maximum_stock_level": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter maximum stock level",
                }
            ),
            "storage_location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter storage location"}
            ),
        }


class MedicineSupplierForm(forms.ModelForm):
    class Meta:
        model = MedicineSupplier
        fields = ["medicine", "supplier", "price", "supply_date"]
        widgets = {
            "medicine": forms.Select(attrs={"class": "form-select"}),
            "supplier": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter price"}
            ),
            "supply_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }
