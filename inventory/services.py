from decimal import Decimal
from django.db import transaction

from .models import (
    ProductBatch
)
from .models import (
    WarehouseStock
)
from .models import (
    InventoryLedger
)


@transaction.atomic
def issue_stock_fifo(
        product,
        warehouse,
        quantity_needed):

    quantity_needed = Decimal(
        quantity_needed
    )

    consumed_batches = []

    batches = ProductBatch.objects.filter(
        product=product,
        warehouse=warehouse,
        quantity_remaining__gt=0
    ).order_by(
        'received_date'
    )

    for batch in batches:

        if quantity_needed <= 0:
            break

        available = batch.quantity_remaining

        if available >= quantity_needed:

            batch.quantity_remaining -= quantity_needed

            batch.save()

            consumed_batches.append({
                'batch': batch,
                'qty': quantity_needed,
                'cost': batch.unit_cost
            })

            quantity_needed = 0

        else:

            batch.quantity_remaining = 0

            batch.save()

            consumed_batches.append({
                'batch': batch,
                'qty': available,
                'cost': batch.unit_cost
            })

            quantity_needed -= available

    if quantity_needed > 0:

        raise Exception(
            "Insufficient stock"
        )

    return consumed_batches


@transaction.atomic
def increase_stock(
        product,
        warehouse,
        qty):

    stock, created = (
        WarehouseStock.objects.get_or_create(
            product=product,
            warehouse=warehouse
        )
    )

    stock.quantity += qty

    stock.save()

    return stock


@transaction.atomic
def decrease_stock(
        product,
        warehouse,
        qty):

    stock = WarehouseStock.objects.get(
        product=product,
        warehouse=warehouse
    )

    if stock.quantity < qty:

        raise Exception(
            "Insufficient Stock"
        )

    stock.quantity -= qty

    stock.save()

    return stock


def create_ledger_entry(

    product,
    warehouse,
    trans_type,
    qty,
    balance,
    reference,
    user

):

    InventoryLedger.objects.create(

        product=product,

        warehouse=warehouse,

        transaction_type=trans_type,

        quantity=qty,

        balance_after=balance,

        reference_number=reference,

        created_by=user

    )


@transaction.atomic
def process_stock_in(

    warehouse,
    product,
    qty,
    cost,
    batch_number,
    user

):

    ProductBatch.objects.create(

        warehouse=warehouse,

        product=product,

        batch_number=batch_number,

        quantity_received=qty,

        quantity_remaining=qty,

        unit_cost=cost

    )

    stock = increase_stock(
        product,
        warehouse,
        qty
    )

    create_ledger_entry(

        product,

        warehouse,

        'IN',

        qty,

        stock.quantity,

        batch_number,

        user

    )


@transaction.atomic
def process_stock_out(

    warehouse,
    product,
    qty,
    reference,
    user

):

    issue_stock_fifo(
        product,
        warehouse,
        qty
    )

    stock = decrease_stock(
        product,
        warehouse,
        qty
    )

    create_ledger_entry(

        product,

        warehouse,

        'OUT',

        qty,

        stock.quantity,

        reference,

        user

    )
