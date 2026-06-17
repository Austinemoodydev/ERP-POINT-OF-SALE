from decimal import Decimal
from django.db import models
# ← import Sum directly, cleaner than models.Sum
from django.db.models import Sum

from .models import (
    Account,
    GeneralLedger,
    VATTransaction,    # ← import from models.py
    TaxTransaction,    # ← import from models.py
)


def trial_balance():

    accounts = Account.objects.all()

    report = []

    for account in accounts:

        debit = (
            GeneralLedger.objects
            .filter(account=account)
            .aggregate(total=Sum('debit'))
            ['total']
            or Decimal('0')
        )

        credit = (
            GeneralLedger.objects
            .filter(account=account)
            .aggregate(total=Sum('credit'))
            ['total']
            or Decimal('0')
        )

        report.append({
            'account': account.name,
            'debit': debit,
            'credit': credit
        })

    return report


def profit_and_loss():

    income_accounts = Account.objects.filter(
        account_type='INCOME'
    )

    expense_accounts = Account.objects.filter(
        account_type='EXPENSE'
    )

    total_income = Decimal('0')
    total_expense = Decimal('0')

    for account in income_accounts:

        credit = (
            GeneralLedger.objects
            .filter(account=account)
            .aggregate(total=Sum('credit'))
            ['total']
            or Decimal('0')
        )

        total_income += credit

    for account in expense_accounts:

        debit = (
            GeneralLedger.objects
            .filter(account=account)
            .aggregate(total=Sum('debit'))
            ['total']
            or Decimal('0')
        )

        total_expense += debit

    return {
        'income': total_income,
        'expenses': total_expense,
        'profit': total_income - total_expense
    }


def balance_sheet():

    assets = Decimal('0')
    liabilities = Decimal('0')
    equity = Decimal('0')

    asset_accounts = Account.objects.filter(
        account_type='ASSET'
    )

    liability_accounts = Account.objects.filter(
        account_type='LIABILITY'
    )

    equity_accounts = Account.objects.filter(
        account_type='EQUITY'
    )

    for acc in asset_accounts:

        assets += (
            GeneralLedger.objects
            .filter(account=acc)
            .aggregate(balance=Sum('balance'))
            ['balance']
            or Decimal('0')
        )

    for acc in liability_accounts:

        liabilities += (
            GeneralLedger.objects
            .filter(account=acc)
            .aggregate(balance=Sum('balance'))
            ['balance']
            or Decimal('0')
        )

    for acc in equity_accounts:

        equity += (
            GeneralLedger.objects
            .filter(account=acc)
            .aggregate(balance=Sum('balance'))
            ['balance']
            or Decimal('0')
        )

    return {
        'assets': assets,
        'liabilities': liabilities,
        'equity': equity
    }


def cash_flow():

    cash_account = Account.objects.get(
        code='1000'
    )

    inflow = (
        GeneralLedger.objects
        .filter(account=cash_account)
        .aggregate(total=Sum('debit'))
        ['total']
        or Decimal('0')
    )

    outflow = (
        GeneralLedger.objects
        .filter(account=cash_account)
        .aggregate(total=Sum('credit'))
        ['total']
        or Decimal('0')
    )

    return {
        'cash_in': inflow,
        'cash_out': outflow,
        'net_cash': inflow - outflow
    }


def vat_report():

    total_taxable = (
        VATTransaction.objects
        .aggregate(total=Sum('taxable_amount'))
        ['total']
        or Decimal('0')
    )

    total_vat = (
        VATTransaction.objects
        .aggregate(total=Sum('vat_amount'))
        ['total']
        or Decimal('0')
    )

    return {
        'taxable_sales': total_taxable,
        'vat_collected': total_vat
    }


def tax_report():

    return TaxTransaction.objects.values(
        'tax_type'
    ).annotate(
        total=Sum('amount')
    )
