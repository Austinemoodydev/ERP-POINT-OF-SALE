from products.models import Product
from sales.models import Customer
from hr.models import Employee


def global_search(query):

    return {

        "products":
        Product.objects.filter(
            name__icontains=query
        ),

        "customers":
        Customer.objects.filter(
            name__icontains=query
        ),

        "employees":
        Employee.objects.filter(
            first_name__icontains=query
        )

    }
