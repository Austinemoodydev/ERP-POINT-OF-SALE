from django.contrib import admin

from .models import *

admin.site.register(Customer)
admin.site.register(Quotation)
admin.site.register(QuotationItem)
admin.site.register(SalesOrder)
admin.site.register(SalesOrderItem)
admin.site.register(POSSale)
admin.site.register(POSSaleItem)
admin.site.register(SalesInvoice)
admin.site.register(CustomerLedger)
admin.site.register(CustomerPayment)
admin.site.register(SalesAccountingEntry)
# Register your models here.
