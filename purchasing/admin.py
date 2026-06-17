from django.contrib import admin
from .models import *


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_code', 'name', 'phone', 'email', 'is_active')
    search_fields = ('name', 'supplier_code', 'phone')
    list_filter = ('is_active',)


@admin.register(PurchaseRequisition)
class PurchaseRequisitionAdmin(admin.ModelAdmin):
    list_display = ('requisition_no', 'requested_by', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('requisition_no',)


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'supplier', 'status', 'order_date')
    list_filter = ('status',)
    search_fields = ('po_number',)


@admin.register(GoodsReceivedNote)
class GoodsReceivedNoteAdmin(admin.ModelAdmin):
    list_display = ('grn_number', 'purchase_order',
                    'warehouse', 'received_date')
    search_fields = ('grn_number',)


@admin.register(SupplierInvoice)
class SupplierInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number',
        'supplier',
        'invoice_date',
        'due_date',
        'total_amount',
        'is_paid'
    )
    list_filter = ('is_paid',)


admin.site.register(PurchaseRequisitionItem)
admin.site.register(PurchaseOrderItem)
admin.site.register(PurchaseApproval)
admin.site.register(GoodsReceivedItem)
admin.site.register(SupplierLedger)
