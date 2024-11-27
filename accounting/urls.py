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

    path("accounts/receivable/list", views.AccountsReceivableListView.as_view(), name="accounts_receivable_list"),
    path("accounts/receivable/create/", views.AccountsReceivableCreateView.as_view(), name="accounts_receivable_create"),
    path("accounts/receivable/update/<int:pk>/", views.AccountsReceivableUpdateView.as_view(), name="accounts_receivable_update"),
    path("accounts/receivable/delete/<int:pk>/", views.AccountsReceivableDeleteView.as_view(), name="accounts_receivable_delete"),

    path("accounts/payable/list", views.AccountsPayableListView.as_view(), name="accounts_payable_list"),
    path("accounts/payable/create/", views.AccountsPayableCreateView.as_view(), name="accounts_payable_create"),
    path("accounts/payable/update/<int:pk>/", views.AccountsPayableUpdateView.as_view(), name="accounts_payable_update"),
    path("accounts/payable/delete/<int:pk>/", views.AccountsPayableDeleteView.as_view(), name="accounts_payable_delete"),

    path("invoice/list", views.InvoiceListView.as_view(), name="invoice_list"),
    path("invoice/create/", views.InvoiceCreateView.as_view(), name="invoice_create"),
    path("invoice/update/<int:pk>/", views.InvoiceUpdateView.as_view(), name="invoice_update"),
    path("invoice/delete/<int:pk>/", views.InvoiceDeleteView.as_view(), name="invoice_delete"),

    path("asset/list", views.AssetListView.as_view(), name="asset_list"),
    path("asset/create/", views.AssetCreateView.as_view(), name="asset_create"),
    path("asset/update/<int:pk>/", views.AssetUpdateView.as_view(), name="asset_update"),
    path("asset/delete/<int:pk>/", views.AssetDeleteView.as_view(), name="asset_delete"),
]
