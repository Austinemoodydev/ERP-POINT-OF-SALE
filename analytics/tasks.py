from celery import shared_task
from .forecasting import monthly_sales_forecast
from .models import ForecastSnapshot, AIRecommendation, ReportSchedule
from inventory.models import WarehouseStock
from products.models import Product  # ← ADD THIS
from integrations.email_services import send_email
from datetime import timedelta
from django.utils import timezone


@shared_task
def generate_forecast():
    prediction = monthly_sales_forecast()
    ForecastSnapshot.objects.create(
        name='Monthly Sales',
        forecast_type='SALES',
        predicted_value=prediction,
        confidence_score=90
    )
    return True


@shared_task
def ai_recommendations():
    stocks = WarehouseStock.objects.all()
    for item in stocks:
        if item.quantity < item.product.minimum_stock:
            AIRecommendation.objects.create(
                recommendation=f"Reorder {item.product.name}",
                priority='HIGH',
                impact_estimate=10000
            )
    return True


@shared_task
def scheduled_reports():
    reports = ReportSchedule.objects.filter(active=True)
    for report in reports:
        send_email(
            subject=report.name,
            message="ERP Scheduled Report",
            recipient=report.email_to
        )
    return True


@shared_task
def low_stock_alerts():
    stocks = WarehouseStock.objects.filter(quantity__lte=10)  # ← was Stock
    for s in stocks:
        AIRecommendation.objects.create(
            recommendation=f"Low stock {s.product.name}",
            priority='CRITICAL'
        )
    return True


@shared_task
def expiry_alerts():
    future = timezone.now() + timedelta(days=30)
    products = Product.objects.filter(expiry_date__lte=future)  # ← NOW WORKS
    for p in products:
        AIRecommendation.objects.create(
            recommendation=f"{p.name} expires soon",
            priority='HIGH'
        )
    return True
