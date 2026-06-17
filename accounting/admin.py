from django.contrib import admin

from .models import (
    Account,
    JournalEntry,
    JournalEntryLine,
    GeneralLedger,
    BankAccount,
    BankTransaction,
    BankReconciliation,
    VATTransaction,
    TaxTransaction,
)

admin.site.register(Account)
admin.site.register(JournalEntry)
admin.site.register(JournalEntryLine)
admin.site.register(GeneralLedger)
admin.site.register(BankAccount)
admin.site.register(BankTransaction)
admin.site.register(BankReconciliation)
admin.site.register(VATTransaction)
admin.site.register(TaxTransaction)
