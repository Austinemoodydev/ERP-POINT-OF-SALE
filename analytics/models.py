from django.db import models

# Create your models here.

from django.conf import settings


class ForecastSnapshot(models.Model):

    FORECAST_TYPES = (
        ('SALES', 'Sales'),
        ('DEMAND', 'Demand'),
        ('PROFIT', 'Profit'),
        ('CASHFLOW', 'Cash Flow'),
    )

    name = models.CharField(
        max_length=255
    )

    forecast_type = models.CharField(
        max_length=50,
        choices=FORECAST_TYPES
    )

    forecast_date = models.DateField()

    predicted_value = models.DecimalField(
        max_digits=18,
        decimal_places=2
    )

    confidence_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} - {self.forecast_date}"


class AIRecommendation(models.Model):

    PRIORITIES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    )

    recommendation = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITIES,
        default='MEDIUM'
    )

    implemented = models.BooleanField(
        default=False
    )

    impact_estimate = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.recommendation[:50]


class DashboardWidget(models.Model):

    WIDGET_TYPES = (
        ('SALES_CHART', 'Sales Chart'),
        ('PROFIT_CHART', 'Profit Chart'),
        ('INVENTORY', 'Inventory'),
        ('CUSTOMERS', 'Customers'),
        ('FORECAST', 'Forecast'),
        ('KPI', 'KPI'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=255
    )

    widget_type = models.CharField(
        max_length=50,
        choices=WIDGET_TYPES
    )

    position_x = models.IntegerField(
        default=0
    )

    position_y = models.IntegerField(
        default=0
    )

    width = models.IntegerField(
        default=6
    )

    height = models.IntegerField(
        default=4
    )

    active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.title


class KPI(models.Model):

    KPI_TYPES = (
        ('SALES', 'Sales'),
        ('PROFIT', 'Profit'),
        ('CUSTOMERS', 'Customers'),
        ('INVENTORY', 'Inventory'),
        ('EXPENSES', 'Expenses'),
    )

    name = models.CharField(
        max_length=255
    )

    kpi_type = models.CharField(
        max_length=50,
        choices=KPI_TYPES
    )

    target_value = models.DecimalField(
        max_digits=18,
        decimal_places=2
    )

    current_value = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0
    )

    start_date = models.DateField()

    end_date = models.DateField()

    active = models.BooleanField(
        default=True
    )

    def achievement_percentage(self):

        if self.target_value == 0:
            return 0

        return round(
            (self.current_value / self.target_value) * 100,
            2
        )

    def __str__(self):
        return self.name


class ReportSchedule(models.Model):

    FREQUENCY_CHOICES = (
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
    )

    REPORT_TYPES = (
        ('SALES', 'Sales'),
        ('INVENTORY', 'Inventory'),
        ('PROFIT_LOSS', 'Profit & Loss'),
        ('BALANCE_SHEET', 'Balance Sheet'),
        ('CASHFLOW', 'Cash Flow'),
        ('PAYROLL', 'Payroll'),
    )

    name = models.CharField(
        max_length=255
    )

    report_type = models.CharField(
        max_length=50,
        choices=REPORT_TYPES
    )

    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES
    )

    email_to = models.EmailField()

    active = models.BooleanField(
        default=True
    )

    last_run = models.DateTimeField(
        null=True,
        blank=True
    )

    next_run = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
