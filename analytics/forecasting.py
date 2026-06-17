from datetime import timedelta
from django.db.models import Sum
from sales.models import SalesInvoice


def monthly_sales_forecast():

    monthly_sales = (
        SalesInvoice.objects
        .values('invoice_date__month')
        .annotate(
            total=Sum('total_amount')
        )
        .order_by(
            'invoice_date__month'
        )
    )

    if not monthly_sales:
        return 0

    average = sum(
        item['total']
        for item in monthly_sales
    ) / len(monthly_sales)

    forecast = average * 1.10

    return forecast
