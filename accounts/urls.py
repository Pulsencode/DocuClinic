from django.urls import path

from .views import (
    SignUpView,
    PatientListView,
    PatientCreateView,
    PatientDetailView,
    PatientUpdateView,
    PatientDeleteView,
    )


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('patients/', PatientListView.as_view(), name='patient_list'),
    path('patients/add/', PatientCreateView.as_view(), name='patient_create'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('patients/edit/<int:pk>/', PatientUpdateView.as_view(), name='patient_update'),
    path('patients/delete/<int:pk>/', PatientDeleteView.as_view(), name='patient_delete'),
]
