from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
# from django.views.generic.base import TemplateView
from django.views.static import serve
from django.contrib.auth import views


urlpatterns = [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.LoginView.as_view(), name="login"),
    path("inventory/", include("inventory.urls")),
    path("patients/", include("patients.urls")),
]
