from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(APIKey)
admin.site.register(Webhook)
admin.site.register(ERPIntegration)
