from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from products.models import Category, Product

@login_required
def dashboard(request):
    context = {
        'daily_sales': 0,
        'monthly_sales': 0,
        'total_customers': 0,
        'total_products': 0,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
@ensure_csrf_cookie
def cashier(request):
    products = Product.objects.filter(is_active=True).select_related('category').order_by('name')
    context = {
        'categories': Category.objects.filter(is_active=True).order_by('name'),
        'products': products,
        'quick_products': products[:8],
    }
    return render(request, 'pos/cashier.html', context)
