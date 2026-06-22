from django.contrib import admin

# Register your models here.

from .models import (
    ForecastSnapshot,
    AIRecommendation,
    DashboardWidget,
    KPI,
    ReportSchedule
)

admin.site.register(ForecastSnapshot)
admin.site.register(AIRecommendation)
admin.site.register(DashboardWidget)
admin.site.register(KPI)
admin.site.register(ReportSchedule)
