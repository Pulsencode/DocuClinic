from django.urls import path

from .views import (
    PatientListView,
    PatientCreateView,
    PatientDetailView,
    PatientUpdateView,
    PatientDeleteView,
    )

urlpatterns = [
    path('patients_list', PatientListView.as_view(), name='patient_list'),
    path('patient/add/', PatientCreateView.as_view(), name='patient_create'),
    path('patient/detail/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('patient/update/<int:pk>/', PatientUpdateView.as_view(), name='patient_update'),
    path('patient/delete/<int:pk>/', PatientDeleteView.as_view(), name='patient_delete'),
]
