from decimal import Decimal
from django.db import models
from accounting.services import (
    post_journal_entry
)

from accounting.models import (
    Account
)
from .models import (                  # ← add this
    Payroll,
    PAYERecord,
    NSSFRecord,
    SHARecord,
    Payslip,
    PayrollSettings,
    PAYETaxBand,
)


def calculate_payroll(payroll):

    gross = (
        payroll.basic_salary +
        payroll.allowances
    )

    paye = gross * Decimal('0.30')

    nssf = Decimal('2160')

    sha = gross * Decimal('0.0275')

    deductions = (
        paye +
        nssf +
        sha
    )

    net_salary = (
        gross -
        deductions
    )

    payroll.gross_salary = gross
    payroll.deductions = deductions
    payroll.net_salary = net_salary

    payroll.save()

    PAYERecord.objects.create(
        payroll=payroll,
        amount=paye
    )

    NSSFRecord.objects.create(
        payroll=payroll,
        amount=nssf
    )

    SHARecord.objects.create(
        payroll=payroll,
        amount=sha
    )


def post_payroll_journal(
        payroll,
        user):

    salary_expense = Account.objects.get(
        code='5100'
    )

    cash_account = Account.objects.get(
        code='1000'
    )

    post_journal_entry(

        reference=f"PAY-{payroll.id}",

        description='Payroll Posting',

        posting_date=payroll.payroll_month,

        user=user,

        lines=[

            {
                'account': salary_expense,
                'debit': payroll.gross_salary,
                'credit': 0
            },

            {
                'account': cash_account,
                'debit': 0,
                'credit': payroll.net_salary
            }

        ]
    )


def calculate_paye(taxable_income):

    total_tax = Decimal('0')

    bands = PAYETaxBand.objects.order_by(
        'min_amount'
    )

    for band in bands:

        if taxable_income > band.min_amount:

            taxable = min(
                taxable_income,
                band.max_amount
            ) - band.min_amount

            total_tax += (
                taxable *
                band.rate /
                Decimal('100')
            )

    return total_tax
