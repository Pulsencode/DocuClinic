from django.urls import path
from .import views

urlpatterns = [
    path('clinic/create/', views.ClinicCreateView.as_view(), name='clinic_create'),
    path('clinic/<int:pk>/update/', views.ClinicUpdateView.as_view(), name='clinic_update'),
    path('clinic/<int:pk>/', views.ClinicDetailView.as_view(), name='clinic_detail'),
    path('clinic/<int:pk>/delete/', views.ClinicDeleteView.as_view(), name='clinic_delete'),
]
