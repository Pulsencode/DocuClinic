from django.urls import path

from . import views

urlpatterns = [
    path("accounts/list/", views.AccountListView.as_view(), name="accounts_list"),
    path("accounts/create/", views.AccountCreateView.as_view(), name="accounts_create"),
    path("accounts/update/<int:pk>", views.AccountUpdateView.as_view(), name="accounts_update"),
    path("accounts/delete/<int:pk>", views.AccountDeleteView.as_view(), name="accounts_delete"),

    path("general/entry/list", views.GeneralLedgerEntryListView.as_view(), name="general_entry_list"),
    path("general/entry/create/", views.GeneralLedgerEntryCreateView.as_view(), name="general_entry_create"),
    path("general/entry/update/<int:pk>/", views.GeneralLedgerEntryUpdateView.as_view(), name="general_entry_update"),
    path("general/entry/delete/<int:pk>/", views.GeneralLedgerEntryDeleteView.as_view(), name="general_entry_delete"),

    path("account/receivable/list", views.AccountsReceivableListView.as_view(), name="accounts_receivable_list"),
    path("account/receivable/create/", views.AccountsReceivableCreateView.as_view(), name="accounts_receivable_create"),
    path("account/receivable/update/<int:pk>/", views.AccountsReceivableUpdateView.as_view(), name="accounts_receivable_update"),
    path("account/receivable/delete/<int:pk>/", views.AccountsReceivableDeleteView.as_view(), name="accounts_receivable_delete"),
]
