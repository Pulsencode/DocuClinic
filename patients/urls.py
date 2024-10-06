from django.urls import path

from .views import (
    PatientListView,
    PatientCreateView,
    PatientDetailView,
    PatientUpdateView,
    PatientDeleteView,
    )

urlpatterns = [
    path('patients/', PatientListView.as_view(), name='patient_list'),
    path('patients/add/', PatientCreateView.as_view(), name='patient_create'),
    path('patients/detail/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('patients/update/<int:pk>/', PatientUpdateView.as_view(), name='patient_update'),
    path('patients/delete/<int:pk>/', PatientDeleteView.as_view(), name='patient_delete'),
]
