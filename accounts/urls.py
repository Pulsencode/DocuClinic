from django.urls import path

from . import views


urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("dashboard/", views.Dashboard.as_view(), name="dashboard"),
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('doctors/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('doctors/create/', views.DoctorCreateView.as_view(), name='doctor_create'),
    path('doctors/<int:pk>/update/', views.DoctorUpdateView.as_view(), name='doctor_update'),
    path('doctors/<int:pk>/delete/', views.DoctorDeleteView.as_view(), name='doctor_delete'),
    path('appointment/create/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('doctor/dashboard/', views.DoctorDashboardView.as_view(), name='dashboard'),
    path('appointment/update/<int:pk>/', views.AppointmentUpdateView.as_view(), name='appointment_update'),
    path('appointment/delete/<int:pk>/', views.AppointmentDeleteView.as_view(), name='appointment_delete'),
]
