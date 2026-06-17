from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Tenant)
admin.site.register(SubscriptionPlan)
admin.site.register(TenantSubscription)
admin.site.register(TrialAccount)
admin.site.register(Invoice)
admin.site.register(SubscriptionPayment)
admin.site.register(UsageTracking)
admin.site.register(TenantDomain)
