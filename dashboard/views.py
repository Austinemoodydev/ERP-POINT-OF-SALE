from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    context = {
        'daily_sales': 0,
        'monthly_sales': 0,
        'total_customers': 0,
        'total_products': 0,
    }
    return render(request, 'dashboard/dashboard.html', context)
