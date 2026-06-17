from django.shortcuts import render
from .reports import *


def financial_dashboard(request):

    context = {

        'trial_balance': trial_balance(),

        'profit_loss': profit_and_loss(),

        'balance_sheet': balance_sheet(),

        'cash_flow': cash_flow(),

        'vat': vat_report(),

        'tax': tax_report()

    }

    return render(
        request,
        'accounting/dashboard.html',
        context
    )
# Create your views here.
