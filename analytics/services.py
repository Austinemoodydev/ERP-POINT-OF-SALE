# Predict future inventory demand.
from products.models import StockLevel
from django.db.models import Sum
from sales.models import SalesOrderItem
from inventory.models import WarehouseStock
from sales.models import Customer
from sales.models import SalesInvoice
from accounting.models import GeneralLedger


def product_demand_forecast(product):

    sold = (
        SalesOrderItem.objects
        .filter(
            product=product
        )
        .aggregate(
            total=Sum('quantity')
        )
    )

    quantity = sold['total'] or 0

    projected = quantity * 1.15

    return projected


def reorder_recommendations():
    recommendations = []
    products = WarehouseStock.objects.select_related('product').all()

    for stock in products:
        try:
            level = stock.product.stocklevel
            if stock.quantity <= level.minimum_stock:
                recommendations.append({
                    'product': stock.product.name,
                    'current_quantity': stock.quantity,
                    'minimum_stock': level.minimum_stock,
                    'reorder_quantity': level.maximum_stock - stock.quantity,
                })
        except StockLevel.DoesNotExist:
            continue

    return recommendations


def customer_lifetime_value(customer):

    sales = (
        SalesInvoice.objects
        .filter(
            customer=customer
        )
        .aggregate(
            total=Sum(
                'total_amount'
            )
        )
    )

    return sales['total'] or 0


def top_customers():

    return Customer.objects.all().order_by(
        '-credit_limit'
    )[:20]


def gross_profit():

    revenue = (
        GeneralLedger.objects
        .filter(
            account__code='4000'
        )
        .aggregate(
            total=Sum('credit')
        )
    )

    cogs = (
        GeneralLedger.objects
        .filter(
            account__code='5000'
        )
        .aggregate(
            total=Sum('debit')
        )
    )

    revenue_total = revenue['total'] or 0
    cogs_total = cogs['total'] or 0

    return revenue_total - cogs_total
