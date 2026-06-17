from decimal import Decimal
from django.db import transaction

from .models import (
    JournalEntry,
    JournalEntryLine,
    GeneralLedger,
)


@transaction.atomic
def post_journal_entry(
        reference,
        description,
        posting_date,
        user,
        lines):

    total_debit = sum(
        Decimal(str(line['debit']))
        for line in lines
    )

    total_credit = sum(
        Decimal(str(line['credit']))
        for line in lines
    )

    if total_debit != total_credit:

        raise Exception(
            "Journal is not balanced"
        )

    journal = JournalEntry.objects.create(
        reference=reference,
        description=description,
        posting_date=posting_date,
        created_by=user,
        posted=True
    )

    for line in lines:

        JournalEntryLine.objects.create(
            journal=journal,
            account=line['account'],
            debit=line['debit'],
            credit=line['credit']
        )

        last_gl = GeneralLedger.objects.filter(
            account=line['account']
        ).order_by('-id').first()

        previous_balance = (
            last_gl.balance
            if last_gl
            else 0
        )

        new_balance = (
            previous_balance
            + line['debit']
            - line['credit']
        )

        GeneralLedger.objects.create(
            account=line['account'],
            journal_entry=journal,
            posting_date=posting_date,
            reference=reference,
            debit=line['debit'],
            credit=line['credit'],
            balance=new_balance
        )

    return journal
