from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, PatientDetails

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm your password'
    }))
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
        }

class PatientForm(forms.ModelForm):
    class Meta:
        model = PatientDetails
        fields = ['username', 'email', 'phone_number_country_code', 'phone_number', 'address', 'condition']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            # 'phone_number_country_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country code'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'address': forms.Textarea(attrs={'class':'form-control', "rows": 2}),
            'condition': forms.Textarea(attrs={'class':'form-control', "rows": 2})
        }
    phone_number_country_code = forms.CharField(required=False, max_length=3, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Country code'}))