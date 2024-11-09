from django.contrib import admin
from .models import Account, GeneralLedgerEntry, AccountsPayable, AccountsReceivable, Asset,Invoice

admin.site.register(Account)
admin.site.register(GeneralLedgerEntry)
admin.site.register(AccountsPayable)
admin.site.register(AccountsReceivable)
admin.site.register(Asset)
admin.site.register(Invoice)
