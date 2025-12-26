from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from accounts import views

urlpatterns = [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.base.login_user, name="login"),
    path("inventory/", include("inventory.urls")),
    path("medicalrecords/", include("medicalrecords.urls")),
    path("accounting/", include("accounting.urls")),
    path("clinic/", include("clinic.urls")),
    path("appointments/", include("appointments.urls")),
]
