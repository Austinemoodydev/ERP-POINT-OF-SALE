from django.db import models
from django.conf import settings
from decimal import Decimal


class Account(models.Model):

    ACCOUNT_TYPES = (
        ('ASSET', 'Asset'),
        ('LIABILITY', 'Liability'),
        ('EQUITY', 'Equity'),
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    )

    code = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(
        max_length=255
    )

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPES
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.code} - {self.name}"


class JournalEntry(models.Model):   # ← now at top level, not inside Account

    reference = models.CharField(
        max_length=100
    )

    description = models.TextField()

    posting_date = models.DateField()

    branch = models.ForeignKey(
        'core.Branch',
        on_delete=models.CASCADE,
        null=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    posted = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.reference


class JournalEntryLine(models.Model):

    journal = models.ForeignKey(
        JournalEntry,
        on_delete=models.CASCADE,
        related_name='lines'
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT
    )

    debit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    credit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )


class GeneralLedger(models.Model):

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT
    )

    journal_entry = models.ForeignKey(
        JournalEntry,
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        'core.Branch',
        on_delete=models.CASCADE,
        null=True
    )

    posting_date = models.DateField()

    reference = models.CharField(
        max_length=100
    )

    debit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    credit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class BankAccount(models.Model):

    account_name = models.CharField(
        max_length=255
    )

    bank_name = models.CharField(
        max_length=255
    )

    account_number = models.CharField(
        max_length=100
    )

    current_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return self.account_name


class BankTransaction(models.Model):

    TRANSACTION_TYPES = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
    )

    bank_account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    reference = models.CharField(
        max_length=100
    )

    transaction_date = models.DateField()

    notes = models.TextField(
        blank=True
    )


class BankReconciliation(models.Model):

    bank_account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE
    )

    statement_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    system_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    reconciled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    reconciliation_date = models.DateField()


class VATTransaction(models.Model):

    reference = models.CharField(
        max_length=100
    )

    taxable_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    vat_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    transaction_date = models.DateField()

    def __str__(self):
        return self.reference


class TaxTransaction(models.Model):

    reference = models.CharField(
        max_length=100
    )

    tax_type = models.CharField(
        max_length=50
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    tax_date = models.DateField()

    def __str__(self):
        return self.reference


def tax_report():

    return TaxTransaction.objects.values(
        'tax_type'
    ).annotate(
        total=models.Sum('amount')
    )


def branch_profit(branch):

    income = GeneralLedger.objects.filter(
        branch=branch,
        account__account_type='INCOME'
    ).aggregate(
        total=models.Sum('credit')
    )['total'] or Decimal('0')

    expense = GeneralLedger.objects.filter(
        branch=branch,
        account__account_type='EXPENSE'
    ).aggregate(
        total=models.Sum('debit')
    )['total'] or Decimal('0')

    return {

        'branch': branch.name,

        'income': income,

        'expense': expense,

        'profit': income - expense

    }
