from django.urls import path

from . import views

urlpatterns = [
    path("accounts/list/", views.AccountListView.as_view(), name="accounts_list"),
]
