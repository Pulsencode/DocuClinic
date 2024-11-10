from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from accounts import views as views

urlpatterns = [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.login_user, name="login"),
    path("inventory/", include("inventory.urls")),
    path("patients/", include("patients.urls")),
    path("physicians/", include("physicians.urls")),
    path("operators/", include("operators.urls")),
    path("medicalrecords/", include("medicalrecords.urls")),
    path("administration/", include("administration.urls")),
    path("accounting/", include("accounting.urls")),
]
