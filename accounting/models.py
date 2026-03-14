from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=50,
        choices=[
            ("Asset", "Asset"),
            ("Liability", "Liability"),
            ("Expense", "Expense"),
            ("Revenue", "Revenue"),
            ("Equity", "Equity"),
        ],
    )

    def __str__(self):
        return self.name


class GeneralLedgerEntry(models.Model):
    date = models.DateField()
    description = models.TextField()
    debit_account = models.ForeignKey(
        Account, related_name="debit_entries", on_delete=models.CASCADE
    )
    credit_account = models.ForeignKey(
        Account, related_name="credit_entries", on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date} - {self.amount}"


class AccountsReceivable(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    description = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("PAID", "Paid"),
            ("OVERDUE", "Overdue"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"


class AccountsPayable(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    description = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("PAID", "Paid"),
            ("OVERDUE", "Overdue"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=100)
    organization_name = models.CharField(max_length=100)
    date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.invoice_number} - {self.organization_name}"


class Asset(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        limit_choices_to={"type": "Asset"},
    )
    name = models.CharField(max_length=100)
    purchase_date = models.DateField()
    purchase_value = models.DecimalField(max_digits=10, decimal_places=2)
    current_value = models.DecimalField(max_digits=10, decimal_places=2)
    current_value_date = models.DateField()
    depreciation_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.purchase_value}"
