from django.urls import path

from .views import (
    PatientListView,
    PatientCreateView,
    PatientDetailView,
    PatientUpdateView,
    PatientDeleteView,
    )

urlpatterns = [
    path('list', PatientListView.as_view(), name='patient_list'),
    path('add/', PatientCreateView.as_view(), name='patient_create'),
    path('detail/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('update/<int:pk>/', PatientUpdateView.as_view(), name='patient_update'),
    path('delete/<int:pk>/', PatientDeleteView.as_view(), name='patient_delete'),
]
