from .models import UsageTracking, TenantSubscription


def check_product_limit(tenant):

    usage = UsageTracking.objects.get(
        tenant=tenant
    )

    subscription = (
        TenantSubscription.objects
        .filter(
            tenant=tenant,
            active=True
        )
        .first()
    )

    if usage.current_products >= subscription.plan.max_products:

        raise Exception(
            "Product limit reached"
        )
