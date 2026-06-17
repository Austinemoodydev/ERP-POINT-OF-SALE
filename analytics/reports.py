from core.models import Branch
from django.db.models import Sum
from core.models import Branch
from sales.models import SalesInvoice


def branch_performance():

    report = []

    branches = Branch.objects.all()

    for branch in branches:

        sales = (
            SalesInvoice.objects
            .filter(
                branch=branch
            )
            .aggregate(
                total=Sum(
                    'total_amount'
                )
            )
        )

        report.append({

            'branch':
            branch.name,

            'sales':
            sales['total'] or 0

        })

    return report
