from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
# from django.views.generic.base import TemplateView
from django.views.static import serve
# from django.contrib.auth import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", auth_views.LoginView.as_view(
        template_name='registration/login.html',  # your login template
        next_page='login_redirect'  # name of your redirect view
    ), name="login"),
    path("inventory/", include("inventory.urls")),
    path("patients/", include("patients.urls")),
]
