from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    Account,
    AccountsPayable,
    AccountsReceivable,
    Asset,
    GeneralLedgerEntry,
    Invoice,
)


@admin.register(Account)
class AccountAdmin(ModelAdmin):
    pass


@admin.register(GeneralLedgerEntry)
class GeneralLedgerEntryAdmin(ModelAdmin):
    pass


@admin.register(AccountsPayable)
class AccountsPayableAdmin(ModelAdmin):
    pass


@admin.register(AccountsReceivable)
class AccountsReceivableAdmin(ModelAdmin):
    pass


@admin.register(Asset)
class AssetAdmin(ModelAdmin):
    pass


@admin.register(Invoice)
class InvoiceAdmin(ModelAdmin):
    pass
