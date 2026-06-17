from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(ETIMSSettings)
admin.site.register(ElectronicInvoice)
admin.site.register(VATRate)
admin.site.register(VATTransaction)
admin.site.register(WithholdingTax)
admin.site.register(TaxLedger)
admin.site.register(TaxReturn)
admin.site.register(AuditTrail)
admin.site.register(DataChangeLog)
admin.site.register(SecurityLog)
