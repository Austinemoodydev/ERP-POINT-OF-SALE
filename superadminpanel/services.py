from django.contrib.auth import get_user_model
from saas.models import Tenant, TenantSubscription
from products.models import Product
from sales.models import SaleInvoice

User = get_user_model()


def system_metrics():

    return {

        "tenants": Tenant.objects.count(),

        "subscriptions":
        TenantSubscription.objects.count(),

        "active_users":
        User.objects.count(),

        "products":
        Product.objects.count(),

        "sales":
        SaleInvoice.objects.count()

    }
